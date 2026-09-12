from simulator.city_sim import CitySimulator

class CityTools:
    def __init__(self, simulator: CitySimulator):
        self.sim = simulator

    def get_city_state(self) -> dict:
        """Returns the current state of all incidents, resources, and roads in the city."""
        return self.sim.get_state()

    def dispatch_unit(self, unit_id: str, incident_id: str) -> bool:
        """Assigns a resource unit to an incident using shortest-path routing. Returns True if successful."""
        return self.sim.dispatch(unit_id, incident_id)

    def block_road(self, road_id: str) -> bool:
        """Simulates a road blockage. Forces agents to replan routes."""
        self.sim.block_road(road_id)
        return True

    def unblock_road(self, road_id: str) -> bool:
        """Removes a road blockage."""
        self.sim.unblock_road(road_id)
        return True

    def add_emergency(self, type: str, location: int, priority: int) -> str:
        """Adds a new emergency incident to the city graph."""
        return self.sim.add_incident(type, location, priority)
