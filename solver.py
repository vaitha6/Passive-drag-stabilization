import numpy as np
import pandas as pd
import random
import helpers 
import __init__


# Tracking particle collisions
particle_counts = {face: [] for face in __init__.face_normals.keys()}

# Initialize lists to store angular velocity and acceleration data for plotting
angular_velocity_history = []
angular_acceleration_history = []

# Simulation loop
for step in range(__init__.total_steps):
    
    total_torque = np.zeros(3)  # Reset total torque for each __init__.timestep
    collisions_per_face = {face: 0 for face in __init__.face_normals.keys()}  # Reset particle count for this __init__.timestep
    collision_points = []
    sum_surface = 0

    # Compute rotation matrix based on current __init__.angles
    rotation_matrix = helpers.compute_rotation_matrix(__init__.angles)
    particle_direction = np.array([1, 0, 0])  # Particles moving along +X in global frame

    # Calculate dot products and probabilities
    dot_products = {}
    for face, normal in __init__.face_normals.items():
        global_normal = rotation_matrix @ normal  # Rotate normal to global frame
        dot_product = np.dot(global_normal, particle_direction)
        if dot_product > 0:  # Consider only faces eligible for collision
            dot_products[face] = dot_product
            sum_surface += __init__.sat_object.surface_area[face]
    
    #Compute actual number of particles colliding with satellite per __init__.timestep based on density model
    actual_num_particles = sum(helpers.density_array[0]) * 10**6 * __init__.particle_velocity[0] * __init__.timestep * sum_surface
    
    #Compute simulated number of particles based on arbitrary simulated particle mass 
    num_particles = int(np.ceil(actual_num_particles * __init__.actual_particle_mass / __init__.particle_mass))

    if dot_products:
        # Normalize dot products to probabilities
        total_dot = sum(dot_products.values())
        total_surface = sum(__init__.sat_object.surface_area.values())
        probabilities = {face: dp / total_dot for face, dp in dot_products.items()}
        # Distribute particles across eligible faces based on probabilities
        
        for _ in range(num_particles):
            face = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
            collision_point = helpers.generate_collision_point(face)  # Random collision point
            r = collision_point - __init__.sat_object.com # Lever arm (in meters)
            satellite_velocity = np.cross(r, __init__.sat_object.angular_velocity)
            relative_velocity = satellite_velocity - __init__.particle_velocity
            force = (__init__.particle_mass * relative_velocity)/__init__.timestep
            torque = np.cross(r, force)  # Torque due to one particle
            total_torque += torque  # Accumulate torque
            collisions_per_face[face] += 1  # Increment particle count for the selected face
            collision_points.append((rotation_matrix @ (collision_point - __init__.sat_object.com), __init__.face_colors[face]))

    # Angular acceleration: alpha = I^(-1) * total_torque
    angular_acceleration = np.linalg.inv(__init__.sat_object.inertia_matrix).dot(total_torque)

    # Update angular velocity: omega = omega + alpha * dt
    __init__.sat_object.angular_velocity += angular_acceleration * __init__.timestep

    # Update rotational __init__.angles: theta = theta + omega * dt
    __init__.angles += __init__.sat_object.angular_velocity * __init__.timestep

    # Store particle counts for this __init__.timestep
    for face, count in collisions_per_face.items():
        particle_counts[face].append(count)
    
    # Store angular velocity, acceleration and collision points data ready for export
    angular_velocity_history.append(__init__.sat_object.angular_velocity.copy())
    angular_acceleration_history.append(angular_acceleration.copy())
    
    # Print results for the current __init__.timestep
    if(step%10==0):
        
        print(f"Step {step + 1}:")
        print(f"  Angular Acceleration: {angular_acceleration}")
        print(f"  Angular Velocity: {__init__.sat_object.angular_velocity}")
        print(f"  __init__.angles: {__init__.angles}")
        print(f"  Particle Counts: {collisions_per_face}")
        print("-" * 40)

#Exporting angular velocity, acceleration and collision points

np.savetxt("angular_velocity_" + __init__.sat_object.sim_id + ".csv", angular_velocity_history, delimiter=",")
np.savetxt("angular_acceleration_" + __init__.sat_object.sim_id + ".csv", angular_acceleration_history, delimiter=",")

(pd.DataFrame.from_dict(data=particle_counts, orient='index')
   .to_csv("particle_counts_" + __init__.sat_object.sim_id + ".csv", header=False))

