'''
Execute and record values from scenarios.

Felix Sosa
March 8, 2018
'''
import matplotlib.pyplot as plt
import csv
from importlib import import_module
from counterfactual import counterfactual_simulation
import pandas as pd
from features import *
# Import the scenario file and store them in a variable
scenarios = import_module('moral_kinematics_scenarios')

# Scenarios used in experiment 1
clip_names_exp1 = {
    "long_distance":"video3",
    "dodge":"video7",
    "bystander":"video12",
    "stays_put":"video4",
    "short_distance":"video1",
    "med_push":"video9",
    "long_push":"video10",
    "push_patient":"video11",
    "double_push":"video8",
    "fast_push":"video6",
    "slow_push":"video5",
    "med_push_latent_movement":"video2"
}

# Scenarios used in experiment 2 (see paper)
clip_names_exp2 = {
    "long_distance":"video3",
    "dodge":"video7",
    "bystander":"video12",
    "stays_put":"video4",
    "short_distance":"video1",
    "med_push":"video9",
    "long_push":"video10",
    "push_patient":"video11",
    "double_push":"video8",
    "hmm":"harm_moving_moving",
    "hms":"harm_moving_static",
    "hsm":"harm_static_moving",
    "vmm":"victim_moving_moving",
    "vms":"victim_moving_static",
    "vsm":"victim_static_moving",
    "hss":"harm_static_static",
    "vss":"victim_static_static"
}

# Scenarios used in experiment 3 (see paper)
clip_names_exp3 = {
    "stays_put":"video1",
    "stays_put_red":"video2",
    "short_distance":"video3",
    "new2":"video4",
    "new":"video5",
    "med_distance":"video6",
    "long_push":"video7",
    "exp6_video26":"video8",
    "exp6_video25":"video9",
    "exp6_video20":"video10",
    "exp6_video19":"video11",
    "double_push":"video12",
    "dodge":"video13",
    "bystander":"video14",
    "harm_moving_moving":"video15",
    "harm_moving_static":"video16",
    "harm_static_moving":"video17",
    "victim_moving_moving":"video18",
    "victim_moving_static":"video19",
    "victim_static_moving":"video20",
}
# Dictionary for clip names, ensuring everything is named the same way
#  as it was collected in the experiments
exp_map = [clip_names_exp1,clip_names_exp2,clip_names_exp3]

def unique(x):
    '''
    Return unique elements in a list
    '''
    z = []
    for y in x:
        if y not in z:
            z.append(y)
    return z

def record_effort():
    '''
    Records the effort values for all simulations across the three
    experiments and saves them to a csv file for analysis
    '''
    # Friction values for the simulations. Values are 0.01-1.00
    damping_vals = list(map(lambda x: x/100, range(1,101)))
    # Function for changing column names in dataframe
    chg_name = lambda x: map(lambda y: "effort_"+str(y), x)
    # Dataframe for results
    results = pd.DataFrame()
    results['experiment'] = ""
    results['clip'] = ""
    results[damping_vals] = ""
    # The sets of clips for each experiment
    experiment_clips = [scenarios.__experiment1__,
                        scenarios.__experiment2__,
                        scenarios.__experiment3__]
    # Iterate through clip sets
    for exp_idx in range(len(experiment_clips)):
        # Iterate clips, record effort vals
        for clip in experiment_clips[exp_idx]:
            scene = getattr(scenarios,clip)
            row = [exp_idx+1, clip]
            for d_val in damping_vals:
                env = scene(False,std_dev=0,frict=d_val)
                env.run()
                # Build dataframe row
                row.append(env.agent.effort_expended)
            results.loc[len(results.index)] = row
    # Rename columns to indicate effort values
    results.columns = ['experiment','clip'] + list(chg_name(damping_vals))
    results.to_csv('model_effort.csv')
    return results

def record_causality():
    '''
    Records the causality values for all simulations across the three
    experiments and saves them to a csv file for analysis
    '''
    # The standard deviations used in the counterfactual simulations
    std_devs = list(map(lambda x: x/10, range(0,21)))
    # Simulations in which the patient would not have moved if agent
    #  was removed
    latent_movement_clips = ['med_push_latent_movement']
    # Simple function for changing column names in dataframe
    chg_name = lambda x: map(lambda y: "causality_"+str(y), x)
    # Dataframe for collecting results
    results = pd.DataFrame()
    results['experiment'] = ""
    results['clip'] = ""
    results[std_devs] = ""
    # Dataframe for collecting results
    r = pd.DataFrame()
    r['experiment'] = ""
    r['clip'] = ""
    r[std_devs] = ""
    # The sets of clips for each experiment
    exp_clips = [scenarios.__experiment1__,
                 scenarios.__experiment2__,
                 scenarios.__experiment3__]
    # To save compute, don't run duplicate simulations
    unique_clips = unique(exp_clips[0]+exp_clips[1]+exp_clips[2])
    # Gather causality values
    for clip in unique_clips:
        # Row entry
        row = [0, clip]
        scene = getattr(scenarios,clip)
        # Gather graound-truth scenario
        t_scene = scene(False)
        t_scene.run()
        # If clip involves latent movement, assign 0.0
        if clip in latent_movement_clips:
            for s_d in std_devs:
                row.append(0.0)
        else:
            for s_d in std_devs:
                causality = counterfactual_simulation(scene,std_dev=s_d,
                                                      num_times=1000)
                row.append(causality)
        # Determine Agent causality
        results.loc[len(results.index)] = row
    # Distribute results across experiments
    idx = 0
    for exp_idx in range(len(exp_clips)):
        for clip in exp_clips[exp_idx]:
            r = r.append(results.loc[results['clip'] == clip],
                         ignore_index=True)
            r.at[idx,'experiment'] = exp_idx+1
            idx+=1
    # Rename columns to indicate effort values
    r.columns = ['experiment','clip'] + list(chg_name(std_devs))
    r.to_csv('model_causality.csv')
    return results

def record_features():
    '''
    Records the feature values for all simulations, using json files,
    across the three experiments and saves them to a csv file for analysis
    '''
    # The list of features to be recorded
    features = ['distance','duration','contact','frequency',
                'agent_moving', 'patient_moving',
                'fireball_moving', 'collision_agent_patient',
                'collision_agent_fireball']
    # Dataframe for results
    results = pd.DataFrame()
    results['experiment'] = ""
    results['clip'] = ""
    results[features] = ""
    exp_clips = [scenarios.__experiment1__,
                 scenarios.__experiment2__,
                 scenarios.__experiment3__]
    # The sets of clips for each experiment
    json_files = ["../../data/json/experiment1/",
                  "../../data/json/experiment2/",
                  "../../data/json/experiment3/"]
    for exp_idx in range(len(exp_clips)):
        for clip in exp_clips[exp_idx]:
            row = [exp_idx+1]
            row.append(clip)
            row.append(distance(json_files[exp_idx]+clip+".json"))
            row.append(duration(json_files[exp_idx]+clip+".json"))
            row.append(contact(json_files[exp_idx]+clip+".json"))
            row.append(frequency(json_files[exp_idx]+clip+".json"))
            row.append(agent_moving(json_files[exp_idx]+clip+".json"))
            row.append(patient_moving(json_files[exp_idx]+clip+".json"))
            row.append(fireball_moving(json_files[exp_idx]+clip+".json"))
            row.append(collision_agent_patient(json_files[exp_idx]+
                                               clip+".json"))
            row.append(collision_agent_fireball(json_files[exp_idx]+
                                                clip+".json"))
            results.loc[len(results.index)] = row
    # Rename columns to indicate effort values
    results.to_csv('../../data/model/model_features.csv')
    return results

def rename(csv):
    results = pd.read_csv(csv)
    exp1 = results[results['experiment'] == 1]
    exp2 = results[results['experiment'] == 2]
    exp3 = results[results['experiment'] == 3]
    exps = [exp1,exp2,exp3]
    for idx in range(len(exps)):
        exps[idx] = exps[idx].replace({"clip":exp_map[idx]})
    results = pd.concat(exps)
    del results["Unnamed: 0"] # Not sure, but this shows up from read_csv
    results.to_csv(csv)

record_features()
rename('../../data/model/model_features.csv')
rename('../../data/model/model_effort.csv')
rename('../../data/model/model_causality.csv')
