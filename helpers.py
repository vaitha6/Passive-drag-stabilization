from nrlmsise00 import msise_model
import msise00
from datetime import datetime
import random
from scipy.spatial.transform import Rotation as R
import numpy as np
import __init__ 

#Density model: NRLMSIS-00
density_array = msise_model(datetime(2013, 12, 1, 8, 3, 20), 600, 75, -70, 150, 150, 4, lst=16)
#density_array = msise00.run(time=datetime(2013, 3, 31, 12), altkm=150., glat=65., glon=-148.)

"""
The density model uses an arbitrary input relevant to the Delfi n3xt mission to calculate the number of particles colliding with the satellite
"""


# Generate collision points for particles on each face
def generate_collision_point(face):
    """
    Generate a random collision point for a given face.
    :param face: The face to generate collision point for.
    :return: Collision point on the satellite surface (in meters).
    """
    if face == "+X":
        return np.array([__init__.sat_object.length,  random.uniform(0, __init__.sat_object.width),  random.uniform(0, __init__.sat_object.height)]) 
    elif face == "-X":
        return np.array([0,  random.uniform(0, __init__.sat_object.width),  random.uniform(0, __init__.sat_object.height)]) 
    elif face == "+Y":
        return np.array([ random.uniform(0, __init__.sat_object.length), __init__.sat_object.width, random.uniform(0, __init__.sat_object.height)]) 
    elif face == "-Y":
        return np.array([ random.uniform(0, __init__.sat_object.length), 0,  random.uniform(0, __init__.sat_object.height)])
    elif face == "+Z":
        return np.array([ random.uniform(0, __init__.sat_object.length),  random.uniform(0, __init__.sat_object.width), __init__.sat_object.height])
    elif face == "-Z":
        return np.array([ random.uniform(0, __init__.sat_object.length),  random.uniform(0, __init__.sat_object.width), 0])

#Function to compute rotation matrix from current angles
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


