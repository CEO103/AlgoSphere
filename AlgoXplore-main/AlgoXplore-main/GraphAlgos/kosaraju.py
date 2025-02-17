import networkx as nx
import matplotlib.pyplot as plt
import argparse
import random
import tkinter as tk
from tkinter import messagebox

def create_graph(edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G

def kosaraju(G, V):
    node_colors = ['skyblue'] * len(G.nodes())  # Set color for each node in the graph
    node_list = list(G.nodes())  # Get all nodes

    adj = [[] for _ in range(V + 1)]
    for u, v in G.edges():
        adj[u].append(v)

    stack = []
    visited = [0] * (V + 1)

    def sort(node):
        visited[node] = 1
        for i in adj[node]:
            if not visited[i]:
                sort(i)
        stack.append(node)

    for i in range(V + 1):
        if not visited[i]:
            sort(i)

    stack.reverse()

    visited = [0] * (V + 1)

    rev_adj = [[] for _ in range(V + 1)]
    for u, v in G.edges():
        rev_adj[v].append(u)

    def dfs(node, l):
        visited[node] = 1
        l.append(node)
        for i in rev_adj[node]:
            if not visited[i]:
                dfs(i, l)

    count = 0
    colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(V + 1)]  # Adjust color length to match nodes

    k = 0
    for i in stack:
        l = []
        if not visited[i]:
            dfs(i, l)
            for m in l:
                if m in node_list:
                    node_colors[node_list.index(m)] = colors[k]  # Color for the component
            yield node_colors
            count += 1
            k += 1

    yield count  # Yield the count of connected components at the end

def visualize_kosaraju(graph, V):
    pos = nx.circular_layout(graph)  # Default layout to circular
    pos = nx.spring_layout(graph, k = 13.5, scale=5, iterations=100)
    fig, ax = plt.subplots(figsize=(8, 8))
    mng = plt.get_current_fig_manager()
    mng.window.wm_geometry("+0+0") 
    stop_animation = False

    def on_close(event):
        nonlocal stop_animation
        stop_animation = True

    fig.canvas.mpl_connect('close_event', on_close)

    generator = kosaraju(graph, V)
    total_components = None
    unique_colors = {}
    check=1
    for node_colors in generator:
        if stop_animation:
            check=0
            break

        if isinstance(node_colors, int):
            total_components = node_colors
            continue

        ax.clear()
        for color in node_colors:
            if color !="skyblue" and color not in unique_colors:
                unique_colors[color] = f'Component {len(unique_colors) + 1}'

        legend_entries = [plt.Rectangle((0, 0), 1, 1, color = color, label=label)
                          for color, label in unique_colors.items()]
        ax.legend(handles=legend_entries, loc='upper right', fontsize=9,bbox_to_anchor=(1.05, 1))
        nx.draw(
            graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
            font_color='black',
            edge_color='black',
            arrowstyle='-|>',  # Arrow style
            arrowsize=20,  # Arrow size
            width=2
        )
        plt.title("Kosaraju's Algorithm Visualization",fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
        plt.pause(1.5)

    if total_components is not None and check:
        plt.title(f"Kosaraju's Algorithm Visualization\nTotal Number of Connected Components: {total_components-1}",fontsize=16,
        fontname='Times New Roman',
        fontweight='bold')
        plt.pause(1.5)

    plt.show()

def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Input Error", message)
    root.destroy()

import ast

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Kosaraju's Algorithm")
parser.add_argument('--edges', type=str, help='List of edges in the format [(u, v), (u, v), ...]')
args = parser.parse_args()

# Check if arguments are provided
if args.edges is not None:
    try:
        edges = ast.literal_eval(args.edges)  # Safely convert string input to a Python list of tuples
        if not isinstance(edges, list):
            raise ValueError("Edges must be provided as a list of tuples.")
        
        # Validate that each edge is a tuple of length 2
        for edge in edges:
            if not isinstance(edge, tuple) or len(edge) != 2:
                raise ValueError("Each edge must be a tuple of two elements: (u, v).")
        
        # Get the maximum vertex count from the edges
        v = max(max(u, v) for u, v in edges)

    except (ValueError, SyntaxError) as e:
        show_error(f"Error parsing edges: {e}")
        exit()

else:
    v = 8  # Default number of vertices
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 7), (4, 5), (5, 6), (6, 4), (4, 7), (6, 7)]  # Default edges

# Check for input errors
if v <= 0:
    show_error("The number of vertices must be a positive integer.")
else:
    # Create the graph from user-provided edges
    G = create_graph(edges)

    # Visualize Kosaraju's algorithm on the created graph
    try:
        visualize_kosaraju(G, v)
    except ValueError as e:
        show_error(str(e))
