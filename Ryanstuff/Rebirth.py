class RebirthSystem:
    def __init__(self, initial_cost=2, cost_multiplier=2.0): #price of the rebirth
        self.initial_cost = initial_cost
        self.current_cost = initial_cost
        self.cost_multiplier = cost_multiplier
        self.rebirth_count = 0
        self.multiplier = 1.0

    def can_rebirth(self, knowledge):
        return knowledge >= self.current_cost

    def rebirth(self, knowledge, insight):
        if self.can_rebirth(knowledge):
            self.rebirth_count += 1
            self.multiplier *= 1.5  # or any multiplier you prefer
            knowledge = 0
            insight += 1  # or increase insight as you like
            self.current_cost = int(self.current_cost * self.cost_multiplier)
            return knowledge, insight, self.multiplier
        return knowledge, insight, self.multiplier
