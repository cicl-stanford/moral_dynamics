'''
Implementation of feature-based models over the trajectory data
of simulations.

04/02/2021
Felix Sosa
'''
import json

def distance(json_file):
    '''
    Takes in a json and outputs the distance the agents traveled
    in terms of (x,y) units.

    json_file: json file to be parsed
    object_idx: the object to be indexed
    '''
    with open(json_file) as f:
        j = json.load(f)
    object_trajectory = j["objects"]['agent']
    beg = object_trajectory[0]
    end = object_trajectory[-1]
    return ((end['x']-beg['x'])**2+(end['y']-beg['y'])**2)**0.5

def duration(json_file):
    '''
    Takes in a json and outputs the duration of contact between
    a patient and agent in terms of seconds.
    '''
    with open(json_file) as f:
        j = json.load(f)
    a_trajectory = j["objects"]['agent']
    p_trajectory = j["objects"]['patient']
    duration = 0
    for a,p in zip(a_trajectory,p_trajectory):
        if ((a['x']-p['x'])**2 + (a['y']-p['y'])**2)**0.5 <= 50.0: # each agent has radius of 25
            duration += 1
    return (duration/50)/0.75 # The 0.75 is due to slowing the videos 75% in post-processing

def contact(json_file):
    '''
    Takes in a json and outputs whether the agent collides
    with patient at all.
    '''
    with open(json_file) as f:
        j = json.load(f)
    a_trajectory = j["objects"]['agent']
    p_trajectory = j["objects"]['patient']
    for a,p in zip(a_trajectory,p_trajectory):
        if ((a['x']-p['x'])**2 + (a['y']-p['y'])**2)**0.5 <= 50.0: # each agent has radius of 25
           return True
    return False

def frequency(json_file):
    '''
    Takes in a json and outputs number of times agent collides
    with patient.
    '''
    with open(json_file) as f:
        j = json.load(f)
    a_trajectory = j["objects"]['agent']
    p_trajectory = j["objects"]['patient']
    collided = False
    collisions = 0
    for a,p in zip(a_trajectory,p_trajectory):
        if ((a['x']-p['x'])**2 + (a['y']-p['y'])**2)**0.5 <= 50.0 and not collided: # each agent has radius of 25
            collided = True
            collisions += 1
        if ((a['x']-p['x'])**2 + (a['y']-p['y'])**2)**0.5 > 50.0:
            collided = False
    return collisions

def agent_moving(json_file):
    '''
    Takes in a json and outputs whether the agent
    was moving initially in the simulation.

    json_file: json file to be parsed
    '''
    with open(json_file) as f:
        j = json.load(f)
    return j["config"]['agent_init_moving']

def patient_moving(json_file):
    '''
    Takes in a json and outputs whether the patient
    was moving initially in the simulation.

    json_file: json file to be parsed
    '''
    with open(json_file) as f:
        j = json.load(f)
    return j["config"]['patient_init_moving']

def fireball_moving(json_file):
    '''
    Takes in a json and outputs whether the fireball
    was moving initially in the simulation.

    json_file: json file to be parsed
    '''
    with open(json_file) as f:
        j = json.load(f)
    return j["config"]['fireball_init_moving']

def collision_agent_fireball(json_file):
    '''
    Takes in a json and outputs whether the agent
    and fireball collided.

    json_file: json file to be parsed
    '''
    with open(json_file) as f:
        j = json.load(f)
    return j["config"]['collision_agent_fireball']

def collision_agent_patient(json_file):
    '''
    Takes in a json and outputs whether the agent
    and patient collided.

    json_file: json file to be parsed
    '''
    with open(json_file) as f:
        j = json.load(f)
    return j["config"]['collision_agent_patient']
