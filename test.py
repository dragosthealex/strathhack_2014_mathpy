# coding: utf-8
import pygame
import pygame.locals
import random
# Initialise screen
pygame.init()
# Make a screen with size
screen = pygame.display.set_mode((400, 300))
# Set title
pygame.display.set_caption('ZOMBIEEES!!!')

noOfEvents = 0

# The group of sprites displayed

# The events
# Constructor needs time range, coords range and difficulty
class Event(pygame.sprite.Sprite):
	# Constructs the event.
	def __init__(self, minTime, maxTime, minX, maxX, minY, maxY, difficulty):
		# Create the sprite constructor
		pygame.sprite.Sprite.__init__(self)
		# Set the time, x, and y
		random.seed()
		self.time = random.randrange(minTime, maxTime)
		self.x = random.randrange(minX, maxX)
		self.y = random.randrange(minY, maxY)
		self.left = 1000
		#self.question = MathQuestion(difficulty)
	
	def drawMe(self):
		evSurface = pygame.Surface((40,40))
		self.circle = pygame.draw.circle(evSurface, (0, 0, 255), [20, 20], 20)
		font = pygame.font.SysFont("comicsansms", 20)
		time = str(self.left/100)
		timeText = font.render(time, True, (0,255,0))
		evSurface.blit(timeText, (0, 0))
		screen.blit(evSurface, [self.x-5, self.y-5])

clock = pygame.time.Clock()

def eventGenerator(elapsed, number, difficulty, noOfEvents):
	if elapsed > 300:
		if number == 20:
			anEvent = Event(0, 10, 0, 300, 0, 200, 1)
			anEvent.drawMe()
			events[noOfEvents] = anEvent
			return True
	else:
		return False

run = True

# We count how much has passed since the last event
elapsed = 0

while run:
		clock.tick(60)
		elapsed = elapsed + 1

		random.seed()
		randNo = random.randrange(0, 40)
		noOfEvents = noOfEvents + 1
		drawn = eventGenerator(elapsed, randNo, 1, noOfEvents)

		if drawn:
			elapsed = 0

		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
		pygame.display.flip()
		pygame.event.pump()