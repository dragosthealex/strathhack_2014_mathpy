import pygame
import pygame.locals
import random
from Tkinter import *
import Tkinter as ttk

pygame.init()

screen = pygame.display.set_mode((720,415))
pygame.display.set_caption('ZOMBIEZ!')

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
		self.image = pygame.Surface([40, 40])
		self.image.fill((0,255,0))
		self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
	def getQuestion():
		return self.question

	def getPosition(self):
		return (self.x, self.y)

	def update(self):
		if self.timeLeft <= 100:
			self.kill()
		else:
			if self.timeLeft <= self.lifetime/3:
				self.image.fill((255,0,0))
			else: 
				if self.timeLeft <= (self.lifetime * 2) / 3 :
					self.image.fill((255,255,0))
				else:
					self.image.fill((0, 255, 0))
			self.timeLeft = self.timeLeft - 1
			self.time = str(self.timeLeft/100)
			self.font = pygame.font.SysFont("comicsansms", 20)
			

			self.timeText = self.font.render(self.time, True, (0,0,0))
			self.image.blit(self.timeText, (10,10))

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
			#theEvent.question = CreateQuestion(difficulty)
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
		self.x = random.randrange(50, 450)
		self.y = random.randrange(50, 450)

class Panel(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color, layer):
		self.groups = panelsLayer, panels
		self._layer = layer
		self.color = color
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.image = pygame.Surface([width, height])
		self.image.fill(self.color)
		self.rect = pygame.Rect(x, y, width, height)

	def setQuestion(self, clickedEvent):
		font = self.font = pygame.font.SysFont("comicsansms", 20)
		# Replace the mock question with 'clickedEvent.getQuestion()'
		self.image.fill(self.color)
		# Check if the event is still available
		#if events.has(clickedEvent):
		self.question = self.font.render(clickedEvent, True, (0,0,0))
		self.image.blit(self.question, (0,0))



run = True

# We count how much has passed since the last event
elapsed = 0
clock = pygame.time.Clock()

# If you click on one of the events, you'll see the question in the quest panel
bigPanel = Panel(0, 340, 720, 75, (100,100,100), 3)
questPanel = Panel(260, 350, 200, 25, (200,0,0), 2)
ansPanel = Panel(260, 380, 200, 25, (200,0,0), 1)

panelsLayer.move_to_back(bigPanel)

while run:
		clock.tick(100)
		elapsed = elapsed + 1
		events.update()
		random.seed()
		randNo = random.randrange(0, 40)
		drawn = eventGenerator(elapsed, randNo, 1)
		if drawn:
			elapsed = 0

		screen.fill((0,0,0))
		events.draw(screen)

		# When an event clicked
		questPanel.setQuestion("123")
		panelsLayer.draw(screen)
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
		pygame.display.flip()
		pygame.event.pump()
