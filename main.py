import pygame as pg
import random, pickle, math
pg.init()

#game screen size
screen_size=(800,600)

#frame rate
clock=pg.time.Clock()
#-----------------------------------------------------------------
def game():
    pg.init()

    #loading game images
    ball=pg.image.load("images/ball.png")
    aball=pg.image.load('images/ball armour.png')
    bg=pg.image.load('images/background.jpg')
    plank=pg.image.load('images/plank.png')
    hole=pg.image.load('images/hole.png')
    holelight=pg.image.load('images/hole light.png')
    coin=pg.image.load('images/coin.png')
    coinf=pg.image.load('images/coin faded.png')
    boost=pg.image.load('images/boost.png')
    pause=pg.image.load('images/pause.png')
    beam=pg.image.load('images/beam.png')
    laser=pg.image.load('images/laser icon.png')
    magnet=pg.image.load('images/magnet icon.png')
    replay=pg.image.load('images/replay.png')
    rcoin=pg.image.load('images/coin red.png')
    arm=pg.image.load('images/arm.png')
    boostf=pg.image.load('images/boost faded.png')
    magnetf=pg.image.load('images/magnet icon faded.png')
    armf=pg.image.load('images/arm faded.png')
    laserf=pg.image.load('images/laser icon faded.png')

    #changing size of the images
    bg=pg.transform.scale(bg,screen_size)
    ball=pg.transform.scale(ball,(70,70))
    aball=pg.transform.scale(aball, (70,70))
    plank=pg.transform.scale(plank,(800,100))
    hole=pg.transform.scale(hole, (120,50))
    holelight=pg.transform.scale(holelight, (120,50))
    coin=pg.transform.scale(coin, (30,30))
    coin2=pg.transform.scale(coin, (50,50))
    coin3=pg.transform.scale(coin, (256,256))
    boost=pg.transform.scale(boost, (100,100))
    laser=pg.transform.scale(laser, (100,100))
    pause=pg.transform.scale(pause, screen_size)
    beam=pg.transform.scale(beam, (70,600))
    magnet=pg.transform.scale(magnet, (100,100))
    replay=pg.transform.scale(replay, (200,200))
    arm=pg.transform.scale(arm,(100,100))
    boostf=pg.transform.scale(boostf, (100,100))
    magnetf=pg.transform.scale(magnetf, (100,100))
    laserf=pg.transform.scale(laserf, (100,100))
    armf=pg.transform.scale(armf, (100,100))
    coinf=pg.transform.scale(coinf, (50,50))
    
    #loading fonts
    TNR1=pg.font.SysFont("Times New Roman", 50)
    TNR2=pg.font.SysFont("Times New Roman", 200)
    TNR3=pg.font.SysFont("Times New Roman", 110)

    #text
    PETC=TNR1.render('Press enter to continue...', 1, (0,0,0)) #PETC-Press Enter To Continue
    PETE=TNR1.render('Press enter to exit...', 1, (0,0,0)) #PETC-Press Enter To Exit
    gameover=TNR3.render('Game over!', 1, (0,0,0))
    paused=TNR3.render('PAUSED!', 1, (255,255,255))
       
    #for tracking score
    scoreadder=1 #adds to score only when scoreadder==1
    score=0

    #initializes the screen
    screen=pg.display.set_mode(screen_size)
    pg.display.set_caption("Ball Drop")

    #pygame loop
    i=True

    #l for flag=6
    l=[]

    #iteration counter
    count=1

    #plank counter
    pcount=1

    #coin counter
    ccount=0
    c1adder=1
    c2adder=1
    c3adder=1

    #initial speed of the plank moving upwards
    speed=4
    factor=0
    #flag to control the game
    #flag -1: welcome screen
    #flag 0: normal game run
    #flag 1: stops game when ball crashes
    #flag 2: shows score
    #flag 3: quit screen
    #flag 4: laser
    #flag 5: pause screen
    #flag 6: boost
    #flag 7: exit screen
    flag=-1

    #initial x coordinate of the ball
    #it is half of the screen, ie 400 minus half the width of the ball
    x=365
    y=800

    #x coordinate for holes
    hole1=random.randint(100,280)
    hole2=random.randint(420,600)

    #x coordinate for coins
    x_c1=800
    x_c2=800
    x_c3=800
    #to display or not to display coins
    p1=0
    p2=0
    p3=0

    #for magnet
    mg=False
    mg_used=-30

    #required points for all 4
    m_pt=10
    b_pt=5
    l_pt=8
    a_pt=2
    #Number of levels it is active for
    m_level=7
    b_level=7
    l_level=11
    a_level=5
    #for playing again
    repeat=0
    #for shield
    armour=False
    armed=False
    a_used=-30
    #for bars when the powerup is active
    h_b=0
    h_m=0
    h_a=0
    h_l=0
    parts_b=100/b_level
    parts_m=100/m_level
    parts_a=100/a_level
    parts_l=100/l_level
    bar_b=False
    bar_m=False
    bar_a=False
    bar_l=False
    #for showing coins
    showcoins=False
    while i:
        #changes the colour of the coin
        if score==50:
            coin=pg.image.load('images/coin red.png')
            coin=pg.transform.scale(coin, (30,30))
        if score==100:
            coin=pg.image.load('images/coin green.png')
            coin=pg.transform.scale(coin, (30,30))
            
        if flag==-1:
            welcome=TNR3.render('WELCOME!', 1, (0,0,0))
            screen.blit(bg, (0,0))
            screen.blit(welcome, (90,200))
            screen.blit(PETC, (250,550))
            #necessary to allow the left and right arrow keys to be pressed
            #and keep repeating the event so the key can be pressed and held
            #instead of pressing it down again and again
            #the first argument is the initial delay on the first click, while
            #the second argument is the interval between the occurence of each
            #event, ie each time the ball moves even though the key is not pressed
            #again, both in milliseconds
            pg.key.set_repeat(10, 5)

        if flag==5: #pause screen
            screen.blit(pause, (0,0))
            screen.blit(paused, (180,175))
            
        if flag==4: #boost
            #text to be displayed on screen
            displayscore=TNR1.render(str(score), 1, (0,0,0))
            displaycoins=TNR1.render(str(ccount), 1, (0,0,0))
            if scoreadder==1:
                score+=1
                scoreadder=0
            factor=pcount/(0.5/40)
            y=800-factor
            screen.blit(bg, (0,0))
            screen.blit(ball, (x,100))
            screen.blit(plank, (0,y))
            screen.blit(hole, (hole1,y+30))
            screen.blit(hole, (hole2,y+30))
            screen.blit(ball,(x,100))
            screen.blit(displayscore, (399,0))
            screen.blit(coin2, (500,0))
            screen.blit(displaycoins, (555,0))

        if flag==6: #when laser is active
            bar_l=True
            fac=0 #resets factor for each point
            if len(l)>2:
                fac=l[len(l)-1]-l[0]+70 #finds how much of the background has to be shown on the blank            
            #text to be displayed on screen
            displayscore=TNR1.render(str(score), 1, (0,0,0))
            displaycoins=TNR1.render(str(ccount), 1, (0,0,0))
            if scoreadder==1:
                score+=1
                scoreadder=0
            factor=pcount/(0.5/20)
            y=800-factor
            screen.blit(bg, (0,0))
            screen.blit(plank, (0,y))
            screen.blit(hole, (hole1,y+30))
            screen.blit(hole, (hole2,y+30))
            #stores the positions where the laser has been used
            l+=[x]
            l.sort() #arranges them from lowest to highest
            #shows the background behind the cut area
            screen.blit(bg, (l[0],y), pg.Rect(l[0],y,fac,600))
            #shows the beam
            screen.blit(beam, (x,140))
            screen.blit(ball,(x,100))
            screen.blit(displayscore, (399,0))
            screen.blit(coin2, (500,0))
            screen.blit(displaycoins, (555,0))
     
        if flag==0: #normal game run
            #text to be displayed on screen
            displayscore=TNR1.render(str(score), 1, (0,0,0))
            displaycoins=TNR1.render(str(ccount), 1, (0,0,0))
            #factor decides how fast the plank moves and it depends on speed
            #as speed increases, factor increases
            factor=pcount/(0.5/speed)
            #y coordinate of plank
            #as factor increases, y coordinate decreases faster and faster
            y=800-factor
            if y-150>100 and y-150<170: #decides whether coin has been collected or not
                if x_c1>x-10 and x_c1<x+80 and p1:
                    if c1adder==1:
                        if score<50:
                            ccount+=1
                        if score>=50 and score<100:
                            ccount+=2
                        if score>=100:
                            ccount+=4
                        c1adder=0
                
            if y-300>100 and y-300<170:
                
                if x_c2 >x-10 and x_c2<x+80 and p2:
                    if c2adder==1:
                        if score<50:
                            ccount+=1
                        if score>=50 and score<100:
                            ccount+=2
                        if score>=100:
                            ccount+=4
                        c2adder=0
                
            if y-450>100 and y-450<170:
                
                if x_c3>x-10 and x_c3<x+80 and p3:
                    if c3adder==1:
                        if score<50:
                            ccount+=1
                        if score>=50 and score<100:
                            ccount+=2
                        if score>=100:
                            ccount+=4
                        c3adder=0

            #when ball is above plank
            if y+40>=150 and y+40<1000:
                screen.blit(bg,(0,0))
                
                screen.blit(plank,(0,y))
                screen.blit(hole, (hole1,y+30))
                screen.blit(hole, (hole2,y+30))
                
                screen.blit(ball,(x,100))
                screen.blit(displayscore, (399,0))
                #show coin only if it is not taken
                if y>590:
                    if c1adder==1 and p1:
                        screen.blit(coin, (x_c1, y-150))
                    if c2adder==1 and p2:
                        screen.blit(coin, (x_c2, y-300))
                    if c3adder==1 and p3:
                        screen.blit(coin, (x_c3, y-450))
                elif y>100:
                    if mg: #changes the coordinates of the coins when magnet is active
                        fc1=math.fabs(x+30-x_c1)/2
                        if x+30>x_c1 and x_c1!=800:
                            x_c1+=fc1
                        else:
                            x_c1-=fc1
                        fc2=math.fabs(x+30-x_c2)/2
                        if x+30>x_c2 and x_c2!=800:
                            x_c2+=fc2
                        else:
                            x_c2-=fc2
                        fc3=math.fabs(x+30-x_c3)
                        if x+30>x_c3 and x_c3!=800:
                            x_c3+=fc3
                        else:
                            x_c3-=fc3
                            
                    if c1adder==1 and p1:
                        screen.blit(coin, (x_c1, y-150))
                    if c2adder==1 and p2:
                        screen.blit(coin, (x_c2, y-300))
                    if c3adder==1 and p3:
                        screen.blit(coin, (x_c3, y-450))
                    
                screen.blit(coin2, (500,0))
                screen.blit(displaycoins, (555,0))
                
            if y+40<=100:
                #shows the ball, plank and background after the ball passes the hole
                screen.blit(bg,(0,0))
                screen.blit(ball,(x,100))
                screen.blit(plank,(0,y))
                screen.blit(hole, (hole1,y+30))
                screen.blit(hole, (hole2,y+30))
                screen.blit(displayscore, (399,0))
                #show coin only if it is not taken
                if c1adder==1:
                    screen.blit(coin, (x_c1, y-150))
                if c2adder==1:
                    screen.blit(coin, (x_c2, y-300))
                if c3adder==1:
                    screen.blit(coin, (x_c3, y-450))
                screen.blit(coin2, (500,0))
                screen.blit(displaycoins, (555,0))

            if y+40>100 and y+40<150: #while the ball is passing through the hole
                check_hole1=range(hole1,hole1+120-60) #120 is size of hole and 60 is width of ball
                check_hole2=range(hole2,hole2+120-60)
                if x in check_hole1:
                    screen.blit(bg,(0,0))
                    screen.blit(plank,(0,y))
                    screen.blit(ball,(x,100))
                    screen.blit(holelight, (hole1,y+30))
                    screen.blit(hole, (hole2,y+30))
                    screen.blit(displayscore, (399,0))

                    showcoins=True
                    
                    screen.blit(coin2, (500,0))
                    screen.blit(displaycoins, (555,0))
                    
                    if scoreadder==1:
                        score+=1
                        scoreadder=0
                    
                elif x in check_hole2:
                    screen.blit(bg,(0,0))
                    screen.blit(plank,(0,y))
                    screen.blit(ball,(x,100))
                    screen.blit(hole, (hole1,y+30))
                    screen.blit(holelight, (hole2,y+30))
                    screen.blit(displayscore, (399,0))
                    
                    showcoins=True
                    
                    if scoreadder==1:
                        score+=1
                        scoreadder=0
                        
                else:
                    #to stop game and show crash moment
                    if armour:
                        screen.blit(bg,(0,0))
                        screen.blit(plank,(0,y))
                        screen.blit(hole, (hole1,y+30))
                        screen.blit(hole, (hole2,y+30))
                        screen.blit(ball,(x,100))
                        screen.blit(displayscore, (399,0))
                        #show coin only if it is not taken
                        showcoins=True
            
                        flag=0
                        armed=True
                        if scoreadder==1:
                            score+=1
                            scoreadder=0
                    else:
                        
                        flag=1
                        screen.blit(bg,(0,0))
                        screen.blit(plank,(0,y))
                        screen.blit(hole, (hole1,y+30))
                        screen.blit(hole, (hole2,y+30))
                        screen.blit(ball,(x,100))
                        screen.blit(displayscore, (399,0))
                        screen.blit(PETC, (250,550))
                        screen.blit(gameover, (200,400))
                        showcoins=True

            if showcoins: #shows coins excepy when magnet is on
                    #show coin only if it is not taken
                    if c1adder==1:
                        screen.blit(coin, (x_c1, y-150))
                    if c2adder==1:
                        screen.blit(coin, (x_c2, y-300))
                    if c3adder==1:
                        screen.blit(coin, (x_c3, y-450))
                    screen.blit(coin2, (500,0))
                    screen.blit(displaycoins, (555,0))
                                            
        if flag not in [7,3,-1,1,5]: #to display boost icon and laser icon

            if ccount>m_pt-1 and score>mg_used+10+m_level and not bar_m: #magnet
                screen.blit(magnet, (450,500))
                screen.blit(coin2, (500,550))
                displaympt=TNR1.render(str(m_pt),1,(0,0,0))
                screen.blit(displaympt, (515-(len(str(m_pt))-1)*12,550))
 
            else:
                screen.blit(magnetf, (450,500))
                screen.blit(coinf, (500,550))
                displaympt=TNR1.render(str(m_pt),1,(0,0,0))
                screen.blit(displaympt, (515-(len(str(m_pt))-1)*12,550))
                #to show bars
                if bar_m:
                    if score>lastscore_m:
                        h_m=h_mo+parts_m
                        h_mo=h_m    
                        lastscore_m+=1     
                    if h_m<h_mo+parts_m-2:
                        h_m+=.2

                    if h_m<70:
                        pg.draw.rect(screen, (0,255,0),(560,500+h_m,25,100))
                    else:
                        pg.draw.rect(screen, (255,0,0),(560,500+h_m,25,100))
                
            if ccount>b_pt-1 and not bar_b: #boost
                screen.blit(boost, (150,500))
                screen.blit(coin2, (200,550))
                displaybpt=TNR1.render(str(b_pt),1,(0,0,0))
                screen.blit(displaybpt, (215-(len(str(b_pt))-1)*12,550))
                
            else:
                screen.blit(boostf, (150,500))
                screen.blit(coinf, (200,550))
                displaybpt=TNR1.render(str(b_pt),1,(0,0,0))
                screen.blit(displaybpt, (215-(len(str(b_pt))-1)*12,550))
                #to show bars
                if bar_b:
                    if score>lastscore_b:
                        h_b=h_bo+parts_b
                        h_bo=h_b    
                        lastscore_b+=1     
                    if h_b<h_bo+parts_b-2:
                        h_b+=.8
                    if h_b<70:
                        pg.draw.rect(screen, (0,255,0),(260,500+h_b,25,100))
                    else:
                        pg.draw.rect(screen, (255,0,0),(260,500+h_b,25,100))
                
            if ccount>l_pt-1 and not bar_l: #laser
                screen.blit(laser, (300,500))
                screen.blit(coin2, (350,550))
                displaylpt=TNR1.render(str(l_pt),1,(0,0,0))
                screen.blit(displaylpt, (365-(len(str(l_pt))-1)*12,550))
            else:
                screen.blit(laserf, (300,500))
                screen.blit(coinf, (350,550))
                displaylpt=TNR1.render(str(l_pt),1,(0,0,0))
                screen.blit(displaylpt, (365-(len(str(l_pt))-1)*12,550))
                if bar_l:
                    if score>lastscore_l:
                        h_l=h_lo+parts_l
                        h_lo=h_l    
                        lastscore_l+=1     
                    if h_l<h_lo+parts_l-2:
                        h_l+=.2
                    if h_l<70:   
                        pg.draw.rect(screen, (0,255,0),(410,500+h_l,25,100))
                    else:
                        pg.draw.rect(screen, (255,0,0),(410,500+h_l,25,100))

            if ccount>a_pt-1 and score>a_used+a_level+15 and not bar_a: #armour
                screen.blit(arm, (0,500))
                screen.blit(coin2, (50,550))
                displayapt=TNR1.render(str(a_pt),1,(0,0,0))
                screen.blit(displayapt, (65-(len(str(a_pt))-1)*12,550))
            else:
                screen.blit(armf, (0,500))
                screen.blit(coinf, (50,550))
                displayapt=TNR1.render(str(a_pt),1,(0,0,0))
                screen.blit(displayapt, (65-(len(str(a_pt))-1)*12,550))
                if bar_a:
                    if score>lastscore_a:
                        h_a=h_ao+parts_a
                        h_ao=h_a    
                        lastscore_a+=1     
                    if h_a<h_ao+parts_a-2:
                        h_a+=.4
                    if h_a<70:
                        pg.draw.rect(screen, (0,255,0),(110,500+h_a,25,100))
                    else:
                        pg.draw.rect(screen, (255,0,0),(110,500+h_a,25,100))
                    
        #when factor is greater than 800, the plank disappears
        if factor>800: #resets variables for laser, boost and normal run
            #resets pcount so that the plank starts from the bottom again
            pcount=1
            scoreadder=1
            showcoins=False
            l=[]
            if score%30==10:
                bg=pg.image.load('images/background yellow.jpg')
                bg=pg.transform.scale(bg, screen_size)
                hole=pg.image.load('images/hole yellow.png')
                hole=pg.transform.scale(hole, (120,50))

            if score%30==20:
                bg=pg.image.load('images/background red.jpg')
                bg=pg.transform.scale(bg, screen_size)
                hole=pg.image.load('images/hole red.png')
                hole=pg.transform.scale(hole, (120,50))

            if score%30==0:
                bg=pg.image.load('images/background.jpg')
                bg=pg.transform.scale(bg, screen_size)
                hole=pg.image.load('images/hole.png')
                hole=pg.transform.scale(hole, (120,50))
            
            #changes hole location
            hole1=random.randint(100,280)
            hole2=random.randint(420,600)

            if flag==0:
                #for coins
                c1adder=1
                c2adder=1
                c3adder=1
                
                x_c1=800 #y_c1=y-100
                x_c2=800 #y_c2=y-200
                x_c3=800 #y_c3=y-300
                
                p1=random.randint(0,2) #randomizes if the coin will be there or not
                p2=random.randint(0,2) 
                p3=random.randint(0,2)

                if p1:
                    x_c1=random.randint(85, 650)
                else:
                    x_c1=800
                if p2:
                    x_c2=random.randint(85,650)
                else:
                    x_c2=800
                if p3:
                    x_c3=random.randint(85,650)
                else:
                    x_c3=800
                
                #does not allow speed to increase above 10
                if speed<10:
                    speed+=.9

            if flag==4: #boost
                if score==score_o+b_level:
                    flag=0
                    b_pt+=2
                    ball=pg.image.load('images/ball.png')
                    ball=pg.transform.scale(ball, (70,70))
                    bar_b=False
                    h_b=0
                    h_bo=0
            
            if flag==6:
                if score==score_o+l_level: #continues the laser for the given points
                    flag=0
                    l_pt+=3
                    ball=pg.image.load('images/ball.png')
                    ball=pg.transform.scale(ball, (70,70))
                    bar_l=False
                    h_l=0
                    h_lo=0

            if mg: #magnet
                if score==score_o+m_level:
                    ball=pg.image.load('images/ball.png')
                    ball=pg.transform.scale(ball, (70,70))
                    m_pt+=4
                    bar_m=False
                    h_m=0
                    h_mo=0
                    mg=False
            if armour: #armour
                if score==score_o+a_level or armed:
                    ball=pg.image.load('images/ball.png')
                    ball=pg.transform.scale(ball, (70,70))
                    a_pt+=1
                    bar_a=False
                    h_a=0
                    h_ao=0
                    armour=False
                    armed=False
                    
        if flag==1:
            #disables repeating
            pg.key.set_repeat()
            #resets the game and shows crash position
            y=800
              
        if flag==2: #shows score
            screen.blit(bg,(0,0))
            displayscore=TNR2.render(str(score),1, (0,0,0))
            displaycoins=TNR1.render(str(ccount),1, (0,0,0))
            yourscore=TNR3.render('Your score is:',1,(0,0,0))
            screen.blit(yourscore, (100,100))
            screen.blit(displayscore, (300,175))
            screen.blit(coin2, (350,400))
            screen.blit(displaycoins, (400,400))
            screen.blit(PETC, (250,550))

        if flag==7: #press enter to exit screen
            screen.blit(bg, (0,0))
            screen.blit(replay, (300,200))
            screen.blit(PETE, (250,550))

        if flag==3: #quits
            i=False
            
        #manages all events
        for event in pg.event.get():
            #to close the window when the X button is pressed
            if event.type==pg.QUIT:
                i=False

            #checks whether a key is pressed
            if event.type==pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    #the ball moves 10 pixels to the left
                    if x>85 and flag!=5:
                        x-=10
                if event.key == pg.K_RIGHT:
                    #the ball moves 10 pixels to the right
                    if x<650 and flag!=5:
                        x+=10
                if event.key== pg.K_RETURN:
                    if flag==7:
                        flag=3 #quits game
                
                    if flag==2:
                        flag=7 #shows replay button
                        
                    if flag==1:
                        flag=2 #shows the score

                    if flag==-1: #exits welcome screen
                        flag=0
                if event.key== pg.K_b: #boost
                    if flag==0:
                        if ccount>b_pt-1:

                            flag=4
                            score_o=score
                            if score==score_o:
                                ball=pg.image.load('images/ball boost.png')
                                ball=pg.transform.scale(ball, (60,60))
                                bar_b=True
                                h_bo=0
                                lastscore_b=score
                            ccount-=b_pt
                if event.key== pg.K_p: #for pausing the game
                    if flag!=5:
                        pg.key.set_repeat()
                        flag_o=flag
                        flag=5
                    else:
                        flag=flag_o
                        pg.key.set_repeat(10, 5)

                if event.key== pg.K_l: #laser
                    if flag==0:
                        if ccount>l_pt-1:
                            score_o=score
                            flag=6

                            if score==score_o:
                                ball=pg.image.load('images/ball laser.png')
                                ball=pg.transform.scale(ball, (70,70))                               
                                bar_l=True
                                h_lo=0
                                lastscore_l=score
                            ccount-=l_pt

                if event.key==pg.K_m: #coin magnet

                    if ccount>m_pt-1:    
                        if mg==False and score>mg_used+m_level+10:
                            mg_used=score
                            score_o=score
                            if score==score_o:
                                ball=pg.image.load('images/ball magnet.png')
                                ball=pg.transform.scale(ball, (70,70))
                                bar_m=True
                                h_mo=0
                                lastscore_m=score
            
                            ccount-=m_pt
                            mg=True
                            
                if event.key==pg.K_s: #armour

                    if ccount>a_pt-1:
                        if armour==False and score>a_used+a_level+15:
                            armour=True
                            a_used=score
                            score_o=score
                            if score==score_o:
                                ball=pg.image.load('images/ball armour.png')
                                ball=pg.transform.scale(ball, (70,70))
                                bar_a=True
                                h_ao=0
                                lastscore_a=score
                            ccount-=a_pt

            if event.type==pg.MOUSEBUTTONDOWN:
                if flag==7:
                    (x,y)=pg.mouse.get_pos()
                    if x in range(300,500) and y in range(200,400):
                        repeat=1
                        flag=3

        if flag!=-1 and flag!=5:        
            count+=1
            pcount+=1
        clock.tick(25) #sets maximum frame rate
        
        pg.display.update()

    pg.quit()
    return score, ccount, repeat

class Game:
    def __init__(self):
        self.L=[]
        
#checks if the Details file exists
try:
    f1=open('Details.dat', 'rb')
    obj=pickle.load(f1)
    f1.close()
except:
    obj=Game()
    f1=open('Details.dat', 'wb')
    pickle.dump(obj,f1)
    f1.close()

k=True
while k:
    print '\n1. Play \n2. Instructions \n3. Highscores \n4. Exit' 
    ch=raw_input('Enter choice: ')
    if ch=='1':
        f1=open('Details.dat', 'rb')
        obj=pickle.load(f1)
        L=obj.L
        name=raw_input('Enter your full name: ')
        f1=open('Details.dat', 'wb')

        play=1
        while play:
            score,coins,play=game()
            L+=[[score,name,coins]]
            
        obj.L=L
        pickle.dump(obj, f1)
        f1.close()

    elif ch=='2':
        print '\nINSTRUCTIONS:'
        print '1) Use the left and right arrow keys to move the ball.'
        print '2) Position the ball so that it passes through either of the holes.'
        print '3) Collect as many coins as you can.'
        print '4) 2 Coins - Shield, 5 Coins - Boost, 8 Coins - Laser, 10 Coins - Magnet'
        print '5) Press \'s\' to activate the shield when the shield icon appears. It lasts for 5 points and can save you from one obstacle.'
        print '6) Press \'b\' to activate the boost when the boost icon appears.'
        print '7) Press \'l\' to activate laser when the laser icon appears.'
        print '8) Press \'m\' to activate coin magnet when the icon appears.'
        print '9) Press \'p\' to pause the game.'
        print '10) Once the coin magnet is used, it cannot be used again for another 10 points.'
        print '11) Once the shield has been used, it cannot be used again for another 15 points.'
        print '12) The number of coins required for each powerup increases everytime it is used.'
        print '13) Enjoy the game!'
        
    elif ch=='3':
        f1=open('Details.dat', 'rb')
        obj=pickle.load(f1)
        L=obj.L
        L.sort(reverse=True)
        no=1
        print
        for l in L:
            if no<11:
                sc=str(l[0])
                print str(no)+'.'+'|Score: '+str(l[0])+'|Coins: '+str(l[2])+ '|Name: '+l[1]
            no+=1
        f1.close()

    elif ch=='4':
        k=False

    else:
        print 'Invalid choice.'
