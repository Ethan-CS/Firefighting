import unittest

import networkx as nx

from weighted_static.verify_certificate import sum_cost_over_defence


class MyTestCase(unittest.TestCase):
    def test_sum_cost_over_defence(self):
        def cost(v):
            return 0.5

        g = nx.path_graph(10)
        f, d = [[1]], [[0, 2]]
        k = 6
        b = 1

        assert sum_cost_over_defence(cost, b, d), f'Cost should not exceed budget for example given'

if __name__ == '__main__':
    unittest.main()
