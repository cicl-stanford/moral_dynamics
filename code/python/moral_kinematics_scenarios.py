'''
The set of scenarios from Moral Kinematics that were replicated for the Moral
Dynamics project.

Each function below defines a scenario. The block comments below the 
function declaration detail the scenario:

P = Patient
A = Agent
F = Fireball
> = Moving Right
< = Moving Left
^ = Moving Up
- = Empty Space

Felix Sosa
'''
from environment import Environment
from handlers import rem0, ap0, af0
# Scenarios used in experiment 1 (see paper)
__experiment1__ = ["long_distance","dodge","bystander","stays_put",
		   "short_distance","med_push","long_push","push_patient",
		   "double_push", "fast_push", "slow_push","med_push_latent_movement"]

# Scenarios used in experiment 2 (see paper)
__experiment2__ = ["long_distance","dodge","bystander","stays_put",
		   "short_distance","med_push","long_push","push_patient",
		   "double_push","harm_moving_moving","harm_moving_static",
		   "harm_static_moving","harm_static_static",
		   "victim_moving_moving","victim_moving_static",
		   "victim_static_moving","victim_static_static"]

# Scenarios used in experiment 3 (see paper)
__experiment3__ = ["dodge","bystander","stays_put","stays_put_red",
		   "short_distance","long_push",
		   "double_push","harm_moving_moving","harm_moving_static",
		   "harm_static_moving","victim_moving_moving",
		   "victim_moving_static","victim_static_moving","new","new2",
		   "exp6_video20","exp6_video19","exp6_video25","exp6_video26",
		   "med_distance"]

def slow_push(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# - A > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (209,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['N', 'R', 'PS', 'S', 'N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (300,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (800,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,ap0),(0,2,af0)]
	# Agent velocities
	vel = 360,150,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def fast_push(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# - A > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (200,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['N', 'R', 'P', 'S', 'N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (300,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (800,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,ap0),(0,2,af0)]
	# Agent velocities
	vel = 400,150,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def run_after_push(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# - A > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (300,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R', 'S', 'N', 'N', 'N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (500,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','R','R','R', 'R']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (800,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(1,2,rem0),(0,1,ap0),(0,2,af0)]
	# Agent velocities
	vel = 300,300,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def long_distance(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > > P - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R', 'R', 'R', 'R', 'R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (800,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,150,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def dodge(view=True,std_dev=0,frict=0.05):
	# - - - ^ - - -
	# P > > A - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['N', 'N', 'DS', 'S', 'S']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (100,300)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','R','R']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 400,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def bystander(view=True,std_dev=0,frict=0.05):
	# - - - A - - -
	# P > > > > > F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,500)
	a_params['color'] = "blue"
	a_params['moves'] = ['N', 'N', 'N', 'N', 'N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (100,300)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','R','R']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def stays_put_red(view=True,std_dev=0,frict=0.05):
	# - - - - P - -
	# F > > A - - -
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,265)
	a_params['color'] = "blue"
	a_params['moves'] = ['S', 'S', 'S', 'S', 'S']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (600,350)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (300,305)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','R','R','R']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def stays_put(view=True,std_dev=0,frict=0.05):
	# - - - - P - -
	# F > > A - - -
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,265)
	a_params['color'] = "blue"
	a_params['moves'] = ['S', 'S', 'S', 'S', 'S']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	f_params['loc'] = (600,350)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Fireball parameters
	p_params['loc'] = (300,305)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','R','R']
	p_params['coll'] = 1
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def short_distance(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# - - A > P - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (740,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R', 'R', 'R', 'R', 'R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (820,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env
def med_distance(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# - - A > P - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (550,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R', 'N', 'N', 'N', 'N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (820,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def med_push(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R', 'R', 'R', 'R', 'N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (500,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def med_push_latent_movement(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > P - - F
	# - - - - - - -
	# In this case, Patient moves after being touched
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R', 'R', 'N', 'N', 'N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (500,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','R','R', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 330,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def long_push(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A P > > > > F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R', 'R', 'R', 'R', 'R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (200,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def push_patient(view=True,std_dev=0,frict=0.05):
	# Test two types of agents, good and bad in the scenario
	# - F - - - - -
	# - - - ^ < < P
	# - - - A - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,400)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','NS','DS2','N','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (900,300)
	p_params['color'] = "green"
	p_params['moves'] = ['L','L','L','L','L','L']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (300,200)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def double_push(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A P > - > - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (200,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','S','N','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (300,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (800,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def harm_moving_moving(view=True,std_dev=0,frict=0.05):
	# Test two types of agents, good and bad in the scenario
	# > > P - - - -
	# - - - < < < F
	# - - - A - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	# a_params['loc'] = (550,100) # <- check this out
	a_params['loc'] = (550,450)
	a_params['color'] = "blue"
	a_params['moves'] = ['NS2','D','D','D','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	# p_params['loc'] = (900,300) # <- check this out
	p_params['loc'] = (50,210)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','R', 'R']
	p_params['coll'] = 1
	# Fireball parameters
	# f_params['loc'] = (450,500) # <- check this out
	f_params['loc'] = (850,330)
	f_params['color'] = "red"
	f_params['moves'] = ['L','L','L','L', 'L']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def victim_moving_moving(view=True,std_dev=0,frict=0.05):
	# Test two types of agents, good and bad in the scenario
	# > > F - - - -
	# - - - < < < P
	# - - - A - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	# a_params['loc'] = (550,100) # <- check this out
	a_params['loc'] = (550,450)
	a_params['color'] = "blue"
	a_params['moves'] = ['NS2','D','D','D','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	# p_params['loc'] = (900,300) # <- check this out
	p_params['loc'] = (850,330)
	p_params['color'] = "green"
	p_params['moves'] = ['L','L','L','L', 'L']
	p_params['coll'] = 1
	# Fireball parameters
	# f_params['loc'] = (450,500) # <- check this out
	f_params['loc'] = (50,210)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','R','R', 'R']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def harm_moving_static(view=True,std_dev=0,frict=0.05):
	# Test two types of agents, good and bad in the scenario
	# - P - - - - -
	# - - - < < < F
	# - - - A - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,380)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','NS','D','D','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	# p_params['loc'] = (900,300) # <- check this out
	p_params['loc'] = (340,230)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N', 'N']
	p_params['coll'] = 1
	# Fireball parameters
	# f_params['loc'] = (450,500) # <- check this out
	f_params['loc'] = (900,280)
	f_params['color'] = "red"
	f_params['moves'] = ['L','L','L','L','L']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def victim_moving_static(view=True,std_dev=0,frict=0.05):
	# Test two types of agents, good and bad in the scenario
	# - F - - - - -
	# - - - < < < P
	# - - - A - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	# a_params['loc'] = (550,100) # <- check this out
	a_params['loc'] = (500,380)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','NS','D','D','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	# p_params['loc'] = (900,300) # <- check this out
	p_params['loc'] = (900,280)
	p_params['color'] = "green"
	p_params['moves'] = ['L','L','L','L', 'L']
	p_params['coll'] = 1
	# Fireball parameters
	# f_params['loc'] = (450,500) # <- check this out
	f_params['loc'] = (340,230)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def harm_static_moving(view=True,std_dev=0,frict=0.05):
	# Test two types of agents, good and bad in the scenario
	# - - - < < < P
	# - - - F - - -
	# - - - A - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,330)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','DS2','S','S','S']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	f_params['loc'] = (500,230)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Fireball parameters
	p_params['loc'] = (900,130)
	p_params['color'] = "green"
	p_params['moves'] = ['L','L','L','L','L']
	p_params['coll'] = 1
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def victim_static_moving(view=True,std_dev=0,frict=0.05):
	# Test two types of agents, good and bad in the scenario
	# - - - < < < F
	# - - - P - - -
	# - - - A - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (500,330)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','DS2','S','S','S']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (500,230)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,130)
	f_params['color'] = "red"
	f_params['moves'] = ['L','L','L','L','L']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def harm_static_static(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > F - - P
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (200,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','RS','S','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (800,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (500,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def victim_static_static(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (200,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','RS','S','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (500,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (800,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def bot_check(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,100)
	a_params['color'] = "blue"
	a_params['moves'] = ['N','N','N','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (900,500)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (900,100)
	f_params['color'] = "red"
	f_params['moves'] = ['U','U','U','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,300,300
	env = Environment(a_params,p_params,f_params,vel,handlers,view)
	# env.run()
	return env

def exp6_video20(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','R','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (300,300)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','R','R','R','R']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (550,300)
	f_params['color'] = "red"
	f_params['moves'] = ['N','N','N','N','N','N','N']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,150,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def exp6_video19(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','R','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	f_params['loc'] = (300,300)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','R','R','R','R','R']
	f_params['coll'] = 2
	# Fireball parameters
	p_params['loc'] = (550,300)
	p_params['color'] = "green"
	p_params['moves'] = ['N','N','N','N','N','N','N']
	p_params['coll'] = 1
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,150,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def exp6_video26(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	f_params['loc'] = (300,300)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','R','R','R']
	f_params['coll'] = 2
	# Fireball parameters
	p_params['loc'] = (750,300)
	p_params['color'] = "green"
	p_params['moves'] = ['L','L','L','L','L']
	p_params['coll'] = 1
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,150,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def exp6_video25(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (100,300)
	a_params['color'] = "blue"
	a_params['moves'] = ['R','R','R','R','R']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (300,300)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','R','R']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (750,300)
	f_params['color'] = "red"
	f_params['moves'] = ['L','L','L','L','L']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 300,150,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def new(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (900,170)
	a_params['color'] = "blue"
	a_params['moves'] = ['L','LD','N','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	p_params['loc'] = (800,240)
	p_params['color'] = "green"
	p_params['moves'] = ['L','L','L','L','L']
	p_params['coll'] = 1
	# Fireball parameters
	f_params['loc'] = (250,300)
	f_params['color'] = "red"
	f_params['moves'] = ['R','R','R','R','R']
	f_params['coll'] = 2
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 250,150,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

def new2(view=True,std_dev=0,frict=0.05):
	# - - - - - - -
	# A > > P - - F
	# - - - - - - -
	a_params, p_params, f_params = {}, {}, {}
	# Agent parameters
	a_params['loc'] = (900,170)
	a_params['color'] = "blue"
	a_params['moves'] = ['L','LD','N','N','N']
	a_params['coll'] = 0
	a_params['type'] = 'B'
	# Patient parameters
	f_params['loc'] = (800,240)
	f_params['color'] = "red"
	f_params['moves'] = ['L','L','L','L','L']
	f_params['coll'] = 2
	# Fireball parameters
	p_params['loc'] = (100,300)
	p_params['color'] = "green"
	p_params['moves'] = ['R','R','R','R','R']
	p_params['coll'] = 1
	# Collision handlers
	handlers =[(0,1,ap0),(0,2,af0),(1,2,rem0)]
	# Agent velocities
	vel = 250,150,150
	env = Environment(a_params,p_params,f_params,vel,handlers,view,std_dev,frict)
	# env.run()
	return env

