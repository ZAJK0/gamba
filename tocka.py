# Example file showing a basic pygame "game loop"
import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((2560, 1540))
clock = pygame.time.Clock()
running = True
fruit = ["img/lemon.png","img/melon.png","img/seven.png"]
winImg = "img/win.png"
fruitWidth = 300
fruitLenght = 300
posx=200
posy1 = 0
posy2 = 0 
posy3 = 0
posy4 = 0
posy5 = 0
posy = [posy1,posy2,posy3,posy4,posy5]
speed1 = 200
speed2 = 250
speed3 = 300
speed4 = 350
speed5 = 400
speeds = [speed1,speed2,speed3,speed4,speed5]

res1 = random.randint(0,2)
res2 = random.randint(0,2)
res3 = random.randint(0,2)
res4 = random.randint(0,2)
res5 = random.randint(0,2)
res = [res1,res2,res3,res4,res5]

lemon = pygame.transform.scale(pygame.image.load(fruit[0]),(fruitWidth,fruitLenght))
melon = pygame.transform.scale(pygame.image.load(fruit[1]),(fruitWidth,fruitLenght))
seven = pygame.transform.scale(pygame.image.load(fruit[2]),(fruitWidth,fruitLenght))
win = pygame.transform.scale(pygame.image.load(winImg),(800,800))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame



    if(speeds[3]>0):
        screen.fill("red")
        for x in range(0,4):
            if(speeds[x]>0):
                posy[x] = posy[x]+160
                if(posy[x] >300):
                    posy[x]=posy[x]-1600
                speeds[x]= speeds[x]-5
                    

            
            for i in range(-5,7):    # RENDER YOUR GAME HERE
                if (i%3 == 0):
                    img = lemon
                
                elif(i%3 == 1):
                    img = melon    
                else:
                    img = seven
                screen.blit(img, (posx+400*x,posy[x]+i*400+400*res[x]))
                print("gamba")
        
    if (speeds[3] < 1):
        print("speed")
        print(f"{res1}, {res2}, {res3}, {res4}")        
        if (res1 == res2 == res3 == res4):
            print("You win")
            screen.blit(win, (800,500))
            pygame.display.flip()

            pygame.time.wait(200)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(120)  # limits FPS to 60

pygame.quit()