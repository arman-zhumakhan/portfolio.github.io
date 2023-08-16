import os
from enum import IntEnum
from random import uniform
from math import pi
import json

from ipycanvas import MultiCanvas, Canvas, hold_canvas
from ipywidgets import Image


from findirection.envs.grid_base import GridBase
from findirection.envs.arrows import Arrows
from findirection.envs.directions import Direction



class Level(IntEnum): 
    Base     = 0
    Grid     = 1
    Underlay = 2    
    Robot    = 3    
    Overlay  = 4
    Text     = 5



class DrawGrid():

    num_canvases = 6           
    cell_pixels = 64                
    padding = 2                
    wall_width = 4              
    border_width = 5           
    side_panel = None          
    bottom_panel = None        

    base_color = '#c7c3c5'     
    grid_color = '#777'        
    start_color = '#9e0954'    
    start_text_color = '#fff'  
    exit_color = 'green'      
    exit_text_color = '#fff'
    border_color = 'black'     
    wall_color = 'black'       


    def __init__(self, gridbase: GridBase, **kwargs: dict):

        self.grid = gridbase

        self.show_start_text = kwargs.get('show_start_text',True)
        self.show_end_text = kwargs.get('show_end_text',True)        

        self.set_properties(kwargs.get('grid',None))  

        self.add_compass = kwargs.get('add_compass',False)
        self.side_panel = kwargs.get('side_panel',None)    
        self.bottom_panel = kwargs.get('bottom_panel',None)            

        self.load_puddle_sprite() 

        self.create_canvases()    
        self.draw_level()  


    def set_properties( self, grid_props: dict ):  
    
        if grid_props is not None:
            theme = grid_props.get('theme',None)
            if theme is not None:       
                theme_path = os.path.join(self.grid.working_directory,f'themes/{theme}.json')
                if os.path.exists(theme_path):         
                    with open(theme_path) as json_file:
                        grid_props = json.load(json_file)        
                else:   
                    theme_path = os.path.join(os.getcwd(),f'themes/{theme}.json')
                    if os.path.exists(theme_path):         
                        with open(theme_path) as json_file:
                            grid_props = json.load(json_file)  


            colors = grid_props.get('colors',None)
            if colors is not None:
        
                self.base_color = colors.get('base', self.base_color)
                self.grid_color = colors.get('lines', self.grid_color)
                self.start_color = colors.get('start', self.start_color)
                self.start_text_color = colors.get('start_text', self.start_text_color)
                self.exit_color = colors.get('exit', self.exit_color)
                self.exit_text_color = colors.get('exit_text', self.exit_text_color)
                self.border_color = colors.get('border', self.border_color)
                self.wall_color = colors.get('walls', self.wall_color)   

            widths = grid_props.get('widths',None)
            if widths is not None:
                self.padding = widths.get('padding', self.padding)
                self.wall_width = widths.get('walls', self.wall_width)     
                self.border_width = widths.get('border', self.border_width)     


    def calculate_dimensions(self):
        self.width_pixels = self.grid.width * self.cell_pixels + (self.padding*2)
        self.height_pixels = self.grid.height * self.cell_pixels + (self.padding*2)   
        self.total_width = self.width_pixels
        self.total_height = self.height_pixels    

        if self.add_compass or (self.side_panel is not None): 
            if type(self.side_panel) == int:
                self.total_width += self.side_panel
            elif type(self.side_panel) == dict:        
                self.total_width += self.side_panel.get('width',100)
            else:
                self.total_width += 100
   
        if self.bottom_panel is not None: 
            if type(self.bottom_panel) == int:
                self.total_height += self.bottom_panel
            elif type(self.bottom_panel) == dict:
                self.total_height += self.bottom_panel.get('height',50)
            else:   
                self.total_height += 50
    
        self.center = self.cell_pixels//2 - self.padding     
    
    
    def create_canvases(self):      
        self.calculate_dimensions()    

        self.canvases = MultiCanvas(n_canvases=self.num_canvases, 
                                    width=self.total_width, 
                                    height=self.total_height, 
                                    sync_image_data=True)     


    def grid_to_pixels( self, grid_pos, xoff = 0, yoff = 0 ):
        x = (grid_pos[0] * self.cell_pixels) + self.padding + xoff
        y = (grid_pos[1] * self.cell_pixels) + self.padding + yoff   
        return x,y   


    def get_center(self,x,y):
        cx = x + self.center
        cy = y + self.center      
        return cx,cy    



    def draw_rect(self, canvas_index, width, height, color, x=0, y=0):
        canvas = self.canvases[canvas_index]
        canvas.fill_style = color
        canvas.fill_rect(x, y, width, height) 


    def set_reward_area(self,x,y,wd,ht,reward):
        pass

    def draw_grid_areas(self):
        for area in self.grid.grid_areas:
            try:  
                x,y,wd,ht = self.grid.get_area_defn(area[0])
                width  = wd * self.cell_pixels 
                height = ht * self.cell_pixels 
                px, py = self.grid_to_pixels([x,y])

                canvas_index = Level.Base     
                self.draw_rect( canvas_index, width, height, area[1], px, py )                

            except:
                pass   


    def draw_base_areas(self):
        for area in self.grid.base_areas:
            try:  

                area_only = False        
                if type(area[0]).__name__ == 'int':
                    x,y,wd,ht = self.grid.get_area_defn(area)
                    area_only = True
                else:
                    x,y,wd,ht = self.grid.get_area_defn(area[0])
                width  = wd * self.cell_pixels 
                height = ht * self.cell_pixels 
                px, py = self.grid_to_pixels([x,y])

                half_border = self.border_width//2
                if x == 0:
                    px -= half_border
                    width += half_border
                if y == 0:
                    py -= half_border
                    height += half_border
                if (x+wd) == self.grid.width:          
                    width += half_border          
                if (y+ht) == self.grid.height:          
                    height += half_border                

                color = "white" 
                if area_only == False and len(area) > 1: 
                    if type(area[1]).__name__ == 'str': color = area[1]     
                canvas_index = Level.Grid     
                self.draw_rect( canvas_index, width, height, color, px, py )


                borders = None  
                if area_only == False and len(area) > 1: 
                    if type(area[1]).__name__ != 'str': borders = area[1]
                    if len(area) == 3: borders = area[2]

                if borders == None:
                    borders = []
                    if y != 0: borders.append(('N'))
                    if (y+ht) != self.grid.height: borders.append(('S'))
                    if x != 0: borders.append(('W'))
                    if (x+wd) != self.grid.width: borders.append(('E'))        

                canvas = self.canvases[Level.Grid]
                canvas.set_line_dash([0,0])
                canvas.line_cap = 'square'

                for border in borders:                      
                    edge = border[0]
                    canvas.stroke_style = border[1] if len(border) > 1 else self.border_color                                                          
                    canvas.line_width = border[2] if len(border) == 3 else self.border_width 
            
                    if edge == 'N':
                        x1 = self.padding + px
                        y1 = self.padding + py 
                        x2 = x1 + width-(2*self.padding)
                        y2 = y1
                        self.draw_line( canvas, x1, y1, x2, y2 )
   
                    if edge == 'S':
                        x1 = self.padding + px
                        y1 = py + height - self.padding 
                        x2 = x1 + width-(2*self.padding)
                        y2 = y1
                        self.draw_line( canvas, x1, y1, x2, y2 )
        
                    if edge == 'W':
                        x1 = self.padding + px
                        y1 = self.padding + py 
                        x2 = x1
                        y2 = y1 + height-(2*self.padding)
                        self.draw_line( canvas, x1, y1, x2, y2 )        

                    if edge == 'E':
                        x1 = px + width - self.padding
                        y1 = self.padding + py 
                        x2 = x1
                        y2 = y1 + height-(2*self.padding)
                        self.draw_line( canvas, x1, y1, x2, y2 )                                      

            except:
                pass        


    def draw_line( self, canvas, x1, y1, x2, y2 ):
        canvas.begin_path()
        canvas.move_to(x1 , y1 )
        canvas.line_to(x2 , y2 )
        canvas.stroke()      


    def draw_grid(self,canvas):                   
        canvas.stroke_style = self.grid_color
        canvas.line_width = 1
        canvas.set_line_dash([4,8])    

        for y in range(self.grid.height):   
            for x in range(self.grid.width):   
                canvas.stroke_rect(self.cell_pixels * x + self.padding, 
                                   self.cell_pixels * y + self.padding, 
                                   self.cell_pixels,
                                   self.cell_pixels)
      
      
    def draw_start(self,canvas):      
        start_x, start_y = self.grid_to_pixels( self.grid.start )
        canvas.fill_style = self.start_color
        canvas.fill_rect(start_x, start_y, self.cell_pixels, self.cell_pixels)       
        canvas.fill_style = self.start_text_color

        if self.show_start_text:
            canvas.text_align = 'left'
            canvas.font = 'bold 17px sans-serif'
            canvas.fill_text(str("CITYU"), start_x + 5, start_y + 38)     

      
    def draw_exit(self, canvas):
        end_x, end_y = self.grid_to_pixels( self.grid.end )
        canvas.fill_style = self.exit_color
        canvas.fill_rect(end_x, end_y, self.cell_pixels, self.cell_pixels)    
        canvas.fill_style = self.exit_text_color
        if self.show_end_text:
            canvas.text_align = 'left'
            canvas.font = 'bold 20px sans-serif'
            canvas.fill_text(str("HOME"), end_x + 5, end_y + 40)       
      
      
    def draw_border(self,canvas):    
        canvas.stroke_style = self.border_color
        canvas.line_width = self.border_width
        canvas.set_line_dash([0,0])
        canvas.stroke_rect(self.padding, 
                           self.padding, 
                           self.width_pixels-(2*self.padding),
                           self.height_pixels-(2*self.padding))     


    def draw_maze(self,canvas):    
        if self.grid.add_maze: 
            self.grid.maze.write_to_canvas( canvas,
                                            self.grid.height*self.cell_pixels,
                                            self.padding, 
                                            color = self.wall_color,
                                            wall_width = self.wall_width)    


    def load_puddle_sprite(self):        
        image_path = os.path.join(self.grid.working_directory,'images/big_puddle.png')
        self.big_puddle = Image.from_file(image_path)  
        image_path = os.path.join(self.grid.working_directory,'images/small_puddle.png')
        self.small_puddle = Image.from_file(image_path)  
      
        if self.grid.drawmode == 'colab':
            image_path = os.path.join(self.grid.working_directory,'images/small_puddle.png')
            self.small_puddle = Image.from_file(image_path)    
        else:
            self.puddle_canvas = Canvas(width=self.cell_pixels, height=self.cell_pixels, sync_image_data=True)                 
            self.puddle_canvas.draw_image( self.big_puddle, 0, 0 )          



    def draw_puddles(self):   
        if self.grid.puddles:      
            canvas = self.canvases[Level.Grid]
            with hold_canvas(canvas):  
                if isinstance(self.grid.puddles[0],list):
                    for row in range(self.grid.height):
                        for col in range(self.grid.width):
                            self.draw_splash( canvas, col, row, self.grid.puddles[row][col] ) 
                else:
                    for (x, y), puddle_size in self.grid.puddles:
                        self.draw_splash( canvas, x, y, puddle_size )     


    def draw_splash(self,canvas,x,y,puddle_type):
        if puddle_type > 0:
            if self.grid.drawmode != 'colab':
                scale = puddle_type / 2

                splash_canvas = Canvas(width=self.cell_pixels, height=self.cell_pixels)
                with hold_canvas(splash_canvas):          

                    pos_x = self.cell_pixels//2
                    pos_y = self.cell_pixels//2

                    splash_canvas.translate(pos_x, pos_y)

                    splash_canvas.scale(scale)

                    splash_canvas.translate( -pos_x, -pos_y )
         
                    splash_canvas.draw_image(self.puddle_canvas, 0, 0)          

            x_px = x * self.cell_pixels + self.padding
            y_px = y * self.cell_pixels + self.padding
            if puddle_type==1:
                canvas.draw_image(self.small_puddle,x_px,y_px,width=self.cell_pixels,height=self.cell_pixels)
            else:
                canvas.draw_image(self.big_puddle,x_px,y_px,width=self.cell_pixels,height=self.cell_pixels)


    def draw_compass(self,canvas):      
        if self.add_compass: 
            arrows = Arrows(64,2,length=15,width=5,height=11)
            arrows.draw(canvas,
                        self.width_pixels + 27, 14,
                        [Direction.North,Direction.West,Direction.South,Direction.East],
                        center_width = 28 )

            canvas.font = 'bold 20px sans-serif'
            canvas.fill_text(str("W"), self.width_pixels + 13, 52)    
            canvas.fill_text(str("N"), self.width_pixels + 49, 18)     
            canvas.fill_text(str("E"), self.width_pixels + 82, 52)     
            canvas.fill_text(str("S"), self.width_pixels + 51, 85)        


    def draw_info_panel(self):  

        if type(self.side_panel) == dict:
            width = self.side_panel.get('width',200)
            height = self.side_panel.get('height',self.height_pixels)
            color = self.side_panel.get('color','white')
            self.draw_rect(Level.Base, width, height, color, x = self.width_pixels, y = 0)   

        if type(self.bottom_panel) == dict:
            width = self.bottom_panel.get('width',self.total_width)
            height = self.bottom_panel.get('height',100)
            color = self.bottom_panel.get('color','white')                
            self.draw_rect(Level.Base, width, height, color, x = 0, y = self.height_pixels)     


    def clear( self, all_info = False ):

        canvas = self.canvases[Level.Overlay]
        
        if self.side_panel is not None:
            canvas.clear_rect(self.width_pixels,0,(self.total_width-self.width_pixels),self.total_height)   

        if self.bottom_panel is not None:
            canvas.clear_rect(0,self.height_pixels,self.total_width,(self.total_height-self.height_pixels))         

        if all_info == True:
            canvas.clear()




    def draw_level(self):

        self.canvases[Level.Overlay].clear()
        self.canvases[Level.Grid].clear()

        self.draw_info_panel() 

        self.draw_rect(Level.Base, self.width_pixels, self.height_pixels, self.base_color)   

        self.draw_grid_areas()         

        canvas = self.canvases[Level.Grid]

        with hold_canvas(canvas):        
            self.draw_start(canvas)
            self.draw_exit(canvas)   
            self.draw_grid(canvas)      
            self.draw_maze(canvas) 
            self.draw_border(canvas)              
            self.draw_base_areas()        
            self.draw_compass(canvas) 

        self.draw_puddles()         


    def create_canvas(self):
    
        width = 200
        height = 200

        canvas = MultiCanvas(2, width=width, height=height, sync_image_data=True)

        canvas[0].fill_style = 'white' 
        canvas[0].fill_rect(0, 0, width, height) 

        return canvas                                       