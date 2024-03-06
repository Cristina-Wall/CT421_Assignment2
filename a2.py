import networkx as nx
import random
import matplotlib.pyplot as plt
from collections import Counter
import copy

# Method to generate a small world graph with n nodes, each node connected to k nearest neighbors, and rewiring probability p.
def generate_small_world_graph(nodes, k, p):
    return nx.watts_strogatz_graph(nodes, k, p)

# Method to assign random colours to each node
def assign_random_colors(graph, colors):
    color_mapping = {node: {'color': tuple(random.choice(colors))} for node in graph.nodes}
    nx.set_node_attributes(graph, color_mapping)

# Method to define a list of colours
def choose_colors(num_colors):
    # Choose random numbers for RBG elements of each colour
    return [(random.random(), random.random(), random.random()) for _ in range(num_colors)]

# Method to count how many conflicts there are
def count_conflicts(graph):
    conflicts = 0
    for node in graph.nodes:
        neighbors = list(graph.neighbors(node))
        for neighbor in neighbors:
            if graph.nodes[node]['color'] == graph.nodes[neighbor]['color']:
                conflicts += 1
    return conflicts

# Method to change the colors of the nodes
def change_node_color(graph, node, colors):
    neighbor_colors = [graph.nodes[neighbor].get('color') for neighbor in graph.neighbors(node) if 'color' in graph.nodes[neighbor]]
    neighbor_color_counts = Counter(tuple(color) for color in neighbor_colors)
    # Check if there's a colour not present among neighbors
    available_colors = [color for color in colors if neighbor_color_counts[tuple(color)] == 0]
    if available_colors:
        new_color = random.choice(available_colors)
    else:
        # If all colours are present among neighbors, choose the colour with the fewest occurrences
        new_color = min(neighbor_color_counts, key=neighbor_color_counts.get)
    
    # Create a new dictionary with updated color attribute
    new_attributes = {node: {'color': new_color}}

    # Update node attributes
    nx.set_node_attributes(graph, new_attributes)

# Method to add a new color to the list of colors
def add_color(colors):
    new_color = (random.random(), random.random(), random.random())
    colors.append(new_color)
    return colors

# Choose the colours and generate the starting graph
colors = choose_colors(2)
graph1 = generate_small_world_graph(100, 5, 0.25)
# Assign random colours to the nodes of the starting graph
assign_random_colors(graph1, colors)
conflicts = count_conflicts(graph1)
print(f'Initial conflicts: {conflicts}')

# Add the graphs to a list so that we can plot them if needed
graphs = [graph1]

# Create new graphs and update them in iterations
while conflicts > 0:
    for i in range(100):
        new_graph = copy.deepcopy(graphs[i])
        for node in new_graph.nodes:
            change_node_color(new_graph, node, colors)
        conflicts = count_conflicts(new_graph)
        print(f'Conflicts after iteration {i+1}: {conflicts}')
        
        graphs.append(copy.deepcopy(new_graph))

        if(conflicts == 0):
            break

        new_graph.clear()
    
    # While the graph has conflicts add another color and repeat
    colors = add_color(colors)

print("Num colors at end: ", len(colors))

# Plot all graphs
# fix, axes = plt.subplots(1, len(graphs), figsize=(15, 5))
# for i, graph in enumerate(graphs):
#     node_colors = list(nx.get_node_attributes(graph, 'color').values())
#     nx.draw(graph, ax=axes[i], with_labels=True, node_color=node_colors)
#     axes[i].set_title(f'Tree {i+1}')
# plt.tight_layout()
# plt.show()

# Plot the initial graph and the final graph
fix, axes = plt.subplots(1, 2, figsize=(10, 5))
node_colors_1 = list(nx.get_node_attributes(graphs[0], 'color').values())
nx.draw(graphs[0], ax=axes[0], with_labels=True, node_color=node_colors_1)
axes[0].set_title('Initial Graph')

last_graph_pos = len(graphs) - 1
node_colors_2 = list(nx.get_node_attributes(graphs[-1], 'color').values())
nx.draw(graphs[-1], ax=axes[1], with_labels=True, node_color=node_colors_2)
axes[1].set_title('Final Graph')
plt.tight_layout()
plt.show()

# Print the list of colours of the nodes in graphs[0]
# print(list(nx.get_node_attributes(graphs[0], 'color').values()), "\n\n")
# print(list(nx.get_node_attributes(graphs[-1], 'color').values()), "\n\n")
