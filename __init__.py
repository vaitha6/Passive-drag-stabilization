import numpy as np

# Constants
actual_particle_mass = 1E-23  # kg
particle_mass = 1E-11  # kg
particle_velocity = [5000, 0, 0]  # m/s

#Simulation setup
timestep = 0.1  # seconds
total_steps = 100 # Total timesteps

# Initialize angles
angles = np.zeros(3) # theta_x, theta_y, theta_z

# Face normals in the satellite's body frame
face_normals = {
    "+X": np.array([1, 0, 0]),
    "-X": np.array([-1, 0, 0]),
    "+Y": np.array([0, 1, 0]),
    "-Y": np.array([0, -1, 0]),
    "+Z": np.array([0, 0, 1]),
    "-Z": np.array([0, 0, -1]),
}

face_colors = {
    "+X": "red",
    "-X": "red",
    "+Y": "green",
    "-Y": "green",
    "+Z": "blue",
    "-Z": "blue",
}

class Satellite:

    def __init__(self, length, width, height, com, initial_angular_velocity, inertia_matrix, sim_id):
        """
        Initialize the satellite object with its physical parameters.
        
        :param length: Length of the satellite (m)
        :param width: Width of the satellite (m)
        :param height: Height of the satellite (m)
        :param com: Position vector of the Center of Mass (m), given as a NumPy array [x, y, z]
        :param initial_angular_velocity: Initial angular velocity vector (rad/s), NumPy array [ωx, ωy, ωz]
        :param inertia_matrix: 3x3 Moment of Inertia matrix (kg·m²), NumPy array
        """
        self.length = length
        self.width = width
        self.height = height
        self.com = np.array(com, dtype=float)  # Ensure it's a NumPy array
        self.angular_velocity = np.array(initial_angular_velocity, dtype=float)
        self.inertia_matrix = np.array(inertia_matrix, dtype=float)

        self.surface_area = {
            "+X": self.width*self.height,
            "-X": self.width*self.height,
            "+Y": self.length*self.height,
            "-Y": self.length*self.height,
            "+Z": self.width*self.length,
            "-Z": self.width*self.length,
            }

        self.sim_id = input("Enter simulation id")
    

"""Parameters of the Delfi n3xt satellite 
When changing values, change sim_id to a description that matches the input, for example:

For a 3U cubesat, sim_id = "cubesat_3U"
For Delfi-PQ with initial angular veloicty only in Y-direction, sim_id = "Delfi_vY" viz.
"""

sat_object = Satellite(
    length=0.3,  # meters
    width=0.1,   # meters
    height=0.1,  # meters
    com=[0.1, 0.05, 0.05],  # meters
    initial_angular_velocity=[(np.pi/180)*15, (np.pi/180)*9, 0],  # Initial ω in rad/s
    inertia_matrix=np.diag([0.03699, 0.03701, 0.005]),  # Given as a diagonal matrix
)



