import pygame
import random
import mysql.connector
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

bet = 50
lines = 1
point = 0
winSum = 0
spinned = False

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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

class LinesClass:
    def __init__(self, img, position_x, position_y):
        self.image = pygame.image.load(img)
        self.position_x = position_x
        self.position_y = position_y

    def draw(self, surface):
        surface.blit(self.image, (self.position_x, self.position_y))

linesUrl = ["img/cara_1.png","img/cara_2.png","img/cara_3.png","img/cara_4.png","img/cara_5.png","img/cara_6.png","img/cara_7.png","img/cara_8.png","img/cara_9.png","img/cara_10.png","img/cara_11.png"]
line1 = LinesClass(linesUrl[8],72,236)
line2 = LinesClass(linesUrl[7],72,136)
line3 = LinesClass(linesUrl[1],72,336)
line4 = LinesClass(linesUrl[5],72,68)
line5 = LinesClass(linesUrl[6],72,119)
line6 = LinesClass(linesUrl[0],72,103)
line7 = LinesClass(linesUrl[4],72,103)
line8 = LinesClass(linesUrl[2],72,122)
line9 = LinesClass(linesUrl[3],72,122)
line10 = LinesClass(linesUrl[9],72,134)
line11 = LinesClass(linesUrl[10],72,134)

linesComp = [line1,line2,line3,line4,line5,line6,line7,line8,line9]

def showStats():
    screen.blit(overlay, (0,0))
    betText1 = font2.render(f"BET: {bet}", True, (255, 255, 255))  
    betText2 = font2.render(f"LINES: {lines}", True, (255, 255, 255))  
    betText3 = font2.render(f"POINTS: {point}", True, (255, 255, 255))  

    screen.blit(betText3, (40 ,430 ))
    screen.blit(betText1, (380 ,430 ))
    screen.blit(betText2, (620 ,430 ))


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
                                        
        screen.blit(line.image, (line.position_x,line.position_y))
        showStats()
        
        if (rows[2][surc2]==rows[3][4]):
            if(rows[3][surv2]==rows[4][surb2]):
                winSum = winSum+50*bet*multiply
            else:
                winSum = winSum+10*bet*multiply
        else: 
            winSum = winSum+5*bet*multiply

def spin():
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
    speed1 = 100
    speed2 = 125
    speed3 = 150
    speed4 = 200
    speed5 = 225
    speeds = [speed1,speed2,speed3,speed4,speed5]

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
                    posy[x] = posy[x]+40  
                    if(posy[x] > 800):
                        posy[x]=posy[x]-700
                    speeds[x]= speeds[x]-5


                for i in range(0,14):    
                    img = rows[x][i%7] 
                    screen.blit(img, (posx+130*x,posy[x]+i*100-1010))
            showStats()
            
        if (speeds[4] < 1):

            global spinned
            spinned = False

            if (lines >= 1):  
                checkLines(rows,4,2,0,5,3,line1)
            if (lines >= 3):  
                checkLines(rows,3,1,6,4,2,line2)
                checkLines(rows,5,3,1,6,4,line3)

            if (lines >= 5):  
                checkLines(rows,3,2,1,5,2,line4)
                checkLines(rows,5,2,6,5,4,line5)

            if (lines >= 7):  
                checkLines(rows,3,1,0,6,4,line10)
                checkLines(rows,5,3,0,4,2,line11)

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
                showStats()
                pygame.display.flip()
                pygame.time.wait(500)            
            break
        pygame.display.flip()
    

    clock.tick(60) 
while running:
    user = ""
    while(user == ""):
        screen.blit(pozadie, (0,0))

        font = pygame.font.Font(None, 72)  
        fontRend = render('Prilozte svoje kartu', font,WHITE,BLACK,0)
        screen.blit(render('Prilozte svoje kartu', font,WHITE,BLACK,1), (800 // 2 - fontRend.get_width() // 2,480 // 2 - fontRend.get_height() // 2))
       
        pygame.display.flip()
        id, text = reader.read()
        print(id)
        print(text)
        mydb = mysql.connector.connect(host="us.vybrat.eu", user="3ATVojar_pavian", password="Jcauq55Ua0",database="3ATVojar_pavian")
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT COUNT(*) FROM `body` WHERE user = '{text}'")
        result = mycursor.fetchone()
        mycursor.close()
        print(result[0])
        if result[0] == 1:
            user = text
        else:
            screen.blit(pozadie, (0,0))
            fontRend = render('Nespravna karta', font,WHITE,BLACK,0)
            screen.blit(render('Nespravna karta', font,WHITE,BLACK,1), (800 // 2 - fontRend.get_width() // 2,480 // 2 - fontRend.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(3000)

    GPIO.cleanup() 
    mydb = mysql.connector.connect(host="us.vybrat.eu", user="3ATVojar_pavian", password="Jcauq55Ua0",database="3ATVojar_pavian")
    mycursor = mydb.cursor()
    mycursor.execute(f"select *from body where user = '{user}'")
    result = mycursor.fetchone()
    for i in result:
        print(i)
    point = result[3]   
    mycursor.close()
    screen.blit(stone, (-7,47)) 
    font = pygame.font.Font(None, 36)  
    screen.blit(stone, (-7,47)) 
    row1 = random.sample(items, len(items))
    row2 = random.sample(items, len(items))
    row3 = random.sample(items, len(items))
    row4 = random.sample(items, len(items))
    row5 = random.sample(items, len(items))
    rows = [row1,row2,row3,row4,row5]
    posy = [800,300,800,300,800]
    for x in range(0,5):
        for i in range(0,14):    
            img = rows[x][i%7] 
            screen.blit(img, (posx+130*x,posy[x]+i*100-1010))

    showStats()
    while running and (user != "") and (point >= 50):
        if (spinned == False):
            GPIO.setmode(GPIO.BOARD) # 7 11 12 13
            GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            if GPIO.input(40) == GPIO.HIGH:
                if bet > 50:
                    bet -= 50
                    print(bet)
                    showStats()
                    pygame.time.delay(200)

            if GPIO.input(38) == GPIO.HIGH:
                if bet < 1000:
                    bet += 50
                    print(bet)
                    showStats()
                    pygame.time.delay(200)
            if GPIO.input(12) == GPIO.HIGH:
                if(point >= bet*lines):
                    print (spinned)
                    spinned = True
                    spin()
                    # screen.blit(betText, (800 // 2 - betText.get_width() // 2,440  - betText.get_height() // 2))
                    pygame.display.flip()
                    mydb = mysql.connector.connect(host="us.vybrat.eu", user="3ATVojar_pavian", password="Jcauq55Ua0",database="3ATVojar_pavian")
                    mycursor = mydb.cursor()     
                    mycursor.execute(f"UPDATE body SET point = {point} WHERE user = '{user}'")
                    mydb.commit()
                    mycursor.close()
                else:
                    if (point < 50):
                        user = ""
                        # font = pygame.font.Font(None, 36)
                        font = pygame.font.Font(None, 72)  
                        fontRend = render('Nemate dost bodov na spin', font,WHITE,BLACK,0)
                        screen.blit(render('Nemate dost bodov na spin', font,WHITE,BLACK,1), (800 // 2 - fontRend.get_width() // 2,480 // 2 - fontRend.get_height() // 2))
        
                        # uvodText = font.render("Nemate dost bodov na spin", True, (255, 255, 255))
                        # screen.blit(uvodText, (800 // 2 - uvodText.get_width() // 2,480 // 2 - uvodText.get_height() // 2))
                        pygame.display.flip()
                        mydb = mysql.connector.connect(host="us.vybrat.eu", user="3ATVojar_pavian", password="Jcauq55Ua0",database="3ATVojar_pavian")
                        mycursor = mydb.cursor()     
                        mycursor.execute(f"UPDATE body SET point = {point} WHERE user = '{user}'")
                        mydb.commit()
                        mycursor.close()
            if GPIO.input(7) == GPIO.HIGH: 
                if (lines > 1):
                    lines = lines-2
                screen.blit(stone, (-7,47)) 
                for x in range(0,5):
                    for i in range(0,14):    # RENDER YOUR GAME HERE
                        img = rows[x][i%7] 
                        screen.blit(img, (posx+130*x,posy[x]+i*100-1010))
                    print(posy)

                showStats()
                for i in range(lines):
                    print (i)
                    screen.blit(linesComp[i].image, (linesComp[i].position_x,linesComp[i].position_y))
                pygame.time.delay(200)                
            if GPIO.input(11) == GPIO.HIGH: 
                if (lines < 9):
                    lines = lines+2
                screen.blit(stone, (-7,47)) 
                for x in range(0,5):
                    for i in range(0,14):    # RENDER YOUR GAME HERE
                        img = rows[x][i%7] 
                        screen.blit(img, (posx+130*x,posy[x]+i*100-1010))
                showStats()
                for i in range(lines):
                    screen.blit(linesComp[i].image, (linesComp[i].position_x,linesComp[i].position_y))
                pygame.time.delay(200)                
            
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
                            if (point < 50):
                                user = ""
                            # font = pygame.font.Font(None, 36)
                            font = pygame.font.Font(None, 72)  
                            fontRend = render('Nemate dost bodov na spin', font,WHITE,BLACK,0)
                            screen.blit(render('Nemate dost bodov na spin', font,WHITE,BLACK,1), (800 // 2 - fontRend.get_width() // 2,480 // 2 - fontRend.get_height() // 2))
        
                            # uvodText = font.render("Nemate dost bodov na spin", True, (255, 255, 255))
                            # screen.blit(uvodText, (800 // 2 - uvodText.get_width() // 2,480 // 2 - uvodText.get_height() // 2))
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
                        for x in range(0,5):
                            for i in range(0,14):    # RENDER YOUR GAME HERE
                                img = rows[x][i%7] 
                                screen.blit(img, (posx+130*x,posy[x]+i*100-1010))
                            print(posy)

                        showStats()
                        for i in range(lines):
                            print (i)
                            screen.blit(linesComp[i].image, (linesComp[i].position_x,linesComp[i].position_y))

                    if event.key == pygame.K_d:
                        if (lines < 9):
                            lines = lines+2
                        screen.blit(stone, (-7,47)) 
                        for x in range(0,5):
                            for i in range(0,14):    # RENDER YOUR GAME HERE
                                img = rows[x][i%7] 
                                screen.blit(img, (posx+130*x,posy[x]+i*100-1010))
                        showStats()
                        for i in range(lines):
                            screen.blit(linesComp[i].image, (linesComp[i].position_x,linesComp[i].position_y))
                            
                # if  event.type == pygame.MOUSEBUTTONDOWN:
                #     pos = pygame.mouse.get_pos()
                    # if button.is_hover(pos):
                    #     spin()
        # button.draw(screen)
        pygame.display.flip()
    if (point <= 49):
        screen.blit(pozadie, (0,0))
        font = pygame.font.Font(None, 72)  
        fontRend = render('Nemate ziadne body', font,WHITE,BLACK,0)
        screen.blit(render('Nemate ziadne body', font,WHITE,BLACK,1), (800 // 2 - fontRend.get_width() // 2,480 // 2 - fontRend.get_height() // 2))
        
        pygame.display.flip()
        pygame.time.wait(5000)


pygame.quit()