from decimal import Decimal

zero = Decimal(0)

discount_slab = (
    {'start': 0, 'end': 10, 'amt': 50},
    {'start': 10, 'end': 20, 'amt': 100},
    {'start': 20, 'end': 50, 'amt': 500},
    # here end of slab is 50km since that is the max value
    {'start': 50, 'end': 50, 'amt': 1000},
)


def get_delivery_cost(distance):
    distance_in_km = distance/Decimal(1000)
    for x in discount_slab:
        if x['start'] <= distance_in_km < x['end']:
            # convert inr to paisa
            return Decimal(x['amt']*100)
    return Decimal(0)


