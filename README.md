# Moral Dynamics

This repo contains all material for the paper "Moral Dynamics: Grounding Moral Judgment in Intuitive Physics and Intuitive Psychology" by Felix Sosa, Tomer Ullman, Joshua Tenenbaum, Samuel Gershman, and Tobias Gerstenberg. 

### Abstract

When holding others morally responsible, we care about what they did, and what they thought. Traditionally, research in moral psychology has relied on vignette studies, in which a protagonist's actions and thoughts are explicitly communicated. While this research has revealed what variables are important for moral judgment, such as actions and intentions, it is limited in providing a more detailed understanding of exactly how these variables affect moral judgment. Using dynamic visual stimuli that allow for a more fine-grained experimental control, recent studies have proposed a direct mapping from visual features to moral judgments. We embrace the use of visual stimuli in moral psychology, but question the plausibility of a feature-based theory of moral judgment. We propose that the connection from visual features to moral judgments is mediated by an inference about what the observed action reveals about the agent's mental states, and what causal role the agent's action played in bringing about the outcome. We present a computational model that formalizes moral judgments of agents in visual scenes as computations over an intuitive theory of physics combined with an intuitive theory of mind. We test the model's quantitative predictions in three experiments across a wide variety of dynamic interactions between agent and patient.

![Banner](figures/banner.png)

# Repo Structure

```
.
├── code
│   ├── R
│   │   ├── cache
│   │   └── data
│   ├── blender
│   ├── experiments
│   │   ├── experiment_1
│   │   ├── experiment_2
│   │   └── experiment_3
│   └── python
├── data
│   ├── empirical
│   └── model
├── docs
├── figures
│   ├── diagrams
│   │   ├── experiment1
│   │   ├── experiment2
│   │   ├── experiment3
│   │   └── selection
│   └── plots
└── videos
    ├── experiment1
    ├── experiment2
    └── experiment3
```
## code

This directory contains all code related to the project.

### R

Code used to analyze and visualize our data. A rendered html file of the analysis is [here](https://cicl-stanford.github.io/moral_dynamics/).

### experiments

Code for our three experiments. The experiments were run using [psiturk](https://psiturk.org/). 

### blender

Code used to render our physical simulations into videos using [Blender](https://www.blender.org/).

### python

Code used to develop the physical simulations for our experiments and model.

* ```agents.py``` contains the ```Agent``` class, defining the methods for the agents in our simulations
* ```environment.py``` contains the ```Environement``` class, defining the methods for the simulation environments
* ```handlers.py``` contains three necessary collision handlers for the physics engine that resolve collisions (e.g. what should happen when an Agent collides with a Patient)
* ```record.py``` contains functions for recording predictions from our model
* ```convert_to_json.py``` contains methods for converting physics data from a given simulation into a JSON that is then used to render the simulation in 3D
* ```moral_kinematics_scenarios.py``` contains all of the defined simulations we used in our paper
* ```features.py``` contains all of the functions for computing kinematic features from simulation JSON data
* ```video.py``` contains all of the functions for recording the simulations as videos that then are used for stimuli in our experiments

## data

Anonymized data from Experiments 1, 2, and 3. 

## figures

Figures from the paper, and the diagrams of the different video clips. 

## videos 

Video clips from each experiment. 
