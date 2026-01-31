import unittest
from Astar import AstarSolver
from Node import Node
from HighLevel import HighLevel
from CTNode import CTNode

class MyTestCase(unittest.TestCase):
    def test_astar_coords_validation(self):
        restrict = {
            (1,1): 2,
            (1,2): 2
        }
        size = 4
        start = Node(1,1,1)
        solver = AstarSolver(restrict,size,start,start)
        self.assertEqual(solver.is_valid(start),True)
        self.assertEqual(solver.is_valid(Node(4,4,4)), False)
        self.assertEqual(solver.is_valid(Node(-1,4,4)), False)
        self.assertEqual(solver.is_valid(Node(1,1,2)), False)

    def test_astar_neighbors(self):
        restrict = {
            (1, 1): 2,
            (1, 2): 2
        }
        size = 4
        start = Node(1, 1, 1)
        solver = AstarSolver(restrict, size, start, start)

        self.assertEqual(len(solver.get_neighbors(Node(1,1,1))), 3)
        self.assertEqual(len(solver.get_neighbors(Node(0,0,0))),3)
        self.assertEqual(len(solver.get_neighbors(Node(1,1,4))),5)

    def test_colissions(self):
        ct = CTNode({})
        ct.paths = [
            [(0,0),(1,0),(1,1)],
            [(1,0),(0,0),(1,1)],
        ]
        self.assertEqual(ct.get_first_colission(), (2,0,1))
        ct.paths = [
            [(0, 0), (1, 0), (1, 1)],
            [(1, 0), (0, 0), (1, 3),(1,1)]
        ]
        self.assertEqual(ct.get_first_colission(), (3,0,1))
        ct.paths = [
            [(1,0)],
            [(1,1)]
        ]
        self.assertEqual(ct.get_first_colission(), False)

    def test_creating_children_ctnodes(self):
        high = HighLevel()
        high.grid_size = 5
        high.start_coords = [(0,0,0),(1,0,0)]
        high.end_coords = [(3,3,0),(2,0,0)]
        root_ct = CTNode({})

        high.create_child_ct_node()
if __name__ == '__main__':
    unittest.main()
