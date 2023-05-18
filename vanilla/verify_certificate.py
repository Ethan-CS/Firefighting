# takes two lists - burned and defended at each time-step - verifies this satisfies FF conditions
def verify_certificate(instance, d):
    i = len(d)  # time at which process terminated
    f = instance.burning_from_defences(d)
    assert len(f) <= len(d), f'lists of burned ({f}) and defended ({d}) are different lengths'

    okay_1, f_union, d_union = defences_valid(f, i, d)
    assert len(f_union) + len(d_union) <= instance.graph.number_of_nodes(), \
        f'{len(f_union)}+{len(d_union)} should be less than/equal to {instance.graph.number_of_nodes()}'

    return okay_1 and (no_spread_after_end(d_union, f_union, instance.graph)
                       and k_vertices_saved(instance.k, f_union, d_union, instance.graph))


# (1) each v in di in d is neither burned nor defended at time i,
def defences_valid(f, i, d):
    f_so_far, d_so_far = [], []  # maintain a list of 'all burned/defended so far' for each i that we add to

    # check each v not burned/defended so far
    for j in range(1, i + 1):
        # add the burned and defended vertices of j to 'so-far' lists
        f_so_far.extend(f[j - 1])
        # check no vertices to defend are either burned or defended so far
        for v in d[j - 1]:
            if (v in f_so_far) or (v in d_so_far):
                # print(f'{v} should not have been defended at time {j}')
                return False, [], []
            # else:
                # print(f'{v} is okay to defend at time {j}')
        d_so_far.extend(d[j - 1])  # can update defences now for next check
    return True, f_so_far, d_so_far


# (2) At time t, no undefended vertex is adjacent to a burning vertex
def no_spread_after_end(f_union, d_union, g):
    unburned = list(set(g.nodes)-set(f_union).union(d_union))
    for u in unburned:
        for v in g.neighbors(u):
            if v in f_union:
                return False
    return True


# (3) At least k vertices are saved at the end of time t.
def k_vertices_saved(k, f_union, d_union, g):
    return len(d_union) + len(list(set(g.nodes)-set(f_union).union(d_union))) >= k

