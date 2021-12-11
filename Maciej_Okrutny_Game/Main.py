from Game import*

################################################################
#Game project

pygame.init()
resolution=(1280,720)


window = pygame.display.set_mode(resolution) # window size is set by pygame.display.set_mode 


pygame.display.set_caption("Maciej Okrutny Gra")

    
def Local_Game():
    run=True
    pause=False
    pause_image = pygame.font.Font.render(pygame.font.SysFont("", 96), "Pauza", True, (255, 255, 255))
    clock=0
    score=0
    num_enemy=0
    name_enemy=["Jack","Bandit"]
    player=Player()
    background= Background()
    beams = [
        Beam(10,720,background.width,40),
        Beam(500,670,20,50),
        Beam(570,610,200,20),
        Beam(900,590,300,20)
    ]
    attacks=[]
    enemys = [  
        Enemy(name_enemy[num_enemy],player.x_cord+500,background.width) for _ in range(1,21)
    ]
    while run:
        clock+=pygame.time.Clock().tick(60)/1000# max fps  
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit the program
                run=False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = not pause
        keys=pygame.key.get_pressed()        
        if clock >= 1:
            clock = 0
            
            enemys.append(Enemy(name_enemy[num_enemy],player.x_cord+100,background.width))
            num_enemy+=1
            if num_enemy>1:
                num_enemy=0
        if pause:
            window.blit(pause_image, (500, 300))
            pygame.display.update()
            continue
        background.tick(player,resolution)

        player.tick(keys, beams,attacks,background.width)
        if player.dead() or end_game(player, background.width): run=False
        background.draw(window)
        pygame.draw.rect(window, (255,0,0), [15,20,player.hp,10], 0)
        
        player.draw(window,background.width,resolution)
        
        for beam in beams:
            beam.draw(window,background.x_cord)

        for enemy in enemys:
            colision(player,enemy)
            enemy.tick(beams,player.x_cord, background.width)
            enemy.draw(window,background.x_cord)
            if enemy.draw_hp_status():
                enemys.remove(enemy)

        for attack in attacks:
            attack.tick()
            attack.draw(window,background.x_cord)   
            object_list=[]
            object_list.extend(enemys)
            object_list.extend(beams)
            for obejct in object_list:
                if attack.destruction(obejct):
                    try:
                        attacks.remove(attack)
                        score += 10
                    except ValueError:
                        pass
                        
    
        
        pygame.display.update()     
        
def main():
    run=True
    clock=0
    background=pygame.image.load("Menu_img/Menu.jpg")
    background=pygame.transform.scale(background,(1280, 720))
    button_play=Button((resolution[0]/2),resolution[1]/2,"Menu_img/play_button")
    while run:
        clock+=pygame.time.Clock().tick(60)# max fps  
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit the program
                run=False
        if button_play.tick():
            Local_Game()

        window.blit(background,(0,0))
        button_play.draw(window)        
        pygame.display.update()
    


if __name__ == "__main__":
    main()
    
