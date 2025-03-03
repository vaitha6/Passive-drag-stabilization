# Attitude dynamics of satellites in the presence of drag in Low Earth Orbit

This repository contains code to simulate the attitude dynamics of a satellite in Low Earth Orbit (LEO) based on a Monte Carlo analysis. The goal is to identify the most stable configuration/ geometry of the satellite such that the drag can be used to passively stabilise the satellite. The current code models only the rotation of the satellite and not its translational movement, i.e., orbital velocity and altitude are considered a constant. (This is only temporary)

## Satellite properties

class "satellite" stores satellite objects with parameters including dimensions along the X, Y and Z-axis, the position of the centre of mass, the initial angular velocity vector and the inertia tensor matrix. The current code consists of a simulation attempted for the Delfi n3xt satellite with its parameters taken from [link text]([http://dev.nodeca.com](https://www.eucass.eu/component/docindexer/?task=download&id=4465))

## Drag force

The drag experienced in LEO is simulated in the form of particle collisions with the satellite surface. Assumptions:

- Particles have a uniform velocity in the axial direction opposing the direction of velocity of the satellite.
- The collision takes place with only the satellite's faces directed towards the particles.
- Particles collide uniformly over a given face determined by a probability distribution function.

The intensity of drag can be varied by changing the mass, velocity and/or number of particles colliding with the satellite per timestep.


