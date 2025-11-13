import pygame
from collections import deque
import random
import time
import matplotlib.pyplot as plt

# Grid settings
GRID_STEP = 50

def bfs_pathfind(start, goal, obstacles, grid_width, grid_height, step_size, allow_diagonal=True):
    """BFS pathfinding from start to goal, avoiding filled squares"""
    queue = deque([(start, [start])])
    visited = {start}
    nodes_explored = 0
    
    while queue:
        current, path = queue.popleft()
        nodes_explored += 1
        
        if current == goal:
            return path, nodes_explored
        
        # Check neighbors based on movement type
        if allow_diagonal:
            moves = [(0, step_size), (0, -step_size), (step_size, 0), (-step_size, 0),
                     (step_size, step_size), (step_size, -step_size), 
                     (-step_size, step_size), (-step_size, -step_size)]
        else:
            moves = [(0, step_size), (0, -step_size), (step_size, 0), (-step_size, 0)]
        
        for dx, dy in moves:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Check bounds and obstacles
            if (0 <= neighbor[0] < grid_width and 0 <= neighbor[1] < grid_height and 
                neighbor not in visited and neighbor not in obstacles):
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return [], nodes_explored  # No path found

def generate_random_obstacles(num_obstacles, grid_width, grid_height, step_size):
    """Generate random obstacle positions"""
    obstacles = set()
    max_obstacles = (grid_width // step_size) * (grid_height // step_size) // 4
    num_obstacles = min(num_obstacles, max_obstacles)
    
    while len(obstacles) < num_obstacles:
        grid_x = random.randint(0, (grid_width // step_size) - 1) * step_size
        grid_y = random.randint(0, (grid_height // step_size) - 1) * step_size
        obstacles.add((grid_x, grid_y))
    
    return obstacles

def test_computational_cost():
    """Test 1: Computational cost of single pathfinding"""
    print("=" * 60)
    print("TEST 1: COMPUTATIONAL COST OF SINGLE PATHFINDING")
    print("=" * 60)
    
    grid_width = 1000
    grid_height = 400
    step_size = 50
    
    # NO OBSTACLES for consistent behavior
    obstacles = set()
    
    # Test different distances
    distances = [100, 200, 400, 600, 800]
    results = []
    
    for distance in distances:
        start = (0, 0)
        goal = (min(distance, grid_width - step_size), 0)
        
        start_time = time.time()
        path, nodes_explored = bfs_pathfind(start, goal, obstacles, grid_width, grid_height, step_size)
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        results.append({
            'distance': distance,
            'time_ms': execution_time,
            'nodes_explored': nodes_explored,
            'path_length': len(path)
        })
        
        print(f"Distance: {distance}px | Time: {execution_time:.3f}ms | "
              f"Nodes explored: {nodes_explored} | Path length: {len(path)}")
    
    return results

def test_multiple_agents():
    """Test 2: Growth as more agents are added"""
    print("\n" + "=" * 60)
    print("TEST 2: GROWTH WITH MULTIPLE AGENTS")
    print("=" * 60)
    
    grid_width = 1000
    grid_height = 400
    step_size = 50
    
    # NO OBSTACLES for consistent behavior
    obstacles = set()
    
    agent_counts = [1, 2, 5, 10, 15, 20]
    results = []
    
    # Use FIXED start/goal pairs for reproducibility
    random.seed(42)
    fixed_pairs = []
    for _ in range(20):  # Pre-generate 20 pairs
        start = (random.randint(0, (grid_width // step_size) - 1) * step_size,
                random.randint(0, (grid_height // step_size) - 1) * step_size)
        goal = (random.randint(0, (grid_width // step_size) - 1) * step_size,
               random.randint(0, (grid_height // step_size) - 1) * step_size)
        fixed_pairs.append((start, goal))
    
    for num_agents in agent_counts:
        total_start_time = time.time()
        total_nodes = 0
        total_path_length = 0
        
        # Use first num_agents pairs
        for i in range(num_agents):
            start, goal = fixed_pairs[i]
            
            path, nodes_explored = bfs_pathfind(start, goal, obstacles, grid_width, grid_height, step_size)
            total_nodes += nodes_explored
            total_path_length += len(path)
        
        total_end_time = time.time()
        total_time = (total_end_time - total_start_time) * 1000
        
        results.append({
            'num_agents': num_agents,
            'total_time_ms': total_time,
            'avg_time_ms': total_time / num_agents,
            'total_nodes': total_nodes,
            'avg_nodes': total_nodes / num_agents
        })
        
        print(f"Agents: {num_agents} | Total time: {total_time:.3f}ms | "
              f"Avg time/agent: {total_time/num_agents:.3f}ms | "
              f"Total nodes: {total_nodes}")
    
    return results

def test_resolution_scaling():
    """Test 3: Growth as resolution is increased"""
    print("\n" + "=" * 60)
    print("TEST 3: GROWTH WITH INCREASED RESOLUTION")
    print("=" * 60)
    
    grid_width = 1000
    grid_height = 400
    step_sizes = [100, 50, 25, 20, 10]  # Smaller step = higher resolution
    
    # NO OBSTACLES for consistent behavior
    
    results = []
    
    for step_size in step_sizes:
        grid_cells = (grid_width // step_size) * (grid_height // step_size)
        
        obstacles = set()
        
        start = (0, 0)
        goal = (grid_width - step_size, grid_height - step_size)
        
        start_time = time.time()
        path, nodes_explored = bfs_pathfind(start, goal, obstacles, grid_width, grid_height, step_size)
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        
        results.append({
            'step_size': step_size,
            'grid_cells': grid_cells,
            'time_ms': execution_time,
            'nodes_explored': nodes_explored,
            'path_length': len(path)
        })
        
        print(f"Step size: {step_size}px | Grid cells: {grid_cells} | "
              f"Time: {execution_time:.3f}ms | Nodes: {nodes_explored} | "
              f"Path length: {len(path)}")
    
    return results

def test_distance_scaling():
    """Test 4: Cost increase as targets get further away"""
    print("\n" + "=" * 60)
    print("TEST 4: COST INCREASE WITH DISTANCE (NO OBSTACLES)")
    print("=" * 60)
    
    grid_width = 2000
    grid_height = 2000
    step_size = 50
    
    # NO OBSTACLES - pure BFS exploration to show quadratic growth
    obstacles = set()
    
    # Test increasing distances from corner (0,0) WITHOUT diagonal movement
    distances = [200, 400, 800, 1200, 1600, 2000]
    results = []
    
    for distance in distances:
        # Move along axes (not diagonal) to maximize exploration
        start = (0, 0)
        goal = (min(distance, grid_width - step_size), min(distance, grid_height - step_size))
        
        start_time = time.time()
        # DISABLE DIAGONAL to force more exploration
        path, nodes_explored = bfs_pathfind(start, goal, obstacles, grid_width, grid_height, step_size, allow_diagonal=False)
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        manhattan_distance = abs(goal[0] - start[0]) + abs(goal[1] - start[1])
        
        results.append({
            'target_distance': distance,
            'manhattan_distance': manhattan_distance,
            'time_ms': execution_time,
            'nodes_explored': nodes_explored,
            'path_length': len(path)
        })
        
        print(f"Target: {distance}px | Manhattan: {manhattan_distance}px | "
              f"Time: {execution_time:.3f}ms | Nodes: {nodes_explored} | "
              f"Path length: {len(path)}")
    
    return results

def plot_results(test1, test2, test3, test4):
    """Generate plots for all tests"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Test 1: Distance vs Time
    ax1 = axes[0, 0]
    distances = [r['distance'] for r in test1]
    times = [r['time_ms'] for r in test1]
    ax1.plot(distances, times, 'o-', linewidth=2, markersize=8)
    ax1.set_xlabel('Distance', fontsize=11)
    ax1.set_ylabel('Time', fontsize=11)
    ax1.set_title('Test 1: Computational Cost vs Distance', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Test 2: Number of Agents vs Total Time
    ax2 = axes[0, 1]
    agents = [r['num_agents'] for r in test2]
    total_times = [r['total_time_ms'] for r in test2]
    ax2.plot(agents, total_times, 's-', color='orange', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Agents', fontsize=11)
    ax2.set_ylabel('Total Time', fontsize=11)
    ax2.set_title('Test 2: Scaling with Multiple Agents', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Test 3: Grid Cells vs Time (Resolution)
    ax3 = axes[1, 0]
    grid_cells = [r['grid_cells'] for r in test3]
    res_times = [r['time_ms'] for r in test3]
    ax3.plot(grid_cells, res_times, '^-', color='green', linewidth=2, markersize=8)
    ax3.set_xlabel('Number of Grid Cells', fontsize=11)
    ax3.set_ylabel('Time', fontsize=11)
    ax3.set_title('Test 3: Scaling with Grid Resolution', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Test 4: Manhattan Distance vs Nodes Explored
    ax4 = axes[1, 1]
    manhattan_dists = [r['manhattan_distance'] for r in test4]
    nodes = [r['nodes_explored'] for r in test4]
    ax4.plot(manhattan_dists, nodes, 'd-', color='red', linewidth=2, markersize=8)
    ax4.set_xlabel('Manhattan Distance', fontsize=11)
    ax4.set_ylabel('Nodes Explored', fontsize=11)
    ax4.set_title('Test 4: BFS Search Growth', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('pathfinding_performance_analysis.png', dpi=300, bbox_inches='tight')
    print("\n" + "=" * 60)
    print("Plots saved to 'pathfinding_performance_analysis.png'")
    print("=" * 60)
    plt.show()

def main():
    random.seed(42)  # For reproducibility
    
    print("\nSTARTING PATHFINDING PERFORMANCE ANALYSIS")
    print("=" * 60 + "\n")
    
    test1_results = test_computational_cost()
    test2_results = test_multiple_agents()
    test3_results = test_resolution_scaling()
    test4_results = test_distance_scaling()
    
    plot_results(test1_results, test2_results, test3_results, test4_results)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()