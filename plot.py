"""
Created on Thu Sep 13 2024

@author: Dalia Manfrin
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

# Paths for input and output
source = 'C:/Users/Dalia/Desktop/project/particle_counts.npy'
destination = 'C:/Users/Dalia/Desktop/project/distribution.png'

# Load particle counts results
particle_counts = np.load(source, allow_pickle=True)

data_distribution = [item for sublist in particle_counts for item in sublist]
data = np.array(data_distribution)

def plot_particle_distribution():
    """
    This function generates and saves a histogram plot of particle counts over time.
    """
    bins = np.arange(data.min() - 1 / 2, data.max() + 1, 1)
    
    plt.figure(figsize=(6, 4))
    sns.set(style="whitegrid")
    sns.histplot(data, bins=bins, kde=False, color='mediumslateblue')
    
    # Label the axes and set the title
    plt.xlabel('Particle Count', fontsize=13)
    plt.ylabel('Frequency', fontsize=13)
    
    # Set custom x-ticks
    labels = np.arange(0, bins.max(), 5)
    plt.gca().set_xticks(labels)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(destination, dpi=300)
    plt.show()

plot_particle_distribution()

print(f"Figure saved at {destination}")
