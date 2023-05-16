import unittest
import networkx as nx

from vanilla.verify_certificate import *


class MyTestCase(unittest.TestCase):
    def test_verify_certificate_empty(self):
        verify_certificate([], [], nx.Graph())

    def test_defences_valid(self):
        g = nx.complete_graph(4)
        f, d = [[0], [2, 3]], [[1], []]

        assert defences_valid(len(f), f, d, g)[0], 'Did not verify true certificate'
        d_bad = [[0], []]
        assert not defences_valid(len(f), f, d_bad, g)[0], 'Did not reject certificate when burning vertex defended'
        d_bad = [[1], [1]]
        assert not defences_valid(len(f), f, d_bad, g)[0], 'Did not reject certificate when defendeding vertex again'

    def test_no_spread_after_end(self):
        g = nx.complete_graph(4)

        f, d = [[0], [2, 3]], [[1], []]
        f_union, d_union = set().union(*f), set().union(*d)
        assert no_spread_after_end(len(f), f, d, f_union, d_union, g)

        f, d = [[0], [1, 3]], [[], []]
        f_union, d_union = set().union(*f), set().union(*d)

        assert not no_spread_after_end(len(f), f, d, f_union, d_union, g)


if __name__ == '__main__':
    unittest.main()
