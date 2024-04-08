# Example file showing a basic pygame "game loop"
import pygame
import random
import mysql.connector
# pygame setup

user = "zajo"
mydb = mysql.connector.connect(host="localhost", user="root", password="",database="gamba")
mycursor = mydb.cursor()
mycursor.execute(f"select *from body where user = '{user}'")
result = mycursor.fetchone()
for i in result:
    print(i)


point = result[3]


pygame.init()
screen = pygame.display.set_mode((2560, 1540))
clock = pygame.time.Clock()
running = True

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREEN_HOVER = (0, 200, 0)

fruit = ["img/lemon.png","img/melon.png","img/seven.png"]
winImg = "img/win.png"
fruitWidth = 300
fruitLenght = 300
posx=400

lemon = pygame.transform.scale(pygame.image.load(fruit[0]),(fruitWidth,fruitLenght))
melon = pygame.transform.scale(pygame.image.load(fruit[1]),(fruitWidth,fruitLenght))
seven = pygame.transform.scale(pygame.image.load(fruit[2]),(fruitWidth,fruitLenght))
win = pygame.transform.scale(pygame.image.load(winImg),(800,800))

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text, text_rect)

    def is_hover(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False
    
button = Button("Click Me", 300, 200, 200, 100, GREEN, GREEN_HOVER, lambda: print("Button Clicked"))

def spin():
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    # fill the screen with a color to wipe away anything from last frame
    global point
    point = point-50
    posy1 = 0
    posy2 = 0 
    posy3 = 0
    posy4 = 0
    posy5 = 0
    posy = [posy1,posy2,posy3,posy4]
    speed1 = 200
    speed2 = 250
    speed3 = 300
    speed4 = 350
    speed5 = 400
    speeds = [speed1,speed2,speed3,speed4]

    res1 = random.randint(0,2)
    res2 = random.randint(0,2)
    res3 = random.randint(0,2)
    res4 = random.randint(0,2)
    res5 = random.randint(0,2)
    res = [res1,res2,res3,res4,res5]

    while (True):

        if event.type == pygame.KEYDOWN:
            pass
        if(speeds[3]>0):
            screen.fill("red")
            for x in range(0,4):
                if(speeds[x]>0):
                    posy[x] = posy[x]+160
                    if(posy[x] >180):
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
            
        if (speeds[3] < 1):
            print(f"{res1}, {res2}, {res3}, {res4}")        
            if (res1 == res2 == res3 == res4):
                print("You win")
                screen.blit(win, (800,500))
                pygame.display.flip()
                point = point+1000

                pygame.time.wait(200)
                
                
            print(point)
            pygame.display.flip()

            pygame.time.wait(1000)

            break
        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()
        

    clock.tick(60)  # limits FPS to 60

while running:
    print(point)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mycursor.execute(f"UPDATE body SET point = {point} WHERE user = '{user}'")
            mydb.commit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                spin()

        if  event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if button.is_hover(pos):
                spin()
    button.draw(screen)
    pygame.display.flip()
 






pygame.quit()