import json
import time
import threading
import math
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import serial


SERIAL_PORT = "COM12"
BAUD_RATE = 115200
WEB_PORT = 8000

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "indexgo.html"

serial_conn = None
state_lock = threading.RLock()


PROJECT_POINTS = {
    "HOUSE_1": {"name": "Emergency House 1", "lat": 13.02000, "lon": 80.19000, "kind": "house"},
    "HOUSE_2": {"name": "Emergency House 2", "lat": 13.01000, "lon": 80.21400, "kind": "house"},
    "HOUSE_3": {"name": "Emergency House 3", "lat": 13.04500, "lon": 80.22800, "kind": "house"},

    "A1": {"name": "Ambulance A1", "lat": 13.02000, "lon": 80.19000, "kind": "ambulance"},

    "J1": {"name": "Junction 1 — Kathipara", "lat": 13.00727, "lon": 80.20371, "kind": "junction"},
    "J2": {"name": "Junction 2 — Guindy", "lat": 13.00805, "lon": 80.21944, "kind": "junction"},
    "J3": {"name": "Junction 3 — T Nagar", "lat": 13.04180, "lon": 80.23410, "kind": "junction"},

    "HOSPITAL_1": {"name": "Hospital 1", "lat": 13.03500, "lon": 80.24500, "kind": "hospital"},
    "HOSPITAL_2": {"name": "Hospital 2", "lat": 13.05500, "lon": 80.22500, "kind": "hospital"},
}


state = {
    "status": "READY",
    "last_event": None,
    "event_history": [],

    "emergency": {
        "active": False,
        "source": None,
        "location": None,
        "hospital": None
    },

    "ambulances": {
        "A1": {
            "status": "AVAILABLE",
            "lat": PROJECT_POINTS["A1"]["lat"],
            "lon": PROJECT_POINTS["A1"]["lon"],
            "selected": False
        }
    },

    "selected_ambulance": None,
    "selected_hospital": None,
    "nearby_junctions": [],

    "junctions": {
        "J1": {
            "traffic": "NORMAL", "signal": "RED", "time": 0,
            "blocked": False, "selected": False,
            "ir_entry": False, "ir_exit": False,
            "last_ir_event": None, "last_ir_time": None
        },
        "J2": {
            "traffic": "NORMAL", "signal": "RED", "time": 0,
            "blocked": False, "selected": False,
            "ir_entry": False, "ir_exit": False,
            "last_ir_event": None, "last_ir_time": None
        },
        "J3": {
            "traffic": "NORMAL", "signal": "RED", "time": 0,
            "blocked": False, "selected": False,
            "ir_entry": False, "ir_exit": False,
            "last_ir_event": None, "last_ir_time": None
        },
    },

    "route": [],
    "route_coordinates": [],

    "blocked": [],

    "backend": {
        "serial_connected": False,
        "last_serial_line": ""
    }
}


def add_history(message):
    with state_lock:
        state["event_history"].insert(0, {
            "time": time.strftime("%H:%M:%S"),
            "message": message
        })
        state["event_history"] = state["event_history"][:40]


def clear_route_selection():
    for j in state["junctions"].values():
        j["selected"] = False

    for key in state["junctions"]:
        if key not in state["blocked"]:
            state["junctions"][key]["signal"] = "RED"
            state["junctions"][key]["time"] = 0

    for a in state["ambulances"].values():
        a["selected"] = False


def set_route(route):
    state["route"] = route

    for j in state["junctions"].values():
        j["selected"] = False

    for node in route:
        if node in state["junctions"]:
            state["junctions"][node]["selected"] = True

    state["route_coordinates"] = []
    for node in route:
        p = PROJECT_POINTS.get(node)
        if p:
            state["route_coordinates"].append({
                "id": node,
                "lat": p["lat"],
                "lon": p["lon"]
            })


def select_ambulance(name="A1"):
    if name in state["ambulances"]:
        state["selected_ambulance"] = name
        for key in state["ambulances"]:
            state["ambulances"][key]["selected"] = (key == name)
        state["ambulances"][name]["status"] = "SELECTED FOR EMERGENCY"


def handle_ir_event(event_type, junction):
    junction = junction.upper().strip()
    if junction not in state["junctions"]:
        return

    now = time.strftime("%H:%M:%S")

    with state_lock:
        j = state["junctions"][junction]
        j["last_ir_event"] = "ENTRY" if event_type == "IR_ENTRY" else "EXIT"
        j["last_ir_time"] = now

        if event_type == "IR_ENTRY":
            j["ir_entry"] = True
            j["ir_exit"] = False
            message = f"📡 IR ENTRY DETECTED — {junction}"

            if (state["emergency"]["active"] and
                    state["selected_ambulance"] and
                    j.get("selected", False)):
                ambulance = state["selected_ambulance"]
                state["ambulances"][ambulance]["status"] = f"AT {junction}"

        else:
            j["ir_exit"] = True
            j["ir_entry"] = False
            message = f"📡 IR EXIT DETECTED — {junction}"

            if (state["emergency"]["active"] and
                    state["selected_ambulance"] and
                    j.get("selected", False)):
                ambulance = state["selected_ambulance"]
                state["ambulances"][ambulance]["status"] = "EN ROUTE"

    add_history(message)



def distance_km(a, b):
    lat1 = math.radians(a["lat"])
    lat2 = math.radians(b["lat"])
    dlat = lat2 - lat1
    dlon = math.radians(b["lon"] - a["lon"])
    x = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(x))


def calculate_emergency(source_junction):
    source_map = {
        "J1": "HOUSE_1",
        "J2": "HOUSE_2",
        "J3": "HOUSE_3",
    }

    house_id = source_map.get(source_junction, "HOUSE_1")
    house = PROJECT_POINTS[house_id]

    junction_distances = []
    for jid in ("J1", "J2", "J3"):
        p = PROJECT_POINTS[jid]
        junction_distances.append((distance_km(house, p), jid))
    junction_distances.sort()

    hospital_distances = []
    for hid in ("HOSPITAL_1", "HOSPITAL_2"):
        p = PROJECT_POINTS[hid]
        hospital_distances.append((distance_km(house, p), hid))
    hospital_distances.sort()
    nearest_hospital = hospital_distances[0][1]
    corridor = {
        "J1": ["J1", "J2"],
        "J2": ["J2"],
        "J3": ["J3"],
    }

    route_junctions = corridor[source_junction][:]
    route = [house_id] + route_junctions + [nearest_hospital]

    return {
        "house": house_id,
        "route": route,
        "hospital": nearest_hospital,
        "nearby_junctions": [jid for _, jid in junction_distances],
        "junction_distances_km": {jid: round(d, 3) for d, jid in junction_distances},
        "hospital_distances_km": {hid: round(d, 3) for d, hid in hospital_distances},
    }


def handle_event(event_type, value):
    print(f"[EVENT] {event_type} : {value}", flush=True)

    with state_lock:
        state["last_event"] = {
            "type": event_type,
            "value": value,
            "time": time.strftime("%H:%M:%S")
        }

        if event_type == "EMERGENCY":
            clear_route_selection()

            calc = calculate_emergency(value)
            house_id = calc["house"]
            route = calc["route"]
            hospital = calc["hospital"]

            state["status"] = "EMERGENCY_RECEIVED"
            state["emergency"] = {
                "active": True,
                "source": value,
                "location": house_id,
                "hospital": hospital
            }

            select_ambulance("A1")
            state["selected_hospital"] = hospital
            state["nearby_junctions"] = calc["nearby_junctions"]
            set_route(route)

            if value in state["junctions"]:
                state["junctions"][value]["signal"] = "GREEN"
                state["junctions"][value]["time"] = 15

                if serial_conn is not None and serial_conn.is_open:
                    command = f"TIMED_GREEN_{value},15\\n"
                    try:
                        serial_conn.write(command.encode("utf-8"))
                        print(f"A1 COMMAND > {command.strip()}", flush=True)
                        add_history(f"🟢 GREEN COMMAND SENT — {value} — 15 seconds")
                    except Exception as e:
                        print("SERIAL WRITE ERROR:", repr(e), flush=True)

            add_history(f"🚨 EMERGENCY BUTTON PRESSED — {value}")
            add_history(f"Emergency source mapped to {house_id}")
            add_history("A1 selected as available ambulance")
            add_history(
                f"Nearest hospital calculated: {hospital} "
                f"({calc['hospital_distances_km'][hospital]} km)"
            )
            add_history(
                "Nearby junctions: " +
                " → ".join(calc["nearby_junctions"])
            )
            add_history(f"Route selected: {' → '.join(route)}")

        elif event_type == "ACCIDENT":
            state["status"] = "ACCIDENT_DETECTED"

            if value in state["junctions"]:
                state["junctions"][value]["blocked"] = True
                state["junctions"][value]["signal"] = "RED"
                state["junctions"][value]["time"] = 0

            if value not in state["blocked"]:
                state["blocked"].append(value)

            add_history(f"⚠️ ACCIDENT BUTTON PRESSED — {value}")
            add_history(f"Accident received from physical IoT button at {value}")

            if state["emergency"]["active"] and value == "J2":
                new_route = ["HOUSE_1", "J1", "J3", "HOSPITAL_2"]
                state["selected_hospital"] = "HOSPITAL_2"
                state["emergency"]["hospital"] = "HOSPITAL_2"
                set_route(new_route)

                state["junctions"]["J3"]["selected"] = True
                state["junctions"]["J3"]["signal"] = "GREEN"
                state["junctions"]["J3"]["time"] = 15

                if serial_conn is not None and serial_conn.is_open:
                    command = "TIMED_GREEN_J3,15\\n"
                    try:
                        serial_conn.write(command.encode("utf-8"))
                        print(f"A1 COMMAND > {command.strip()}", flush=True)
                        add_history("🟢 GREEN COMMAND SENT — J3 — 15 seconds")
                    except Exception as e:
                        print("SERIAL WRITE ERROR:", repr(e), flush=True)

                add_history("🔄 Existing route invalidated because J2 is blocked")
                add_history("Alternative route analyzed: J1 → J3 → HOSPITAL_2")
                add_history(f"New route selected: {' → '.join(new_route)}")

        elif event_type == "PASSED":
            add_history(f"🚑 AMBULANCE PASSED — {value}")


def process_line(line):
    if not line:
        return

    print("A1 SERIAL >", repr(line), flush=True)

    msg = line.replace("\x00", "").strip()
    upper = msg.upper()

    with state_lock:
        state["backend"]["last_serial_line"] = msg

    if upper.startswith("LIFELANE_EVENT:"):
        parts = msg.split(":")
        if len(parts) >= 3:
            event_name = parts[1].strip().upper()
            event_value = parts[2].strip().upper()
            if event_name in ("IR_ENTRY", "IR_EXIT"):
                handle_ir_event(event_name, event_value)
            else:
                handle_event(event_name, event_value)
            return

    for j in ("J1", "J2", "J3"):
        if upper == f"{j}_TRAFFIC_ENTRY":
            handle_ir_event("IR_ENTRY", j)
            return
        if upper == f"{j}_TRAFFIC_EXIT":
            handle_ir_event("IR_EXIT", j)
            return

    if "EMERGENCY" in upper:
        for j in ("J1", "J2", "J3"):
            if j in upper:
                handle_event("EMERGENCY", j)
                return

    if "ACCIDENT" in upper:
        for j in ("J1", "J2", "J3"):
            if j in upper:
                handle_event("ACCIDENT", j)
                return

    for j in ("J1", "J2", "J3"):
        if f"{j}_PASSED" in upper:
            handle_event("PASSED", j)
            return

    for j in ("J1", "J2", "J3"):
        if f"{j}_TRAFFIC_LOW" in upper:
            with state_lock:
                state["junctions"][j]["traffic"] = "LOW"
            return

        if f"{j}_TRAFFIC_HIGH" in upper:
            with state_lock:
                state["junctions"][j]["traffic"] = "HIGH"
            return

        if f"{j}_TRAFFIC_NEAR" in upper:
            with state_lock:
                state["junctions"][j]["traffic"] = "NEAR"
            return

        if f"{j}_TRAFFIC_FAR" in upper:
            with state_lock:
                state["junctions"][j]["traffic"] = "FAR"
            return


def serial_worker():
    global serial_conn

    while True:
        try:
            if serial_conn is None or not serial_conn.is_open:
                print(f"Connecting to A1 on {SERIAL_PORT}...", flush=True)

                serial_conn = serial.Serial(
                    SERIAL_PORT,
                    BAUD_RATE,
                    timeout=0.2
                )

                time.sleep(2)

                with state_lock:
                    state["backend"]["serial_connected"] = True

                print(f"CONNECTED TO A1: {SERIAL_PORT}", flush=True)
                add_history(f"Connected to A1 on {SERIAL_PORT}")

            data = serial_conn.readline()

            if data:
                process_line(
                    data.decode(errors="ignore").strip()
                )

        except Exception as e:
            print("SERIAL ERROR:", repr(e), flush=True)

            with state_lock:
                state["backend"]["serial_connected"] = False

            try:
                if serial_conn:
                    serial_conn.close()
            except Exception:
                pass

            serial_conn = None
            time.sleep(2)


def fetch_overpass():
    query = """
    [out:json][timeout:30];
    (
      nwr["amenity"="hospital"](12.80,80.05,13.25,80.35);
      nwr["healthcare"="hospital"](12.80,80.05,13.25,80.35);
      nwr["highway"="traffic_signals"](12.80,80.05,13.25,80.35);
    );
    out center tags;
    """

    req = Request(
        "https://overpass-api.de/api/interpreter",
        data=query.encode("utf-8"),
        headers={"User-Agent": "LifeLaneAI/1.0"}
    )

    with urlopen(req, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def get_places():
    try:
        raw = fetch_overpass()

        hospitals = []
        signals = []

        for e in raw.get("elements", []):
            tags = e.get("tags", {})

            if e["type"] == "node":
                lat = e.get("lat")
                lon = e.get("lon")
            else:
                center = e.get("center", {})
                lat = center.get("lat")
                lon = center.get("lon")

            if lat is None or lon is None:
                continue

            name = tags.get("name", "Unnamed")

            if (
                tags.get("amenity") == "hospital"
                or tags.get("healthcare") == "hospital"
            ):
                hospitals.append({
                    "id": f"osm_hospital_{e['type']}_{e['id']}",
                    "name": name,
                    "lat": lat,
                    "lon": lon
                })

            if tags.get("highway") == "traffic_signals":
                signals.append({
                    "id": f"osm_signal_{e['type']}_{e['id']}",
                    "name": name,
                    "lat": lat,
                    "lon": lon
                })

        return {
            "hospitals": hospitals,
            "signals": signals,
            "source": "OpenStreetMap / Overpass"
        }

    except Exception as e:
        print("OVERPASS ERROR:", repr(e), flush=True)

        return {
            "hospitals": [],
            "signals": [],
            "source": "OSM unavailable"
        }


class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def send_json(self, data):
        payload = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(payload))
        )
        self.send_header(
            "Cache-Control",
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        self.send_header("Pragma", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(payload)

    def do_GET(self):
        try:
            path = urlparse(self.path).path

            if path == "/api/state":
                with state_lock:
                    data = json.loads(
                        json.dumps(
                            state,
                            ensure_ascii=False
                        )
                    )

                self.send_json(data)
                return

            if path == "/api/health":
                self.send_json({
                    "ok": True,
                    "server": "LifeLane AI",
                    "time": time.strftime("%H:%M:%S")
                })
                return

            if path == "/api/places":
                self.send_json(get_places())
                return

            if path == "/api/project-points":
                self.send_json(PROJECT_POINTS)
                return

            if path == "/" or path == "/index.html":
                if not INDEX_FILE.exists():
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"index.html not found")
                    return

                data = INDEX_FILE.read_bytes()

                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    "text/html; charset=utf-8"
                )
                self.send_header(
                    "Content-Length",
                    str(len(data))
                )
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(data)
                return

            self.send_response(404)
            self.end_headers()

        except Exception as e:
            print("HTTP ERROR:", repr(e), flush=True)


def main():
    print()
    print("=" * 60)
    print("       LIFELANE AI - LIVE IOT SERVER")
    print("=" * 60)
    print(f"A1 Serial : {SERIAL_PORT}")
    print(f"Web       : http://localhost:{WEB_PORT}")
    print("=" * 60)
    print()

    threading.Thread(
        target=serial_worker,
        daemon=True
    ).start()

    server = ThreadingHTTPServer(
        ("127.0.0.1", WEB_PORT),
        Handler
    )

    print(
        "WEB SERVER RUNNING:",
        f"http://localhost:{WEB_PORT}",
        flush=True
    )

    print(
        "API:",
        f"http://localhost:{WEB_PORT}/api/state",
        flush=True
    )

    print(
        "MAP DATA:",
        f"http://localhost:{WEB_PORT}/api/places",
        flush=True
    )

    print()

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server.server_close()

        try:
            if serial_conn:
                serial_conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
