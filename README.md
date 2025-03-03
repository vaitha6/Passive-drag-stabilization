# Attitude dynamics of satellites in the presence of drag in Low Earth Orbit

This repository contains code to simulate the attitude dynamics of a satellite in Low Earth Orbit (LEO) based on a Monte Carlo analysis. The goal is to identify the most stable configuration/ geometry of the satellite such 
that the drag can be used to passively stabilise the satellite. The current code models only the rotation of the satellite and not its tranlsational movement, i.e, orbital velocity and altitude are considered a constant.
(This is only temporary)

## Satellite properties

class "satellite" stores satellite objects with parameters inlcuding dimensions along X, Y and Z-axii, position of centre of mass, initial angular velocity vector and the inertia tensor matrix. The current code consists of
a simulation attempted for the Delfi n3xt satellite with its parameters taken from [link text]([http://dev.nodeca.com](https://www.eucass.eu/component/docindexer/?task=download&id=4465))

## Drag force

The drag in LEO experienced in LEO is simulated in the form of particle collisions with the satellite surface. 
