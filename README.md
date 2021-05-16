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

# Example: Setting up a scenario

Here, we demonstrate how one can setup up their own scenario using the Moral Dynamics framework.

We decided to represent each scenario as a callable function. We'll setup a simple scenario with three agents, defined by the ```Agent``` class, in a simple environment, defined by the ```Environment``` class. In this scenario we will have an "agent" that pushes a "patient" into a "fireball". When the "patient" collides with the "fireball" we want the patient to be removed from the scene, so as to demonstrate the patient was harmed.

```python
def simple_scenario(view=True,std_dev=0,frict=0.05)
    # A simple scenario
      
    # Agents
    # We define our agents via their parameters through dictionaries
    agent, patient, fireball = {}, {}, {}
    # Agent parameters include:
    # Starting location, indexed by 'loc'
    agent['loc'] = (100,300) 
    patient['loc'] = (800,300)
    fireball['loc'] = (500,300)
    # Color of the agent, indexed by 'color'
    agent['color'] = "blue"
    patient['color'] = "green"
    fireball['color'] = "red"
    # The actions the agent takes during the simulation (i.e. it's policy),
    #  indexed by 'moves'. Importantly, actions are discretized and time-limited.
    #  They only last a certain amount of ticks and when an agent has finished its 
    #  policy, the simulation will stop.
    agent['moves'] = ['R', 'R', 'R', 'R', 'R']
    patient['moves'] = ['N', 'N', 'N', 'N', 'N']
    fireball['moves'] = ['N', 'N', 'N', 'N', 'N']
    # A collision type, indexed by 'col'. This is a native pymunk property that
    #  let's pymunk know which collision handlers apply to which objects.
    agent['coll'] = 0
    patient['coll'] = 1
    fireball['coll'] = 3
    
    # Environment
    # The environment also needs to be defined. First we define the collision handlers.
    #  These are formally defined in handlers.py and then placed in a list of triples,
    #  that denote the function that is called during a collision and the collision types 
    #  the function applies to. In order, the three below simply notify when the agent 
    #  collides with a patient, when the agent collides with the fireball, and removes the 
    #  patient when it collides with the fireball, respectively.
    handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
    # We also define the target velcoties for each of the agents as a triple, with the
    #  implicit ordering of agent, patient, fireball (first object, second object, third object)
    vel = 300,150,150
    # Finally, we take each of these defined parameters and pass them into the Environment class
    #  constructor.
    env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
    # This is then returned as an object to be queried by the various modules within the framework.
    return env
```

Now that we have defined our scenario, we can construct it with a simple call and use it:

```python
simple_env = simple_scenario()

# To run and view the scenario for debugging
simple_env.run(view=True)

# To run a counterfactual of the scenario
from counterfactual import counterfactual_simulation
# Probability that the agent caused the outcome of the simple_scenario
prob_of_cause = counterfactual_simulation(environment=simple_env,std_dev=1.2,num_times=1000,view=False)
```

To record the variables of interest from these scenarios such as effort, causality, and features en masse, refer to the documentation within the record.py file.

