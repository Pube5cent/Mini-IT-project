class RebirthSystem:
    def __init__(self, initial_cost=2, cost_multiplier=2.0, saved_multiplier=1.0, saved_count=0):
        self.initial_cost = initial_cost
        self.current_cost = initial_cost
        self.cost_multiplier = cost_multiplier
        self.rebirth_count = saved_count
        self.multiplier = saved_multiplier

    def can_rebirth(self, knowledge):
        return knowledge >= self.current_cost

    def rebirth(self, knowledge, knowledge_per_click, items, active_upgrades):
        if not self.can_rebirth(knowledge):
            return knowledge, knowledge_per_click, items, active_upgrades, self.multiplier, self.rebirth_count

        # Increase rebirth count and multiplier
        self.rebirth_count += 1
        self.multiplier = 1 + self.rebirth_count * 0.1  # example scaling

        # Scale up the rebirth cost
        self.current_cost *= self.cost_multiplier

        # Reset core values
        knowledge = 0
        knowledge_per_click = 1

        # Reset items
        for item in items.values():
            item["owned"] = 0
            if "base_cost" in item:
                item["cost"] = item["base_cost"]

        # Clear active upgrades
        active_upgrades.clear()

        return knowledge, knowledge_per_click, items, active_upgrades, self.multiplier, self.rebirth_count
