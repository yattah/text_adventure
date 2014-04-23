import random
import collections
global taunts
global verblist
prev_room = None
curr_room = None
global room_num
room_num = -1

class Room(object):
	def __init__(self):
		global room_num
		self.name = self
		self.feature = None
		self.get_desc()
		self.exitf = random.choice(directions)
		self.exitb = ''
		self.visited = False
		room_num += 1
		self.room_num = room_num
		self.actor = None
		rooms.append(self)
		if random.choice(range(100)) > 20:
			self.get_actor()
		else:
			pass

	def get_desc(self):
		x = random.choice(open('rooms.txt').readlines()).split('\t')
		self.desc = x[0].strip()
		if len(x) > 1:
			self.feature = x[1].strip()
			self.feature_lootable = x[2].strip()
		else:
			pass

	def get_exitf(self):
		self.exitf = random.choice(directions)
		if self.exitf == roomlink[rooms[self.room_num - 1].exitf]:
			while self.exitf == self.exitb:
				self.exitf = random.choice(directions)
		else:
			pass

	def get_actor(self):
		if random.choice(range(100)) > 10:
			x = random.choice(open('npc.txt').readlines()).split('\t')
			self.actor = Actor(x[1].strip())
			self.actor.desc = x[0] % self.actor.name
			self.actor.get_inv()
		else:
			x = random.choice(open('enemies.txt').readlines()).split('\t')
			self.actor = Enemy(x[1].strip())
			self.actor.desc = x[0] % self.actor.name
# 		self.actor.inventory = ['potion']


class Actor(object):
	def __init__(self, name):
		self.name = name
		self.gold = 100
		self.inventory = []
		self.dead = False
		self.looted = False
		self.wit = random.choice(range(6))
		self.strength = random.choice(range(6))
		self.toughness = random.choice(range(6))
		self.agility = random.choice(range(6))
		self.max_hp = 10 + self.toughness
		self.max_mp = 3 * self.wit
		self.curr_hp = self.max_hp
		self.curr_mp = self.max_mp
		self.hostile = False
		self.performances = 0
		self.performed = False
		self.sex = random.choice(['He', 'She'])

	def get_inv(self):
		self.purchase = False
		self.first_time = False
		x = random.choice(range(4)) + 1
		print "getting %d items for mechant inv" % x
		x = range(x)
		for i in x:
			self.inventory.append(random.choice(price.keys()))

	def status(self):
		print "Name: %s" % self.name
		print "HP: %d/%d" % (self.curr_hp, self.max_hp)
		print "MP: %d/%d" % (self.curr_mp, self.max_mp)
		print "\nStats: \nStrength: %s\nAgility: %s\nToughness: %s\nWit: %s\n" % (
		self.strength, self.agility, self.toughness, self.wit)
		print "Gold: %d" % self.gold
		self.inv()


	def inv(self):
		d = {x:player.inventory.count(x) for x in player.inventory}
		for i in d:
			print "%dx %s" % (d[i], ''.join(i))


# learn more class inheritance dummeh
class Enemy(Actor):
	def __init__(self, name):
		super(Enemy, self).__init__(name)
		self.hostile = True
		self.gold = random.choice(range(50))


def move(arg):
	global curr_room
	arg = ' '.join(arg)
	if arg in curr_room.exitf:
		get_roomz(arg)
	elif arg in curr_room.exitb:
		room_loader(curr_room.room_num - 1)
		enter_room(curr_room)
	else:
		print "You can't go that way."
# 		print "debug: you tried to go %r" % arg
		print "current room exits to %s, %s" % (curr_room.exitf, curr_room.exitb)


def input_checker(arg, check):
# 	print "does this work?"
	arg = ''.join(arg).split(' ')
# 	print "arg is %r, check is %r\n" % (arg, check)
	valid = False
	try:
		j = 0
		for i in arg:
# 			print "i is %r" % i
# 			print "looped %d times" % j
			if check in arg[j]:
				arg = check
				valid = True
# 				print "set arg to", arg
			else:
				j += 1
	except AttributeError:
		print "you have attribute errored"
		valid = False
		return valid
# 	print "valid is: %s\n" % valid
	return valid, arg



def attack(arg):
	if 'darkness' in arg:
		print "You cast magic missle at the darkness."
	elif curr_room.actor == None:
		print "There is nothing here to attack."
	else:
		valid = input_checker(arg, curr_room.actor.name)
		if valid[0] != True:
			print "Instead of doing that, you dont."
		else:
			arg = valid[1]
			if curr_room.actor.dead == False:
				curr_room.actor.dead = True
				print "You slay the [%s]." % curr_room.actor.name
			elif curr_room.actor.dead == True and arg == curr_room.actor.name:
				print "You have already slain the [%s]" % curr_room.actor.name
			else:
				print "There is no %s to attack." % arg

def status(x):
	print player.status()


def room_loader(num):
	global curr_room
	curr_room = rooms[num]


def look(arg):
#  	arg = ''.join(arg)
	tits = False
	if curr_room.actor != None:
		valid = input_checker(arg, curr_room.actor.name)
		if valid[0] == True:
			print "You eye the %s. %s %s you." % (valid[1],
			curr_room.actor.sex, random.choice(taunts))
			tits = True

 	if curr_room.feature != None and tits == False:
		valid = input_checker(arg, curr_room.feature)
		if valid[0] == True:
			print "you look at the %s" % curr_room.feature
			print "It looks expensive, but not too ostentatious or anything."
			print "After all, this is a dungeon."
			tits = True

	if (curr_room.actor != None and curr_room.actor.dead == False and tits == False):
		print "You see a %s" % curr_room.actor.name
	elif curr_room.actor != None and curr_room.actor.dead == True:
		if curr_room.actor.looted == True:
			print "The corpse of a %s lies on the floor" % curr_room.actor.name
		else:
			print "The corpse of a [%s] lies on the floor" % curr_room.actor.name

	if tits == True:
		pass
	elif tits == False and curr_room.feature != None:
		print "You are in", (curr_room.desc % curr_room.feature)
		print "Exits are [%s], [%s]" % (curr_room.exitf, curr_room.exitb)
	else:
		print "You are in", curr_room.desc
		print "Exits are [%s], [%s]" % (curr_room.exitf, curr_room.exitb)


def create_player():
	global player
	name = raw_input('Enter Your Name\n> ')
	player = Actor(name)
	player.inventory = ['potion', 'potion', 'armor']


def examine(arg):
	n = random.choice(xrange(20)) + player.wit
	if n >= 15:
		print "You examine the %s for %d" % (arg, n)
		print "You find a %s" % 'dick'
	else:
		print "you examine the %s and find nothing unusual." % arg
	print "Perception: %d" % n


def enter_room(room):
# 	print "entering room no.%d" % curr_room.room_num
	if curr_room.visited == True:
		print "You retrace your steps"
	else:
		curr_room.visited = True

	if room.feature == None:
		print "<------>\nYou enter", room.desc
	else:
		print "<------>\nYou enter", room.desc % room.feature

	if curr_room.actor != None and curr_room.actor.dead == False:
		print curr_room.actor.desc
	elif curr_room.actor != None and curr_room.actor.dead == True:
		if curr_room.actor.looted == True:
			print "The corpse of a %s lies on the floor" % curr_room.actor.name
		else:
			print "The corpse of a [%s] lies on the floor" % curr_room.actor.name
	else:
		pass
	print "Exits are [%s] [%s]" % (room.exitf, room.exitb)


def get_roomz(arg):
	"""This func will check to see if players are going forward or backward, and
	generate or load a room accordingly"""
	global rooms
	global curr_room
	global room_num
	x = random.choice(xrange(100))
	if curr_room == None:
		curr_room = Room()
		enter_room(curr_room)
	elif (curr_room.room_num < room_num):
		room_loader(curr_room.room_num + 1)
		enter_room(curr_room)
	else:
		curr_room = Room()
		curr_room.exitb = roomlink[rooms[curr_room.room_num - 1].exitf]
		curr_room.get_exitf()
		enter_room(curr_room)


def store(name):
	print "\n%s:" % name
	if curr_room.actor.first_time == False:
		print "Welcome to my shop.  What do you want to do?"
	else:
		print "Would you like to do anything else?"
	print "1: buy\n2: sell\n3: leave"
	x = raw_input('> ')
	if ('1' or 'buy') in x:
		buy(name)
	elif ('2' or 'sell') in x:
		print "I can't buy anything right now."
	elif ('3' or 'leave') in x and curr_room.actor.purchase == True:
		print "%s: \nDon't be a stranger! I've got plenty more where that came from!" % name
	elif ('3' or 'leave') in x:
		print "%s: \nWell don't mind me, not like its hard to make a living" % name
		print "in a creepy dungeon or anything.  \nI've got kids to feed!"
	else:
		print "I don't understand you good sir."
		store(name)


def buy(name):
	print "Come closer, take a look at my wares."
	y = 1
	for i in curr_room.actor.inventory:
		print "%d. %s: %d gold" % (y, curr_room.actor.inventory[y - 1],
		price[curr_room.actor.inventory[y - 1]])
		y += 1
	j = int(raw_input('> '))
	if type(j) == int:
		player.inventory.append(curr_room.actor.inventory[j - 1])
		player.gold -= price[curr_room.actor.inventory[j - 1]]
		print "one %s coming up." % curr_room.actor.inventory[j - 1]
		curr_room.actor.purchase = True
		curr_room.actor.first_time = True
		store(name)
	else:
		print "cant buy that shit"


def potion(arg):
	if arg in player.inventory and player.curr_hp < player.max_hp:
		player.inventory.remove(arg)
		x = random.choice(xrange(5)) + player.wit
		player.curr_hp += x
		if player.curr_hp > player.max_hp:
			player.curr_hp = player.max_hp
			print "You are fully healed."
		else:
			print "healed for %d" % x
			print "Health is now %d/%d" % (player.curr_hp, player.max_hp)
	else:
		print "You are already fully healed."


def use(arg):
	arg = ''.join(arg)
	if arg in player.inventory:
		if arg == 'potion':
			potion(arg)
		elif arg == 'scroll':
# 			scroll()
			print "scrolls leel"
		else:
			print "elesed out"
	else:
		print "You don't have a %s" % arg


def take(arg):
# 	''.join(arg)
	try:
		if curr_room.actor.dead == True and curr_room.actor.name in arg:
			if curr_room.actor.looted == False:
				print "You search the corpse of the %s and find:" % curr_room.actor.name
				print curr_room.actor.inventory
				print "You place these items into your backpack."
				x = len(curr_room.actor.inventory)
				for i in range(x):
					player.inventory.append(curr_room.actor.inventory.pop())
				curr_room.actor.looted = True
			else:
				print "You search the corpse but find no additional valuables."
	except TypeError:
		print "type error 1"
# 	try:
# 		if arg in curr_room.feature and curr_room.feature_lootable == 'True':
# 			player.inventory.append(curr_room.feature)
# 			print "You take the %s" % curr_room.feature
# 			curr_room.feature = "missing %s" %curr_room.feature
# 			player.status()
# 			look('room')
# 		else:
# 			print "You cannot take that."
# 	except TypeError:
# 		print "type error 2"


def talk(arg):
  	arg = ' '.join(arg)
	try:
		if curr_room.actor.name in arg and curr_room.actor.dead == False:
			print "You approach the %s." % curr_room.actor.name
			if curr_room.actor.hostile == True:
				attack(curr_room.actor.name)
			else:
				store(curr_room.actor.name)
		elif curr_room.actor.dead == True and curr_room.actor.performed == False:
			player.performances += 1
			print "You recite poetry to the %s's corpse, but get no response." % curr_room.actor.name
			print "You have performed %d times without being booed." % player.performances
			curr_room.actor.performed = True
		elif curr_room.actor.dead == True:
			print "You recite poetry to the %s's corpse, and it eyes you sorrowfully." % curr_room.actor.name
			print "Your second stanza is so terrible that the %s's corpse explodes." % curr_room.actor.name
			curr_room.actor = None
		else:
			print "You cannot talk to that."
	except AttributeError:
		print "excepted: There is no %s to talk to." % arg


def execprint(arg):
	x = arg.split()
	for i in ', ':
		x = i.join(x).split(i)
	if x:
		if not x[0] in verblist:
			print "I dont understand that"
		else:
			func = verblist[x[0]]
			args = x[1:]
# 			args = ''.join(x[1:])
			func(args)


def input(store = False):
	while not dead:
		x = raw_input('> ').lower()
		if (x == 'q' or x == 'quit'):
			exit(0)
		elif store == True:
			return x
		else:
			print "\n"
			execprint(x)


def start():
	global dead
	dead = False
	print "-" * 50
	print "         COZMIX: THE QUEST FOR COMPLETION"
	print "-" * 50
	print "Inputs are [go], [look], [equip], [help], [inventory]"
	create_player()
	print "\nWelcome %s.  Good Luck." % player.name
	get_roomz(None)
	input()


taunts = [
'jeers at',
'beckons toward',
'menaces',
'leers at',
'glares at',
'taunts at',
'ignores',
'regards'
]

directions = [
'north',
'south',
'east',
'west'
]

roomlink = {
'north': 'south',
'east': 'west',
'south': 'north',
'west': 'east'
}

verblist = {
"look": look,
"examine": examine,
"go": move,
"talk": talk,
'attack': attack,
'kill': attack,
'buy': buy,
'status': status,
'drink': use,
'take': take,
'loot': take,
'inv': status,
'inventory': status
}

price = {
'potion': 10,
'sword': 20,
'armor': 50,
}

rooms = []

start()
