#    Quetz development version
#   Copyright (C) 2011 Milan Boers
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.gui.DirectGuiBase import DirectGuiWidget

class MainMenuWidget(DirectGuiWidget):
	def __init__(self):
		DirectGuiWidget.__init__(self)
		
		self.frame = DirectFrame(frameSize=(-1.5, 1.5, -1, 1), frameColor=(0.2, 0.2, 0.2, 0.7), pos=(0,0,0), parent=self)
		
		# Add widgets
		b = DirectLabel(text = "Enter server IP (v4): ", scale = .05, pos = (-0.2 , 0, 0.5 ),                          parent=self)
		self.serverEdit = DirectEntry(text = "" ,             scale = .05, pos = ( 0.05, 0, 0.5 ), command=self.setServer,       parent=self)
		
		b = DirectLabel(text = "Nickname: ",             scale = .05, pos = (-0.2 , 0, 0.4 ),                          parent=self)
		self.nicknameEdit = DirectEntry(text = "" ,           scale = .05, pos = ( 0.05, 0, 0.4 ), command=self.setNickname,     parent=self)
		
		b = DirectCheckButton(text = "Joypad support",   scale = .05, pos = ( 0   , 0, 0.3 ), command = self.setJoypad,     parent=self)
		b = DirectCheckButton(text = "Fullscreen",       scale = .05, pos = ( 0   , 0, 0.2 ), command = self.setFullscreen, parent=self)
		b = DirectButton(text = "New game",              scale = .05, pos = ( 0   , 0, 0.1 ), command=self.newGame,         parent=self)
		
		
		b = OnscreenText(text = "Quetz Menu",            scale = .07, pos = ( 0.95,-0.95), fg=(1,0.5,0.5,1),           parent=self)
		
		b = DirectButton(text = "Disconnect",            scale = .05, pos = ( 0   , 0, 0   ), command = self.disconnect, parent=self)
		
	def newGame(self):
		if self.serverEdit.get() == "":
			base.startGame(None, self.nicknameEdit.get())
		else:
			base.startGame(self.serverEdit.get(), self.nicknameEdit.get())
		self.destroy()
	
	def disconnect(self):
		base.stopGame()
	
	def setServer(self, textEntered):
		print textEntered
	
	def setNickname(self, textEntered):
		print setNickname
	
	def setJoypad(self, status):
		if status:
			base.joypad = modules.joypad.Joypad()
	
	def setFullscreen(self, status):
		if status:
			wp = WindowProperties()
			wp.setSize(base.pipe.getDisplayWidth(), base.pipe.getDisplayHeight())
			wp.setFullscreen(True)
			base.win.requestProperties(wp)
		else:
			wp = WindowProperties()
			wp.setFullscreen(False)
			base.win.requestProperties(wp)