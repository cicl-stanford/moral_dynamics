import moral_kinematics_scenarios as scenarios
import pymunk
from pymunk.vec2d import Vec2d
import pygame
import pymunk.pygame_util
from pygame.locals import *
import handlers
from agents import Agent
from math import sin, cos, radians
from video import vid_from_img, make_video
from random import choice

def counterfactual_simulation(environment,std_dev,num_times,view=False):
    '''
    Runs the counterfactual simulation and returns the causality judgment
    for the agent.

    environment::env -- simulation to be run
    std_dev::float   -- noise of counterfactual simulation
    num_times::int   -- number of samples to draw from noisy simulation
    view::bool       -- render simulation or not
    '''
    # Determine counterfactual probability
    #   collision
    counterfactual_prob = 0.0
    # Gather true/factual environment outcome
    true_env = environment(view)
    true_env.run()
    true_outcome = true_env.patient_fireball_collision
    # Sample noisy simulation
    for _ in range(num_times):
        env = environment(view)
        env.agent_patient_collision = true_env.agent_patient_collision
        env.agent_fireball_collision = true_env.agent_fireball_collision
        # Run the counterfactual simulation
        env.counterfactual_run(std_dev)
        # Determine outcome
        counterfactual_outcome = env.patient_fireball_collision
        counterfactual_prob += int(true_outcome == counterfactual_outcome)
    return 1- counterfactual_prob / num_times

def run_rotate():
    '''
    Runs the simulations and saves the JSON files with an arbitrary rotation
    about the center of the screen.
    '''
    def rotate(obj,theta=-20,origin=(500,300)):
        '''
        Rotates objects about a center
        '''
        # Translate w/r to visual origin (500,300)
        obj.body.position -= Vec2d(origin)
        # Radians to degrees
        theta = radians(theta)
        x, y = obj.body.position
        x_ = x*cos(theta) - y*sin(theta)
        y_ = y*cos(theta) + x*sin(theta)
        obj.body.position = [x_,y_]
        # Translate w/r to actual origin (0,0)
        obj.body.position += Vec2d(origin)

    video = False
    thetas = list(range(-19,-9))+list(range(10,19))
    for scene in scenarios.__experiment3__:
        theta = choice(thetas)
        sim = getattr(scenarios, scene)
        env = sim(True)
        env.run()
        # Gather position data
        pos = env.position_dict
        agent_positions = env.position_dict['agent']
        patient_positions = env.position_dict['patient']
        fireball_positions = env.position_dict['fireball']

        # Setup pygame and pymunk
        space = pymunk.Space()
        space.damping = 0.05
        screen = pygame.display.set_mode((1000,600))
        options = pymunk.pygame_util.DrawOptions(screen)
        clock = pygame.time.Clock()
        if video:
            save_screen = make_video(screen)
        # Setup empty agents
        agent = Agent(0,0,'blue',0,[])
        patient = Agent(0,0,'green',0,[])
        fireball = Agent(0,0,'red',0,[])
        # Add agent to space
        space.add(agent.body, agent.shape,
                  patient.body, patient.shape,
                  fireball.body, fireball.shape)
        pygame.init()
        running = True

        while running:
            # print(agent_positions[0])
            try:
                # Extract position data
                a_pos = agent_positions.pop(0)
                p_pos = patient_positions.pop(0)
                f_pos = fireball_positions.pop(0)
                # Set positions of objects
                agent.body.position = Vec2d(a_pos['x'],a_pos['y'])
                patient.body.position = Vec2d(p_pos['x'],p_pos['y'])
                fireball.body.position = Vec2d(f_pos['x'],f_pos['y'])
                # Rotate objects about the center
                rotate(agent,theta)
                rotate(patient,theta)
                rotate(fireball,theta)
                # Render space on screen (if requested)
                screen.fill((255,255,255))
                space.debug_draw(options)
                pygame.display.flip()
                clock.tick(60)
                space.step(1/60.0)
                if video:
                    next(save_screen)
            except Exception as e:
                running = False
        pygame.quit()
        pygame.display.quit()
        if video:
            vid_from_img("final_"+scene)

