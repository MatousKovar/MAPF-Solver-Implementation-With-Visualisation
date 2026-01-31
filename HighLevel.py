"""Module for class HighLevel"""
import heapq
import copy
from Astar import AstarSolver
from CTNode import CTNode
from Node import Node

class HighLevel():
    """High Level represents the solver of MAPF problem using Conflict-based search
       It finds paths for each agent individually and then finds colisions in those paths
       Each instance of problem with given set of constraints is in CTNode class
       This class just creates CTNode instances and then solves them using Astar search implemented in AstarSolver
    """
    def __init__(self):
        self.grid_size = 0
        self.start_coords = []
        self.end_coords = []
        self.solver = None

    def _get_valid_int(self, prompt):
        """Helper to ensure user inputs an integer."""
        while True:
            try:
                value = int(input(prompt))
                if value <= 0:
                    print("Please enter a positive integer.")
                    continue
                return value
            except ValueError:
                print("Invalid input. Please enter a number.")

    def _get_valid_coords(self, prompt, must_exist=False):
        """Helper to get x y coordinates with validation."""
        while True:
            in_string = input(prompt)
            # Handle empty string (stop condition)
            if in_string.strip() == '':
                if must_exist:
                    print("Input required. Do not leave blank.")
                    continue
                return None
            
            try:
                parts = in_string.split()
                if len(parts) != 2:
                    print("Format error. Please enter exactly two numbers: 'x y'")
                    continue
                
                x, y = int(parts[0]), int(parts[1])
                
                # Check bounds
                if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
                    print(f"Coordinates out of bounds. Must be between 0 and {self.grid_size - 1}.")
                    continue
                    
                return x, y
            except ValueError:
                print("Invalid format. Please use integers.")

    def get_inputs(self):
        """Reads user inputs with validation"""
        print("--- MAPF Solver Setup ---")
        self.grid_size = self._get_valid_int("Enter Grid Size (N): ")
        
        print("\n--- Enter Starting Positions (Press Enter to finish) ---")
        agent_count = 1
        while True:
            coords = self._get_valid_coords(f"Agent {agent_count} start (x y): ", must_exist=False)
            if coords is None:
                if len(self.start_coords) == 0:
                    print("You must add at least one agent.")
                    continue
                break
            
            self.start_coords.append(Node(coords[0], coords[1], 0))
            agent_count += 1

        print(f"\n--- Enter Ending Positions (Need {len(self.start_coords)} positions) ---")
        # We enforce that the number of goals matches the number of agents
        for i in range(len(self.start_coords)):
            coords = self._get_valid_coords(f"Agent {i+1} goal (x y): ", must_exist=True)
            self.end_coords.append(Node(coords[0], coords[1], 0))
            
        print("\nInput successful. Initializing solver...")
        self.solver = AstarSolver({}, self.grid_size, Node(0, 0, 0), Node(0, 0, 0))
    
    def solve_ct_node(self,ctnode: CTNode):
        """
        Uses solver to get paths for all agents with constraints inside CTNode
        """
        for i,(start,end) in enumerate(zip(self.start_coords,self.end_coords)):
            self.solver.change_config(start,end,ctnode.get_constraint(i))
            path = self.solver.run(99999)
            if not path:
                return False
            ctnode.set_path(path)
        return True

    def create_child_ct_node(self, agent,constraint: Node, parent_node: CTNode):
        """
        Creates child CT_node based on constraint specified in constraint
        Finds updated path only for the agent with new constraint
        :param agent - number of agent which will have new constraint added in new CTNode:
        :param constraint - constraint of given agent:
        :param parent_node - parent node, which has all the constraints that the child will inherit:
        :return: CTNode child
        """
        #creating copies and updating constraints
        constraints = copy.deepcopy(parent_node.constraints)
        constraints[agent][constraint.coords()] = constraint.timestep()
        paths = copy.deepcopy(parent_node.paths)

        #creating child node
        child_node = CTNode(constraints)
        child_node.paths = paths

        #updating path for affected agent
        start = self.start_coords[agent]
        end = self.end_coords[agent]
        self.solver.change_config(start, end, child_node.get_constraint(agent))
        path = self.solver.run(99999)
        #Path does not exist
        if not path:
            return False
        child_node.paths[agent] = path
        return child_node


    def run(self,max_iterations):
        """main method of HighLevel
           Starts without any constraints
           Uses min heap for storing CTNode instances
           Whenever new CTNode is created it is saved to heap sorted by CTNode price
           If CTNode has no conflicting paths - result is returned as 2D array of paths for each agent
        """
        q = []
        start_constraints = [{} for x in self.start_coords] # creates empty dict of constraints
        start_node = CTNode(start_constraints)
        if not self.solve_ct_node(start_node):
            return False
        heapq.heappush(q, (0, start_node))
        cnt = 0
        while bool(q) and cnt < max_iterations:
            _,current_node = heapq.heappop(q)

            # Collision returns list of tuples (Agent, Node)
            collision = current_node.get_first_collision()

            if not collision:
                return current_node.paths

            child1 = self.create_child_ct_node(collision[0][0],collision[0][1],current_node)
            child2 = self.create_child_ct_node(collision[1][0],collision[1][1],current_node)
            if not child1 or not child2:
                return False

            heapq.heappush(q,(child1.get_cost(),child1))
            heapq.heappush(q,(child2.get_cost(),child2))
            cnt += 1
        return False
