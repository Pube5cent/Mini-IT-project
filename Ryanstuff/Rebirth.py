

rebirth_count = 0
rebirth_multiplier = 1.0
rebirth_cost = 2  # Knowledge needed to rebirth

def get_multiplier():
    return rebirth_multiplier

def get_rebirth_info():
    return rebirth_count, rebirth_multiplier, rebirth_cost

def try_rebirth(Knowledge, items):
    global rebirth_count, rebirth_multiplier, rebirth_cost

    if Knowledge >= rebirth_cost:
        rebirth_count += 1
        rebirth_multiplier = 1.0 + rebirth_count * 2.0
        Knowledge = 0

        for item in items.values():
            item["owned"] = 0
            item["elapsed"] = 0.0
            item["cost"] = item["cost"] / (1.15 ** item["owned"])  # Optional cost reset
        
        rebirth_cost = int(rebirth_cost * 5.0) #rebirth cost increases 

        print(f"Rebirth successful! Multiplier is now x{rebirth_multiplier:.1f}")

    return Knowledge  # Return updated knowledge after rebirth
