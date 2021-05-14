'''
Agent Classes for Moral Dynamics.

March 14, 2017
Felix Sosa
'''
import pymunk
import pygame
import glob
from random import gauss
# Distance agents move per action
move_lat_distance = 160
move_long_distance = 160
wait_period = 27

def is_inside(body_pos, tgt_pos):
	'''
	Helper function that determines whether an object is within the
	bounds of some position, to some degree eps

	body_pos::Vec2d -- position of object
	tgt_pos::Vec2s  -- target position
	'''
	eps = 2
	return (body_pos[0] < (tgt_pos[0] + eps) and
		body_pos[0] > (tgt_pos[0] - eps) and
		body_pos[1] < (tgt_pos[1] + eps) and
		body_pos[1] > (tgt_pos[1] - eps))

class Agent:
	def __init__(self, x, y, color, collision, moves, mass=1, rad=25):
		'''
		Class for agents in scenarios. Used to instantiate the Blue Agent,
		Green Agent, and Fireball in the Moral Dynamics project.

		x::float -- x dimension of initial location in a scenario
		y::float -- y dimension of initial location in a scenario
		color::str -- agent's color
		collision::int -- collision type for agent body (used in pymunk)
		moves::list -- actions the agent will take for a given scenario
		mass::float  -- optional mass parameter for agent's body
		rad::float   -- optional radius for agent's body
		'''
		# Actions available to agents
		self.action_dict = {
			'U':self.move_up,
			'D':self.move_down,
			'R':self.move_right,
			'L':self.move_left,
			'N':self.do_nothing,
			'S':self.stay_put,
			'DS':self.move_down_special,
			'DS2':self.move_down_special_2,
			'RS':self.move_right_special,
			'NS':self.do_nothing_special,
			'NS2':self.do_nothing_special_2,
			'LD' :self.move_left_diag,
			'P' :self.push_right,
			'PS' :self.push_right_slow
		}
		# Agent attributes
		self.body = pymunk.Body(mass,1)
		self.body.position = (x,y)
		self.shape = pymunk.Circle(self.body, rad)
		self.shape.color = pygame.color.THECOLORS[color]
		self.shape.collision_type = collision
		self.shape.elasticity = 1
		self.effort_expended = 0
		self.actions = [self.action_dict[x] for x in moves]
		self.moves = moves
		self.tick = 0
		self.counterfactual_tick = None

	# Action definitions
	def move_right(self, velocity, clock, screen, space, options, view, std_dev=0):
		# Move agent right
		intended_x_pos = self.body.position[0]+move_lat_distance
		tgt_pos = [intended_x_pos,self.body.position[1]]
		tmp_std = std_dev
		std_dev = 0
		while self.body.position[0] < intended_x_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity.length < velocity:
				if self.counterfactual_tick and self.tick < self.counterfactual_tick:
					std_dev = 0
				elif self.counterfactual_tick and self.tick >= self.counterfactual_tick:
					std_dev = tmp_std
				direction = [intended_x_pos,self.body.position[1]] - self.body.position
				direction = direction.normalized()
				noise = [gauss(0,std_dev), gauss(0,std_dev)]
				direction += noise
				direction = direction.normalized()
				impulse = (velocity - self.body.velocity.length)*direction
				self.body.apply_impulse_at_local_point(impulse)
				self.effort_expended += impulse.length
			yield

	def move_left(self,velocity,clock,screen,space,options,view,std_dev=0):
		# Move agent left
		intended_x_pos = self.body.position[0]-move_lat_distance
		tmp_std = std_dev
		std_dev = 0
		while self.body.position[0] > intended_x_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity.length < velocity:
				if self.counterfactual_tick and self.tick < self.counterfactual_tick:
					std_dev = 0
				elif self.counterfactual_tick and self.tick >= self.counterfactual_tick:
					std_dev = tmp_std
				direction = [intended_x_pos,self.body.position[1]] - self.body.position
				direction = direction.normalized()
				noise = [gauss(0,std_dev), gauss(0,std_dev)]
				direction += noise
				direction = direction.normalized()
				impulse = (velocity - self.body.velocity.length)*direction
				self.body.apply_impulse_at_local_point(impulse)
				self.effort_expended += impulse.length
			yield

	def move_up(self,velocity,clock,screen,space,options,view,std_dev=0):
		# Move agent up
		intended_y_pos = self.body.position[1]+move_long_distance
		tgt_pos = [self.body.position[0], intended_y_pos]
		tmp_std = std_dev
		std_dev = 0
		while self.body.position[1] < intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity.length < velocity:
				if self.counterfactual_tick and self.tick < self.counterfactual_tick:
					std_dev = 0
				elif self.counterfactual_tick and self.tick >= self.counterfactual_tick:
					std_dev = tmp_std
				direction = [self.body.position[0], intended_y_pos] - self.body.position
				direction = direction.normalized()
				noise = [gauss(0,std_dev), gauss(0,std_dev)]
				direction += noise
				direction = direction.normalized()
				impulse = (velocity - self.body.velocity.length)*direction
				self.body.apply_impulse_at_local_point(impulse)
				self.effort_expended += impulse.length
			yield

	def move_down(self,velocity,clock,screen,space,options,view,std_dev=0):
		# Move agent up
		intended_y_pos = self.body.position[1]-move_long_distance
		tgt_pos = [self.body.position[0], intended_y_pos]
		tmp_std = std_dev
		std_dev = 0
		while self.body.position[1] > intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity.length < velocity:
				if self.counterfactual_tick and self.tick < self.counterfactual_tick:
					std_dev = 0
				elif self.counterfactual_tick and self.tick >= self.counterfactual_tick:
					std_dev = tmp_std
				direction = [self.body.position[0], intended_y_pos] - self.body.position
				direction = direction.normalized()
				noise = [gauss(0,std_dev), gauss(0,std_dev)]
				direction += noise
				direction = direction.normalized()
				impulse = (velocity - self.body.velocity.length)*direction
				self.body.apply_impulse_at_local_point(impulse)
				self.effort_expended += impulse.length
			yield

	def stay_put(self,velocity,clock,screen,space,options,view,std_dev=0):
		# Agent stays put. This is different from do_nothing in that the 
		# 	agent will apply a force to maintain its current location if 
		# 	pushed or pulled in some direction.
		for _ in range(wait_period):
			if view:
				for event in pygame.event.get():
					pass
			if abs(self.body.velocity[1]) > 0:
				imp = -1*self.body.velocity[1]
				self.body.apply_impulse_at_local_point((0,imp))
				self.effort_expended += abs(imp)
			if abs(self.body.velocity[0]) > 0:
				imp = -1*self.body.velocity[0]
				self.body.apply_impulse_at_local_point((imp,0))
				self.effort_expended += abs(imp)
			yield

	def move_right_special(self,velocity,clock,screen,space,options,view,std_dev=0):
		# Move agent right (special case for replicating scenarios in 
		# 	Moral Kinematics)
		tick = 0
		intended_x_pos = self.body.position[0]+move_lat_distance+move_lat_distance*0.6
		tgt_pos = [intended_x_pos,self.body.position[1]]
		tmp_std = std_dev
		std_dev = 0
		while self.body.position[0] < intended_x_pos:
			if view:
				for event in pygame.event.get():
					pass
			tick += 1
			if self.body.velocity.length < velocity:
				if self.counterfactual_tick and self.tick < self.counterfactual_tick:
					std_dev = 0
				elif self.counterfactual_tick and self.tick >= self.counterfactual_tick:
					std_dev = tmp_std
				direction = [intended_x_pos,self.body.position[1]] - self.body.position
				direction = direction.normalized()
				noise = [gauss(0,std_dev), gauss(0,std_dev)]
				direction += noise
				direction = direction.normalized()
				impulse = (velocity - self.body.velocity.length)*direction
				self.body.apply_impulse_at_local_point(impulse)
				self.effort_expended += impulse.length
			yield

	def move_down_special(self,velocity,clock,screen,space,options,view,std_dev=0):
		# Move agent down (special case for replicating scenarios in 
		# 	Moral Kinematics)
		intended_y_pos = self.body.position[1]-move_long_distance/3.0
		tgt_pos = [self.body.position[0], intended_y_pos]
		tmp_std = std_dev
		std_dev = 0
		while self.body.position[1] > intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity.length < velocity:
				if self.counterfactual_tick and self.tick < self.counterfactual_tick:
					std_dev = 0
				elif self.counterfactual_tick and self.tick >= self.counterfactual_tick:
					std_dev = tmp_std
				direction = [self.body.position[0], intended_y_pos] - self.body.position
				direction = direction.normalized()
				noise = [gauss(0,std_dev), gauss(0,std_dev)]
				direction += noise
				direction = direction.normalized()
				impulse = (velocity - self.body.velocity.length)*direction
				self.body.apply_impulse_at_local_point(impulse)
				self.effort_expended += impulse.length
			yield
		for _ in range(wait_period):
			if view:
				for event in pygame.event.get():
					pass
			yield

	def move_down_special_2(self,velocity,clock,screen,space,options,view,std_dev=0):
		# Move agent down (special case for replicating scenarios in 
		# 	Moral Kinematics)
		intended_y_pos = self.body.position[1]-move_long_distance/2.5
		tgt_pos = [self.body.position[0], intended_y_pos]
		tmp_std = std_dev
		std_dev = 0
		while self.body.position[1] > intended_y_pos:
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity.length < velocity:
				if self.counterfactual_tick and self.tick < self.counterfactual_tick:
					std_dev = 0
				elif self.counterfactual_tick and self.tick >= self.counterfactual_tick:
					std_dev = tmp_std
				direction = [self.body.position[0], intended_y_pos] - self.body.position
				direction = direction.normalized()
				noise = [gauss(0,std_dev), gauss(0,std_dev)]
				direction += noise
				direction = direction.normalized()
				impulse = (velocity - self.body.velocity.length)*direction
				self.body.apply_impulse_at_local_point(impulse)
				self.effort_expended += impulse.length
			yield
		for _ in range(wait_period):
			if view:
				for event in pygame.event.get():
					pass
			yield
	
	def do_nothing(self,velocity,clock,screen,space,options,view,std_dev=0):
		# Agent does nothing
		for _ in range(wait_period):
			if view:
				for event in pygame.event.get():
					pass
			yield

	def do_nothing_special(self,velocity,clock,screen,space,options,view,std_dev=0):
		# Do nothing (special case for replicating scenarios in 
		# Moral Kinematics)
		for _ in range(wait_period+5):
			if view:
				for event in pygame.event.get():
					pass
			yield

	def do_nothing_special_2(self,velocity,clock,screen,space,options,view,std_dev=0):
		# Do nothing (special case for replicating scenarios in 
		# 	Moral Kinematics)
		for _ in range(wait_period+10):
			if view:
				for event in pygame.event.get():
					pass
			yield
	def move_left_diag(self, velocity, clock, screen, space, options, view, std_dev=0):
		tgt_pos = self.body.position + (-100,50)
		# Move agent right
		while not is_inside(self.body.position, tgt_pos):
				if view:
					for event in pygame.event.get():
						pass
				# Update velocity and record effort
				if self.body.velocity.length < velocity:
					# Compute vector direction
					direction = tgt_pos - self.body.position
					direction = direction.normalized()
					impulse = velocity*direction - self.body.velocity
					self.body.apply_impulse_at_local_point(impulse)
					self.effort_expended += impulse.length
				yield

	def push_right(self, velocity, clock, screen, space, options, view, std_dev=0):
		# Move agent right
		intended_x_pos = self.body.position[0]+move_lat_distance
		tgt_pos = [intended_x_pos,self.body.position[1]]
		tmp_std = std_dev
		std_dev = 0
		while self.body.position[0] < intended_x_pos:
			multiplier = self.body.position[0]/intended_x_pos*0.8
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity.length < velocity+velocity*multiplier:
				if self.counterfactual_tick and self.tick < self.counterfactual_tick:
					std_dev = 0
				elif self.counterfactual_tick and self.tick >= self.counterfactual_tick:
					std_dev = tmp_std
				direction = [intended_x_pos,self.body.position[1]] - self.body.position
				direction = direction.normalized()
				noise = [gauss(0,std_dev), gauss(0,std_dev)]
				direction += noise
				direction = direction.normalized()
				impulse = (velocity+velocity*multiplier - self.body.velocity.length)*direction
				self.body.apply_impulse_at_local_point(impulse)
				self.effort_expended += impulse.length
			yield

	def push_right_slow(self, velocity, clock, screen, space, options, view, std_dev=0):
		# Move agent right
		intended_x_pos = self.body.position[0]+move_lat_distance
		tgt_pos = [intended_x_pos,self.body.position[1]]
		tmp_std = std_dev
		std_dev = 0
		while self.body.position[0] < intended_x_pos:
			multiplier = self.body.position[0]/intended_x_pos*0.5
			if view:
				for event in pygame.event.get():
					pass
			if self.body.velocity.length < velocity+velocity*multiplier:
				if self.counterfactual_tick and self.tick < self.counterfactual_tick:
					std_dev = 0
				elif self.counterfactual_tick and self.tick >= self.counterfactual_tick:
					std_dev = tmp_std
				direction = [intended_x_pos,self.body.position[1]] - self.body.position
				direction = direction.normalized()
				noise = [gauss(0,std_dev), gauss(0,std_dev)]
				direction += noise
				direction = direction.normalized()
				impulse = (velocity+velocity*multiplier - self.body.velocity.length)*direction
				self.body.apply_impulse_at_local_point(impulse)
				self.effort_expended += impulse.length
			yield

	def act(self,velocity,clock,screen,space,options,view,std_dev=0):
		# Execute policy
		actions = iter(self.actions)
		actions_left = True
		action = next(actions)
		while actions_left:
			try:
				for _ in action(velocity,clock,screen,space,options,view,std_dev):
					yield
				action = next(actions)
			except:
				return

	def vec_move(self,trajectory,velocity,clock,screen,space,options,view,std_dev=0):
		for tgt_pos in trajectory:
			while not is_inside(self.body.position, tgt_pos):
				print(self.body.position)
				if view:
					for event in pygame.event.get():
						pass
				# Update velocity and record effort
				if self.body.velocity.length < velocity:
					# Compute vector direction
					direction = tgt_pos - self.body.position
					direction = direction.normalized()
					impulse = velocity*direction - self.body.velocity
					self.body.apply_impulse_at_local_point(impulse)
					self.effort_expended += impulse.length
				yield
