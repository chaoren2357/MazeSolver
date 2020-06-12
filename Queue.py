class Queue(object):
	def __init__(self,items=[]):
		self.items = items
		self.length = len(items)
	def addQueue(self,item):
		if isinstance(item,list):
			self.items+=item
			self.length+=len(item)
		else:
			self.items.append(item)
			self.length+=1
	def isEmpty(self):
		return self.length==0
	def popOut(self):
		self.length -=1
		return self.items.pop(0)

