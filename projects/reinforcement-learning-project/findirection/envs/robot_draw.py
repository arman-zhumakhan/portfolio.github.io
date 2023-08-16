
from ipycanvas import Canvas, hold_canvas
from ipywidgets import Image
from time import sleep

import random
import os

from findirection.envs.robot_position import RobotPosition
from findirection.envs.draw_grid import Level


class RobotDraw( RobotPosition ):

    sprite_count = 0
    canvas_sprites = []

    x_offset = 0
    y_offset = 0  


    def __init__( self, level, **kwargs ):                      
        super().__init__( level, **kwargs )

        self.move_step = 0

        self.canvas = self.grid.canvases[Level.Robot] 

        robot_params = kwargs.get('robot',{})   

        self.sprite_change = robot_params.get('sprite_change',2)

        offset = kwargs.get('offset',[0,0])  
        self.x_offset = offset[0]
        self.y_offset = offset[1]

        self.show_robot = robot_params.get('show',True)
   
        self.sleep = robot_params.get('sleep',0.07)    
        self.canvas_sleep = robot_params.get('canvas_sleep',40)                    

        self.sprite_index = robot_params.get('initial_sprite',4)     
        self.load_sprites()


    def get_number_of_sprites(self):
        num_sprites = len(self.canvas_sprites)
        return num_sprites    


    def load_single_sprint(self):
        image_path = os.path.join(self.level.working_directory,f'images/klint.png')        
        self.sprite = Image.from_file(image_path)         


    def add_sprite(self,index):
        image_path = os.path.join(self.level.working_directory, f'images/klint.png')
        sprites = Image.from_file(image_path)
        canvas = Canvas(width=self.robot_size, height=self.robot_size)
        canvas.draw_image(sprites, 0, 0)
        self.canvas_sprites.append(canvas)      


    def load_sprites(self):

        self.canvas_sprites = []
        if self.level.drawmode == 'colab':
            self.load_single_sprint()
        else:
            for row in range(5):
                for col in range(2):           
                    index = (row*2) + col
                    self.add_sprite(index)
            self.add_sprite(index+1)          


    def update_sprite(self):   

        if self.get_number_of_sprites() > 1:
            self.sprite_count += 1
            if self.sprite_count > self.sprite_change: 
                self.sprite_count = 0   
                self.sprite_index = self.sprite_index + random.randint(-1,+1)   
                if self.sprite_index < 0: 
                    self.sprite_index = 0
                if self.sprite_index >= self.get_number_of_sprites():
                    self.sprite_index = (self.get_number_of_sprites()-1)   

                            
    def draw_sprite(self,index):   

        x = self.x + self.x_offset
        y = self.y + self.y_offset

        if self.level.drawmode == 'colab':  
            self.canvas.clear_rect(x-10, y-10, self.robot_size+10, self.robot_size+10)                      
            self.canvas.draw_image(self.sprite, x, y ) 

        elif self.sprite_index < self.get_number_of_sprites():
            with hold_canvas(self.canvas):
                self.canvas.clear_rect(x, y, self.robot_size)                       
                self.canvas.draw_image(self.canvas_sprites[index], x, y )                            


    def draw(self):    
        if self.show_robot:   
            self.draw_sprite(self.sprite_index)
            self.update_sprite()      


    def move_direction(self,direction):        
      
        if self.test_for_valid_move(direction):          
            move_method_name = f"move_{direction.name}"        

            if self.level.drawmode == 'colab':
                self.move_direction_colab( move_method_name )
            else:
                for _ in range(self.robot_size//self.step):
                    getattr(self,move_method_name)()  
                    self.draw()  
                    sleep(self.sleep)     
                    self.move_step += 1                 

            self.move_count += 1     


    def move_direction_colab( self, move_method_name ):        
                                 
        with hold_canvas(self.canvas):         
            for _ in range(self.robot_size//self.step):
                getattr(self,move_method_name)()  
                self.canvas.clear_rect(self.x-10, self.y-10, self.robot_size+10, self.robot_size+10)             
                self.canvas.draw_image(self.sprite, self.x, self.y )                     
                self.canvas.sleep(self.canvas_sleep)  
                sleep(self.sleep)
                self.move_step += 1


    def reset(self):
        self.move_step = 0
        self.canvas.clear()
        self.set_cell_position(self.initial_position) 
        self.draw()


    def partial_move(self,direction,sprite_index=None):        
              
        if direction is not None:
            if self.test_for_valid_move(direction):
                move_method_name = f"move_{direction.name}"        
                getattr(self,move_method_name)()  

                if sprite_index is not None:
                    self.sprite_index = sprite_index 
                self.draw()                
                self.move_count += 1 

                return True

        return False 