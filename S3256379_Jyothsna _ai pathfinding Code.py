#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import random

def create_farm_grid(rows, cols, num_obstacles):
    grid = np.zeros((rows, cols))
    obstacles = set()
    while len(obstacles) < num_obstacles:
        obstacle = (random.randint(0, rows - 1), random.randint(0, cols - 1))
        if obstacle != (0, 0) and obstacle != (rows - 1, cols - 1):
            obstacles.add(obstacle)
    for obstacle in obstacles:
        grid[obstacle] = -1
    return grid

def visualize_grid(grid, path=None, start=None, end=None, title="Farm Grid"):
    plt.figure(figsize=(8, 8))
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == -1:
                color = 'black' 
            elif path and (i, j) in path:
                color = 'green' 
            elif (i, j) == start:
                color = 'blue' 
            elif (i, j) == end:
                color = 'red' 
            else:
                color = 'white' 

            plt.gca().add_patch(plt.Rectangle((j, grid.shape[0] - i - 1), 1, 1, edgecolor='gray', facecolor=color))

    plt.xlim(0, grid.shape[1])
    plt.ylim(0, grid.shape[0])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(title)
    plt.show()

def dfs(grid, start):
    rows, cols = grid.shape
    visited = set()
    path = []

    def explore(x, y):
        if (x, y) in visited or x < 0 or y < 0 or x >= rows or y >= cols or grid[x, y] == -1:
            return

        visited.add((x, y))
        path.append((x, y))

        explore(x - 1, y)
        explore(x + 1, y)
        explore(x, y - 1)
        explore(x, y + 1)

    explore(*start)
    return path

def bfs(grid, start, target):
    rows, cols = grid.shape
    visited = set()
    queue = deque([(start, [start])])  

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == target:
            return path

        if (x, y) in visited or x < 0 or y < 0 or x >= rows or y >= cols or grid[x, y] == -1:
            continue

        visited.add((x, y))

        queue.append(((x - 1, y), path + [(x - 1, y)]))
        queue.append(((x + 1, y), path + [(x + 1, y)]))
        queue.append(((x, y - 1), path + [(x, y - 1)]))
        queue.append(((x, y + 1), path + [(x, y + 1)]))

    return []  

def visualize_robot_movement(grid, path, title):
    pygame.init()
    cell_size = 40
    rows, cols = grid.shape
    screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
    pygame.display.set_caption(title)

    colors = {
        "free": (255, 255, 255), 
        "obstacle": (0, 0, 0),  
        "path": (0, 255, 0),    
        "start": (0, 0, 255),   
        "end": (255, 0, 0),     
        "robot": (255, 255, 0)   
    }

    clock = pygame.time.Clock()

    def draw_grid():
        for i in range(rows):
            for j in range(cols):
                rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                if grid[i, j] == -1:
                    color = colors["obstacle"]
                elif (i, j) == start:
                    color = colors["start"]
                elif (i, j) == end:
                    color = colors["end"]
                else:
                    color = colors["free"]
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1) 

    for position in path:
        screen.fill((0, 0, 0))
        draw_grid()

        for step in path[:path.index(position) + 1]:
            rect = pygame.Rect(step[1] * cell_size, step[0] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, colors["path"], rect)
        robot_rect = pygame.Rect(position[1] * cell_size, position[0] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, colors["robot"], robot_rect)

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    rows, cols = 10, 10
    num_obstacles = 15
    grid = create_farm_grid(rows, cols, num_obstacles)

    start = (0, 0)
    end = (rows - 1, cols - 1)

    dfs_path = dfs(grid, start)
    visualize_grid(grid, dfs_path, start=start, end=end, title="DFS Full Coverage Path")
    visualize_robot_movement(grid, dfs_path, title="DFS Robot Movement")

    bfs_path = bfs(grid, start, end)
    visualize_grid(grid, bfs_path, start=start, end=end, title="BFS Shortest Path")
    visualize_robot_movement(grid, bfs_path, title="BFS Robot Movement")

