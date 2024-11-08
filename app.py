import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Define PC cases with their dimensions (height, width, depth in mm)
cases = {
    "NZXT H7 Elite": {
        "dimensions": (505, 230, 480),  # height, width, depth
        "color": (0.53, 0.81, 0.92),  # Light blue
        "description": "ATX Mid-Tower"
    },
    "Lian Li LANCOOL 216": {
        "dimensions": (491.7, 235, 480.9),
        "color": (0.6, 0.98, 0.6),    # Light green
        "description": "ATX Mid-Tower"
    },
    "Meshify 2 Compact": {
        "dimensions": (424, 210, 475),
        "color": (0.87, 0.63, 0.87),  # Light purple
        "description": "Compact ATX"
    },
    "Fractal Design Node 202": {
        "dimensions": (332, 125, 385),
        "color": (0.94, 0.90, 0.55),  # Light yellow
        "description": "Mini-ITX"
    }
}

def create_figure():
    """Create and configure the matplotlib figure with proper styling."""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Set background color
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    
    return fig, ax

def draw_box(ax, x_offset, y, z, height, width, depth, color, label, description):
    """Draw a 3D box with improved styling and labels.
    x is width (facing us), y is depth (back on desk), z is height"""
    vertices = [
        # Front face (width × height)
        [(x_offset, y, z), 
         (x_offset + width, y, z), 
         (x_offset + width, y, z + height), 
         (x_offset, y, z + height)],
        # Right side (depth × height)
        [(x_offset + width, y, z), 
         (x_offset + width, y + depth, z), 
         (x_offset + width, y + depth, z + height), 
         (x_offset + width, y, z + height)],
        # Back face (width × height)
        [(x_offset + width, y + depth, z), 
         (x_offset, y + depth, z), 
         (x_offset, y + depth, z + height), 
         (x_offset + width, y + depth, z + height)],
        # Left side (depth × height)
        [(x_offset, y + depth, z), 
         (x_offset, y, z), 
         (x_offset, y, z + height), 
         (x_offset, y + depth, z + height)],
        # Top face (width × depth)
        [(x_offset, y, z + height), 
         (x_offset + width, y, z + height), 
         (x_offset + width, y + depth, z + height), 
         (x_offset, y + depth, z + height)],
        # Bottom face (width × depth)
        [(x_offset, y, z), 
         (x_offset + width, y, z), 
         (x_offset + width, y + depth, z), 
         (x_offset, y + depth, z)]
    ]
    
    box = Poly3DCollection(vertices, alpha=0.6, edgecolor='black', linewidth=1)
    box.set_facecolor(color)
    ax.add_collection3d(box)
    
    # Add labels with dimensions
    label_text = f"{label}\n{description}\n{height}×{width}×{depth} mm"
    ax.text(x_offset + width/2, y + depth/2, z + height + 20, label_text, 
            ha='center', va='bottom', fontsize=9, fontweight='bold')

def draw_soda_can(ax, x_offset):
    """Draw a more realistic soda can for scale."""
    height = 122  # mm
    radius = 33   # mm
    resolution = 100
    
    theta = np.linspace(0, 2*np.pi, resolution)
    z = np.linspace(0, height, resolution)
    theta, z = np.meshgrid(theta, z)
    
    x = radius * np.cos(theta) + x_offset
    y = radius * np.sin(theta)
    
    # Draw can with gradient color
    ax.plot_surface(x, y, z, color='royalblue', alpha=0.7, 
                   rstride=5, cstride=5, linewidth=0.1)
    
    # Add label
    ax.text(x_offset, 0, height + 20, 'Soda Can\n(122×66 mm)', 
            ha='center', va='bottom', fontsize=9, fontweight='bold')

def main():
    fig, ax = create_figure()
    
    # Calculate total width needed
    total_width = sum(case_info['dimensions'][1] for case_info in cases.values())
    spacing = 50  # mm between cases
    
    # Plot cases with proper spacing
    current_x = 0
    for label, case_info in cases.items():
        height, width, depth = case_info['dimensions']
        draw_box(ax, current_x, 0, 0, height, width, depth,
                case_info['color'], label, case_info['description'])
        current_x += width + spacing
    
    # Add soda can for scale
    draw_soda_can(ax, current_x + 50)
    
    # Set axis limits to match real dimensions
    max_height = max(case_info['dimensions'][0] for case_info in cases.values())
    max_depth = max(case_info['dimensions'][2] for case_info in cases.values())
    total_width_with_spacing = current_x + 150  # Add space for soda can
    
    ax.set_xlim([-50, total_width_with_spacing + 50])
    ax.set_ylim([-50, max_depth + 50])
    ax.set_zlim([0, max_height + 100])
    
    # Customize axes
    ax.set_xlabel('Width (mm)', labelpad=10)
    ax.set_ylabel('Depth (mm)', labelpad=10)
    ax.set_zlabel('Height (mm)', labelpad=10)
    
    # Set title
    plt.title('PC Case Size Comparison\nwith Soda Can for Scale', 
             y=1.1, fontsize=14, fontweight='bold')
    
    # Adjust view angle for better perspective
    ax.view_init(elev=20, azim=-45)
    
    # Set aspect ratio and limits to maintain true proportions
    ax.set_box_aspect([(total_width_with_spacing + 100)/500, 
                      (max_depth + 100)/500, 
                      (max_height + 100)/500])
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
