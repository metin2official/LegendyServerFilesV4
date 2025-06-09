import app, ui ,wndMgr, player 

class BloktanKurtar(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Initialize()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Initialize(self):
		self.bKurtar=0
	
	def Destroy(self):
		self.ClearDictionary()
		self.bKurtar=0

	def Open(self):
		self.SetPosition(110, wndMgr.GetScreenHeight()-110)
		self.SetTop()
		self.SetSize(32,50)
		self.AddFlag('movable')
		self.bKurtar = ui.Button()
		self.bKurtar.SetParent(self)
		self.bKurtar.SetUpVisual("d:/ymir work/bloktankurtar/bkurtar_1.tga")
		self.bKurtar.SetOverVisual("d:/ymir work/bloktankurtar/bkurtar_2.tga")
		self.bKurtar.SetDownVisual("d:/ymir work/bloktankurtar/bkurtar_3.tga")
		self.bKurtar.SetEvent(ui.__mem_func__(self.BloktanKurtar))
		self.bKurtar.SetPosition(0, 0)
		self.bKurtar.SetTop()
		self.bKurtar.Show()
		ui.ScriptWindow.Show(self)
		self.Hide()

	def GosterGizle(self,guiGG):
		if guiGG: self.Show()
		else: self.Hide()

	def BloktanKurtar(self):
		player.BloktanKurtar()
		self.GosterGizle(False)
		
		
