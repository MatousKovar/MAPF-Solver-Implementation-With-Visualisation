"""Runs conflict based search"""
from Visualise import Visualise
from HighLevel import HighLevel

# Some constants for visualisation
WIDTH, HEIGHT = 600, 600

def run():
    """Runs algorithm"""
    solver = HighLevel()
    solver.get_inputs()
    paths = solver.run(99999)
    vis = Visualise(WIDTH,HEIGHT,solver.grid_size,paths,solver.end_coords)
    if not paths:
        vis.no_solution(solver.start_coords)
    vis.run()


run()
