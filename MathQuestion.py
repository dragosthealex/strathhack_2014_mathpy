# coding utf-8
import random

class MathQuestion:
	"""docstring for MathQuestion"""
	def __init__(self, difficulty):
		self.difficulty = difficulty
		if difficulty == "easy" :
			self.num1 = random.randint(0, 15)
			self.num2 =	random.randint(1, 15)
			prob = random.randint(0, 100)
			if prob <= 40 :
				self.question = str(self.num1) + ' + ' + str(self.num2) + ' = ?'
				self.answer = self.num1 + self.num2 
			elif prob <= 80 :
				self.question = str(self.num1) + ' - ' + str(self.num2) + ' = ?'
				self.answer = self.num1 - self.num2 
			elif prob <= 90 :
				self.question = str(self.num1) + ' * ' + str(self.num2) + ' = ?'
				self.answer = self.num1 * self.num2 
			elif prob <= 100 :
				self.question = str(self.num1 * self.num2) + ' / ' + str(self.num2) + ' = ?'
				self.answer = self.num1  
		elif difficulty == "medium" :
			self.num1 = random.randint(0, 20)
			self.num2 =	random.randint(1, 20)
			prob = random.randint(0, 100)
			if prob <= 35 :
				self.question = str(self.num1) + ' + ' + str(self.num2) + ' = ?'
				self.answer = self.num1 + self.num2 
			elif prob <= 70 :
				self.question = str(self.num1) + ' - ' + str(self.num2) + ' = ?'
				self.answer = self.num1 - self.num2 
			elif prob <= 85 :
				self.question = str(self.num1) + ' * ' + str(self.num2) + ' = ?'
				self.answer = self.num1 * self.num2 
			elif prob <= 100 :
				self.question = str(self.num1 * self.num2) + ' / ' + str(self.num2) + ' = ?'
				self.answer = self.num1 
		elif difficulty == "hard" :
			self.num1 = random.randint(10, 30)
			self.num2 =	random.randint(10, 15)
			prob = random.randint(0, 100)
			if prob <= 30 :
				self.question = str(self.num1) + ' + ' + str(self.num2) + ' = ?'
				self.answer = self.num1 + self.num2 
			elif prob <= 60 :
				self.question = str(self.num1) + ' - ' + str(self.num2) + ' = ?'
				self.answer = self.num1 - self.num2 
			elif prob <= 80 :
				self.question = str(self.num1) + ' * ' + str(self.num2) + ' = ?'
				self.answer = self.num1 * self.num2 
			elif prob <= 100 :
				self.question = str(self.num1 * self.num2) + ' / ' + str(self.num2) + ' = ?'
				self.answer = self.num1 						


q1 = MathQuestion("hard")
print q1.question + str(q1.answer)


		