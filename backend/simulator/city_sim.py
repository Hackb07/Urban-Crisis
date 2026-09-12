import random
import time
import threading
import heapq
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Set

@dataclass
class Incident:
    id: str
    type: str # Fire, Medical, Police
    location: int # Node ID in the graph
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
    current_path: List[int] = None

@dataclass
class Road:
    id: str
    start: int
    end: int
    weight: int # Distance/Time
    status: str # open, blocked

class CitySimulator:
    def __init__(self):
        self.incidents: Dict[str, Incident] = {}
        self.resources: Dict[str, Resource] = {}
        self.roads: Dict[str, Road] = {}
        self.adj: Dict[int, List[Tuple[int, str]]] = {} # node -> [(neighbor, road_id)]
        self.lock = threading.Lock()
        self.tick_count = 0

        self._setup_graph_city()

    def _setup_graph_city(self):
        # Professional Graph City: 10 Nodes with various connections
        # Designing a non-trivial network to prove routing intelligence
        connections = [
            (0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1),
            (5, 6, 1), (6, 7, 1), (7, 8, 1), (8, 9, 1), (9, 0, 1),
            (0, 5, 3), (1, 6, 3), (2, 7, 3), (3, 8, 3), (4, 9, 3),
            (0, 2, 2), (2, 4, 2), (4, 6, 2), (6, 8, 2), (8, 0, 2)
        ]

        for i in range(10):
            self.adj[i] = []

        for u, v, w in connections:
            # Create bidirectional roads
            for start, end in [(u, v), (v, u)]:
                road_id = f"r{start}_{end}"
                self.roads[road_id] = Road(road_id, start, end, w, "open")
                self.adj[start].append((end, road_id))

        # Setup Resources
        types = ["Fire", "Medical", "Police"]
        for i in range(9):
            res_id = f"unit_{i}"
            self.resources[res_id] = Resource(res_id, types[i % 3], random.randint(0, 9), "idle")

    def dijkstra(self, start: int, end: int) -> Optional[List[int]]:
        """Calculates the shortest path avoiding blocked roads"""
        distances = {node: float('inf') for node in self.adj}
        distances[start] = 0
        pq = [(0, start, [start])]
        visited = set()

        while pq:
            (dist, current, path) = heapq.heappop(pq)

            if current in visited: continue
            visited.add(current)

            if current == end: return path

            for neighbor, road_id in self.adj[current]:
                road = self.roads[road_id]
                if road.status == "blocked": continue

                new_dist = dist + road.weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))

        return None

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
                inc = self.incidents[incident_id]

                path = self.dijkstra(unit.location, inc.location)
                if path is None: return False # No route available

                unit.status = "busy"
                unit.assigned_incident = incident_id
                unit.current_path = path[1:] # Path from current loc to target
                return True
            return False

    def update(self):
        """Simulate one tick of time"""
        with self.lock:
            self.tick_count += 1
            for unit in self.resources.values():
                if unit.status == "busy" and unit.assigned_incident:
                    # Check if the current path is still valid
                    if unit.current_path:
                        next_node = unit.current_path[0]
                        # Find road to next node
                        road_id = next((rid for n, rid in self.adj[unit.location] if n == next_node), None)

                        if road_id and self.roads[road_id].status == "open":
                            unit.location = next_node
                            unit.current_path.pop(0)
                        else:
                            # PATH BLOCKED! Recalculate.
                            inc = self.incidents.get(unit.assigned_incident)
                            if inc:
                                new_path = self.dijkstra(unit.location, inc.location)
                                if new_path:
                                    unit.current_path = new_path[1:]
                                else:
                                    # Totally stuck
                                    unit.status = "broken"

                        # Check if arrived
                        inc = self.incidents.get(unit.assigned_incident)
                        if inc and unit.location == inc.location:
                            inc.status = "resolved"
                            unit.status = "idle"
                            unit.assigned_incident = None
                            unit.current_path = None

    def get_state(self):
        with self.lock:
            return {
                "incidents": {k: asdict(v) for k, v in self.incidents.items()},
                "resources": {k: asdict(v) for k, v in self.resources.items()},
                "roads": {k: asdict(v) for k, v in self.roads.items()},
                "tick": self.tick_count
            }
