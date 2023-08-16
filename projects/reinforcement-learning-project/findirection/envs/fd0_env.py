import numpy as np
import gym
from gym.spaces import Discrete, MultiDiscrete
from findirection.envs.actions import Actions
from findirection.envs.grid_level import GridLevel
from findirection.envs.robot_draw import RobotDraw


class FindDirection_v0(gym.Env):
  
    def __init__(self, **kwargs):
        super().__init__()

        self.width = 6  
        self.height = 6      
        self.max_x = self.width - 1
        self.max_y = self.height - 1


        self.action_space = Discrete(5)          
          
        self.observation_space = MultiDiscrete([self.width, self.height])
                                        
        self.start = kwargs.get('start',[0,0])       
        self.end = kwargs.get('end',[self.max_x,self.max_y])        
      
        self.initial_pos = kwargs.get('initial_pos',self.start)  

        self.x = self.initial_pos[0]
        self.y = self.initial_pos[1]
        
        self.level = GridLevel( **kwargs )  
      
        self.robot = RobotDraw(self.level,**kwargs)   
        self.robot.draw()
        
    def take_action(self, action):
     
        if   action == Actions.North: self.y -= 1
        elif action == Actions.South: self.y += 1
        elif action == Actions.West:  self.x -= 1
        elif action == Actions.East:  self.x += 1    
      
        if self.x < 0: self.x = 0
        if self.y < 0: self.y = 0
        if self.x > self.max_x: self.x = self.max_x
        if self.y > self.max_y: self.y = self.max_y   
 
    def reset(self):
        self.robot.set_cell_position(self.initial_pos)      
        self.robot.reset()               
        self.x = self.initial_pos[0]
        self.y = self.initial_pos[1]        
        return np.array([self.x,self.y])  

    def step(self, action):  
        self.take_action(action)      
        obs = np.array([self.x,self.y])              
        done = (self.x == self.end[0]) and (self.y == self.end[1])
        reward = 0 if done else -1 
        info = {}
        return obs, reward, done, info
          
    def render(self, mode='human', action=0, reward=0 ):
        print(f"{Actions(action): <5}: ({self.x},{self.y}) reward = {reward}")    
      
        self.robot.move(self.x,self.y) 
        return self.level.draw() 