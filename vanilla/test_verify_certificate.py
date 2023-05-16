import unittest
import networkx as nx

from vanilla.verify_certificate import *


class MyTestCase(unittest.TestCase):
    def test_verify_certificate_empty(self):
        verify_certificate([], [], nx.Graph(), 0)

    def test_verify_certificate_path(self):
        g = nx.path_graph(10)
        f, d = [[1], [0]], [[2], []]
        k = 5
        verify_certificate(f, d, g, 5)

    def test_defences_valid(self):
        g = nx.complete_graph(4)
        f, d = [[0], [2, 3]], [[1], []]

        assert defences_valid(len(f), f, d)[0], 'Did not verify true certificate'
        d_bad = [[0], []]
        assert not defences_valid(len(f), f, d_bad)[0], 'Did not reject certificate when burning vertex defended'
        d_bad = [[1], [1]]
        assert not defences_valid(len(f), f, d_bad)[0], 'Did not reject certificate when defendeding vertex again'

    def test_no_spread_after_end(self):
        g = nx.complete_graph(4)

        f, d = [[0], [2, 3]], [[1], []]
        f_union, d_union = set().union(*f), set().union(*d)
        assert no_spread_after_end(f_union, d_union, g)

        f, d = [[0], [1, 3]], [[], []]
        f_union, d_union = set().union(*f), set().union(*d)

        assert not no_spread_after_end(f_union, d_union, g)

    def test_k_vertices_saved(self):
        g = nx.complete_graph(4)
        f, d = [[0], [2, 3]], [[1], []]
        f_union, d_union = set().union(*f), set().union(*d)
        k = 1

        assert k_vertices_saved(k, f_union, d_union, g), f'{k} vertices defended'

        g = nx.path_graph(4)
        f, d = [[0]], [[1]]
        f_union, d_union = set().union(*f), set().union(*d)
        k = 1
        assert k_vertices_saved(k, f_union, d_union, g), f'{k} vertices defended'
        k = 3
        assert k_vertices_saved(k, f_union, d_union, g), f'{k} vertices defended'
        k = 4
        assert not k_vertices_saved(k, f_union, d_union, g), f'{k} vertices defended'


if __name__ == '__main__':
    unittest.main()
