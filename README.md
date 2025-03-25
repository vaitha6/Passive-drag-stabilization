# Attitude dynamics of satellites in the presence of drag in Low Earth Orbit

This repository contains code to simulate the attitude dynamics of a satellite in Low Earth Orbit (LEO) based on a Monte Carlo analysis. The goal is to identify the most stable configuration/ geometry of the satellite such that the drag can be used to passively stabilise the satellite. The current code models only the rotation of the satellite and not its translational movement, i.e., orbital velocity and altitude are considered a constant. (This is only temporary)

## Satellite properties

class "satellite" stores satellite objects with parameters including dimensions along the X, Y and Z-axis, the position of the centre of mass, the initial angular velocity vector and the inertia tensor matrix. The current code consists of a simulation attempted for the Delfi n3xt satellite with its parameters taken from [link text]((https://www.eucass.eu/component/docindexer/?task=download&id=4465))

## Drag force

The drag experienced in LEO is simulated in the form of particle collisions with the satellite surface (Due to highly rarefied flow in LEO). Assumptions:

- Particles have a uniform velocity in the axial direction opposing the direction of velocity of the satellite.
- The collision takes place with only the satellite's faces directed towards the particles.
- Particles collide uniformly over a given face determined by a probability distribution function.

The intensity of drag is determined from the NRLMSIS-00 model using a Python interface [link text](https://pypi.org/project/nrlmsise00/). Based on a given epoch and physical co-ordinates (latitude, longitude and altitude), the model provides the particle number density for each species of gas present. 

To reduce the computational effort, a lower number of particles are simulated to collide with the satellite, with the total mass colliding being identical. 

## Simulation setup

The attitude of the satellite is calculated at discrete timesteps based on the following equations:

1. **Lever Arm (r):**  
   The lever arm is the vector from the center of mass (\(\text{COM}\)) to the collision point:  
   \[
   \mathbf{r} = \text{collision\_point} - \text{COM}
   \]

2. **Satellite Velocity at Collision Point (\(\mathbf{v}_{\text{satellite}}\)):**  
   The velocity of the satellite at the collision point is obtained using the cross product of the angular velocity (\(\boldsymbol{\omega}\)) and the lever arm (\(\mathbf{r}\)):  
   \[
   \mathbf{v}_{\text{satellite}} = \boldsymbol{\omega} \times \mathbf{r}
   \]

3. **Relative Velocity (\(\mathbf{v}_{\text{rel}}\)):**  
   The velocity of the particles is given as \(\mathbf{v}_{\text{particle}}\). The relative velocity between the satellite surface and the incoming particles is:  
   \[
   \mathbf{v}_{\text{rel}} = \mathbf{v}_{\text{satellite}} - \mathbf{v}_{\text{particle}}
   \]

4. **Force (\(\mathbf{F}\)):**  
   Assuming an impulse-based approach where the force acts over a timestep \(\Delta t\), the force exerted by a single particle is:  
   \[
   \mathbf{F} = \frac{m_p \mathbf{v}_{\text{rel}}}{\Delta t}
   \]
   where \(m_p\) is the mass of an individual particle.

5. **Torque (\(\boldsymbol{\tau}\)):**  
   The torque exerted by a particle due to impact is given by:  
   \[
   \boldsymbol{\tau} = \mathbf{r} \times \mathbf{F}
   \]



