import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Define PC cases with their dimensions and additional details
cases = {
    "NZXT H7 Elite": {
        "dimensions": (505, 230, 480),  # height, width, depth in mm
        "color": (0.53, 0.81, 0.92),    # Light blue
        "description": "ATX Mid-Tower",
        "volume": "55.7L"
    },
    "Lian Li LANCOOL 216": {
        "dimensions": (491.7, 235, 480.9),
        "color": (0.6, 0.98, 0.6),      # Light green
        "description": "ATX Mid-Tower",
        "volume": "55.6L"
    },
    "Meshify 2 Compact": {
        "dimensions": (424, 210, 475),
        "color": (0.87, 0.63, 0.87),    # Light purple
        "description": "Compact ATX",
        "volume": "42.4L"
    },
    "Fractal Design Node 202": {
        "dimensions": (332, 125, 385),
        "color": (0.94, 0.90, 0.55),    # Light yellow
        "description": "Mini-ITX",
        "volume": "16.0L"
    }
}

class PCCaseVisualizer:
    def __init__(self, cases_data):
        self.cases = cases_data
        self.fig = None
        self.ax = None
        
    def create_figure(self):
        """Create and configure the matplotlib figure with proper styling."""
        self.fig = plt.figure(figsize=(14, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Set colors and style
        self.ax.set_facecolor('white')
        self.fig.patch.set_facecolor('white')
        
        # Remove panes for cleaner look
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        
        # Make grid lines lighter
        self.ax.grid(True, linestyle='--', alpha=0.3)
        
    def draw_box(self, x_offset, y, z, height, width, depth, color, label, description, volume):
        """Draw a 3D box with improved styling and labels."""
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
        self.ax.add_collection3d(box)
        
        # Add labels with improved formatting
        label_text = f"{label}\n{description}\n{height}×{width}×{depth} mm\n{volume}"
        self.ax.text(x_offset + width/2, y + depth/2, z + height + 20, label_text, 
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

    def draw_soda_can(self, x_offset):
        """Draw a more realistic soda can for scale."""
        height = 122  # mm
        radius = 33   # mm
        resolution = 100
        
        theta = np.linspace(0, 2*np.pi, resolution)
        z = np.linspace(0, height, resolution)
        theta, z = np.meshgrid(theta, z)
        
        x = radius * np.cos(theta) + x_offset
        y = radius * np.sin(theta)
        
        # Draw can with improved appearance
        can = self.ax.plot_surface(x, y, z, color='royalblue', alpha=0.7,
                                 rstride=5, cstride=5, linewidth=0.1)
        
        # Add label with volume
        volume = np.pi * (radius/1000)**2 * (height/1000) * 1000  # Liters
        label_text = f'Soda Can\n{height}×{2*radius} mm\n{volume:.1f}L'
        self.ax.text(x_offset, 0, height + 20, label_text,
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

    def visualize(self):
        """Create the complete visualization."""
        self.create_figure()
        
        # Calculate layout parameters
        spacing = 50  # mm between cases
        current_x = 0
        
        # Draw cases
        for label, case_info in self.cases.items():
            height, width, depth = case_info['dimensions']
            self.draw_box(current_x, 0, 0, height, width, depth,
                         case_info['color'], label, case_info['description'],
                         case_info['volume'])
            current_x += width + spacing
        
        # Add soda can for scale
        self.draw_soda_can(current_x + 50)
        
        # Set axis limits and labels
        max_height = max(case['dimensions'][0] for case in self.cases.values())
        max_depth = max(case['dimensions'][2] for case in self.cases.values())
        total_width = current_x + 150  # Add space for soda can
        
        self.ax.set_xlim([-50, total_width + 50])
        self.ax.set_ylim([-50, max_depth + 50])
        self.ax.set_zlim([0, max_height + 100])
        
        # Customize axes
        self.ax.set_xlabel('Width (mm)', labelpad=10)
        self.ax.set_ylabel('Depth (mm)', labelpad=10)
        self.ax.set_zlabel('Height (mm)', labelpad=10)
        
        # Set title with improved styling
        plt.title('PC Case Size Comparison\nwith Soda Can for Scale', 
                 y=1.05, fontsize=16, fontweight='bold', pad=20)
        
        # Adjust view angle
        self.ax.view_init(elev=20, azim=-45)
        
        # Set aspect ratio to maintain true proportions
        self.ax.set_box_aspect([(total_width + 100)/500,
                               (max_depth + 100)/500,
                               (max_height + 100)/500])
        
        plt.tight_layout()
        plt.show()

def main():
    visualizer = PCCaseVisualizer(cases)
    visualizer.visualize()

if __name__ == "__main__":
    main()