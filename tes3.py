import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("3D Scatter Plot with Plane and Line in PyQt5")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create matplotlib Figure and Canvas
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Create 3D axes
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Plot example data
        self.plot_3d_scatter_with_plane_and_line()

    def plot_3d_scatter_with_plane_and_line(self):
        # Generate random data
        num_points = 100
        x = np.random.rand(num_points)
        y = np.random.rand(num_points)
        z = np.random.rand(num_points)

        # Clear previous plot
        self.ax.clear()

        # Create scatter plot
        self.ax.scatter(x, y, z, c='r', marker='o')

        # Add blue plane at z=0.6
        self.add_plane(z_value=0.6)

        # Draw the line from (0, 0, 0.6) to (0.3, 0.3, 0.6)
        self.draw_line(start_point=(0, 0, 0.6), end_point=(0.3, 0.3, 0.6))

        # Set labels
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')

        # Invert the Y axis direction
        self.ax.set_ylim(self.ax.get_ylim()[::-1])

        # Set the view angle
        self.ax.view_init(elev=30, azim=-60)  # Adjust the elevation and azimuthal angle

        # Set title
        self.ax.set_title('3D Scatter Plot with Plane and Line')

        # Draw the canvas
        self.canvas.draw()

    def add_plane(self, z_value):
        # Create a grid of x and y values
        x = np.linspace(0, 1, 10)
        y = np.linspace(0, 1, 10)
        X, Y = np.meshgrid(x, y)

        # Z values are constant
        Z = np.full_like(X, z_value)

        # Plot the plane
        self.ax.plot_surface(X, Y, Z, color='blue', alpha=0.5)

    def draw_line(self, start_point, end_point):
        # Extract coordinates
        x = [start_point[0], end_point[0]]
        y = [start_point[1], end_point[1]]
        z = [start_point[2], end_point[2]]

        # Plot the line
        self.ax.plot(x, y, z, color='black', linestyle='-', marker='o')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
