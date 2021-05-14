'''


Felix Sosa
'''
import pymunk
import pygame
import pymunk.pygame_util
from pygame.locals import *
import handlers
from agents import Agent
from video import make_video, vid_from_img

class Environment:
	def __init__(self, a_params, p_params, f_params, vel, handlers=None, 
				 view=True, std_dev=0, frict=0.05):
		'''
		Environment class that contains all necessary components to configure
		and run scenarios.

		a_params::dict -- parameters for the Blue Agent
		p_params::dict -- parameters for the Green Agent
		f_params::dict -- parameters for the Fireball
		vel::tuple     -- velcoties associated with each agent in the scenario
		handlers::tuple -- optional collision handlers
		view::bool     -- flag for whether you want to view the scenario or not
		frict::float   -- friction value for pymunk physics
		std_dev::float -- standard deviation value for noisy counterfactual simulation
		'''
		self.view = view
		self.std_dev = std_dev
		# Objects in environent
		self.agent = Agent(a_params['loc'][0], a_params['loc'][1], 
				   a_params['color'], a_params['coll'],
				   a_params['moves'])
		self.patient = Agent(p_params['loc'][0], p_params['loc'][1], 
				     p_params['color'], p_params['coll'],
				     p_params['moves'])
		self.fireball = Agent(f_params['loc'][0], f_params['loc'][1], 
				      f_params['color'], f_params['coll'],
				      f_params['moves'])
		# Initial location of objects in environment
		self.p_loc = p_params['loc']
		self.a_loc = a_params['loc']
		self.f_loc = f_params['loc']
		# Pymunk space friction
		self.friction = frict
		# Agent velocities
		self.vel = vel
		self.pf_lock = False
		self.af_lock = False
		self.ap_lock = False
		# Engine parameters
		self.space = None
		self.screen = None
		self.options = None
		self.clock = None
		# Collision handlers
		self.coll_handlers = [x for x in handlers] if handlers else handlers
		# Values needed for rendering the scenario in Blender
		self.tick = 0
		self.agent_collision = None
		self.agent_patient_collision = None
		self.agent_fireball_collision = None
		self.patient_fireball_collision = 0
		self.position_dict = {
			'agent':[],
			'patient':[],
			'fireball':[]
		}
		self.screen_size = (1000,600)
		# Configure and run environment
		self.configure()

	def configure(self):
		'''
		Configuration method for Environments. Sets up the pymunk space
		for scenarios.
		'''
		# Configure pymunk space and pygame engine parameters (if any)
		if self.view:
			pygame.init()
			self.screen = pygame.display.set_mode((1000,600))
			self.options = pymunk.pygame_util.DrawOptions(self.screen)
			self.clock = pygame.time.Clock()
		self.space = pymunk.Space()
		self.space.damping = self.friction
		# Configure collision handlers (if any)
		if self.coll_handlers:
			for ob1, ob2, rem in self.coll_handlers:
				ch = self.space.add_collision_handler(ob1, ob2)
				ch.data["surface"] = self.screen
				ch.post_solve = rem
		# Add agents to the pymunk space
		self.space.add(self.agent.body, self.agent.shape,
					   self.patient.body, self.patient.shape,
					   self.fireball.body, self.fireball.shape)
		
	def update_blender_values(self):
		'''
		All scenarios are rendered in the physics engine Blender. In order to do this,
		we store relevant values such as object position, simulation tick count, and
		collision in a JSON file. This file is passed into a bash script that uses it
		to render the relevant scenario in Blender. 

		This method is used to update the JSON files for each scenario.
		'''
		# Append positional information to the dict
		self.position_dict['agent'].append({'x':self.agent.body.position[0], 
							'y':self.agent.body.position[1]})
		self.position_dict['patient'].append({'x':self.patient.body.position[0], 
							'y':self.patient.body.position[1]})
		self.position_dict['fireball'].append({'x':self.fireball.body.position[0], 
							'y':self.fireball.body.position[1]})
		# Record when the Agent collides with someone else
		if handlers.PF_COLLISION and not self.pf_lock:
			self.agent_collision = self.tick
			self.pf_lock = True
		if handlers.AP_COLLISION and not self.ap_lock:
			self.agent_patient_collision = self.tick
			self.ap_lock = True
		if handlers.AF_COLLISION and not self.af_lock:
			self.agent_fireball_collision = self.tick
			self.af_lock = True

	def run(self,video=False,filename=""):
		'''
		Forward method for Environments. Actually runs the scenarios you
		view on (or off) screen.

		video::bool   -- whether you want to record the simulation
		filename::str -- the name of the video file
		'''
		# Agent velocities
		a_vel, p_vel, f_vel = self.vel
		# Agent action generators (yield actions of agents)
		a_generator = self.agent.act(a_vel,self.clock,self.screen,
					     self.space,self.options, self.view,
					     self.std_dev)
		p_generator = self.patient.act(p_vel,self.clock,self.screen,
					       self.space,self.options,self.view,
					       self.std_dev)
		f_generator = self.fireball.act(f_vel,self.clock,self.screen,
						self.space,self.options,self.view,
						self.std_dev)
		# Running flag
		running = True
		# Video creation
		save_screen = make_video(self.screen)
		# Main loop. Run simulation until collision between Green Agent 
		# 	and Fireball
		while running and not handlers.PF_COLLISION:
			try:
				# Generate the next tick in the simulation for each object
				next(a_generator)
				next(p_generator)
				next(f_generator)
				# Render space on screen (if requested)
				if self.view:
					self.screen.fill((255,255,255))
					self.space.debug_draw(self.options)
					pygame.display.flip()
					self.clock.tick(50)
				self.space.step(1/50.0)
				# Update the values for the Blender JSON file
				self.update_blender_values()
				# Increment the simulation tick
				self.tick += 1
				if video:
					next(save_screen)
			except Exception as e:
				running = False
		if self.view:
			pygame.quit()
			pygame.display.quit()
		# Record whether Green Agent and Fireball collision occurred
		self.patient_fireball_collision = 1 if handlers.PF_COLLISION else 0
		# Reset collision handler
		handlers.PF_COLLISION = []
		handlers.AP_COLLISION = []
		handlers.AF_COLLISION = []
		if video:
			vid_from_img(filename)

	def counterfactual_run(self,std_dev,video=False,filename=''):
		'''
		Forward method for Environments. Actually runs the scenarios you
		view on (or off) screen.

		std_dev::float -- noise parameter for simulation
		video::bool    -- whether you want to record the simulation
		filename::str  -- file name for video
		'''
		# We remove the agent from the environment
		self.space.remove(self.space.shapes[0])
		self.space.remove(self.space.bodies[0])
		# Reinitialize pygame
		pygame.init()
		# If viewing, draw simulaiton to screen
		if self.view:
			pygame.init()
			self.screen = pygame.display.set_mode((1000,600))
			self.options = pymunk.pygame_util.DrawOptions(self.screen)
			self.clock = pygame.time.Clock()
		# Set noise parameter
		self.std_dev = std_dev
		save_screen = make_video(self.screen)
		# Agent velocities
		_, p_vel, f_vel = self.vel
		# Counterfactual ticks for agents
		self.patient.counterfactual_tick = self.agent_patient_collision
		self.fireball.counterfactual_tick = self.agent_fireball_collision
		# Agent action generators (yield actions of agents)
		p_generator = self.patient.act(p_vel, self.clock, self.screen,
					       self.space, self.options, self.view,
					       self.std_dev)
		f_generator = self.fireball.act(f_vel, self.clock, self.screen,
						self.space, self.options, self.view,
						self.std_dev)
		# Running flag
		running = True
		# Main loop. Run simulation until collision between Green Agent
		# 	and Fireball
		while running and not handlers.PF_COLLISION:
			try:
				# Generate the next tick in the simulation for each object
				next(p_generator)
				next(f_generator)
				# Render space on screen (if requested)
				if self.view:
					self.screen.fill((255,255,255))
					self.space.debug_draw(self.options)
					pygame.display.flip()
					self.clock.tick(50)
				self.space.step(1/50.0)
				# Update the values for the Blender JSON file
				self.update_blender_values()
				# Increment the simulation tick
				self.tick += 1
				# Increment ticks in agents
				self.patient.tick = self.tick
				self.fireball.tick = self.tick
				if video:
					next(save_screen)
			except:
				running = False
		if self.view:
			pygame.quit()
			pygame.display.quit()
		# Record whether Green Agent and Fireball collision occurred
		self.patient_fireball_collision = 1 if handlers.PF_COLLISION else 0
		# Reset collision handler
		handlers.PF_COLLISION = []
		handlers.AP_COLLISION = []
		handlers.AF_COLLISION = []
		if video:
			vid_from_img(filename)
