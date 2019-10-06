import pew
import random
pew.init()

# Clean screen
screen = pew.Pix.from_iter(((0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),))

# Starting position
x=4 
y=4 

#keys
up=False
down=False
left=False
right=False
deactivate=False

keyCycle=10 # Delay between key inputs
keyCycleIndex=10 # Starting with no delay
loop=0

# Bombs arrays
bombposx=[]
bombposy=[]
bombposcycle=[]

# GameOver and LevelSho screens
gameover=False
levelshow=False
waitGameover=100
waitlevels=100

# Starting level and bombs found
level=1
found=0

def placeBomb():
    #First let's check if there is a bomb already on the XY position
    tentativeX=random.randint(0,7)
    tentativeY=random.randint(0,7)
    xyfree=True
    for bi in range(1,len(bombposx)):
        if bombposx[bi-1]==tentativeX:
            if bombposy[bi-1]==tentativeY:
                xyfree=False
    if xyfree:
        bombposx.append(tentativeX)
        bombposy.append(tentativeY)
        bombposcycle.append(1)
        screen.pixel(tentativeX, tentativeY, 1)
        

def displayBombs():
    global gameover
    global screen
    for bi in range(0,len(bombposx)):
        bomblink=bombposcycle[bi-1] 
        if bomblink>100:
            bomblink=100
            gameover=True
        # Bomb blinking function     
        if loop%(int(100.0/bomblink*1.5)): # *3 defines the increase in the blinking speed
            screen.pixel(bombposx[bi-1], bombposy[bi-1], 0)
        else:
            screen.pixel(bombposx[bi-1], bombposy[bi-1], 1)
            bombposcycle[bi-1]=bombposcycle[bi-1]+1   

# Bomb deactivation function, deactivates the bomb in the place X/Y        
def deactivatef(xd,yd):
    global found,screen
    for bi in range(1,len(bombposx)):
        if bombposx[bi-1]==xd:
            if bombposy[bi-1]==yd:
                # Removes the bomb attributes
                bombposx.pop(bi-1)
                bombposy.pop(bi-1)
                bombposcycle.pop(bi-1)
                found=found+1
                # Fades a bit the player, to give some feedback during deactivation
                screen.pixel(xd, yd, 0)

while True:
    # Game Over Screen
    if gameover:
        # Resets variables
        level=1
        found=0
        bombposx=[]
        bombposy=[]
        bombposcycle=[]
        pew.tick(1/40) # Wait 2.5 secs
        # Sad game over face
        if waitGameover==100:            
            screen = pew.Pix.from_iter((
            (1, 1, 1, 1, 1, 1, 1, 1),
            (1, 3, 1, 1, 1, 1, 1, 3),
            (1, 1, 1, 1, 1, 1, 1, 1),
            (1, 1, 1, 1, 2, 1, 1, 1),
            (1, 1, 1, 1, 3, 1, 1, 1),
            (1, 1, 1, 1, 1, 1, 1, 1),
            (1, 1, 3, 3, 3, 3, 3, 1),
            (1, 3, 1, 1, 1, 1, 1, 3),))
            pew.show(screen)
        waitGameover=waitGameover-1

        # Clears screen
        if waitGameover<0:
            gameover=False
            screen = pew.Pix.from_iter(((0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),))
            levelshow=True
    # Levels screen        
    if levelshow:
        pew.tick(1/30)
        #This algorith draws the "levels tringle", highlighting the current level
        it=0
        for x in range(0,8):
            it=it+1
            for y in range(0,it):
                if level==it+1:
                    screen.pixel(x, 7-y, 3) # Highlight current level
                else:
                    screen.pixel(x, 7-y, 1)
                

            pew.show(screen)
            waitlevels=waitlevels-1
            if waitlevels<0:
                levelshow=False
                screen = pew.Pix.from_iter(((0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0),))
                x=4
                y=4
                bombposx=[]
                bombposy=[]
                bombposcycle=[]


    if not gameover and not levelshow:
        # Cycles to wait to clear the screens
        waitGameover=100
        waitlevels=100
        # Saves position to delete the old pixel
        old_x=x
        old_y=y     
        
        # Key detection
        keys = pew.keys() 
        if keyCycleIndex>keyCycle:
            if keys & pew.K_UP:
                up=True
            elif keys & pew.K_DOWN:
                down=True
            elif keys & pew.K_LEFT:
                left=True
            elif keys & pew.K_RIGHT:
                right=True
            elif keys & pew.K_O:
                deactivate=True
            elif keys & pew.K_X:
                deactivate=True

        # Movement controllers logic
        if (up):
                y=y-1
                up=False
                keyCycleIndex=0

        if (down):
                y=y+1
                down=False
                keyCycleIndex=0
        if (left):
                x=x-1
                left=False
                keyCycleIndex=0
        if (right):
                x=x+1
                right=False
                keyCycleIndex=0
        
        keyCycleIndex=keyCycleIndex+1

        # Keep the player inside the screen limits
        if x>7:
            x=7
            screen.pixel(x, y, 1)
        if x<0:
            x=0
            screen.pixel(x, y, 1)
        if y>7:
            y=7
            screen.pixel(x, y, 1)
        if y<0:
            y=0
            screen.pixel(x, y, 1)   

        # Next level well all bombs found
        if found>level*level:
            found=0
            level=level+1
            levelshow=True

        # Paints all the bombs in the screen
        displayBombs()

        # The random placement algorithm, increases placing rate
        if random.randint(1,1000)>990-(level*2):
            placeBomb()

        # Player position
        screen.pixel(x, y, 3)

        # Deactivates bomb if deactivation pressed
        if (deactivate):
                deactivatef(x,y)
                deactivate=False

        pew.show(screen)

        # cleans previous player pixel
        screen.pixel(old_x, old_y, 0)

        # Constant frame reate
        pew.tick(1/64)
        loop=loop+1
