'''
Collision handlers for the pymunk physics engine used for the 
Moral Dynamics project.

April 2, 2017
Felix Sosa
'''
import pygame
import pymunk
from pygame.locals import *

PF_COLLISION = []
AF_COLLISION = []
AP_COLLISION = []

def rem0(arbiter, space, data):
	'''
	Used with post_solve. Removes the Green Agent after colliding with 
	the Fireball. Expected that Green Agent is in space.shapes[1].

	arbiter -- Pymunk collision arbiter
	space   -- Pymunk space in which simulations are run
	data    -- Pymunk collision data
	'''
	if PF_COLLISION:
		return True
	space.remove(space.shapes[1])
	space.remove(space.bodies[1])
	running = False
	PF_COLLISION.append(1)
	pygame.time.set_timer(QUIT, 1000)
	return True

def ap0(arbiter, space, data):
	'''
	Used with post_solve. Determines if Agent
	and Patient have collided.

	arbiter -- Pymunk collision arbiter
	space   -- Pymunk space in which simulations are run
	data    -- Pymunk collision data
	'''
	if AP_COLLISION:
		return True
	AP_COLLISION.append(1)
	return True

def af0(arbiter, space, data):
	'''
	Used with post_solve. Determines if Agent
	and Fireball have collided.

	arbiter -- Pymunk collision arbiter
	space   -- Pymunk space in which simulations are run
	data    -- Pymunk collision data
	'''
	if AF_COLLISION:
		return True
	AF_COLLISION.append(1)
	return True
