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
		if random.choice(range(100)) > 80:
			x = random.choice(open('npc.txt').readlines()).split('\t')
			self.actor = Actor(x[1].strip())
			self.actor.desc = x[0] % self.actor.name
			self.actor.get_inv(random.choice(xrange(4)) + 1)
		else:
			x = random.choice(open('enemies.txt').readlines()).split('\t')
			self.actor = Enemy(x[1].strip())
			self.actor.desc = x[0] % self.actor.name


class Item(object):
	def __init__(self, chance):
		if chance <= 30 :
			self.weapon()
		elif chance <= 50:
			self.armor()
		else:
			self.consumable()


	def weapon(self):
		x = random.choice(open('weapons.txt').readlines()).split('\t')
		self.name = x[0]
		self.type = 'weapon'
		self.min_dmg = int(x[1])
		self.max_dmg = int(x[2])
		self.cost = int(x[4].strip())
		self.weapon_type = x[5].strip()
		# print "weapon is %s, damage range is %d-%d, cost is: %d" % (self.name,
																		self.min_dmg, self.max_dmg, self.cost)

	def armor(self):
		x = random.choice(open('armor.txt').readlines()).split('\t')
		self.name = x[0]
		self.type = 'armor'
		self.min_armor = int(x[1])
		self.max_armor = int(x[2])
		self.cost = int(x[4].strip())
		self.ac = self.min_armor + random.choice(xrange(self.max_armor - self.min_armor))
		# print "armor is is %s, armor range is %d-%d, cost is: %d, AC is %d" % (self.name,
																self.min_armor, self.max_armor, self.cost, self.ac)


	def consumable(self):
		self.type = 'consumable'
		self.name = 'potion'
		self.cost = 25

class Actor(object):
	def __init__(self, name):
		self.name = name
		self.gold = random.choice(xrange(25))
		self.inventory = []
		self.dead = False
		self.looted = False
		self.wit = random.choice(range(6))
		self.strength = random.choice(range(6))
		self.toughness = random.choice(range(6))
		self.agility = random.choice(range(6))
		self.hostile = False
		self.performances = 0
		self.performed = False
		self.sex = random.choice(['He', 'She'])
		self.weapon = None
		self.weapon_type = 'fist'
		self.min_dmg = 1
		self.max_dmg = 3
		self.armor = None
		self.equipped = []
		self.ac = 10 + (self.agility / 2)
		self.calc_stats()

	def calc_stats(self):
		if self.armor != None:
			self.ac = 10 + self.armor.ac + (self.agility /2)
		self.max_hp = 10 + self.toughness
		self.max_mp = 3 * self.wit
		self.curr_hp = self.max_hp
		self.curr_mp = self.max_mp

	def equip(self, attr):
		if attr == 'weapon':
			self.min_dmg += self.weapon.min_dmg
			self.max_dmg += self.weapon.max_dmg
			self.equipped.append(self.weapon)
		elif attr == 'armor':
			self.equipped.append(self.armor)
			self.calc_stats()

	def unequip(self, attr):
		if attr == 'weapon':
			self.min_dmg -= self.weapon.min_dmg
			self.max_dmg -= self.weapon.max_dmg
			self.equipped.remove(self.weapon)
		elif attr == 'armor':
			self.equipped.remove(self.armor)
			self.calc_stats()

	def get_inv(self, num):
		self.purchase = False
		self.first_time = False
		x = range(num)
		for i in x:
			item = Item(random.choice(xrange(100)))
			# print "chose %s" % item.name
			self.inventory.append(item)

	def status(self):
		print "Name: %s" % self.name
		print "HP: %d/%d" % (self.curr_hp, self.max_hp)
		print "MP: %d/%d" % (self.curr_mp, self.max_mp)
		print "AC: %d" % self.ac
		print "\nStats: \nStrength: %s\nAgility: %s\nToughness: %s\nWit: %s\n" % (
		self.strength, self.agility, self.toughness, self.wit)
		print "Gold: %d" % self.gold
		print "damage range is %d - %d" % ((player.min_dmg + player.strength), (player.strength + player.max_dmg))
		self.is_equipped()
		self.inv()

	def is_equipped(self):
		print "\nYou have equipped:"
		x = 0
		for i in self.equipped:
			print self.equipped[x].name
			x += 1

	def update_short_inv(self):
		"""count the number of instances of an item y for readable inv printing."""
		x = 0
		inv = []
		for i in player.inventory:
			# print player.inventory[x].name
			inv.append(player.inventory[x].name)
			x +=1
		player.short_inv = {y:inv.count(y) for y in inv}

	def inv(self):
		"""Adds the player's current unique inventory items to a dict as keys with
		number of repititions as values, then prints it for the player"""
		self.update_short_inv()
		print "You are carrying:"
		print "Gold: %d" % self.gold
		for i in player.short_inv:
			print "%dx %s" % (player.short_inv[i], ''.join(i))
		print '-----------'


# learn more class inheritance dummeh
class Enemy(Actor):
	def __init__(self, name):
		super(Enemy, self).__init__(name)
		self.hostile = True
		self.gold = random.choice(range(50))
		if room_num >= 1:
			self.inventory.append(get_item())
			# print "equipping %s with %s" % (self.name, self.inventory[0].name)

		else:
			# print "%s has nothing to equip." % self.name
			pass

def get_item():
	x = range(100)
	if x >= 0:
		item = Item(10)
	return item
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
	"""As near as i can tell, this takes player input as arg, and checks for a specific value present in the arg.
	It will return bool valid and set arg to the value being checked for.
	eg. kill the motherfuckin skeleton will return skeleton if check is curr_room.actor.name and there's a skeleton in the room."""
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

def combat(p1, p2):
	print p1.name, "VS", p2.name
	print "-" * len(p1.name + ' vs ' + p2.name)
	x = random.choice(xrange(20)) + p1.strength
	if x >= p2.ac:
		damage = p1.min_dmg + random.choice(xrange(p1.max_dmg - p1.min_dmg)) + p1.strength
		p2.curr_hp = p2.curr_hp - damage
		if p1.name == player.name:

			if p2.curr_hp <= 0:
				p2.dead = True
				print "You %s the %s for %d damage.\n" % (random.choice(attack_dict[p1.weapon_type]), p2.name, damage)
				print "You slay the [%s]" % p2.name
			else:
				print "You %s the %s for %d damage." % (random.choice(attack_dict[p1.weapon_type]), p2.name, damage)
				print "The %s has %d health remaining\n" % (p2.name, p2.curr_hp)
				combat(p2, p1)
		else:
			if p2.curr_hp <= 0:
				global dead
				dead = True
				print "The %s %ss you for %d damage." % (p1.name, random.choice(attack_dict[p1.weapon_type]), damage)
				death(p1.name)
			else:
				print "The %s %ss you for %d damage." % (p1.name, random.choice(attack_dict[p1.weapon_type]), damage)
				print "you have %d health remaining.\n" % p2.curr_hp
				combat(p2, p1)
	else:
		print 'You miss. Attack roll was %d' % x
# enemy attacks


def equip(arg):
	arg = ''.join(arg)
	if arg in player.short_inv.keys():  # therefore we know player has item to equip
# 		so we know it exists, but not what the element is.
		x = 0
		for i in player.inventory:
			if arg in player.inventory[x].name:
				inv_element = x
			else:
				x += 1
# 		figure out what type of item is being equipped
		if player.inventory[inv_element].type == 'armor':
			equip_armor(inv_element)
		elif player.inventory[inv_element].type == 'weapon':
			equip_weapon(inv_element)
		else: # TODO change this when adding scrolls
			use(potion)

	else:
		print "You dont have a %s to equip." % arg


def equip_weapon(inv_element):
# 		player is equipping a weapon
		if player.weapon != None:
			player.inventory.append(player.weapon)
			print "You unequip your %s." %player.weapon.name
			player.unequip('weapon')
			player.weapon = player.inventory[inv_element]
			player.weapon_type = player.weapon.weapon_type
			player.inventory.remove(player.inventory[inv_element])
			print "You equip your %s." % player.weapon.name
			player.equip('weapon')
			player.update_short_inv()

		else:
			player.weapon = player.inventory[inv_element]
			player.weapon_type = player.weapon.weapon_type
			player.inventory.remove(player.inventory[inv_element])
			print "You equip your %s." % player.weapon.name
			player.equip('weapon')
			player.update_short_inv()

def equip_armor(inv_element):
		if player.armor != None:
			player.inventory.append(player.armor)
			print 'You unequip your %s.' % player.armor.name
			player.unequip('armor')
			player.armor = player.inventory[inv_element]
			player.inventory.remove(player.inventory[inv_element])
			print "You don your %s." % player.armor.name
			player.equip('armor')
			player.update_short_inv
		else:
			player.armor = player.inventory[inv_element]
			player.inventory.remove(player.inventory[inv_element])
			print "You don your %s." % player.armor.name
			player.equip('armor')
			player.update_short_inv

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
				combat(player, curr_room.actor)
				# curr_room.actor.dead = True
				# print "You slay the [%s]." % curr_room.actor.name
			elif curr_room.actor.dead == True and arg == curr_room.actor.name:
				print "You have already slain the [%s]" % curr_room.actor.name
			else:
				print "There is no %s to attack." % arg

def status(x):
	player.status()

def inv(x):
	player.inv()

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
		elif curr_room.actor.dead == True and valid[0] == True:
			print "You eye the corpse of the %s" % curr_room.actor.name
		else:
			pass

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
	print "Choose your class, %s." % player.name
	print "1. Warrior"
	x = raw_input('> ').lower()
	if '1' or 'warrior' in x:
		player.strength += 3
		player.agility += 1
		player.toughness += 3
	else:
		print "You should have chosen a class..."
	player.gold = 5 + random.choice(xrange(20))
	player.calc_stats()



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
	try:
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
	except IndexError:
		print "Can't have none o' that..."
		store(name)


def buy(name):
	print "Come closer, take a look at my wares."
	y = 1
	for i in curr_room.actor.inventory:
		print "%d. %s: %d gold" % (y, curr_room.actor.inventory[y - 1].name,
		curr_room.actor.inventory[y - 1].cost)
		y += 1
	j = int(raw_input('> '))
	if type(j) == int and player.gold >= curr_room.actor.inventory[j - 1].cost:
		player.inventory.append(curr_room.actor.inventory[j - 1])
		player.gold -= curr_room.actor.inventory[j - 1].cost
		print "one %s coming up." % curr_room.actor.inventory[j - 1].name
		curr_room.actor.inventory.remove(curr_room.actor.inventory[j-1])
		player.update_short_inv()
		curr_room.actor.purchase = True
		curr_room.actor.first_time = True
		store(name)
	else:
		print "You can't afford that."
		store(name)


def potion(arg):
	if player.curr_hp < player.max_hp:
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
	x = 0
	for i in player.inventory:
		if arg in player.inventory[x].name:
			inv_element = x
			valid = True
		else:
			x += 1

	if valid == True:
		if arg == 'potion':
			potion(player.inventory[inv_element])
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
				print "%d gold." % curr_room.actor.gold
				player.gold += curr_room.actor.gold
				for i in curr_room.actor.inventory:
					print getattr(i, 'name')
				print "You place these items into your backpack."
				x = len(curr_room.actor.inventory)
				for i in range(x):
					player.inventory.append(curr_room.actor.inventory.pop())
				curr_room.actor.looted = True
				player.update_short_inv()
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

def death(killer):
	print "--------------------------"
	print "\n\nYou perished at the hands of a %s" % killer
	print "You explored %d rooms" % len(rooms)
	print "\n Restart?"
	r = raw_input('> ').lower()
	if 'y' in r:
		start()
	else:
		exit(0)

def start():
	global dead
	dead = False
	rooms = []
	curr_room = None
	prev_room = None
	room_num = -1
	print "-" * 50
	print "         COZMIX: THE QUEST FOR COMPLETION"
	print "-" * 50
	print "Inputs are [go], [look], [equip], [help], [inventory]"
	create_player()
	print "\nWelcome %s.  Good Luck." % player.name
	get_roomz(None)
	input()


slashing = [
'slash',
'slice'
]

blunt = [
'crush',
'pummel',
'smash'
]

piercing = [
'stab',
'puncture',
'pierce'
]

fist = [
'slap',
'punch',
'caress',
'kick',
'pummel',
'knee'
]

attack_dict = {
'fist': fist,
"slashing": slashing,
"piercing": piercing,
"blunt": blunt
}

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
'inv': inv,
'inventory': inv,
'equip': equip,
'use': equip
}

price = {
'potion': 10,
'sword': 20,
'armor': 50,
}

rooms = []

start()
