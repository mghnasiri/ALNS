import matplotlib.pyplot as plt
import pandas as pd


def visualize_graph(G, depot, nx, best_route, my_pos, dataset_name_with_extension, file_path):
    fig, ax1 = plt.subplots(1, 1, figsize=(10, 10))
    # ... rest of your code ...
    fig.subplots_adjust(hspace=0.5, top=0.93) # Adjust the space between subplots
    
    fig.canvas.manager.set_window_title(dataset_name_with_extension)
    
    ax1.set_title('Optimal Tour')
    ax1.axis('off')
    # Convert best_route to edges
    tour_edges = [(best_route[i], best_route[i+1]) for i in range(len(best_route) - 1)]
    #tour_edges.append((best_route[-1], best_route[0]))  # To complete the cycle, if it's a round trip

    node_colors = ["red" if node == depot else "yellow" for node in G.nodes()]
    node_sizes = [100 if node == depot else 50 for node in G.nodes()]
    num_edges = len(tour_edges)
    num_nodes = len(G.nodes())

    # Visualizing the graph with the best route highlighted
    nx.draw(G, pos=my_pos, ax=ax1, edgelist=tour_edges, node_color=node_colors, node_size=node_sizes,  
                 edge_color='green', width=2.0, with_labels=True)
    ax1.set_title(f'Graph with {num_nodes} nodes', pad=20)
    
    plt.tight_layout()
    plt.savefig(file_path) 
    plt.close()  # Close the figure after saving to avoid interference with the next plot

    
    
    
def plot_length_improvement(best_lengths, current_lengths,file_path,dataset_name_with_extension,dpi, title='Length Improvement Over Iterations'):
    """
    Plots the improvement of best_length and the current_length over iterations.

    :param best_lengths: List of best lengths at each iteration.
    :param current_lengths: List of current lengths at each iteration.
    :param title: Title of the plot.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(best_lengths, label='Best Length', color='blue')
    plt.plot(current_lengths, label='Current Length', color='orange', linestyle='--')
    plt.xlabel('Iteration')
    plt.ylabel('Length')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.get_current_fig_manager().set_window_title(f'Length Improvement')

    plt.savefig(file_path,dpi=dpi) 
    plt.close()  # Close the figure after saving to avoid interference with the next plot
    
    
def plot_heuristic_weights(iterations, heuristic_weights,file_path,dpi, title):
    plt.figure(figsize=(12, 8))
    for heuristic, weights in heuristic_weights.items():
        if weights:  # Ensure the list is not empty
            plt.plot(range(len(weights)), weights, label=heuristic)
    plt.xlabel('Iteration')
    plt.ylabel('Weight')
    plt.legend()

    plt.savefig(file_path,dpi=dpi) 
    plt.close()  # Close the figure after saving to avoid interference with the next plot    

    


    
