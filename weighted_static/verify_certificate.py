from vanilla.verify_certificate import defences_valid, no_spread_after_end, k_vertices_saved


# As vanilla version, with one extra condition
def verify_certificate(cost, b, f, d, g, k):
    assert len(f) <= len(d), f'lists of burned ({len(f)}) and defended ({len(d)}) are different lengths'
    i = len(f)  # time at which process terminated

    # Extra condition: 1. For each i,the sum of cost(v) over all v in d)i is at most b
    okay_1 = sum_cost_over_defence(cost, b, d)

    okay_2, f_union, d_union = defences_valid(i, f, d)
    return (okay_1 and okay_2) and (no_spread_after_end(d_union, f_union, g) and k_vertices_saved(k, f_union, d_union, g))


def sum_cost_over_defence(cost, b, d):
    for d_i in d:
        cost_i = 0
        for v in d_i:
            cost_i += cost(v)
            if cost_i > b:
                return False
    return True
