class RebirthSystem:
    def __init__(self, initial_cost=2, cost_multiplier=2.0, saved_multiplier=1.0, saved_count=0):
        self.initial_cost = initial_cost
        self.current_cost = initial_cost
        self.cost_multiplier = cost_multiplier
        self.rebirth_count = saved_count
        self.multiplier = saved_multiplier

    def can_rebirth(self, knowledge):
        return knowledge >= self.current_cost

    def rebirth(self, knowledge, insight):
        if self.can_rebirth(knowledge):
            gained_insight = knowledge // 1000
            insight += gained_insight
            self.rebirth_count += 1
            self.multiplier *= 2.0  # or customize here
            knowledge = 0
            self.current_cost = int(self.current_cost * self.cost_multiplier)
            return knowledge, insight, self.multiplier, self.rebirth_count
        return knowledge, insight, self.multiplier, self.rebirth_count
