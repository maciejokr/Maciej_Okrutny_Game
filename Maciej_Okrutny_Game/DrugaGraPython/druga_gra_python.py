import pygame
from random import randint
################################################################
#Game project

pygame.init()
window = pygame.display.set_mode((1280,720)) # window size is set by pygame.display.set_mode 

class Physic:
    def __init__(self,x,y,witdh,height,acc, max_vel):
        self.x_cord = x # x position 
        self.y_cord = y # y position 
        self.hor_velocity=0 # horizontal velocity
        self.ver_velocity=0 # vertical velocity
        self.acc = acc # acceleration 
        self.max_vel= max_vel # max velocity
        self.width=witdh # weight
        self.height=height# height 
        self.previous_x=x # previous x position
        self.previous_y=y # previous y position
        self.jump=False # Control bit jump 
        self.hitbox=pygame.Rect(self.x_cord, self.y_cord, self.width,self.height)

    def physic_tick(self,beams): # tick function for player 
        self.ver_velocity +=0.7
        self.x_cord+=self.hor_velocity
        self.y_cord+=self.ver_velocity
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width,self.height)  # update hitbox
        for beam in beams: 
            ################## Check colision with beams
            if beam.hitbox.colliderect(self.hitbox):
                if self.x_cord+ self.width >= beam.x+1>self.previous_x +self.width: # colision from left side
                     self.x_cord=self.previous_x
                     self.hor_velocity=0      
                if self.x_cord < beam.x+beam.width-1 < self.previous_x: # colision from left side
                     self.x_cord=self.previous_x
                     self.hor_velocity=0                  
                if self.y_cord+ self.height >= beam.y+1>self.previous_y +self.height:
                     self.y_cord=self.previous_y
                     self.jump=False
                     self.ver_velocity=0     
                if self.y_cord <beam.y+ self.height-1<self.previous_y:
                     self.y_cord=self.previous_y
                     self.jump=False
                     self.ver_velocity=0                  
        self.previous_x=self.x_cord # update previous x position
        self.previous_y=self.y_cord # update previous y position
            
class Player(Physic):

    def __init__(self):
        self.image=pygame.image.load("john.png")# image of player
        self.width=self.image.get_width() # weight of player
        self.height=self.image.get_height() # height of player

        super().__init__(0,580,self.width,self.height,0.5,5)
    
    def tick(self,keys,beams): # tick function for player 
        self.physic_tick(beams)
        if keys[pygame.K_a] and self.hor_velocity>self.max_vel*-1: 
            self.hor_velocity-=self.acc
        if keys[pygame.K_d] and self.hor_velocity<self.max_vel: 
            self.hor_velocity+=self.acc
        if not(keys[pygame.K_a] or keys[pygame.K_d]):
            if self.hor_velocity>0:
                self.hor_velocity-=self.acc
            elif self.hor_velocity<0:
                self.hor_velocity+=self.acc
        if keys[pygame.K_SPACE] and self.jump==False:
            self.jump=True
            self.ver_velocity=-10


    def draw(self): # draw player
        window.blit(self.image,(self.x_cord, self.y_cord))


class Beam:
    def __init__(self,x,y,width,height):
        self.x = x # x position
        self.y = y # y position
        self.width = width # width
        self.height = height # height
        self.hitbox=pygame.Rect(self.x, self.y, self.width,self.height)# create hitbox
    
    def draw(self,win):
        pygame.draw.rect(win,(128,128,128),self.hitbox)


    
def main():
    run=True
    player=Player()
    background= pygame.image.load("polana.png")
    beams = [
        Beam(10,650,1000,40),
        Beam(500,500,20,200)
    ]
    while run:
        pygame.time.Clock().tick(60)# max fps  
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit the program
                run=False
        keys=pygame.key.get_pressed()        

        player.tick(keys, beams)
        
        window.blit(background,(0,0))

        player.draw()
        
        for beam in beams:
            beam.draw(window)
        pygame.display.update() 
        

if __name__ == "__main__":
    main()
