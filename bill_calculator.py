TARIFF_PER_KWH = 6.5   # ₹ per unit — adjust for your state

def calculate_bill(total_watts, hours=1):
    kwh  = (total_watts * hours) / 1000
    cost = kwh * TARIFF_PER_KWH
    return round(kwh, 4), round(cost, 2)