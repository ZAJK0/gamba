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
bet = 50

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREEN_HOVER = (0, 200, 0)

fruit = ["img/image3.png","img/image4.png","img/image5.png","img/image6.png","img/image7.png","img/image8.png","img/image9.png",]

# for i in range(3, 9):
#     filename = f"img/image{i}.png"
#     fruit.append(filename)

winImg = "img/win.png"
fruitWidth = 100
fruitLenght = 100
posx=90

item1 = pygame.transform.scale(pygame.image.load(fruit[0]),(fruitWidth,fruitLenght))
item2 = pygame.transform.scale(pygame.image.load(fruit[1]),(fruitWidth,fruitLenght))
item3 = pygame.transform.scale(pygame.image.load(fruit[2]),(fruitWidth,fruitLenght))
item4 = pygame.transform.scale(pygame.image.load(fruit[3]),(fruitWidth,fruitLenght))
item5 = pygame.transform.scale(pygame.image.load(fruit[4]),(fruitWidth,fruitLenght))
item6 = pygame.transform.scale(pygame.image.load(fruit[5]),(fruitWidth,fruitLenght))
item7 = pygame.transform.scale(pygame.image.load(fruit[6]),(fruitWidth,fruitLenght))

items = [item1,item2,item3,item4,item5,item6,item7]

win = pygame.transform.scale(pygame.image.load(winImg),(200,200))
overlay = pygame.transform.scale(pygame.image.load("img/untitled-1.png"),(800,480))
stone = pygame.transform.scale(pygame.image.load("img/Group2.png"),(813,400))



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
    point = point-bet
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

    res1 = random.randint(0,6)
    res2 = random.randint(0,6)
    res3 = random.randint(0,6)
    res4 = random.randint(0,6)
    res5 = random.randint(0,6)
    res = [res1,res2,res3,res4,res5]

    row1 = random.sample(items, len(items))
    row2 = random.sample(items, len(items))
    row3 = random.sample(items, len(items))
    row4 = random.sample(items, len(items))
    row5 = random.sample(items, len(items))
    rows = [row1,row2,row3,row4,row5]


    while (True):
    
        if(speeds[4]>0):
            screen.blit(stone, (-7,47)) 
            for x in range(0,5):
                print(x)
                if(speeds[x]>0):
                    posy[x] = posy[x]+20  
                    if(posy[x] > 800):
                        posy[x]=posy[x]-700

                    speeds[x]= speeds[x]-5
                    print (speeds[4])


                for i in range(0,14):    # RENDER YOUR GAME HERE
                    img = rows[x][i%7] 
                    screen.blit(img, (posx+130*x,posy[x]+i*100-1010))


            
        if (speeds[4] < 1):
            screen.blit(overlay, (0,0))
            print(f"{res1}, {res2}, {res3}, {res4}")        
            # if (rows[0][4] == rows[1][4] == rows[2][4]):
            if (1):
                if (rows[2][4]==rows[3][4]):

                    if(rows[3][4]==rows[4][4]):
                        point = point+100*bet
                    else:
                        point = point+50*bet
                else:
                    point = point+10*bet

                print("You win")

                screen.blit(win, (300,140))
                pygame.display.flip()
                point = point+100*bet

                pygame.time.wait(200)
                
                
            print(point)
            pygame.display.flip()

            pygame.time.wait(1000)

            break
        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        screen.blit(overlay, (0,0))
        pygame.display.flip()
        

    clock.tick(60)  # limits FPS to 60

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mycursor.execute(f"UPDATE body SET point = {point} WHERE user = '{user}'")
            mydb.commit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                spin()
            if event.key ==pygame.K_LEFT:
                if (bet > 50):
                    bet = bet - 50
                    print(bet)
            if event.key == pygame.K_RIGHT:
                bet = bet + 50
                print(bet)

        if  event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if button.is_hover(pos):
                spin()
    button.draw(screen)
    pygame.display.flip()
 






pygame.quit()