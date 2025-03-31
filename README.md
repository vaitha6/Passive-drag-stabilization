# Attitude dynamics of satellites in the presence of drag in Low Earth Orbit

This repository contains code (refer to [main.py](main.py)) to simulate the attitude dynamics of a satellite in Low Earth Orbit (LEO) based on a discrete collision-based method. The goal is to identify the most stable configuration/ geometry of the satellite such that the drag can be used to passively stabilise it. The current code models only the rotation of the satellite and not its translational movement, i.e., orbital velocity and altitude are considered a constant. (This is only temporary)

## Satellite properties

class "satellite" stores satellite objects with parameters including dimensions along the X, Y and Z-axis, the position of the centre of mass, the initial angular velocity vector and the inertia tensor matrix. The current code consists of a simulation attempted for the Delfi n3xt satellite with its parameters taken from [www.eucass.eu](https://www.eucass.eu/component/docindexer/?task=download&id=4465)

## Drag force

The drag experienced in LEO is simulated in the form of particle collisions with the satellite surface (Due to highly rarefied flow in LEO). Assumptions:

- Particles have a uniform velocity in the axial direction opposing the direction of velocity of the satellite.
- The collision takes place with only the satellite's faces directed towards the particles.
- Particles collide uniformly over a given face determined by a probability distribution function.

The intensity of drag is determined from the NRLMSIS-00 model using a Python interface [pypi.org](https://pypi.org/project/nrlmsise00/). Based on a given epoch and physical co-ordinates (latitude, longitude and altitude), the model provides the particle number density for each species of gas present. 

To reduce the computational effort, a lower number of particles are simulated to collide with the satellite, with the total mass colliding being identical. 

To check if a particle collides with a given satellite surface, the dot product of the area vector with the particle velocity vector is calculated as a criterion.

The collision points are randomly distributed over a surface using the random.uniform() function. The torque produced by each particle is calculated as a cross product of the position vector with respect to the centre of mass of the satellite and the collision force vector. The cumulative torque provides the change in angular velocity which is added at each timestep.

## Sample simulation

## Delfi-n3Xt Satellite Parameters

| Parameter                      | Value                                     | Unit        |
|--------------------------------|-------------------------------------------|------------|
| **Length**                     | 0.1                                       | meters     |
| **Width**                      | 0.1                                       | meters     |
| **Height**                     | 0.3                                       | meters     |
| **Center of Mass (CoM)**        | (0.05, 0.05, 0.1)                         | meters     |
| **Initial Angular Velocity**    | (15, 9, 4)                                | degrees/s      |
| **Moment of Inertia (Ixx)**     | 0.03699                                   | kg·m²      |
| **Moment of Inertia (Iyy)**     | 0.03701                                   | kg·m²      |
| **Moment of Inertia (Izz)**     | 0.005                                     | kg·m²      |

## Density model

| Parameter                     | Value                                  | Unit        |
|--------------------------------|----------------------------------------|------------|
| **Density Model Used**         | MSISE00 Atmosphere Model               | —          |
| **Density Calculation Date**   | December 1, 2013, 08:03:20 UTC         | —          |
| **Altitude**                   | 600                                    | km         |
| **Latitude**                   | 75                                     | degrees    |
| **Longitude**                  | -70                                    | degrees    |
| **Solar Activity Index (F10.7A, F10.7B)** | (150, 150)                 | sfu        |
| **Geomagnetic Activity Index (AP)** | 4                               | —          |
| **Local Solar Time**           | 16                                     | hours      |

## Simulation parameters

| Parameter                     | Value                                  | Unit        |
|--------------------------------|----------------------------------------|------------|
| **Actual Mass per Particle**   | 1e-23                                  | kg         |
| **Simulated Particle Mass**    | 1e-11                                  | kg         |
| **Actual number of particles**   | ~ 3.106e+15                                 |          |
| **Simulated number of particles**    | 3100                                  |          |
| **Particle Velocity**          | (5000, 0, 0)                           | m/s        |
| **Timestep**                   | 0.1                                    | seconds    |
| **Total Simulation Time**      | 100                                    | seconds    |

## Results

![image](AngularVnA_vs_time_updated.png)
