"""Module for class CTNode"""
from Node import Node

class CTNode:
    """Class for representing node in Constraint tree in Conflict-based search algorighm
       Node has path for each agent seaprately, constraints for each agent and price of the node
    """
    def __init__(self, constraints):
        self.constraints = constraints
        self.paths = []
        self.cost = None

    def __lt__(self,other):
        return self.get_cost() < other.get_cost()

    def set_path(self, path):
        """Used when solving paths for root CT_node"""
        self.paths.append(path)

    def get_constraint(self, agent_id):
        """Returns constraints for given agent"""
        return self.constraints[agent_id]

    def get_cost(self):
        """Cost is sum of lengths of individual paths"""
        res = 0
        for x in self.paths:
            res += len(x)
        return res

    def get_first_collision(self):
        """
        Iterates through all timesteps
        In each step it takes all possible pairs of agents and compares their postion
        If they are at the same position at the same time - collision is created
        Swap is not allowed
        :return: list of constraints for both agents that the first collision appeared for
        """
        longest_path_len = len(max(self.paths, key=len))

        for i in range(longest_path_len):  # timestep
            for j, _ in enumerate(self.paths):
                for k in range(j + 1, len(self.paths)):
                    if i < len(self.paths[j]) and i < len(self.paths[k]): # Both have index in range
                        if self.paths[j][i] == self.paths[k][i]:  # both agents still havent reached end
                            x, y = self.paths[i][j]
                            return [(j, Node(x, y, i)), (k, Node(x, y, i))]
                        if i + 1 < len(self.paths[j]) and i + 1 < len(self.paths[k]): # Swapping
                            if self.paths[j][i + 1] == self.paths[k][i] and self.paths[k][i+1] == self.paths[j][i]:
                                x, y = self.paths[k][i]
                                return [(j, Node(x, y, i + 1)), (k, Node(x, y, i))]
                    if len(self.paths[j]) > i >= len(self.paths[k]): # one is out of the bounds
                        if self.paths[j][i] == self.paths[k][-1]:
                            x, y = self.paths[j][i]
                            return [(j, Node(x, y, i)), (k, Node(x, y, i))]
                    if len(self.paths[k]) > i >= len(self.paths[j]):
                        if self.paths[j][-1] == self.paths[k][i]:
                            x, y = self.paths[j][-1]
                            return [(j, Node(x, y, i)), (k, Node(x, y, i))]
        return False

    # def get_agent_position(self, timestep, agent_nr):
    #     """Returns """
    #     return Node(self.paths[agent_nr][timestep][0], self.paths[agent_nr][timestep][1], timestep)
