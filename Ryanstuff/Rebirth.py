class RebirthSystem:
    def __init__(self):
        self.rebirth_count = 0
        self.multiplier = 1

    def can_rebirth(self, upgrades, cap):
        return all(u["level"] >= cap for u in upgrades)

    def perform_rebirth(self, upgrades):
        self.rebirth_count += 1
        self.multiplier = 1 + self.rebirth_count
        for u in upgrades:
            u["level"] = 0
            u["progress"] = 0
            u["last_tick"] = 0  # optionally reset timing
        return self.multiplier