card_infos = {
    "reserve": dict(
        points_bump=0.5 / 100,
        max_travel_credit=300,
        annual_fee=550,
    ),
    "preferred": dict(
        points_bump=0.25 / 100,
        max_travel_credit=0,
        annual_fee=95,
    ),
}


def calculate_points_worth(card_info, portal_redemption, spending):
    points = (
        (spending["lyft"] * 10)
        + (spending["travel_dining"] * 3)
        + (spending["everything_else"] * 1)
    )
    points_worth = points * (0.01 + (card_info["points_bump"] * portal_redemption))
    return points_worth


def calculate_net_value(card_info, portal_redemption, spending):
    points_worth = calculate_points_worth(card_info, portal_redemption, spending)
    net_value = (
        points_worth
        + min(spending["travel_dining"], card_info["max_travel_credit"])
        - card_info["annual_fee"]
    )
    return net_value


def calculate_breakeven(card_info, portal_redemption, spending_percents, start=10000):
    assert (
        sum([s for s in spending_percents.values()]) == 1.00
    ), "Spending percents must sum to 100.0%"

    converge = False
    total_spending = start
    while converge == False:
        spending = {
            cat: total_spending * perc for cat, perc in spending_percents.items()
        }
        nv = calculate_net_value(
            card_infos["reserve"], portal_redemption=True, spending=spending
        )
        if round(nv, 2) == 0:
            converge = True
        elif nv > 0:
            total_spending += -total_spending * 0.01
        elif nv < 0:
            total_spending += total_spending * 0.01
    return total_spending
