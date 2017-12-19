import sys,math,random,time,pygame,socket,json
from pygame.locals import *
FPS=30
WINWIDTH=640
WINHEIGHT=480
HALF_WINWIDTH= int(WINWIDTH/2)
HALF_WINHEIGHT= int(WINHEIGHT/2)
NUMGRASS=80
NUMROCKS=10
GRASSCOLOR=(34,224,57)
WHITE=(255,255,255)
RED=(255,0,0)
BLUE=(0,162,232)

NUMICECUBES=5
FREEZETIME=3
CAMERASLACK=90
MOVERATE=9
BOUNCERATE=6
BOUNCEHEIGHT=30
STARTSIZE=50
WINSIZE=350
INVULTIME=2
GAMEOVERTIME=4
SLOWTIME=8
MAXHEALTH=3
NUMGRASS=80
NUMHEART=2
NUMDRINKS=2
NUMBANANAS=7
NUMSQUIRRELS=40
SQUIRRELMINSPEED=3
SQUIRRELMAXSPEED=7
DIRCHANGEFREQ=2
LEFT='left'
RIGHT='right'

def main():
    global DISPLAYSURF,FPSCLOCK,BASICFONT,GRASSIMAGES,ROCKIMAGES,L_SQUIR_IMG,R_SQUIR_IMG,HEART_IMG,PL_IMG,PR_IMG,DRINK_IMG,BANANA_IMG,ICECUBE,s, SCORE,FONT2
    pygame.init()
    GRASSIMAGES = []
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12345                # Reserve a port for your service.

    s.connect((host, port))
     
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('gameicon.png'))
    DISPLAYSURF=pygame.display.set_mode((WINWIDTH,WINHEIGHT),RESIZABLE)
    pygame.display.set_caption('Client 1')
    BASICFONT= pygame.font.Font('freesansbold.ttf',32)
    FONT2= pygame.font.Font('freesansbold.ttf',28)
    HEART_IMG=pygame.image.load('heart.png')
    DRINK_IMG=pygame.image.load('drink.png')
    BANANA_IMG=pygame.image.load('banana.png')
    L_SQUIR_IMG=pygame.image.load('minion.png')
    ICECUBE=pygame.image.load('iceCube.png')
    R_SQUIR_IMG=pygame.transform.flip(L_SQUIR_IMG,True,False)
    PL_IMG=pygame.image.load('pminion.png')
    PR_IMG=pygame.transform.flip(PL_IMG,True,False)
    SCORE=0
  
    ROCKIMAGES=[]
    for i in range(1,4):
        ROCKIMAGES.append(pygame.image.load('rock%s.png' %i))
    for i in range(1,5):
        GRASSIMAGES.append(pygame.image.load('grass%s.png' % i))
        
    while True:
        runGame()

def runGame():

    global DISPLAYSURF,WINWIDTH,WINHEIGHT,HALF_WINWIDTH,HALF_WINHEIGHT,SCORE,s
    playerScore=""
    camerax=0
    cameray=0
    gameOverMode=False
    gameOverStartTime=0
    invulnerableMode=False
    invulnerableStartTime=0
    slowMode=True
    slowModeStartTime=0
    winMode=False
    gameOverSurf1=BASICFONT.render('You Lose',True,WHITE)
    gameOverRect1=gameOverSurf1.get_rect()

    gameOverSurf2=BASICFONT.render('You Win',True,WHITE)
    gameOverRect2=gameOverSurf2.get_rect()

    winSurf=BASICFONT.render('You have reached OMEGA MINION!!',True,WHITE)
    winRect=winSurf.get_rect()
    winRect.center=(HALF_WINWIDTH,HALF_WINHEIGHT)

    winSurf2=BASICFONT.render('(Press r to restart)',True,WHITE)
    winRect2=winSurf2.get_rect()
    winRect2.center=(HALF_WINWIDTH,HALF_WINHEIGHT +30)

    freezeMode=False
    freezeStartTime=0
    currentTime=120-1
    
    freezeSurf=BASICFONT.render('FREEZED',True,WHITE)
    freezeRect=freezeSurf.get_rect()
    

    moveRight=False
    moveLeft=False
    moveUp=False
    moveDown=False
    
    heartObjs=[]
    grassObjs=[]
    rockObjs=[]
    squirrelObjs=[]
    drinkObjs=[]
    bananaObjs=[]
    iceObjs=[]
    playerObj={'surface':pygame.transform.scale(PL_IMG,(STARTSIZE,STARTSIZE)),
               'facing': LEFT,
               'size': STARTSIZE,
               'x': HALF_WINWIDTH,
               'y': HALF_WINHEIGHT,
               'bounce':0,
               'health': MAXHEALTH,
               'score':0
               }

    scoreSurf=BASICFONT.render(playerObj['score'],True,WHITE)
    scoreRect=scoreSurf.get_rect()
    scoreRect.center=(HALF_WINWIDTH,HALF_WINHEIGHT)
    
    for i in range(10):
        grassObjs.append(makeNewGrass(camerax,cameray))
        grassObjs[i]['x'] = random.randint(0, WINWIDTH)
        grassObjs[i]['y'] = random.randint(0, WINHEIGHT)
    for i in range(10):
        rockObjs.append(makeNewRock(camerax,cameray))
        rockObjs[i]['x'] = random.randint(0,WINWIDTH)
        rockObjs[i]['y'] = random.randint(0,WINHEIGHT)
    

    while True:
       
       
               
        if invulnerableMode and time.time()-invulnerableStartTime>INVULTIME:
            invulnerableMode=False

        if freezeMode and time.time()-freezeStartTime>FREEZETIME:
            freezeMode=False
            currentTime=120-1
            """if playerObj['facing']=='left':
                playerObj['surface']=pygame.transform.scale(L_SQUIR_IMG,(playerObj['size'],playerObj['size']))
            else:
                playerObj['surface']=pygame.transform.scale(R_SQUIR_IMG,(playerObj['size'],playerObj['size']))"""

        if slowMode and time.time()-slowModeStartTime>SLOWTIME:
            slowMode=False

        if slowMode:
             for sObj in squirrelObjs:
                if sObj['movex']>0 :
                    sObj['x']+=1
                    sObj['y']+=1
                    sObj['bounce']+=1
                    if sObj['bounce']>sObj['bouncerate']:
                        sObj['bounce']=0
                    
                else:
                    sObj['x']-=1
                    sObj['y']-=1
                    sObj['bounce']+=1
                    if sObj['bounce']>sObj['bouncerate']:
                        sObj['bounce']=0
                    
        else:
            for sObj in squirrelObjs:
                sObj['x']+=sObj['movex']
                sObj['y']+=sObj['movey']
                sObj['bounce']+=1
                if sObj['bounce']>sObj['bouncerate']:
                    sObj['bounce']=0
                if random.randint(0,99)<DIRCHANGEFREQ:
                    sObj['movex']=getRandomVelocity()
                    sObj['movey']=getRandomVelocity()
                    if sObj['movex']<0:
                        sObj['surface']=pygame.transform.scale(L_SQUIR_IMG,(sObj['width'],sObj['height']))
                    else:
                        sObj['surface']=pygame.transform.scale(R_SQUIR_IMG,(sObj['width'],sObj['height']))    
                

        for i in range(len(grassObjs)-1,-1,-1):
            if isOutsideActiveArea(camerax,cameray,grassObjs[i]):
                del grassObjs[i]
        for i in range(len(rockObjs)-1,-1,-1):
            if isOutsideActiveArea(camerax,cameray,rockObjs[i]):
                del rockObjs[i]
        for i in range(len(squirrelObjs)-1,-1,-1):
            if isOutsideActiveArea(camerax,cameray,squirrelObjs[i]):
                del squirrelObjs[i]
        for i in range(len(heartObjs)-1,-1,-1):
            if isOutsideActiveArea(camerax,cameray,heartObjs[i]):
                del heartObjs[i]
        for i in range(len(drinkObjs)-1,-1,-1):
            if isOutsideActiveArea(camerax,cameray,drinkObjs[i]):
                del drinkObjs[i]
        for i in range(len(bananaObjs)-1,-1,-1):
            if isOutsideActiveArea(camerax,cameray,bananaObjs[i]):
                del bananaObjs[i]
       
        while len(squirrelObjs)<NUMSQUIRRELS:
            squirrelObjs.append(makeNewSquirrel(camerax,cameray))
        while len(rockObjs)<NUMROCKS:
            rockObjs.append(makeNewRock(camerax,cameray))
        while len(grassObjs)<NUMGRASS:
            grassObjs.append(makeNewGrass(camerax,cameray))
        while len(heartObjs)<NUMHEART:
            heartObjs.append(makeNewHeart(camerax,cameray))
        while len(drinkObjs)<NUMDRINKS:
            drinkObjs.append(makeNewDrink(camerax,cameray))
        while len(bananaObjs)<NUMBANANAS:
            bananaObjs.append(makeNewBanana(camerax,cameray))
        
        

        playerCenterx=playerObj['x']+ int(playerObj['size']/2)
        playerCentery=playerObj['y']+ int(playerObj['size']/2)

        if (camerax+HALF_WINWIDTH)-playerCenterx>CAMERASLACK:
            camerax=playerCenterx+CAMERASLACK-HALF_WINWIDTH
        elif playerCenterx - (camerax+HALF_WINWIDTH):
            camerax= playerCenterx-CAMERASLACK-HALF_WINWIDTH
        if(cameray + HALF_WINHEIGHT)-playerCentery>CAMERASLACK:
            cameray=playerCentery+CAMERASLACK-HALF_WINHEIGHT
        elif playerCentery - (cameray + HALF_WINHEIGHT)>CAMERASLACK:
            cameray=playerCentery-CAMERASLACK-HALF_WINHEIGHT
            
        DISPLAYSURF.fill(GRASSCOLOR)
        
                    


        for gObj in grassObjs:
            gRect=pygame.Rect((gObj['x']-camerax,gObj['y']-cameray,gObj['width'],gObj['height']))
            DISPLAYSURF.blit(GRASSIMAGES[gObj['grassImage']],gRect)


        for rObj in rockObjs:
            rObj['rect']=pygame.Rect((rObj['x']-camerax,rObj['y']-cameray,rObj['width'],rObj['height']))
            DISPLAYSURF.blit(ROCKIMAGES[rObj['rockImage']],rObj['rect'])
        
        
            
        for hObj in heartObjs:
            hObj['rect']=pygame.Rect((hObj['x']-camerax,hObj['y']-cameray,hObj['width'],hObj['height']))
            DISPLAYSURF.blit(hObj['surface'],hObj['rect'])

        for dObj in drinkObjs:
            dObj['rect']=pygame.Rect((dObj['x']-camerax,dObj['y']-cameray,dObj['width'],dObj['height']))
            DISPLAYSURF.blit(dObj['surface'],dObj['rect'])

        for bObj in bananaObjs:
            bObj['rect']=pygame.Rect((bObj['x']-camerax,bObj['y']-cameray,bObj['width'],bObj['height']))
            DISPLAYSURF.blit(bObj['surface'],bObj['rect'])
        
        for sObj in squirrelObjs:
            sObj['rect']=pygame.Rect((sObj['x']-camerax,sObj['y']-cameray-getBounceAmount(sObj['bounce'],sObj['bouncerate'],sObj['bounceheight']),sObj['width'],sObj['height']))
            DISPLAYSURF.blit(sObj['surface'],sObj['rect'])

        
    
        

        flashIsOn=round(time.time(),1)*10%2==1
        if not gameOverMode and not(invulnerableMode and flashIsOn):
            playerObj['rect']=pygame.Rect((playerObj['x']-camerax,playerObj['y']-cameray-getBounceAmount(playerObj['bounce'],BOUNCERATE,BOUNCEHEIGHT),playerObj['size'],playerObj['size']))
            DISPLAYSURF.blit(playerObj['surface'],playerObj['rect'])
          

        drawHealthMeter(playerObj['health'])
        scoreSurf=BASICFONT.render("You: " +str(playerObj['score']),True,WHITE)
        scoreRect=scoreSurf.get_rect()
        scoreRect.center=(WINWIDTH-100,20)
        DISPLAYSURF.blit(scoreSurf,scoreRect)

        other=playerScore
        s.send(str(playerObj['score']))
        playerScore=s.recv(1024)
        if playerScore == "over":
            gameOverMode=True
        score2Surf=BASICFONT.render("Other: " +playerScore,True,WHITE)
        score2Rect=score2Surf.get_rect()
        score2Rect.center=(WINWIDTH-100,60)
        DISPLAYSURF.blit(score2Surf,score2Rect)
        print playerScore
            
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            
            elif event.type==KEYDOWN and not freezeMode:
                if event.key in (K_UP,K_w):
                    moveUp=True
                    moveDown=False
                elif event.key in (K_DOWN,K_s):
                    moveUp=False
                    moveDown=True
                if event.key in (K_RIGHT,K_d):
                    moveRight=True
                    moveLeft=False
                    if playerObj['facing']==LEFT:
                        playerObj['facing']=RIGHT
                        playerObj['surface']=pygame.transform.scale(PR_IMG,(playerObj['size'],playerObj['size']))
                elif event.key in (K_LEFT,K_a):
                    moveLeft=True
                    moveRight=False
                    if playerObj['facing']==RIGHT:
                        playerObj['facing']=LEFT
                        playerObj['surface']=pygame.transform.scale(PL_IMG,(playerObj['size'],playerObj['size']))
                if event.key == K_r and winMode:
                    return
            elif event.type==KEYUP:
                if event.key in (K_UP,K_w):
                    moveUp=False
                elif event.key in (K_DOWN,K_s):
                    moveDown=False
                if event.key in (K_RIGHT,K_d):
                    moveRight=False
                elif event.key in (K_LEFT,K_a):
                    moveLeft=False
                if event.key==K_ESCAPE:
                    terminate()
            elif event.type==VIDEORESIZE:
                DISPLAYSURF=pygame.display.set_mode(event.dict['size'],HWSURFACE| DOUBLEBUF|RESIZABLE)
                WINWIDTH,WINHEIGHT=DISPLAYSURF.get_size()
                HALF_WINWIDTH=int(WINWIDTH/2)
                HALF_WINHEIGHT=int(WINHEIGHT/2)
                playerObj['rect']=pygame.Rect((playerObj['x']-camerax,playerObj['y']-cameray-getBounceAmount(playerObj['bounce'],BOUNCERATE,BOUNCEHEIGHT),playerObj['size'],playerObj['size']))
                
        if not gameOverMode:
            if moveLeft:
                playerObj['x']-=MOVERATE
            elif moveRight:
                playerObj['x']+=MOVERATE
            if moveUp:
                playerObj['y']-=MOVERATE
            elif moveDown:
                playerObj['y']+=MOVERATE

            if ((moveLeft or moveRight or moveUp or moveDown) or playerObj['bounce']!=0) and not freezeMode:
                playerObj['bounce']+=1
            if playerObj['bounce']>BOUNCERATE:
                playerObj['bounce'] = 0

            for i in range(len(heartObjs)-1,-1,-1):
                if playerObj['rect'].colliderect(heartObjs[i]['rect']) and not winMode:
                    if playerObj['health']<3:
                        playerObj['health']+=1
                    del heartObjs[i]
                    
            for i in range(len(bananaObjs)-1,-1,-1):
                if playerObj['rect'].colliderect(bananaObjs[i]['rect']) and not winMode:
                    playerObj['score']+=1
                    del bananaObjs[i]

            for i in range(len(squirrelObjs)-1,-1,-1):
                if playerObj['rect'].colliderect(squirrelObjs[i]['rect']) and not winMode:
                    if squirrelObjs[i]['width']*squirrelObjs[i]['height']<=playerObj['size']**2:
                        playerObj['size']+=int((squirrelObjs[i]['height']*squirrelObjs[i]['width'])**0.2)+1
                        del squirrelObjs[i]
                        if playerObj['facing']==RIGHT:
                            playerObj['surface']=pygame.transform.scale(PR_IMG,(playerObj['size'],playerObj['size']))
                        elif playerObj['facing']==LEFT:
                            playerObj['surface']=pygame.transform.scale(PL_IMG,(playerObj['size'],playerObj['size']))

                    elif not invulnerableMode:
                        invulnerableMode=True
                        invulnerableStartTime=time.time()
                        playerObj['health']=playerObj['health']-1
                        if playerObj['health']==0:
                            gameOverMode=True
                            gameOverStartTime=time.time()

            for i in range(len(rockObjs)-1,-1,-1):
                if playerObj['rect'].colliderect(rockObjs[i]['rect']) and not invulnerableMode and not winMode:
                    playerObj['health']-=1
                    invulnerableMode=True
                    invulnerableStartTime=time.time()
                    if playerObj['health']==0:
                          gameOverMode=True
                          gameOverStartTime=time.time()

            for i in range(len(drinkObjs)-1,-1,-1):
                if playerObj['rect'].colliderect(drinkObjs[i]['rect']):
                    slowMode=True
                    slowModeStartTime=time.time()
                    del drinkObjs[i]
                              
        else:
            gameOverRect1.center=(HALF_WINWIDTH,HALF_WINHEIGHT)
            gameOverRect2.center=(HALF_WINWIDTH,HALF_WINHEIGHT)
            s.send("over")
            if(int(other)>playerObj['score']): 
                DISPLAYSURF.blit(gameOverSurf1,gameOverRect1)
            else:
                DISPLAYSURF.blit(gameOverSurf2,gameOverRect2)
            if time.time()-gameOverStartTime>GAMEOVERTIME:
                s.send("okay")
                return

        if freezeMode and not gameOverMode:
            freezeRect.center=(HALF_WINWIDTH,HALF_WINHEIGHT)
            DISPLAYSURF.blit(freezeSurf,freezeRect)
            temp=(int)(currentTime/30)
            drawMeter(temp)
            currentTime-=1
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeNewGrass(camerax,cameray):
        gr={}
        gr['grassImage']=random.randint(0,len(GRASSIMAGES)-1)
        gr['width']=GRASSIMAGES[0].get_width()
        gr['height']=GRASSIMAGES[0].get_height()
        gr['x'],gr['y']=getRandomOffCameraPos(camerax,cameray,gr['width'],gr['height'])
        gr['rect']=pygame.Rect((gr['x'],gr['y'],gr['width'],gr['height']))
        return gr

def drawMeter(currentTime):
    for i in range(currentTime):
        pygame.draw.rect(DISPLAYSURF,BLUE,(50,5+(MAXHEALTH-i)*10,20,10))
    for i in range(MAXHEALTH):
        pygame.draw.rect(DISPLAYSURF,WHITE,(50,5+(MAXHEALTH-i)*10,20,10),2)

def getRandomOffCameraPos(camerax,cameray,objWidth,objHeight):
    WINWIDTH,WINHEIGHT=DISPLAYSURF.get_size()
    cameraRect=pygame.Rect(camerax,cameray,WINWIDTH,WINHEIGHT)
    while True:
        x=random.randint(camerax-WINWIDTH,camerax+(2*WINWIDTH))
        y=random.randint(cameray-WINHEIGHT,cameray+(2*WINHEIGHT))
        objRect=pygame.Rect(x,y,objWidth,objHeight)
        if not objRect.colliderect(cameraRect):
            return x,y

def makeNewHeart(camerax,cameray):
    heart={}
    heart['width']=25
    heart['height']=25
    heart['x'],heart['y']=getRandomOffCameraPos(camerax,cameray,heart['width'],heart['height'])
    heart['surface']=pygame.transform.scale(HEART_IMG,(heart['width'],heart['height']))
    return heart

def makeNewBanana(camerax,cameray):
    banana={}
    banana['width']=25
    banana['height']=25
    banana['x'],banana['y']=getRandomOffCameraPos(camerax,cameray,banana['width'],banana['height'])
    banana['surface']=pygame.transform.scale(BANANA_IMG,(banana['width'],banana['height']))
    return banana

def makeNewDrink(camerax,cameray):
    drink={}
    drink['width']=30
    drink['height']=30
    drink['x'],drink['y']=getRandomOffCameraPos(camerax,cameray,drink['width'],drink['height'])
    drink['surface']=pygame.transform.scale(DRINK_IMG,(drink['width'],drink['height']))
    return drink
                          
def makeNewRock(camerax,cameray):
    rock={}
    rock['width']=30
    rock['height']=30
    rock['x'],rock['y']=getRandomOffCameraPos(camerax,cameray,rock['width'],rock['height'])
    rock['rockImage']=random.randint(0,len(ROCKIMAGES)-1)
    rock['rect']=pygame.Rect((rock['x'],rock['y'],rock['width'],rock['height']))                       
    return rock
    
    
def makeNewSquirrel(camerax,cameray):
    sq={}
    generalSize=random.randint(10,103)
    multiplier=random.randint(1,3)
    sq['width']=(generalSize+random.randint(0,10))*multiplier
    sq['height']=(generalSize+random.randint(0,10))*multiplier
    sq['x'],sq['y']=getRandomOffCameraPos(camerax,cameray,sq['width'],sq['height'])
    sq['movex']=getRandomVelocity()
    sq['movey']=getRandomVelocity()
    if sq['movex']<0:
        sq['surface']=pygame.transform.scale(L_SQUIR_IMG,(sq['width'],sq['height']))
    else:
        sq['surface']=pygame.transform.scale(R_SQUIR_IMG,(sq['width'],sq['height']))
    sq['bounce']=0
    sq['bouncerate']=random.randint(10,18)
    sq['bounceheight']=random.randint(10,50)
    return sq

def getRandomVelocity():
    speed=random.randint(SQUIRRELMINSPEED,SQUIRRELMAXSPEED)
    if random.randint(0,1)==0:
        return speed
    else:
        return -speed

def getBounceAmount(currentBounce,bounceRate,bounceHeight):
    return int(math.sin((math.pi/float(bounceRate))*currentBounce)*bounceHeight)

def terminate():
    pygame.quit()
    sys.exit()

def isOutsideActiveArea(camerax,cameray,obj):
    boundsLeftEdge=camerax-WINWIDTH
    boundsTopEdge=cameray-WINHEIGHT
    boundsRect=pygame.Rect(boundsLeftEdge,boundsTopEdge,3*WINWIDTH,3*WINHEIGHT)
    objRect=pygame.Rect(obj['x'],obj['y'],obj['width'],obj['height'])
    return not boundsRect.colliderect(objRect)

def drawHealthMeter(health):
    for i in range(health):
        pygame.draw.rect(DISPLAYSURF,RED,(15,5+(10*MAXHEALTH)-i*10,20,10))
    for i in range(MAXHEALTH):
        pygame.draw.rect(DISPLAYSURF,WHITE,(15,5+(10*MAXHEALTH)-i*10,20,10),1)

def makeNewIce(camerax,cameray):
    ice={}
    ice['width']=25
    ice['height']=25
    WINWIDTH,WINHEIGHT=DISPLAYSURF.get_size()
    cameraRect=pygame.Rect(camerax,cameray,WINWIDTH,WINHEIGHT)
    while True:
        ice['x']=random.randint(camerax-WINWIDTH,cameray+2*WINWIDTH)
        ice['y']=random.randint(cameray-WINHEIGHT,cameray+2*WINHEIGHT)
        objRect=pygame.Rect(ice['x'],ice['y'],ice['width'],ice['height'])
        if not objRect.colliderect(cameraRect):
            break
    ice['rect']=pygame.Rect(ice['x'],ice['y'],ice['width'],ice['height'])
    return ice

if __name__ == '__main__':
    main()
