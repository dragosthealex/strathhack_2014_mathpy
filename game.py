
import os, sys, pygame, random

# Screen dimensions
screenWidth = 720
screenHeight = 450

menuItems = pygame.sprite.Group()
events = pygame.sprite.Group()
panels = pygame.sprite.Group()
questions = pygame.sprite.Group()
panelsLayer = pygame.sprite.LayeredUpdates()
mainMenuItems = pygame.sprite.Group()

class PopUp():
    def __init__(self, circle):
        self.circle = circle
        self.visible = True

class createQuestion():
    def __init__(self, difficulty):
        num1 = random.randint(0, 36 / difficulty)
        num2 = random.randint(1, 36 / difficulty)
        prob = random.randint(0, 100)
        if prob <= 25:
            self.question = str(num1) + ' + ' + str(num2) + ' = ?'
            self.answer = str(num1 + num2)
        elif prob <= 50:
            self.question = str(num1) + ' - ' + str(num2) + ' = ?'
            self.answer = str(num1 - num2)
        elif prob <= 75:
            self.question = str(num1) + ' * ' + str(num2) + ' = ?'
            self.answer = str(num1 * num2)
        elif prob <= 100:
            num1 = random.randint(0, 18 / difficulty)
            num2 = random.randint(1, 18 / difficulty)
            self.question = str(num1 * num2) + ' / ' + str(num2) + ' = ?'
            self.answer = str(num1)

class MainMenuItem(pygame.sprite.Sprite):
    def __init__ (self, text, fontSize, uniqueId, isButton = True):
        pygame.sprite.Sprite.__init__(self, mainMenuItems)
        self.isButton = isButton
        self.font = pygame.font.Font("overhaul.ttf", fontSize)
        self.text = self.font.render(text, True, (255,255,255))
        self.size = self.font.size(text)
        self.image = pygame.Surface((240, 40))
        self.rect = pygame.Rect(240, 117 + uniqueId * 48, 240, 40)
        self.id = uniqueId

    def update(self):
        self.image.fill((0,0,0))
        self.image.blit(self.text, (120 - self.size[0] / 2, 23 - self.size[1] / 2))

extraMenuItems = pygame.sprite.Group()

class ExtraMenuItem(pygame.sprite.Sprite):
    def __init__(self, text, y, uniqueId):
        pygame.sprite.Sprite.__init__(self, extraMenuItems)
        self.font = pygame.font.Font("overhaul.ttf", 16)
        self.text = self.font.render(text, True, (255,255,255))
        self.size = self.font.size(text)
        self.image = pygame.Surface((240, 40))
        self.rect = pygame.Rect(240, y, 240, 40)
        self.id = uniqueId

    def update(self):
        self.image.fill((0,0,0))
        self.image.blit(self.text, (120 - self.size[0] / 2, 23 - self.size[1] / 2))

events = pygame.sprite.Group()
panelsLayer = pygame.sprite.LayeredUpdates()
panels = pygame.sprite.Group()

class Event(pygame.sprite.Sprite):
    def __init__ (self, x, y, minTime, maxTime):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y

        self.timeLeft = random.randrange(minTime, maxTime)
        self.lifetime = self.timeLeft

        self.image = pygame.image.load('greenSprite.png').convert_alpha()

        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
    def getQuestion(self):
        return self.question

    def getPosition(self):
        return (self.x, self.y)

    def update(self):
        # print self.timeLeft
        if self.timeLeft <= 100:
            self.kill()
            player.loseLife()
        else:
            if self.timeLeft <= self.lifetime/3:
                self.image = pygame.image.load('redSprite.png').convert_alpha()
            elif self.timeLeft <= (self.lifetime * 2) / 3 :
                self.image = pygame.image.load('yellowSprite.png').convert_alpha()
            else:
                self.image = pygame.image.load('greenSprite.png').convert_alpha()
            self.timeLeft = self.timeLeft - 1
            self.time = str(self.timeLeft/100)
            self.font = pygame.font.Font("OpenSans-Regular.ttf", 20)
            self.timeText = self.font.render(self.time, True, (0,0,0))

            self.textSize = self.font.size(self.time);
            self.image.blit(self.timeText, (20 - self.textSize[0] / 2, 20 - self.textSize[1] / 2))
            # print self.time

def eventGenerator(elapsed, randomness, difficulty):
    reqElapsed = getElapsed(difficulty)
    minTime = getMinTime(difficulty)
    maxTime = getMaxTime(difficulty)
    if(elapsed > reqElapsed):
        if(randomness == 20):
            rPoint = RandomPoint()
            theEvent = Event(rPoint.x, rPoint.y, minTime, maxTime)
            while pygame.sprite.spritecollideany(theEvent, events) != None:
                rPoint = RandomPoint()
                theEvent = Event(rPoint.x, rPoint.y, minTime, maxTime)
            theEvent.question = createQuestion(difficulty)
            events.add(theEvent)
            return True
    else:
        return False

def getElapsed(difficulty):
    #for difficulty = 3 (easy), the min diff between two events
    #is 6 sec. for diff = 1 (hard) diff = 2 s
    return 100 * difficulty

def getMinTime(difficulty):
    return difficulty * 300

def getMaxTime(difficulty):
    return difficulty * 300 + (difficulty * 300) / 2

class RandomPoint():
    def __init__(self):
        random.seed()
        self.x = 0
        self.y = 0
        while not validCoords(self.x, self.y):
            self.x = random.randrange(95, 590)
            self.y = random.randrange(120, 320)

def validCoords(x, y):
    if x < 75 or x > 610:
        return False
    if y < 100 or y > 340:
        return False
    if y - 0.4576271186 * x > 509:
        return False
    return True

def areClose(pos1, pos2, distance):
    return (abs(pos1[0] - pos2[0]) <= distance and abs(pos1[1] - pos2[1]) <= distance)

class Pixel(pygame.sprite.Sprite):
    def __init__ (self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([1,1])
        self.image.fill([255,0,0])
        self.rect = pygame.Rect(pos[0], pos[1], 1, 1)

def mouseClick(mousePos):
    collidedWith = pygame.sprite.spritecollideany(Pixel(mousePos), mainMenuItems)
    if collidedWith != None and collidedWith.isButton:
        return collidedWith.id
    collidedWith = pygame.sprite.spritecollideany(Pixel(mousePos), extraMenuItems)
    if collidedWith != None:
        return collidedWith.id

def mouseClickEvent(mousePos):
    collidedWith = pygame.sprite.spritecollideany(Pixel(mousePos), events)
    if collidedWith != None:
        return collidedWith

class Panel(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, layer):
        self.groups = panelsLayer, panels
        self._layer = layer
        self.color = color
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.empty = True
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.answer = ""
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, width, height)

    def setQuestion(self, clickedEvent):
        font = self.font = pygame.font.Font("OpenSans-Regular.ttf", 16)
        # Replace the mock question with 'clickedEvent.getQuestion()'
        self.image.fill(self.color)
        self.image = pygame.image.load('MetalTextBox.png')
        # Check if the event is still available
        if events.has(clickedEvent):
            self.event = clickedEvent
            self.question = self.font.render(clickedEvent.getQuestion().question, True, (0,0,0))
            self.answer = clickedEvent.getQuestion().answer
            self.empty = False
            self.image.blit(self.question, (10,0))

    def setAnswer(self, ansText):
        font = self.font = pygame.font.Font("OpenSans-Regular.ttf", 16)
        self.userAnswer = self.font.render(ansText, True, (0,0,0))
        self.image.fill(self.color)
        self.image = pygame.image.load('MetalTextBox.png')
        self.image.blit(self.userAnswer, (10,0))

    def checkAnswer(self, string):
        if string != questPanel.answer:
            questPanel.event.kill()
            questPanel.image.fill((0,0,0))
            questPanel.image = pygame.image.load('MetalTextBox.png')
            questPanel.empty = True
            player.loseLife()
        else:
            questPanel.event.kill()
            player.scoreIncr()
        #self.image.fill((200,0,0))
        self.image = pygame.image.load('MetalTextBox.png')

class Input():
    def __init__(self):
        self.string = ""

    def addIn(self, char):
        if char == "\b" and char != "\r":
            self.string = self.string[:-1]
            ansPanel.setAnswer(self.string)
        elif char == "\r" and questPanel.empty == False:
            ansPanel.checkAnswer(self.string)
            self.string = ""
        elif char != "\r":
            self.string = self.string + char
            ansPanel.setAnswer(self.string)

class Player():
    def __init__(self, panel1, panel2):
        self.font = pygame.font.Font("OpenSans-Regular.ttf", 16)
        self.score = 0
        self.life = 10
        self.GameOver = False

        self.lifePane = panel1
        lifeStr = "Life " + str(self.life)
        lifeText = self.font.render(lifeStr, True, (0,0,0))
        self.lifePane.image.blit(lifeText, (10, 25))

        self.scorePane = panel2
        scoreStr = "Score " + str(self.score)
        scoreText = self.font.render(scoreStr, True, (0,0,0))
        self.scorePane.image.blit(scoreText, (10, 25))

    def loseLife(self):
        self.life = self.life - 1
        if self.life <= 0:
            self.GameOver = True
        self.lifePane.image.fill((0,180,0))
        lifeStr = "Life " + str(self.life)
        lifeText = self.font.render(lifeStr, True, (0,0,0))
        self.lifePane.image.blit(lifeText, (10, 25))

    def scoreIncr(self):
        self.score = self.score + 1
        self.scorePane.image.fill((180,180,0))
        scoreStr = "Score " + str(self.score)
        scoreText = self.font.render(scoreStr, True, (0,0,0))
        self.scorePane.image.blit(scoreText, (10, 25))

lives = 5
def subtractLife():
    lives = lives - 1

# Initialise pygame and window
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Zombie Plague")

# Play intro song
pygame.mixer.music.load('intro.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Make background and menus
pausedImg = pygame.image.load('paused.png').convert()
background = pygame.image.load('background.png').convert()
mainMenuTitle   = MainMenuItem("Zombie Plague", 24, 0, False)
mainMenuStart   = MainMenuItem("Start",         16, 1)
mainMenuInfo    = MainMenuItem("How to Play",   16, 2)
mainMenuOptions = MainMenuItem("Options",       16, 3)
mainMenuQuit    = MainMenuItem("Quit",          16, 4)
extraMenuBack = ExtraMenuItem("Back to Menu",    8, 5)
extraMenuQuit = ExtraMenuItem("Quit",          402, 6)

# Set internal clock
clock = pygame.time.Clock()
mousePrimed = False
mousePrimedPos = 0

running = True
paused = False
ticks = 0

startMenuIsOpen = True
infoMenuIsOpen = False
optionsMenuIsOpen = False
difficulty = 3

# If you click on one of the events, you'll see the question in the quest panel
questPanel = Panel(260, 385, 200, 25, (200,0,0), 2)
questPanel.image = pygame.image.load('MetalTextBox.png')
ansPanel = Panel(260, 415, 200, 25, (200,0,0), 1)
ansPanel.image = pygame.image.load('MetalTextBox.png')
bigPanel = Panel(0, 375, 720, 75, (100,100,100), 5)
bigPanel.image = pygame.image.load('zombie.png')

livesPanel = Panel(0, 375, 75, 75, (0,180,0), 3)
scorePanel = Panel(645, 375, 75, 75, (180,180,0), 4)

player = Player(livesPanel, scorePanel)

panelsLayer.move_to_back(bigPanel)
userInput = Input()



while startMenuIsOpen:
    clock.tick(60)

    mousePos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePrimed = True
            mousePrimedPos = pygame.mouse.get_pos()

        elif mousePrimed == True and event.type == pygame.MOUSEBUTTONUP and areClose(mousePrimedPos, mousePos, 40):
            # values get printed on the command prompt
            buttonId = mouseClick(mousePos)
            if buttonId == 1:
                startMenuIsOpen = False
                mousePrimed = False
                selectingDifficulty = True
                mainMenuStart.text = mainMenuStart.font.render("Easy", True, (255,255,255))
                mainMenuStart.size = mainMenuStart.font.size("Easy")
                mainMenuInfo.text = mainMenuInfo.font.render("Medium", True, (255,255,255))
                mainMenuInfo.size = mainMenuInfo.font.size("Medium")
                mainMenuOptions.text = mainMenuOptions.font.render("Hard", True, (255,255,255))
                mainMenuOptions.size = mainMenuOptions.font.size("Hard")
                mainMenuQuit.text = mainMenuQuit.font.render("Back", True, (255,255,255))
                mainMenuQuit.size = mainMenuQuit.font.size("Back")
                while selectingDifficulty:
                    clock.tick(60)
                    mousePos = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mousePrimed = True
                            mousePrimedPos = pygame.mouse.get_pos()
                        elif mousePrimed == True and event.type == pygame.MOUSEBUTTONUP and areClose(mousePrimedPos, mousePos, 40):
                            buttonId = mouseClick(mousePos)
                            if buttonId == 1:
                                difficulty = 3
                                selectingDifficulty = False
                            elif buttonId == 2:
                                difficulty = 2
                                selectingDifficulty = False
                            elif buttonId == 3:
                                difficulty = 1
                                selectingDifficulty = False
                            elif buttonId == 4:
                                startMenuIsOpen = True
                                selectingDifficulty = False
                    if not selectingDifficulty:
                        mainMenuStart.text = mainMenuStart.font.render("Start", True, (255,255,255))
                        mainMenuStart.size = mainMenuStart.font.size("Start")
                        mainMenuInfo.text = mainMenuInfo.font.render("How to Play", True, (255,255,255))
                        mainMenuInfo.size = mainMenuInfo.font.size("How to Play")
                        mainMenuOptions.text = mainMenuOptions.font.render("Options", True, (255,255,255))
                        mainMenuOptions.size = mainMenuOptions.font.size("Options")
                        mainMenuQuit.text = mainMenuQuit.font.render("Quit", True, (255,255,255))
                        mainMenuQuit.size = mainMenuQuit.font.size("Quit")
                        break
                    screen.blit(background, (0, 0))
                    mainMenuItems.update()
                    mainMenuItems.draw(screen)
                    pygame.display.flip()
                    pygame.event.pump()
            elif buttonId == 2:
                infoMenuIsOpen = True
                mousePrimed = False
                while infoMenuIsOpen:
                    clock.tick(60)
                    mousePos = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mousePrimed = True
                            mousePrimedPos = pygame.mouse.get_pos()
                        elif mousePrimed == True and event.type == pygame.MOUSEBUTTONUP and areClose(mousePrimedPos, mousePos, 40):
                            buttonId = mouseClick(mousePos)
                            if buttonId == 5:
                                infoMenuIsOpen = False
                            elif buttonId == 6:
                                pygame.quit()
                                sys.exit()
                    if not infoMenuIsOpen:
                        break
                    screen.blit(background, (0, 0))
                    screen.blit(pygame.image.load('info.jpg').convert(), (8, 56))
                    extraMenuItems.update()
                    extraMenuItems.draw(screen)
                    pygame.display.flip()
                    pygame.event.pump()
            elif buttonId == 3:
                optionsMenuIsOpen = True
                mousePrimed = False
                while optionsMenuIsOpen:
                    clock.tick(60)
                    mousePos = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mousePrimed = True
                            mousePrimedPos = pygame.mouse.get_pos()
                        elif mousePrimed == True and event.type == pygame.MOUSEBUTTONUP and areClose(mousePrimedPos, mousePos, 40):
                            buttonId = mouseClick(mousePos)
                            if buttonId == 5:
                                optionsMenuIsOpen = False
                            elif buttonId == 6:
                                pygame.quit()
                                sys.exit()
                    if not optionsMenuIsOpen:
                        break
                    screen.blit(background, (0, 0))
                    screen.blit(pygame.image.load('options.jpg').convert(), (8, 56))
                    extraMenuItems.update()
                    extraMenuItems.draw(screen)
                    pygame.display.flip()
                    pygame.event.pump()
            elif buttonId == 4:
                pygame.quit()
                sys.exit()
            mousePrimed = False

    screen.fill((0,0,0))
    screen.blit(background, (0, 0))


    mainMenuItems.update()
    mainMenuItems.draw(screen)


    pygame.display.flip()
    pygame.event.pump()

# Game begin
# Play ingame song
pygame.mixer.music.stop()
pygame.mixer.music.load("ingame.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

GameOver = False
theEvent = Event(screenWidth / 2, screenHeight / 2, getMinTime(difficulty), getMaxTime(difficulty))
timeout = 1;

while running:
    clock.tick(100)
    ticks = ticks + 1

    events.update()

    timeout = timeout + 1

    random.seed()
    if eventGenerator(ticks, random.randrange(0, 40), difficulty):
        ticks = 0
    
    # Get key states
    keyState = pygame.key.get_pressed()
    
    # Pause
    if keyState[pygame.K_ESCAPE]:
        paused = True

    pygame.key.set_repeat()
    if event.type == pygame.KEYDOWN:
        if keyState[pygame.K_0] and timeout >= 20:
            userInput.addIn("0")
            timeout = 1
        elif keyState[pygame.K_1] and timeout >= 20:
            userInput.addIn("1")
            timeout = 1
        elif keyState[pygame.K_2] and timeout >= 20:
            userInput.addIn("2")
            timeout = 1
        elif keyState[pygame.K_3] and timeout >= 20:
            userInput.addIn("3")
            timeout = 1
        elif keyState[pygame.K_4] and timeout >= 20:
            userInput.addIn("4")
            timeout = 1
        elif keyState[pygame.K_5] and timeout >= 20:
            userInput.addIn("5")
            timeout = 1
        elif keyState[pygame.K_6] and timeout >= 20:
            userInput.addIn("6")
            timeout = 1
        elif keyState[pygame.K_7] and timeout >= 20:
            userInput.addIn("7")
            timeout = 1
        elif keyState[pygame.K_8] and timeout >= 20:
            userInput.addIn("8")
            timeout = 1
        elif keyState[pygame.K_9] and timeout >= 20:
            userInput.addIn("9")
            timeout = 1
        elif keyState[pygame.K_BACKSPACE] and timeout >= 20:
            userInput.addIn("\b")
            timeout = 1
        elif keyState[pygame.K_MINUS] and timeout >= 20:
            userInput.addIn("-")
            timeout = 1
        elif keyState[pygame.K_RETURN] and timeout >= 20:
            userInput.addIn("\r")
            timeout = 1

    mousePos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePrimed = True
            mousePrimedPos = pygame.mouse.get_pos()

        elif mousePrimed == True and event.type == pygame.MOUSEBUTTONUP and areClose(mousePrimedPos, mousePos, 40):
            # values get printed on the command prompt
            mouseClick(mousePos)
            lastClickedEvent = mouseClickEvent(mousePos)
            print lastClickedEvent
            questPanel.setQuestion(lastClickedEvent)

    
    # Make background
    screen.blit(background, (0, 0))
    # Update objects
    events.draw(screen)
    panelsLayer.draw(screen)
    pygame.display.flip()
    pygame.event.pump()

    while player.GameOver:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(pygame.image.load('gameover.jpg').convert(), (0, 0))
        pygame.display.flip()
        pygame.event.pump()

    while paused:
        clock.tick(60)

        # Get key states
        keyState = pygame.key.get_pressed()

        # Resume
        if keyState[pygame.K_SPACE]:
            paused = False
            break
        
        # Allow exiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keyState[pygame.K_q]:
                pygame.quit()
                sys.exit()
        
        # Update screen
        screen.blit(pausedImg, (0, 0))
        
        pygame.display.flip()
        pygame.event.pump()