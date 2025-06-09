import ui
import player
import mouseModule
import ime
import net
import app
import snd
import item
import chat
import uiScriptLocale
import uiCommon
import uiPrivateShopBuilder
import uiPickMoney
import localeInfo
import constInfo
import interfacemodule

if app.__ENABLE_NEW_OFFLINESHOP__:
	import offlineshop
	import uinewofflineshop

INVANTORY_ADET = 4

class SpecialStorageWindow(ui.ScriptWindow):
	UPGRADE_TYPE = 0
	BOOK_TYPE = 1
	STONE_TYPE = 2
	CHEST_TYPE = 3
	remaining_time = 0

	SLOT_WINDOW_TYPE = {
		UPGRADE_TYPE	:	{"window" : player.UPGRADE_INVENTORY,	"slot" : player.SLOT_TYPE_UPGRADE_INVENTORY},
		BOOK_TYPE		:	{"window" : player.BOOK_INVENTORY,		"slot" : player.SLOT_TYPE_BOOK_INVENTORY},
		STONE_TYPE		:	{"window" : player.STONE_INVENTORY,		"slot" : player.SLOT_TYPE_STONE_INVENTORY},
		CHEST_TYPE		:	{"window" : player.CHEST_INVENTORY,		"slot" : player.SLOT_TYPE_CHEST_INVENTORY}
	}

	WINDOW_NAMES = {
		UPGRADE_TYPE	:	"Yükseltme Envanteri",
		BOOK_TYPE		:	"Kitap Envanteri",
		STONE_TYPE		:	"Taþ Envanteri",
		CHEST_TYPE		:	"Sandýk Envanteri"
	}


	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.questionDialog = None
		self.tooltipItem = None
		self.dlgSplitItems = None
		self.wndItemDelete = None
		self.interface = None
		self.sellingSlotNumber = -1
		self.isLoaded = 0
		self.inventoryPageIndex = 0
		self.categoryPageIndex = 0
		self.SetWindowName("SpecialStorageWindow")
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/SpecialStorageWindow.py")
		except:
			import exception
			exception.Abort("SpecialStorageWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.titleName = self.GetChild("TitleName")

			self.inventoryTab = []
			#self.inventoryTab.append(self.GetChild("Inventory_Tab_01"))
			#self.inventoryTab.append(self.GetChild("Inventory_Tab_02"))
			#self.inventoryTab.append(self.GetChild("Inventory_Tab_03"))
			#self.inventoryTab.append(self.GetChild("Inventory_Tab_04"))

			self.categoryTab = []
			self.categoryTab.append(self.GetChild("Category_Tab_01"))
			self.categoryTab.append(self.GetChild("Category_Tab_02"))
			self.categoryTab.append(self.GetChild("Category_Tab_03"))
			self.categoryTab.append(self.GetChild("Category_Tab_04"))
			self.ScrollBar = self.GetChild("ScrollBar")
			self.SiralaButton = self.GetChild("SiralaButton")

		except:
			import exception
			exception.Abort("SpecialStorageWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))

		self.envanterileacilsin = ui.CheckBox()
		self.envanterileacilsin.SetParent(self)
		self.envanterileacilsin.SetPosition(43, 395)
		self.envanterileacilsin.SetEvent(ui.__mem_func__(self.__OnClickEnableEnvanterOn), "ON_CHECK", True)
		self.envanterileacilsin.SetEvent(ui.__mem_func__(self.__OnClickDisableEnvanterOf), "ON_UNCKECK", False)
		self.envanterileacilsin.SetTextInfo("Envanter ile açýlsýn ?")
		self.envanterileacilsin.SetCheckStatus(constInfo.EnvanterAcilsinmi)
		self.envanterileacilsin.Show()

		## Grade button
		# self.inventoryTab[0].SetEvent(lambda arg=0: self.SetInventoryPage(arg))
		# self.inventoryTab[1].SetEvent(lambda arg=1: self.SetInventoryPage(arg))
		# self.inventoryTab[2].SetEvent(lambda arg=2: self.SetInventoryPage(arg))
		# self.inventoryTab[3].SetEvent(lambda arg=3: self.SetInventoryPage(arg))
		# self.inventoryTab[0].Down()

		self.categoryTab[0].SetEvent(lambda arg=0: self.SetCategoryPage(arg))
		self.categoryTab[1].SetEvent(lambda arg=1: self.SetCategoryPage(arg))
		self.categoryTab[2].SetEvent(lambda arg=2: self.SetCategoryPage(arg))
		self.categoryTab[3].SetEvent(lambda arg=3: self.SetCategoryPage(arg))
		self.categoryTab[0].Down()

		## Etc
		self.wndItem = wndItem

		self.wndPopupDialog = uiCommon.PopupDialog()

		self.dlgSplitItems = uiPickMoney.PickMoneyDialog()
		self.dlgSplitItems.LoadDialog()
		self.dlgSplitItems.Hide()

		self.ScrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.Diff = (9*player.SPECIAL_PAGE_COUNT) - 9
		stepSize = 1.0 / self.Diff
		if self.SiralaButton:
			self.SiralaButton.SetEvent(ui.__mem_func__(self.ClickSirala))

		if app.ENABLE_HIGHLIGHT_NEW_ITEM:
			self.listHighlightedSlotBook = []
			self.listHighlightedSlotUpgrade = []
			self.listHighlightedSlotStone = []
			self.listHighlightedSlotChest = []

		#self.SetInventoryPage(0)
		self.SetCategoryPage(0)
		self.RefreshItemSlot()
		self.RefreshBagSlotWindow()

	def OnScroll(self):
		self.RefreshBagSlotWindow()

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.wndItem = 0
		self.questionDialog = None
		self.dlgSplitItems.Destroy()
		self.dlgSplitItems = None
		self.inventoryTab = []
		self.categoryTab = []
		self.titleName = None
		self.interface = None
		self.editButton = None
		self.envanterileacilsin = []

	def __OnClickEnableEnvanterOn(self):
		constInfo.EnvanterAcilsinmi = 1
		chat.AppendChat(chat.CHAT_TYPE_INFO, "<Sistem> Envanter ile açýlma aktif.")

	def __OnClickDisableEnvanterOf(self):
		constInfo.EnvanterAcilsinmi = 0
		chat.AppendChat(chat.CHAT_TYPE_INFO, "<Sistem> Envanter ile açýlma pasif.")

	if app.ENABLE_HIGHLIGHT_NEW_ITEM:
		def HighlightSlot(self, slot, inven_type):
			if inven_type == player.BOOK_INVENTORY:
				if not slot in self.listHighlightedSlotBook:
					self.listHighlightedSlotBook.append(slot)
			elif inven_type == player.UPGRADE_INVENTORY:
				if not slot in self.listHighlightedSlotUpgrade:
					self.listHighlightedSlotUpgrade.append(slot)
			elif inven_type == player.STONE_INVENTORY:
				if not slot in self.listHighlightedSlotStone:
					self.listHighlightedSlotStone.append(slot)
			elif inven_type == player.CHEST_INVENTORY:
				if not slot in self.listHighlightedSlotChest:
					self.listHighlightedSlotChest.append(slot)

		def __RefreshHighlights(self):
			for i in xrange(player.SPECIAL_PAGE_SIZE):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.BOOK_INVENTORY:
					if slotNumber in self.listHighlightedSlotBook:
						self.wndItem.ActivateSlot(i)
				elif self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.UPGRADE_INVENTORY:
					if slotNumber in self.listHighlightedSlotUpgrade:
						self.wndItem.ActivateSlot(i)
				elif self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.STONE_INVENTORY:
					if slotNumber in self.listHighlightedSlotStone:
						self.wndItem.ActivateSlot(i)
				elif self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.CHEST_INVENTORY:
					if slotNumber in self.listHighlightedSlotChest:
						self.wndItem.ActivateSlot(i)

	def BindInterfaceClass(self, interface):
		self.interface = interface

	def Close(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		if self.dlgSplitItems:
			self.dlgSplitItems.Close()
		self.Hide()

	#def SetInventoryPage(self, page):
		#self.inventoryTab[self.inventoryPageIndex].SetUp()
	#	self.inventoryPageIndex = page
		#self.inventoryTab[self.inventoryPageIndex].Down()

		#self.RefreshBagSlotWindow()
	#	self.RefreshBagSlotInventoryWindow(page+1)

	def SetCategoryPage(self, page):
		self.categoryTab[self.categoryPageIndex].SetUp()
		self.categoryPageIndex = page
		self.categoryTab[self.categoryPageIndex].Down()

		self.titleName.SetText(self.WINDOW_NAMES[self.categoryPageIndex])
		self.RefreshBagSlotWindow()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()

	def RefreshStatus(self):
		self.RefreshItemSlot()

	def __InventoryLocalSlotPosToGlobalSlotPos(self, localSlotPos):
		#return self.inventoryPageIndex * player.SPECIAL_PAGE_SIZE + localSlotPos
		self.ScollPos = int(self.ScrollBar.GetPos() * self.Diff)
		return localSlotPos + (self.ScollPos*5)

	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex

	def GetInventoryWindow(self):
		return self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"]
		
	def GetInventoryType(self):
		return self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"]

	def RefreshBagSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVnum=self.wndItem.SetItemSlot

		self.ScollPos = int(self.ScrollBar.GetPos() * self.Diff)
		for i in xrange(player.SPECIAL_PAGE_SIZE*INVANTORY_ADET):
			self.wndItem.EnableSlot(i)
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)
			itemVnum = getItemVNum(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)

			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			setItemVnum(i, itemVnum, itemCount)

			if app.ENABLE_HIGHLIGHT_NEW_ITEM:
				if self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.BOOK_INVENTORY:
					if not slotNumber in self.listHighlightedSlotBook:
						self.wndItem.DeactivateSlot(i)
				elif self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.UPGRADE_INVENTORY:
					if not slotNumber in self.listHighlightedSlotUpgrade:
						self.wndItem.DeactivateSlot(i)
				elif self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.STONE_INVENTORY:
					if not slotNumber in self.listHighlightedSlotStone:
						self.wndItem.DeactivateSlot(i)
				elif self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.CHEST_INVENTORY:
					if not slotNumber in self.listHighlightedSlotChest:
						self.wndItem.DeactivateSlot(i)

		self.wndItem.RefreshSlot()
		if app.ENABLE_HIGHLIGHT_NEW_ITEM:
			self.__RefreshHighlights()

	def RefreshBagSlotInventoryWindow(self, page):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVnum=self.wndItem.SetItemSlot

		for i in xrange(player.SPECIAL_PAGE_SIZE*INVANTORY_ADET):
			self.wndItem.EnableSlot(i)
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)
			itemVnum = getItemVNum(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)

			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			setItemVnum(i, itemVnum, itemCount)

		self.wndItem.RefreshSlot()


	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"])
			if app.__ENABLE_NEW_OFFLINESHOP__:
				if uinewofflineshop.IsBuildingShop() or uinewofflineshop.IsBuildingAuction():
					self.__AddTooltipSaleMode(slotIndex)

	if app.__ENABLE_NEW_OFFLINESHOP__:
		def __AddTooltipSaleMode(self, slot):
			win = self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"]
			itemIndex = player.GetItemIndex(win, slot)
			if itemIndex !=0:
				item.SelectItem(itemIndex)
				if item.IsAntiFlag(item.ANTIFLAG_MYSHOP) or item.IsAntiFlag(item.ANTIFLAG_GIVE):
					return
				
				self.tooltipItem.AddRightClickForSale()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		overSlotPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		self.wndItem.SetUsableItem(False)

		if app.ENABLE_HIGHLIGHT_NEW_ITEM:
			if self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.BOOK_INVENTORY:
				if overSlotPosGlobal in self.listHighlightedSlotBook:
					self.listHighlightedSlotBook.remove(overSlotPosGlobal)
					self.wndItem.DeactivateSlot(overSlotPos)
			elif self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.UPGRADE_INVENTORY:
				if overSlotPosGlobal in self.listHighlightedSlotUpgrade:
					self.listHighlightedSlotUpgrade.remove(overSlotPosGlobal)
					self.wndItem.DeactivateSlot(overSlotPos)
			elif self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.STONE_INVENTORY:
				if overSlotPosGlobal in self.listHighlightedSlotStone:
					self.listHighlightedSlotStone.remove(overSlotPosGlobal)
					self.wndItem.DeactivateSlot(overSlotPos)
			elif self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] == player.CHEST_INVENTORY:
				if overSlotPosGlobal in self.listHighlightedSlotChest:
					self.listHighlightedSlotChest.remove(overSlotPosGlobal)
					self.wndItem.DeactivateSlot(overSlotPos)

		self.wndItem.SetUsableItem(False)
		self.ShowToolTip(overSlotPosGlobal)

	def OnPickItem(self, count):
		itemSlotIndex = self.dlgSplitItems.itemGlobalSlotIndex
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uinewofflineshop.IsBuildingShop() and uinewofflineshop.IsSaleSlot(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
		selectedItemVNum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"], itemSlotIndex, selectedItemVNum, count)

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)
		selectedItemVNum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
		itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemCount  = mouseModule.mouseController.GetAttachedItemCount()

			if self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"] == attachedSlotType:
				#if attachedItemVID == selectedItemVNum:
				if item.IsKey(attachedItemVID):
					net.SendItemUseToItemPacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
				else:
					net.SendItemMovePacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex, 0) #This modifi: last value: attachedItemCount
				#else:
					#net.SendItemUseToItemPacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)

			mouseModule.mouseController.DeattachObject()
		else:
			curCursorNum = app.GetCursor()

			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)
			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)

				if itemCount > 1:
					self.dlgSplitItems.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgSplitItems.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgSplitItems.Open(itemCount)
					self.dlgSplitItems.itemGlobalSlotIndex = itemSlotIndex
			else:
				itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"], itemSlotIndex, selectedItemVNum, itemCount)

				self.wndItem.SetUseMode(False)
				snd.PlaySound("sound/ui/pick.wav")

	def __SellItem(self, itemSlotPos, soruSorma=False):
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uinewofflineshop.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
		self.sellingSlotNumber = itemSlotPos
		itemIndex = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotPos)
		itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotPos)

		item.SelectItem(itemIndex)

		if item.IsAntiFlag(item.ANTIFLAG_SELL):
			popup = uiCommon.PopupDialog()
			popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
			popup.SetAcceptEvent(self.__OnClosePopupDialog)
			popup.Open()
			self.popup = popup
			return

		if soruSorma:
			net.SendItemSellPacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotPos, itemCount)
			snd.PlaySound("sound/ui/money.wav")
			return
	
		itemPrice = item.GetISellItemPrice()

		item.GetItemName(itemIndex)
		itemName = item.GetItemName()

		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.count = itemCount

	def SellItem(self):
		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uinewofflineshop.IsBuildingShop() and uinewofflineshop.IsSaleSlot(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], self.sellingSlotNumber):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				return
		net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"])
		snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None

	def __OnClosePopupDialog(self):
		self.pop = None

	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

			if app.__ENABLE_NEW_OFFLINESHOP__:
				if uinewofflineshop.IsBuildingShop() and uinewofflineshop.IsSaleSlot(player.SlotTypeToInvenType(attachedSlotType),attachedSlotPos):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
					return

			if player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")
			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)
			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:
				net.SendSafeboxCheckoutPacket(attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos)
			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos)
			elif player.RESERVED_WINDOW != attachedInvenType or\
				player.UPGRADE_INVENTORY == attachedInvenType or\
				player.BOOK_INVENTORY == attachedInvenType or\
				player.STONE_INVENTORY == attachedInvenType or\
				player.CHEST_INVENTORY == attachedInvenType:

				itemCount = player.GetItemCount(attachedInvenType, attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()

				self.__SendMoveItemPacket(attachedInvenType, attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos, attachedCount)

			mouseModule.mouseController.DeattachObject()

		def __FindEmptyCellForSize(self, itemGrid, size):
			for page in xrange(player.SPECIAL_PAGE_COUNT):
				for slot in xrange(player.SPECIAL_PAGE_SIZE):
					if itemGrid[page][slot] == False:
						possible = True
						for i in xrange(size):
							p = slot + (i * 5)

							try:
								if itemGrid[page][p] == True:
									possible = False
									break
							except IndexError:
								possible = False
								break

						if possible:
							return slot + page * player.SPECIAL_PAGE_SIZE

			return -1

		def AttachItemFromSafebox(self, slotIndex, itemIndex):
			itemGrid = self.__GetCurrentItemGrid()

			emptySlotIndex = self.__FindEmptyCellForSize(itemGrid, item.GetItemSize()[1])
			if emptySlotIndex <> -1:
				net.SendSafeboxCheckoutPacket(slotIndex, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], emptySlotIndex)

			return True

	def UseItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		windowIndex = self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"]
		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		if self.isShowDeleteItemDlg():
			self.wndItemDelete.AddItemWithoutMouse(windowIndex, slotIndex)
			return
	
		if app.IsPressed(app.DIK_LCONTROL) and app.IsPressed(app.DIK_X):
			self.__SellItem(slotIndex, True)
			return

		if app.__ENABLE_NEW_OFFLINESHOP__:
			if uinewofflineshop.IsBuildingShop():
				win = self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"]
				globalSlot 	= slotIndex
				itemIndex 	= player.GetItemIndex(win, globalSlot)
				
				item.SelectItem(itemIndex)
				
				if not item.IsAntiFlag(item.ANTIFLAG_GIVE) and not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
					offlineshop.ShopBuilding_AddItem(win, globalSlot)
				
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)
				
				return

			elif uinewofflineshop.IsBuildingAuction():
				win = self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"]
				globalSlot = slotIndex
				itemIndex 	= player.GetItemIndex(win, globalSlot)

				item.SelectItem(itemIndex)

				if not item.IsAntiFlag(item.ANTIFLAG_GIVE) and not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
					offlineshop.AuctionBuilding_AddItem(win, globalSlot)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANT_SELECT_ITEM_DURING_BUILING)

				return


		if app.IsPressed(app.DIK_LCONTROL):
			if item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
				for i in xrange(201):
					net.SendItemUsePacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)

		elif app.IsPressed(app.DIK_LALT):
			if item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
				if app.ENABLE_SHOW_CHEST_DROP_SYSTEM:
					if self.interface:
						if self.interface.dlgChestDrop:
							if not self.interface.dlgChestDrop.IsShow():
								self.interface.dlgChestDrop.Open(slotIndex)
								net.SendChestDropInfo(slotIndex)
		else:
			net.SendItemUsePacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)

		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __SendMoveItemPacket(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] != player.UPGRADE_INVENTORY and\
			self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] != player.BOOK_INVENTORY and\
			self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] != player.STONE_INVENTORY and\
			self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] != player.CHEST_INVENTORY:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Bu iþlemi gerçekleþtiremezsiniz!")
			return

		net.SendItemMovePacket(srcSlotWindow , srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount)

	def __DropSrcItemToDestItemInInventory(self, veri_1, veri_2, veri_3, veri_4, veri_5):
		if veri_2 == veri_4:
			return

		net.SendItemMovePacket(veri_1, veri_2, veri_3, veri_4, veri_5)

	def ClickSirala(self):
		if constInfo.shop_acik_bro == 1:
			chat.AppendChat(chat.CHAT_TYPE_NOTICE, "Pazar kurarken bunu yapamazsin")
			return

		if app.GetTime() > self.remaining_time:
			net.SendChatPacket("/click_sort_special_storage")
			self.remaining_time = app.GetTime() + 5
		else:
			v = self.remaining_time - app.GetTime()
			chat.AppendChat(chat.CHAT_TYPE_NOTICE, "5 saniyede bir envanterini düzenleyebilirsin. Kalan: %d" % (v))

	def SetDeleteItemDlg(self, wndItemDelete):
		self.wndItemDelete = wndItemDelete

	def isShowDeleteItemDlg(self):
		if self.wndItemDelete:
			if self.wndItemDelete.IsShow():
				return 1
		return 0
