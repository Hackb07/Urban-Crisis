import random
import time
import json
import threading
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

@dataclass
class Incident:
    id: str
    type: str # Fire, Medical, Police
    location: int # Simplified to a 1D or 2D coordinate
    priority: int # 1 (Low) to 5 (Critical)
    status: str # open, resolved
    timestamp: float

@dataclass
class Resource:
    id: str
    type: str # Fire, Medical, Police
    location: int
    status: str # idle, busy, broken
    assigned_incident: Optional[str] = None

@dataclass
class Road:
    id: str
    start: int
    end: int
    status: str # open, blocked

class CitySimulator:
    def __init__(self):
        self.incidents: Dict[str, Incident] = {}
        self.resources: Dict[str, Resource] = {}
        self.roads: Dict[str, Road] = {}
        self.lock = threading.Lock()
        self.tick_count = 0

        self._setup_city()

    def _setup_city(self):
        # Setup 10 locations (0-9)
        # Setup Roads (simple ring for now)
        for i in range(10):
            road_id = f"r{i}_{ (i+1)%10 }"
            self.roads[road_id] = Road(road_id, i, (i+1)%10, "open")

        # Setup Resources
        types = ["Fire", "Medical", "Police"]
        for i in range(9):
            res_id = f"unit_{i}"
            self.resources[res_id] = Resource(res_id, types[i % 3], random.randint(0, 9), "idle")

    def add_incident(self, type: str, location: int, priority: int):
        with self.lock:
            inc_id = f"inc_{len(self.incidents) + 1}"
            self.incidents[inc_id] = Incident(inc_id, type, location, priority, "open", time.time())
            return inc_id

    def block_road(self, road_id: str):
        with self.lock:
            if road_id in self.roads:
                self.roads[road_id].status = "blocked"

    def unblock_road(self, road_id: str):
        with self.lock:
            if road_id in self.roads:
                self.roads[road_id].status = "open"

    def dispatch(self, unit_id: str, incident_id: str):
        with self.lock:
            if unit_id in self.resources and incident_id in self.incidents:
                unit = self.resources[unit_id]
                unit.status = "busy"
                unit.assigned_incident = incident_id
                return True
            return False

    def update(self):
        """Simulate one tick of time"""
        with self.lock:
            self.tick_count += 1
            # Move units toward their assigned incidents
            for unit in self.resources.values():
                if unit.status == "busy" and unit.assigned_incident:
                    inc = self.incidents.get(unit.assigned_incident)
                    if inc:
                        # Simple 1D movement toward target
                        if unit.location < inc.location:
                            unit.location += 1
                        elif unit.location > inc.location:
                            unit.location -= 1

                        if unit.location == inc.location:
                            # Resolved!
                            inc.status = "resolved"
                            unit.status = "idle"
                            unit.assigned_incident = None

    def get_state(self):
        with self.lock:
            return {
                "incidents": {k: asdict(v) for k, v in self.incidents.items()},
                "resources": {k: asdict(v) for k, v in self.resources.items()},
                "roads": {k: asdict(v) for k, v in self.roads.items()},
                "tick": self.tick_count
            }

if __name__ == "__main__":
    # Simple test run
    sim = CitySimulator()
    sim.add_incident("Fire", 5, 5)
    print("Initial State:", sim.get_state())

    sim.dispatch("unit_0", "inc_1")
    print("After Dispatch:", sim.get_state())

    for _ in range(10):
        sim.update()
        time.sleep(0.1)

    print("Final State:", sim.get_state())
