"""This module impolements Astar algorithm"""
import heapq
from Node import Node


class AstarSolver:
    """Class for solving instance of path finding problem using astar
       Astar does not add waiting step when searching
       """
    def __init__(self, constraints: dict, grid: int, start: Node, end: Node):
        """
        :param constraints: dictionary with coordinates as key and timestep as value. Agent cannot be at that position
        :param grid: size of grid
        :param start: starting position
        :param end: ending position
        """
        self.constraints = constraints
        self.grid_size = grid
        self.start = start
        self.end = end
        self.predecessors = {}

    def get_neighbors(self, pos: Node):
        """
        :param cords: Node instance
        :return: returns cordinates when moving to four directions
        """
        possible_moves = []
        x, y = pos.coords()
        t = pos.timestep()
        possible_moves.append(Node(x + 1, y, t + 1))
        possible_moves.append(Node(x - 1, y, t + 1))
        possible_moves.append(Node(x, y + 1, t + 1))
        possible_moves.append(Node(x, y - 1, t + 1))
        # possible_moves.append(Node(x,y,t+1))

        valid_moves = []
        for x in possible_moves:
            if self.is_valid(x):
                valid_moves.append(x)
        return valid_moves

    def is_valid(self, pos: Node):
        """Checks if cordinates run out of map, or if there is a wall"""
        x, y = pos.coords()
        t = pos.timestep()
        # runnig out of bounds
        if x < 0 or y < 0 or x >= self.grid_size or y >= self.grid_size:
            return False

        # Checking constraints
        if (x, y) in self.constraints.keys() and self.constraints[(x, y)] == t:
            return False
        return True

    def manhattan_distance(self, x: Node, y: Node):
        """ Calculates mahhnattan distance between two Node instances"""
        x1, x2 = x.coords()
        y1, y2 = y.coords()
        return abs(x1 - y1) + abs(x2 - y2)

    def heuristic(self, pos: Node, cost):
        """Heuristic is computed by adding lengt of path to pos from start and mannhattan distance to end"""
        return cost + self.manhattan_distance(pos, self.end)

    def get_path(self):
        """Reconstructs path from start to finish"""
        res = []
        res.append(self.end.coords())
        current = self.end
        while current != self.start:
            current = self.predecessors[current]
            res.insert(0, current.coords())
        return res

    def change_config(self, start, end, constraints):
        """Used to change parameters of solver instance"""
        self.start = start
        self.end = end
        self.constraints = constraints

    def run(self, maxiter):
        """Runs astar algorithm and returns path
           This implementation does not allow returning to a node later on!!!
           Waiting is not implemented
        """
        counter = 0
        q = []
        visited = set()
        closed = set()
        price = {}
        heapq.heappush(q, (0, self.start))
        visited.add(self.start)
        price[self.start.coords()] = 0
        while bool(q) and counter < maxiter:
            counter += 1
            _, current = heapq.heappop(q)
            closed.add(current.coords())
            if current.coords() == self.end.coords():
                self.end = current
                return self.get_path()
            for neighbor in self.get_neighbors(current):
                if ((neighbor.coords() in visited) and (price[current.coords()] + 1) >= price[neighbor.coords()]):
                    continue
                visited.add(neighbor.coords())
                self.predecessors[neighbor] = current
                price[neighbor.coords()] = price[current.coords()] + 1
                heapq.heappush(q, (self.heuristic(neighbor, price[neighbor.coords()]), neighbor))
        return False
