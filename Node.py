class Node:
    def __init__(self,x,y,timestep):
        self.x = x
        self.y = y
        self.t = timestep

    def __lt__(self,other):
        return (self.x, self.y, self.t) < (other.x, other.y, other.t)
    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.x, self.y, self.t) == (other.x, other.y, other.t)

    def __hash__(self):
        return hash((self.x, self.y, self.t))
    def coords(self):
        return self.x, self.y

    def timestep(self):
        return self.t


