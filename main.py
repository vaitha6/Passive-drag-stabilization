import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
from scipy.spatial.transform import Rotation as R
from nrlmsise00 import msise_model
from datetime import datetime

#Density model: NRLMSIS-00
density_array = msise_model(datetime(2013, 12, 1, 8, 3, 20), 600, 75, -70, 150, 150, 4, lst=16)

"""
The density model uses an arbitrary input relevant to the Delfi n3xt mission to calculate the number of particles colliding with the satellite
"""


# Constants
actual_particle_mass = 1E-23  # kg
particle_mass = 1E-11  # kg
particle_velocity = [5000, 0, 0]  # m/s

#Simulation setup
timestep = 0.1  # seconds
total_steps = 1000 # Total timesteps

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

class Satellite:
    def __init__(self, length, width, height, com, initial_angular_velocity, inertia_matrix):
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
        
    def __str__(self):
        """Return a string representation of the satellite's parameters."""
        return (f"Satellite Parameters:\n"
                f"  Dimensions (LxWxH): {self.length}m x {self.width}m x {self.height}m\n"
                f"  Center of Mass: {self.com} m\n"
                f"  Initial Angular Velocity: {self.angular_velocity} rad/s\n"
                f"  Inertia Matrix:\n{self.inertia_matrix}\n")
    
    
#Parameters of the Delfi n3xt satellite
Delfi_n3xt = Satellite(
    length=0.1,  # meters
    width=0.1,   # meters 
    height=0.3,  # meters
    com=[0.05, 0.05, 0.1],  # meters
    initial_angular_velocity=[(np.pi/180)*15, (np.pi/180)*9, (np.pi/180)*4],  # Initial ω in rad/s
    inertia_matrix=np.diag([0.03699, 0.03701, 0.005])  # Given as a diagonal matrix
)


# Generate collision points for particles on each face
def generate_collision_point(face):
    """
    Generate a random collision point for a given face.
    :param face: The face to generate collision point for.
    :return: Collision point on the satellite surface (in meters).
    """
    if face == "+X":
        return np.array([Delfi_n3xt.length,  random.uniform(0, Delfi_n3xt.width),  random.uniform(0, Delfi_n3xt.height)]) 
    elif face == "-X":
        return np.array([0,  random.uniform(0, Delfi_n3xt.width),  random.uniform(0, Delfi_n3xt.height)]) 
    elif face == "+Y":
        return np.array([ random.uniform(0, Delfi_n3xt.length), Delfi_n3xt.width, random.uniform(0, Delfi_n3xt.height)]) 
    elif face == "-Y":
        return np.array([ random.uniform(0, Delfi_n3xt.length), 0,  random.uniform(0, Delfi_n3xt.height)])
    elif face == "+Z":
        return np.array([ random.uniform(0, Delfi_n3xt.length),  random.uniform(0, Delfi_n3xt.width), Delfi_n3xt.height])
    elif face == "-Z":
        return np.array([ random.uniform(0, Delfi_n3xt.length),  random.uniform(0, Delfi_n3xt.width), 0])

# Tracking particle collisions
particle_counts = {face: [] for face in face_normals.keys()}

# Initialize lists to store angular velocity and acceleration data for plotting
angular_velocity_history = []
angular_acceleration_history = []

# Store collision data for animation
collision_points_history = []
satellite_orientation_history = np.zeros((total_steps, 3, 3))

# Function to compute rotation matrix from current angles
def compute_rotation_matrix(angles):
    """
    Compute the combined rotation matrix from X, Y, Z rotations.
    :param angles: Array of rotation angles [theta_x, theta_y, theta_z] in radians.
    :return: Combined rotation matrix.
    """
    rot_x = R.from_euler('x', angles[0], degrees=False).as_matrix()
    rot_y = R.from_euler('y', angles[1], degrees=False).as_matrix()
    rot_z = R.from_euler('z', angles[2], degrees=False).as_matrix()
    
    return rot_z @ rot_y @ rot_x  # ZYX rotation order

# Simulation loop
for step in range(total_steps):
    
    total_torque = np.zeros(3)  # Reset total torque for each timestep
    collisions_per_face = {face: 0 for face in face_normals.keys()}  # Reset particle count for this timestep
    collision_points = []
    sum_surface = 0

    # Compute rotation matrix based on current angles
    rotation_matrix = compute_rotation_matrix(angles)
    particle_direction = np.array([1, 0, 0])  # Particles moving along +X in global frame

    # Calculate dot products and probabilities
    dot_products = {}
    for face, normal in face_normals.items():
        global_normal = rotation_matrix @ normal  # Rotate normal to global frame
        dot_product = np.dot(global_normal, particle_direction)
        if dot_product > 0:  # Consider only faces eligible for collision
            dot_products[face] = dot_product
            sum_surface += Delfi_n3xt.surface_area[face]
    
    #Compute actual number of particles colliding with satellite per timestep based on density model
    actual_num_particles = sum(density_array[0]) * 10**6 * particle_velocity[0] * timestep * sum_surface
    
    #Compute simulated number of particles based on arbitrary simulated particle mass 
    num_particles = int(np.ceil(actual_num_particles * actual_particle_mass / particle_mass))

    if dot_products:
        # Normalize dot products to probabilities
        total_dot = sum(dot_products.values())
        total_surface = sum(Delfi_n3xt.surface_area.values())
        probabilities = {face: dp / total_dot for face, dp in dot_products.items()}
        # Distribute particles across eligible faces based on probabilities
        
        for _ in range(num_particles):
            face = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
            collision_point = generate_collision_point(face)  # Random collision point
            r = collision_point - Delfi_n3xt.com # Lever arm (in meters)
            satellite_velocity = np.cross(r, Delfi_n3xt.angular_velocity)
            relative_velocity = satellite_velocity - particle_velocity
            force = (particle_mass * relative_velocity)/timestep
            torque = np.cross(r, force)  # Torque due to one particle
            total_torque += torque  # Accumulate torque
            collisions_per_face[face] += 1  # Increment particle count for the selected face
            collision_points.append(rotation_matrix @ (collision_point - [Delfi_n3xt.length/2, Delfi_n3xt.width/2, Delfi_n3xt.height/2]) + [0.005, 0.005, 0.01])
            
    # Angular acceleration: alpha = I^(-1) * total_torque
    angular_acceleration = np.linalg.inv(Delfi_n3xt.inertia_matrix).dot(total_torque)

    # Update angular velocity: omega = omega + alpha * dt
    Delfi_n3xt.angular_velocity += angular_acceleration * timestep

    # Update rotational angles: theta = theta + omega * dt
    angles += Delfi_n3xt.angular_velocity * timestep

    # Store particle counts for this timestep
    for face, count in collisions_per_face.items():
        particle_counts[face].append(count)
    
    # Store angular velocity and acceleration data for plotting
    angular_velocity_history.append(Delfi_n3xt.angular_velocity.copy())
    angular_acceleration_history.append(angular_acceleration.copy())
    
    collision_points_history.append(collision_points.copy())
    satellite_orientation_history[step] = rotation_matrix
    
    # Print results for the current timestep
    if(step%10==0):
        
        print(f"Step {step + 1}:")
        print(f"  Angular Acceleration: {angular_acceleration}")
        print(f"  Angular Velocity: {Delfi_n3xt.angular_velocity}")
        print(f"  Angles: {angles}")
        print(f"  Particle Counts: {collisions_per_face}")
        print("-" * 40)
