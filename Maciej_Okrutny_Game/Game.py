import pygame
from math import floor
import time

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
        self.direction=1 # Direction
        self.hitbox=pygame.Rect(self.x_cord, self.y_cord, self.width,self.height)

    def physic_tick(self,obejcts,background_width): # tick function for player 

        self.ver_velocity += 0.7

        if self.x_cord + self.hor_velocity < background_width and self.x_cord + self.hor_velocity > 0:
            self.x_cord += self.hor_velocity
        self.y_cord += self.ver_velocity
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)  # odświeżanie hitboxa
        for obecjt in obejcts:
            if obecjt.hitbox.colliderect(self.hitbox):  # cofanie obiektu do miejsca z poprzedniej klatki
                if self.x_cord + self.width >= obecjt.x_cord + 1 > self.previous_x + self.width:  # kolizja z prawej strony
                    self.x_cord = self.previous_x
                    self.hor_velocity = 0
                if self.x_cord <= obecjt.x_cord + obecjt.width - 1 < self.previous_x:  # kolizja z lewej strony
                    self.x_cord = self.previous_x
                    self.hor_velocity = 0
                if self.y_cord + self.height >= obecjt.y_cord + 1 > self.previous_y + self.height:  # kolizja z dołu
                    self.y_cord = self.previous_y
                    self.ver_velocity = 0
                    self.jump = False
                if self.y_cord <= obecjt.x_cord + obecjt.width - 1 < self.previous_y:  # kolizja z góry
                    self.y_cord = self.previous_y
                    self.ver_velocity = 0

        self.previous_x = self.x_cord
        self.previous_y = self.y_cord
            
class Player(Physic):

    def __init__(self):
        self.hp=100
        image=pygame.image.load('Davis/davis_0.png')
        image2=pygame.image.load('Davis/davis_2.png')
        self.stand_right_img=image.subsurface(18, 6, 45, 73)# animation stand in right side of player
        self.stand_left_img=pygame.transform.flip(self.stand_right_img, True, False) # animation stand in right side of player
        self.width=self.stand_right_img.get_width() # weight of player
        self.height=self.stand_right_img.get_height() # height of player
        self.jump_right_img=image.subsurface(258, 482, 52, 73) #animation jumping in right
        self.jump_left_img= pygame.transform.flip(self.jump_right_img, True, False)#animation jumping in left
        self.walk_right_img=[image.subsurface(258+(x*80), 6, 45, 73) for x in range(1,5)] #animation movement
        self.walk_left_img=[pygame.transform.flip(image.subsurface(258+(x*80), 6, 45, 73), True, False) for x in range(1,5)] #animation movement
        self.attack_right=[image2.subsurface(645, 8, 70, 71), image2.subsurface(725, 8, 70, 71) ,image2.subsurface(245, 8, 70, 71), image2.subsurface(325, 8, 70, 71)]
        self.attack_left=[pygame.transform.flip(self.attack_right[0], True, False), pygame.transform.flip(self.attack_right[1], True, False), pygame.transform.flip(self.attack_right[3], True, False), pygame.transform.flip(self.attack_right[3], True, False)]
        self.walk_index=0 # animation index for walking
        self.fight_index=0
        self.fight=False
        self.hit=False
        self.timeLastHit=time.time()
        super().__init__(0,565,self.width,self.height,0.5,5)
    
    def tick(self,keys,beams,attacks, background_width): # tick function for player 
        self.physic_tick(beams, background_width)
        if keys[pygame.K_a] and self.hor_velocity>self.max_vel*-1: 
            self.hor_velocity-=self.acc
        if keys[pygame.K_d] and self.hor_velocity<self.max_vel: 
            self.hor_velocity+=self.acc
        if not(keys[pygame.K_a] or keys[pygame.K_d]):
            if self.hor_velocity>0:
                self.hor_velocity-=self.acc
            elif self.hor_velocity<0:
                self.hor_velocity+=self.acc
        if self.hor_velocity>0:
            self.direction=1 
        elif self.hor_velocity<0:
            self.direction=0
        if (keys[pygame.K_w] and self.jump==False):
            self.jump=True
            self.ver_velocity=-10
        if self.fight==True:
            self.fight_index+=0.5
        if self.fight_index>=4:
            self.fight=False
            self.fight_index=0
        if keys[pygame.K_SPACE] and self.fight==False:
            attacks.append(self.attack(self.x_cord, self.y_cord+(self.height/3)))
    def dead(self):
        if self.hp==0: return True


    def draw(self,window, background_width, resolution): # draw player
        if background_width- resolution[0]/2> self.x_cord>=resolution[0]/2:
            x_scren=resolution[0]/2
        elif self.x_cord>=background_width- resolution[0]/2:
            x_scren=self.x_cord-background_width+resolution[0]
        else:
            x_scren=self.x_cord

        if self.jump and self.fight==False:
            if self.direction==1:
                window.blit(self.jump_right_img,(x_scren, self.y_cord))
            else:
                window.blit(self.jump_left_img,(x_scren, self.y_cord))
        elif self.hor_velocity!=0 and self.fight==False:
            if self.direction==1:
                window.blit(self.walk_right_img[floor(self.walk_index)],(x_scren, self.y_cord))
            else:
                window.blit(self.walk_left_img[floor(self.walk_index)],(x_scren, self.y_cord))   

            self.walk_index+=0.1
            if self.walk_index>3:
                self.walk_index=0
        elif self.hor_velocity==0 and self.fight==False:
            if self.direction==1:
                window.blit(self.stand_right_img,(x_scren, self.y_cord))
            else:
                window.blit(self.stand_left_img,(x_scren, self.y_cord))
        elif self.fight==True:
            if self.direction==1:
                window.blit(self.attack_right[floor(self.fight_index)],(x_scren, self.y_cord))
            else:
                window.blit(self.attack_left[floor(self.fight_index)],(x_scren, self.y_cord))
    def attack(self, x_cord, y_cord):
        self.fight=True
        return Attack(20,x_cord,y_cord,"Davis",500,self.direction)

class Enemy(Physic):
    
    def __init__(self,filname,player_x,background_width):
        self.hp=100
        self.dmg=10
        image=pygame.image.load(f'{filname}/{filname}_0.png')
        self.stand_right_img=image.subsurface(18, 6, 45, 73) # animation stand in right side
        self.stand_left_img=pygame.transform.flip(self.stand_right_img, True, False) # animation stand in right side 
        self.width=self.stand_right_img.get_width() # weight 
        self.height=self.stand_right_img.get_height() # height 
        self.walk_right_img=[image.subsurface(258+(x*80), 6, 45, 73) for x in range(1,5)] #animation movement
        self.walk_left_img=[pygame.transform.flip(image.subsurface(258+(x*80), 6, 45, 73), True, False) for x in range(1,5)] #animation movement
        self.walk_index=0 # animation index for walking
        super().__init__(player_x+1000,565,self.width,self.height,0.1,2)
    
    def tick(self,beams, player_x, background_width): # tick function for 
        self.physic_tick(beams, background_width)
        if self.x_cord>player_x:
            if self.hor_velocity>0:
                self.hor_velocity=0
            self.hor_velocity-=self.acc
            if self.hor_velocity<self.max_vel*(-1):
                self.hor_velocity=self.max_vel*(-1)
        elif self.x_cord<player_x: 
            if self.hor_velocity<0:
                self.hor_velocity=0
            self.hor_velocity+=self.acc
            if self.hor_velocity>self.max_vel:
                self.hor_velocity=self.max_vel
        if self.hor_velocity>0:
            self.direction=1 
        elif self.hor_velocity<0:
            self.direction=0
        


    def draw(self,window, x_background): # 

        if self.hor_velocity!=0:
            if self.direction==1:
                window.blit(self.walk_right_img[floor(self.walk_index)],(self.x_cord + x_background, self.y_cord))
            else:
                window.blit(self.walk_left_img[floor(self.walk_index)],(self.x_cord + x_background, self.y_cord))   

            self.walk_index+=0.2
            if self.walk_index>3:
                self.walk_index=0
        else:
            if self.direction==1:
                window.blit(self.stand_right_img,(self.x_cord + x_background , self.y_cord))
            else:
                window.blit(self.stand_left_img,(self.x_cord + x_background , self.y_cord))

    def hp_status(self):
        if self.hp==0:
            return True

class Attack:
    def __init__(self,dmg,x,y,filename,distance,direction):
        image=pygame.image.load(f'{filename}/attack0.png')
        self.dmg=dmg
        self.x_start_position=x
        self.x_cord=x
        self.y_cord=y
        self.image_right=image.subsurface(5, 105, 72, 24)
        self.width=self.image_right.get_width() #
        self.height=self.image_right.get_height() #
        self.image_left=pygame.transform.flip(self.image_right, True, False)
        self.distance=distance
        self.direction=direction
        self.speed=10
        self.hitbox=pygame.Rect(self.x_cord, self.y_cord, self.width,self.height)


    def tick(self):
        if self.direction==1:
            self.x_cord+=self.speed
        else:
            self.x_cord-=self.speed
        self.hitbox=pygame.Rect(self.x_cord, self.y_cord, self.width,self.height)

    def draw(self,window, x_background):
        if self.direction==1:
            window.blit(self.image_right,(self.x_cord + x_background , self.y_cord))
        else:
            window.blit(self.image_left,(self.x_cord + x_background, self.y_cord))  
    
    def destruction(self,object):
        if object.hitbox.colliderect(self.hitbox):
            object.hp-=self.dmg
            return True
        elif abs(self.x_cord-self.x_start_position)==self.distance:
            return True





class Beam:
    def __init__(self,x,y,width,height):
        self.hp=99999999999
        self.x_cord = x # x position
        self.y_cord = y # y position
        self.width = width # width
        self.height = height # height
        self.hitbox=pygame.Rect(self.x_cord, self.y_cord, self.width,self.height)# create hitbox
    
    def draw(self,win, x_background):
        pygame.draw.rect(win, (200, 200, 200), (self.x_cord + x_background, self.y_cord, self.width, self.height))

class Background:
    def __init__(self):
        self.x_cord=0
        self.y_cord=0
        self.image=pygame.image.load("Map/las.png")
        self.width=self.image.get_width() # width of background
        self.height=self.image.get_height() # height of background 

    
    def tick(self,player,resolution):
        if self.width - resolution[0] / 2 > player.x_cord >= resolution[0] / 2:
            self.x_cord = -player.x_cord + resolution[0] / 2
        elif player.x_cord >= self.width - resolution[0] / 2:
            self.x_cord = - self.width + resolution[0]
        else:
            self.x_cord = 0
    
    def draw(self,window):
        window.blit(self.image,(self.x_cord, self.y_cord))

class Button:
    def __init__(self,x,y,filname):
        self.image=pygame.image.load(f"{filname}.png")
        self.image_hovered=pygame.image.load(f"{filname}_hovered.png")
        self.width= self.image.get_width() # width of Button
        self.height= self.image.get_height() # height of Button
        self.x_cord= x-self.width/2 # position in x
        self.y_cord= y-self.height/2 # position in y
        self.hitbox=pygame.Rect(self.x_cord, self.y_cord, self.width,self.height)
    
    def tick(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]: 
                return True


    def draw(self,window):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.image_hovered,(self.x_cord, self.y_cord))    
        else:
            window.blit(self.image,(self.x_cord, self.y_cord))    
def colision(player,enemy):
    if player.hitbox.colliderect(enemy.hitbox):
        player.hor_velocity = 0
        enemy.hor_velocity = 0
        if enemy.x_cord<player.x_cord:
            enemy.x_cord -=5
        else:
            enemy.x_cord +=5
        if player.hit==False:
            player.timeLastHit=time.time()
            player.hp-=enemy.dmg
        player.hit=True
    
    actual_time=time.time()
    if actual_time-player.timeLastHit>=3.0:
        player.hit=False

def end_game(player,background_width): 
    if player.x_cord+player.width>=background_width:
        return True