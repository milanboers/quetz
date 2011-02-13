# this file belongs to snake.py

import socket
import threading
import thread
import json
import zlib
import time
import SocketServer

PORT = 44454
TIMEOUT_TIME = 1

class PlayerInWorld(object):
	def __init__(self, x, y, z, h, addr):
		self.x = x
		self.y = y
		self.z = z
		self.h = h
		self.addr = addr

class TailObjectInWorld(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class World(object):
	"""
	Models the World as it currently looks like on the server
	"""
	def __init__(self):
		self.players = []
	
	def updatePlayer(self, x, y, z, h, addr):
		playerFound = False
		for player in self.players:
			if player.addr == addr:
				player.x = x
				player.y = y
				player.z = z
				player.h = h
				playerFound = True
				break
		
		if not playerFound:
			#add player
			self.players.append(PlayerInWorld(x, y, z, h, addr))
			print "PLAYER " + str(addr) + " ADDED"
	
	def removePlayer(self, addr):
		for player in self.players:
			if player.addr == addr:
				self.players.remove(player)
				print "PLAYER " + str(addr) + " KICKED"
	
	def getPlayersNotSelf(self, addr):
		playersNotSelf = []
		for player in self.players:
			# Not the player who is asking
			if player.addr <> addr:
				playersNotSelf.append([player.addr, player.x, player.y, player.z, player.h])
		
		#return the players
		return playersNotSelf


class ClientConnection(object):
	def __init__(self, socket, addr, world):
		self.socket = socket
		self.addr = addr
		self.world = world
		
		self.lastrequest = time.time()
		
		thread.start_new_thread(self.checkTimeout, ())
	
	def addData(self, data):
		self.lastrequest = time.time()
		if data == "REQ WORLD":
			# Send the players
			self.socket.sendto("PLAYERS " + zlib.compress(json.dumps(self.world.getPlayersNotSelf(self.addr))), self.addr)
		elif data[0:10] == "SEND P POS":
			try:
				position = json.loads(zlib.decompress(data[11:]))
				self.world.updatePlayer(position[0], position[1], position[2], position[3], self.addr)
			except ValueError:
				pass
	
	def checkTimeout(self):
		while True:
			if time.time() - self.lastrequest > TIMEOUT_TIME:
				self.remove()
				print "PLAYER TIMEOUT " + str(self.addr)
				break
	
	def remove(self):
		self.world.removePlayer(self.addr)


class UDPHandler(object):
	def __init__(self, world, socket):
		self.connectedClients = []
		self.world = world
		self.socket = socket
	
	def handle(self, data, addr):
		for client in self.connectedClients:
			if client.addr == addr:
				client.addData(data)
				break
		else:
			client = self.addClient(addr)
			client.addData(data)
	
	def addClient(self, addr):
		client = ClientConnection(self.socket, addr, self.world)
		self.connectedClients.append(client)
		return client
	
	def removeClient(self, addr):
		for client in self.connectedClients:
			if client.addr == addr:
				client.remove()
				self.connectedClients.remove(client)
				break

class SnakeServer():
	def __init__(self, port):
		print "SNAKE SERVER v 0.01 STARTED"
		
		# Setup the world as it looks like on this server
		world = World()
		print "INITIATED WORLD"
		
		# Setup the socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind(("", port))
		
		self.udphandler = UDPHandler(world, self.socket)
		
		# The daemon
		while True:
			try:
				data, addr = self.socket.recvfrom(1024)
				self.udphandler.handle(data, addr)
			except socket.error:
				# something went wrong, but we have to keep on going for all other clients
				self.udphandler.removeClient(addr)
				pass

server = SnakeServer(PORT)