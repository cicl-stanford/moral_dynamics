import json
import sys
import pygame
import moral_kinematics_scenarios as scenarios
from random import choice
from math import sin, cos, radians
from pymunk.vec2d import Vec2d
from importlib import import_module
# Path to save JSON data to
paths = ['../../data/json/experiment1/',
	 '../../data/json/experiment2/',
	 '../../data/json/experiment3/']
scenarios = import_module('moral_kinematics_scenarios')
experiment_clips = [scenarios.__experiment1__,
		    scenarios.__experiment2__,
                    scenarios.__experiment3__]
def rotate_positions(d,theta):
	'''
	Rotates the position of the objecs about the center of the
	environment

	d::dict -- dictionary of all object positions
	theta::int -- degress of rotation
	'''
	def rotate(x,y,theta,origin=[500,300]):
		'''
		Rotates objects about a center
		'''
		# Translate w/r to visual origin (500,300)
		pos = Vec2d(x,y)
		pos -= Vec2d(origin)
		# Radians to degrees
		theta = radians(theta)
		x, y = pos
		x_ = x*cos(theta) - y*sin(theta)
		y_ = y*cos(theta) + x*sin(theta)
		pos = Vec2d(x_,y_)
		# Translate w/r to actual origin (0,0)
		pos += Vec2d(origin)
		return pos

	for obj in d.keys():
		for pos in d[obj]:
			pos['x'], pos['y'] = rotate(pos['x'], pos['y'],theta)

def convert(rotate=False, path=""):
	'''
	Takes in a list of simulations, runs the simulations, and outputs
	the positional information of all agents within the simulations
	in a JSON format stored in /data/json/.
	'''
	def count_nothing(moves):
		'''
		Counts number of moves in which object does not move

		moves::list -- the moves the object has been assigned
		'''
		return moves.count('N')+moves.count('NS')+moves.count('NS2')+moves.count('S')
	latent_movement_clips = ['med_push_latent_movement']
	thetas = list(range(-19,-9))+list(range(10,19))
	for idx in range(len(paths)):
		for scene in experiment_clips[idx]:
			theta = choice(thetas)
			sim = getattr(scenarios,scene)
			env = sim(False)
			env.run()

			# Set up config for json file
			sim_dict = {} # Dict to be converted to json
			config = {'scene' : env.screen_size[0]} # Screen size (y-axis)
			config['name'] = scene # Name of scenario
			config['collision_agent_patient'] = bool(env.agent_patient_collision)
			config['collision_agent_fireball'] = bool(env.agent_fireball_collision)
			config['agent_init_moving'] = (count_nothing(env.agent.moves) != len(env.agent.moves))
			if scene in latent_movement_clips:
				config['patient_init_moving'] = False
			else:
				config['patient_init_moving'] = (count_nothing(env.patient.moves) != len(env.patient.moves))
			config['fireball_init_moving'] = (count_nothing(env.fireball.moves) != len(env.fireball.moves))
			# Init dictionaries for body positions
			bodies_dict = {}

			# Gather positional data on objects and add to dict
			if rotate:
				rotate_positions(env.position_dict,theta)
				bodies_dict["agent"] = env.position_dict['agent']
				bodies_dict["patient"] = env.position_dict['patient']
				bodies_dict["fireball"] = env.position_dict['fireball']
			else:
				bodies_dict["agent"] = env.position_dict['agent']
				bodies_dict["patient"] = env.position_dict['patient']
				bodies_dict["fireball"] = env.position_dict['fireball']

			# Convert dict to json
			config['ticks'] = env.tick
			sim_dict['config'] = config
			sim_dict["objects"] = bodies_dict

			# Save json
			with open(paths[idx]+config['name']+".json", "w") as j:
				json.dump(sim_dict, j, indent=2)
convert()
