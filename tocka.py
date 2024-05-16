# Example file showing a basic pygame "game loop"
import pygame
import random
import mysql.connector
# pygame setup

bet = 50
lines = 1
spinned = False

pygame.init()
screen = pygame.display.set_mode((800, 480))
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
    
button = Button("", 300, 200, 200, 100, GREEN, GREEN_HOVER, lambda: print("Button Clicked"))


def checkLines(rows,surx2,sury2,surc2,surv2,surb2):
    global point
    if (rows[0][surx2] == rows[1][sury2] == rows[2][surc2]):
    # if (1):
        if (rows[0][surx2] == item1):
            multiply = 20
        elif (rows[0][surx2] == item2):
            multiply = 16
        elif (rows[0][surx2] == item3):
            multiply = 8
        elif (rows[0][surx2] == item4):
            multiply = 12
        elif (rows[0][surx2] == item5):
            multiply = 6
        elif (rows[0][surx2] == item6):
            multiply = 4
        elif (rows[0][surx2] == item7):
            multiply = 2                                                       
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(100, 230, 600, 20))
        if (rows[2][surc2]==rows[3][4]):

            if(rows[3][surv2]==rows[4][surb2]):
                point = point+50*bet*multiply
            else:
                point = point+25*bet*multiply
        else: 
            point = point+5*bet*multiply

        
        screen.blit(rows[0][surx2], (300,140))
        pygame.display.flip()
        pygame.time.wait(500)
        screen.blit(rows[1][sury2], (300,140))
        pygame.display.flip()
        pygame.time.wait(500)
        screen.blit(rows[2][surc2], (300,140))
        pygame.display.flip()
        pygame.time.wait(500)
        screen.blit(rows[3][surv2], (300,140))
        pygame.display.flip()
        pygame.time.wait(500)
        screen.blit(rows[4][surb2], (300,140))
        pygame.display.flip()
        pygame.time.wait(500)




def spin():
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    # fill the screen with a color to wipe away anything from last frame
    global point
    point = point-bet*lines
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

# toto potom vymazat
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
                if(speeds[x]>0):
                    posy[x] = posy[x]+20  
                    if(posy[x] > 800):
                        posy[x]=posy[x]-700

                    speeds[x]= speeds[x]-5


                for i in range(0,14):    # RENDER YOUR GAME HERE
                    img = rows[x][i%7] 
                    screen.blit(img, (posx+130*x,posy[x]+i*100-1010))


            
        if (speeds[4] < 1):
            global spinned
            spinned = False
            print(rows[0][0])

            print(items[0])
            screen.blit(overlay, (0,0))
            print(f"{res1}, {res2}, {res3}, {res4}")      
            if (lines >= 1):  
                checkLines(rows,4,2,0,5,3)
            if (lines >= 3):  
                checkLines(rows,3,1,6,4,2)
                checkLines(rows,5,3,1,6,4)

            if (lines >= 5):  
                checkLines(rows,3,2,1,5,2)
                checkLines(rows,5,2,6,5,4)

            if (lines >= 7):  
                checkLines(rows,3,1,0,6,4)
                checkLines(rows,5,3,0,4,2)

            if (lines >= 9):  
                checkLines(rows,4,1,0,6,3)
                checkLines(rows,4,3,0,4,3)


                
            
            print("test")
            break
        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        screen.blit(overlay, (0,0))
        font2 = pygame.font.Font(None, 50)  
        betText = font2.render(f"bet: {bet}            lines: {lines}", True, (255, 255, 255))  
        screen.blit(betText, (50 ,440 ))
        print(point)
        pygame.display.flip()
        pygame.display.flip()
    

    clock.tick(60)   # limits FPS to 60
while running:
    user = ""
    while(user == ""):
        screen.fill("red")
        font = pygame.font.Font(None, 36)  
        uvodText = font.render("Prilozte svoje kartu", True, (255, 255, 255))  
        screen.blit(uvodText, (800 // 2 - uvodText.get_width() // 2,480 // 2 - uvodText.get_height() // 2))
        pygame.display.flip()
        user = input()

    

    mydb = mysql.connector.connect(host="localhost", user="root", password="",database="gamba")
    mycursor = mydb.cursor()
    mycursor.execute(f"select *from body where user = '{user}'")
    result = mycursor.fetchone()
    for i in result:
        print(i)
    point = result[3]   

    while running and (user != "") and (point > 0):
        if (spinned == False):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mycursor.execute(f"UPDATE body SET point = {point} WHERE user = '{user}'")
                    mydb.commit()
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_SPACE) : 
                        print (spinned)
                        spinned = True
                        spin()
                        # screen.blit(betText, (800 // 2 - betText.get_width() // 2,440  - betText.get_height() // 2))
                        pygame.display.flip()
                    if event.key ==pygame.K_LEFT:
                        if (bet > 50):
                             bet = bet - 50
                        print(bet)
                    if event.key == pygame.K_RIGHT:
                        bet = bet + 50
                        print(bet)
                    
                    if event.key ==pygame.K_a:
                        if (lines > 1):
                            lines = lines-2
                        print(lines)
                    if event.key == pygame.K_d:
                        if (lines < 9):
                            lines = lines+2
                        print(lines)

                if  event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button.is_hover(pos):
                        spin()
        button.draw(screen)
        pygame.display.flip()
    if (point <= 0):
        screen.fill("red")
        font = pygame.font.Font(None, 36)  
        uvodText = font.render("Nemate ziadne body", True, (255, 255, 255))  
        screen.blit(uvodText, (800 // 2 - uvodText.get_width() // 2,480 // 2 - uvodText.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(5000)

        






pygame.quit()