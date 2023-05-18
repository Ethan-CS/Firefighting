import networkx as nx


class VanillaInstance:
    def __init__(self, graph, root, k):
        self.graph = graph
        self.root = root
        self.k = k

    def __str__(self):
        return f'vanilla firefighter instance on:\n' \
               f'graph: {self.graph}\n' \
               f'root: {self.root}\n' \
               f'min saved: {self.k}'

    def burning_from_defences(self, d):
        # Given a defence list d, finds which vertices burned at each time-step
        f = [[self.root]]
        all_burning = [self.root]
        all_defended = list(set().union(*d))

        for i in range(0, len(d)-1):
            # find where the fire could spread
            could_burn = set()
            for b in all_burning:
                for n in self.graph.neighbors(b):
                    if n not in all_burning and n not in all_defended:
                        could_burn.add(n)
            f.append(list(could_burn))
            all_burning.extend((list(could_burn)))
        return f

