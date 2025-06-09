class RebirthSystem:
    def __init__(self, initial_cost=1000, saved_multiplier=1, saved_count=0):
        self.rebirth_count = saved_count
        self.multiplier = saved_multiplier
        self.base_cost = initial_cost
        self.cost = self.calculate_cost()

    def calculate_cost(self):
        # Cost scales up exponentially based on the number of rebirths
        return int(self.base_cost * (2 ** self.rebirth_count))

    def can_rebirth(self, knowledge):
        return knowledge >= self.cost

    def perform_rebirth(self, current_knowledge, items):
        if current_knowledge < self.cost:
            return current_knowledge, False

        # Reset all items
        for item in items.values():
            item["owned"] = 0
            item["cost"] = int(item["cost"] / (1.15 ** item["owned"]))  # Reset to base cost
            item["elapsed"] = 0.0

        # Increase multiplier and count
        self.rebirth_count += 1
        self.multiplier += 1
        self.cost = self.calculate_cost()

        # Reset knowledge to 0
        return 0, True

    def get_state(self):
        return {
            "rebirth_count": self.rebirth_count,
            "multiplier": self.multiplier,
            "cost": self.cost
        }

    def load_state(self, state):
        self.rebirth_count = state.get("rebirth_count", 0)
        self.multiplier = state.get("multiplier", 1)
        self.cost = state.get("cost", self.calculate_cost())
