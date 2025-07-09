import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def plot_skewness_diagram(mode, median, mean, title=None):
    """
    Plot a diagram showing skewness based on the positions of mode, median, and mean.
    
    Parameters:
    -----------
    mode : float
        The mode value
    median : float
        The median value
    mean : float
        The mean value
    title : str, optional
        Title for the plot
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
    
    # Create x range based on the provided statistics
    min_val = min(mode, median, mean) - 5
    max_val = max(mode, median, mean) + 5
    
    x = np.linspace(min_val, max_val, 1000)
    
    # Determine skewness direction and create an appropriate distribution curve
    if mean < median < mode:  # Negative skew
        y = stats.skewnorm.pdf(x, a=-5, loc=(min_val + max_val)/2, scale=(max_val-min_val)/6)
    elif mode < median < mean:  # Positive skew
        y = stats.skewnorm.pdf(x, a=5, loc=(min_val + max_val)/2, scale=(max_val-min_val)/6)
    else:  # Generate a custom distribution to match the specific pattern
        # In this case mode > mean and median > mean (mixed pattern)
        # We'll use a mixture of normal distributions to match this pattern
        y1 = stats.norm.pdf(x, loc=mean-2, scale=2)
        y2 = stats.norm.pdf(x, loc=mode, scale=1.5)
        y = 0.6*y1 + 0.4*y2
        # Normalize to make it look nice
        y = y / np.max(y) * 0.4
        
    ax1.plot(x, y, 'r-', linewidth=2)
    ax1.fill_between(x, y, alpha=0.3, color='skyblue')
    
    if title is None:
        title = f"Skewness Diagram (Mode={mode}, Median={median}, Mean={mean})"
    
    # Set titles and labels
    ax1.set_title(title, fontsize=15)
    ax1.set_ylabel("Frequency", fontsize=12)
    ax1.set_xlabel("Values", fontsize=12)
    
    # Plot vertical lines for mean, median, and mode
    ylim = ax1.get_ylim()
    ax1.vlines(mode, 0, ylim[1]*0.9, colors='purple', linestyles='--', label=f'Mode: {mode}')
    ax1.vlines(median, 0, ylim[1]*0.8, colors='green', linestyles='--', label=f'Median: {median}')
    ax1.vlines(mean, 0, ylim[1]*0.7, colors='red', linestyles='--', label=f'Mean: {mean}')
    ax1.legend()
    
    # Create the skewness arrow diagram in the lower subplot
    ax2.set_ylim(0, 1)
    ax2.set_xlim(min_val, max_val)
    
    # Remove y-axis ticks and labels for the skewness diagram
    ax2.set_yticks([])
    ax2.set_ylabel("Skewness\nIndicator", fontsize=12)
    
    # Plot points for mean, median, and mode on the line
    ax2.plot(mode, 0.5, 'o', color='purple', markersize=10, label='Mode')
    ax2.plot(median, 0.5, 'o', color='green', markersize=10, label='Median')
    ax2.plot(mean, 0.5, 'o', color='red', markersize=10, label='Mean')
    
    # Connect points with a line
    ax2.plot([mean, median, mode], [0.5, 0.5, 0.5], 'k-', alpha=0.3)
    
    # Add labels beneath each point
    ax2.text(mode, 0.3, f"Mode\n{mode}", ha='center', va='top', color='purple', fontweight='bold')
    ax2.text(median, 0.3, f"Median\n{median}", ha='center', va='top', color='green', fontweight='bold')
    ax2.text(mean, 0.3, f"Mean\n{mean}", ha='center', va='top', color='red', fontweight='bold')
    
    # Determine skewness type
    if mean < median < mode:
        skew_text = "Negative Skew (Left-tailed)"
        pearson_skew = 3 * (mean - median)
    elif mode < median < mean:
        skew_text = "Positive Skew (Right-tailed)"
        pearson_skew = 3 * (mean - median)
    else:
        skew_text = "Mixed Skewness Pattern"
        pearson_skew = 3 * (mean - median)
        
    # Calculate Pearson's coefficient of skewness
    pearson_coefficient = round(pearson_skew, 3)
    skew_text += f"\nPearson's Coefficient: {pearson_coefficient}"
    
    ax2.set_title(skew_text, fontsize=12)
    
    plt.tight_layout()
    return fig

# Use the provided values
mode = 34    # Modus
median = 90.5  # Median
mean = 60   # Mean

# Create and display the skewness diagram
fig = plot_skewness_diagram(mode, median, mean, title="Skewness Analysis with Given Statistics")
plt.show()