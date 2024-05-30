# Example file showing a basic pygame "game loop"
import pygame
import random
import mysql.connector
# pygame setup

bet = 50
lines = 1
point = 0
winSum = 0
spinned = False

pygame.init()
screen = pygame.display.set_mode((800, 480))
clock = pygame.time.Clock()
running = True

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
GREEN_HOVER = (0, 200, 0)

font2 = pygame.font.Font(None, 50)  
fruit = ["img/image3.png","img/image4.png","img/image5.png","img/image6.png","img/image7.png","img/image8.png","img/image9.png",]

winImg = "img/win.png"
fruitWidth = 100
fruitLenght = 100
posx=90
posy = []
rows = []

win = pygame.transform.scale(pygame.image.load(winImg),(200,200))
overlay = pygame.transform.scale(pygame.image.load("img/untitled-1.png"),(800,480))
pozadie = pygame.transform.scale(pygame.image.load("img/pozadie.png"),(800,480))
stone = pygame.transform.scale(pygame.image.load("img/Group2.png"),(813,400))

item1 = pygame.transform.scale(pygame.image.load(fruit[0]),(fruitWidth,fruitLenght))
item2 = pygame.transform.scale(pygame.image.load(fruit[1]),(fruitWidth,fruitLenght))
item3 = pygame.transform.scale(pygame.image.load(fruit[2]),(fruitWidth,fruitLenght))
item4 = pygame.transform.scale(pygame.image.load(fruit[3]),(fruitWidth,fruitLenght))
item5 = pygame.transform.scale(pygame.image.load(fruit[4]),(fruitWidth,fruitLenght))
item6 = pygame.transform.scale(pygame.image.load(fruit[5]),(fruitWidth,fruitLenght))
item7 = pygame.transform.scale(pygame.image.load(fruit[6]),(fruitWidth,fruitLenght))

items = [item1,item2,item3,item4,item5,item6,item7]




_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, color1, color2,surface, opx=2):
    textsurface = font.render(text, True, color1).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, color2).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    if (surface):
        return surf
    else:
        return textsurface




linesUrl = ["img/cara_1.png","img/cara_2.png","img/cara_3.png","img/cara_4.png","img/cara_5.png","img/cara_6.png","img/cara_7.png","img/cara_8.png","img/cara_9.png"]

class LinesClass:
    def __init__(self, img, position_x, position_y):
        # Initialize the class with image, and x, y positions
        self.image = pygame.image.load(img)
        self.position_x = position_x
        self.position_y = position_y

    def draw(self, surface):
        # Draw the image on the given surface at the specified position
        surface.blit(self.image, (self.position_x, self.position_y))

line1 = LinesClass(linesUrl[8],72,236)
line2 = LinesClass(linesUrl[7],72,136)
line3 = LinesClass(linesUrl[1],72,336)
line4 = LinesClass(linesUrl[5],72,68)
line5 = LinesClass(linesUrl[6],72,119)
line6 = LinesClass(linesUrl[0],72,103)
line7 = LinesClass(linesUrl[4],72,103)
line8 = LinesClass(linesUrl[2],72,122)
line9 = LinesClass(linesUrl[3],72,122)

linesComp = [line1,line2,line3,line4,line5,line6,line7,line8,line9]




def showStats():
    screen.blit(overlay, (0,0))
    betText = font2.render(f"BET: {bet}         LINES: {lines}         POINTS:{point}", True, (255, 255, 255))  
    screen.blit(betText, (50 ,430 ))




def checkLines(rows,surx2,sury2,surc2,surv2,surb2,line):
    global winSum
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
                                        
        # pygame.draw.rect(screen, (255,255,255), pygame.Rect(100, 230, 600, 20))
        screen.blit(line.image, (line.position_x,line.position_y))


        showStats()
        
        if (rows[2][surc2]==rows[3][4]):

            if(rows[3][surv2]==rows[4][surb2]):
                winSum = winSum+50*bet*multiply
            else:
                winSum = winSum+25*bet*multiply
        else: 
            winSum = winSum+5*bet*multiply




def spin():
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    # fill the screen with a color to wipe away anything from last frame
    global point
    global rows
    global posy
    global winSum
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
            showStats()


            
        if (speeds[4] < 1):
            global spinned
            spinned = False
            print(rows[0][0])

            print(items[0])
            print(f"{res1}, {res2}, {res3}, {res4}")      
            if (lines >= 1):  
                checkLines(rows,4,2,0,5,3,line1)
            if (lines >= 3):  
                checkLines(rows,3,1,6,4,2,line2)
                checkLines(rows,5,3,1,6,4,line3)

            if (lines >= 5):  
                checkLines(rows,3,2,1,5,2,line4)
                checkLines(rows,5,2,6,5,4,line5)

            if (lines >= 7):  
                checkLines(rows,3,1,0,6,4,line6)
                checkLines(rows,5,3,0,4,2,line7)

            if (lines >= 9):  
                checkLines(rows,4,1,0,6,3,line8)
                checkLines(rows,4,3,0,4,3,line9)
            if(winSum > 0):
                point = point + winSum
                font = pygame.font.Font(None, 80)  
                fontRend = render(f"VYHRA: {winSum}", font,WHITE,BLACK,0)
                fontText = render(f"VYHRA: {winSum}", font,WHITE,BLACK,1) 
                screen.blit(fontText, (800 // 2 - fontRend.get_width() // 2,480 // 2 - fontRend.get_height() // 2))
                winSum = 0



            
            print("test")
            break
        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen

        print(point)
        pygame.display.flip()
    

    clock.tick(60)   # limits FPS to 60
while running:
    user = ""
    while(user == ""):
        # user = "fabo"
        screen.blit(pozadie, (0,0))

        font = pygame.font.Font(None, 72)  
        fontRend = render('Prilozte svoje kartu', font,WHITE,BLACK,0)
        screen.blit(render('Prilozte svoje kartu', font,WHITE,BLACK,1), (800 // 2 - fontRend.get_width() // 2,480 // 2 - fontRend.get_height() // 2))
        # uvodText = font.render("Prilozte svoje kartu", True, (255, 255, 255))  
        
        # screen.blit(uvodText, (800 // 2 - uvodText.get_width() // 2,480 // 2 - uvodText.get_height() // 2))
        pygame.display.flip()
        user = input()
    

    mydb = mysql.connector.connect(host="localhost", user="root", password="",database="gamba")
    mycursor = mydb.cursor()
    mycursor.execute(f"select *from body where user = '{user}'")
    result = mycursor.fetchone()
    for i in result:
        print(i)
    point = result[3]   

    screen.blit(stone, (-7,47)) 
    showStats()
    font = pygame.font.Font(None, 36)  

    # text_with_border("VYHRA:dssdassadas", font, WHITE, GREEN, 10)


    while running and (user != ""):
        if (spinned == False):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mycursor.execute(f"UPDATE body SET point = {point} WHERE user = '{user}'")
                    mydb.commit()
                    # running = False
                    user = ""

                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_SPACE) : 
                        if(point >= bet*lines):
                            print (spinned)
                            spinned = True
                            spin()
                            # screen.blit(betText, (800 // 2 - betText.get_width() // 2,440  - betText.get_height() // 2))
                            pygame.display.flip()
                        else:
                            font = pygame.font.Font(None, 36)
                            uvodText = font.render("Nemate dost bodov na spin", True, (255, 255, 255))
                            screen.blit(uvodText, (800 // 2 - uvodText.get_width() // 2,480 // 2 - uvodText.get_height() // 2))
                            pygame.display.flip()
        
                            # mycursor.execute(f"UPDATE body SET point = {point} WHERE user = '{user}'")
                            # mydb.commit()
                            # user = ""
                    if event.key ==pygame.K_LEFT:
                        if (bet > 50):
                             bet = bet - 50
                        print(bet)
                        showStats()
                    if event.key == pygame.K_RIGHT:
                        if (bet < 1000):
                            bet = bet + 50
                        print(bet)
                        showStats()
                    if event.key ==pygame.K_a:
                        if (lines > 1):
                            lines = lines-2
                        screen.blit(stone, (-7,47)) 
                        if (posy != []):
                            for x in range(0,5):
                                for i in range(0,14):    # RENDER YOUR GAME HERE
                                    img = rows[x][i%7] 
                                    screen.blit(img, (posx+130*x,posy[x]+i*100-1010))
                        showStats()
                        for i in range(lines):
                            print (i)
                            screen.blit(linesComp[i].image, (linesComp[i].position_x,linesComp[i].position_y))

                    if event.key == pygame.K_d:
                        if (lines < 9):
                            lines = lines+2
                        showStats()

                        for i in range(lines):
                            screen.blit(linesComp[i].image, (linesComp[i].position_x,linesComp[i].position_y))
                            
                # if  event.type == pygame.MOUSEBUTTONDOWN:
                #     pos = pygame.mouse.get_pos()
                    # if button.is_hover(pos):
                    #     spin()
        # button.draw(screen)
        pygame.display.flip()
    if (point <= 0):
        screen.fill("red")
        font = pygame.font.Font(None, 36)  
        uvodText = font.render("Nemate ziadne body", True, (255, 255, 255))  
        screen.blit(uvodText, (800 // 2 - uvodText.get_width() // 2,480 // 2 - uvodText.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(5000)


pygame.quit()