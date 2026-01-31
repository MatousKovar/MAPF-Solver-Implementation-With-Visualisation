"""Module for visualisin result of path finding"""
import sys
import pygame

# Some constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
AGENT_COLOR = (255, 0, 0)
AGENT_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (125,125,125),(125,125,0),(125,0,125)]

class Visualise():
    """Class uses pygame to visualise algorithm"""
    def __init__(self,width,height,grid_size,paths,end_positions):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.paths = paths
        self.end_positions = end_positions

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("MAPF")
        self.clock = pygame.time.Clock()
        self.screen.fill(BLACK)

    def draw_grid(self):
        """Draws grid_size x grid_size grid"""
        block_size = self.width // self.grid_size
        for x in range(0, self.width, block_size):
            for y in range(0, self.height, block_size):
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

    def draw_agents(self,timestep):
        """Draws agents in given timestep, if agents path is finished in timestep, it is printed in goal destination"""
        block_size = self.width // self.grid_size
        agent_size = block_size // 2
        for i,agent in enumerate(self.paths):
            agent_color = AGENT_COLORS[i % len(AGENT_COLORS)]
            if timestep >= len(agent):
                agent_x = agent[-1][0] * block_size + block_size // 2
                agent_y = agent[-1][1] * block_size + block_size // 2
            else:
                agent_x = agent[timestep][0] * block_size + block_size // 2
                agent_y = agent[timestep][1] * block_size + block_size // 2
            rect = pygame.Rect(agent_x - agent_size // 2, agent_y - agent_size // 2, agent_size,agent_size)
            pygame.draw.rect(self.screen, agent_color, rect)

    def wait_for_start(self):
        """Waits for input and draws starting positions"""
        font = pygame.font.Font(None, 36)
        text = font.render("Press any key to start...", True, WHITE)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        while True:
            self.draw_grid()
            self.draw_goals()
            self.draw_agents(0)
            self.screen.blit(text, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return
            pygame.display.update()

    def draw_goals(self):
        """Renders goal positions onto grid"""
        block_size = self.width // self.grid_size
        agent_size = block_size // 2
        for i, pos in enumerate(self.end_positions):
            x, y = pos.coords()
            agent_color = AGENT_COLORS[i % len(AGENT_COLORS)]
            agent_x = x * block_size + block_size // 2  # center of the block_grid
            agent_y = y * block_size + block_size // 2

            pygame.draw.circle(self.screen, agent_color, (agent_x, agent_y), agent_size // 2)
    def no_solution(self,start_positions):
        """If problem is not solvable using my algorithm, only starting positions are printed"""
        font = pygame.font.Font(None, 36)
        text = font.render("No solution found", True, WHITE)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))

        while True:
            self.draw_grid()
            self.draw_goals()
            self.end_positions = start_positions
            self.draw_goals()
            self.screen.blit(text, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return
            pygame.display.update()

    def run(self):
        """Runs visualisation after pressing any key"""
        t = 0
        longest_path = len(max(self.paths, key=len))

        self.wait_for_start()
        while t < longest_path:
            self.screen.fill(BLACK)
            self.draw_goals()
            self.draw_grid()
            self.draw_agents(t)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            pygame.time.wait(1000)
            t += 1
