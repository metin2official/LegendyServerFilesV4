import dbg
import ui
import snd
import systemSetting
import net
import chat
import app
import localeInfo
import constInfo
import chrmgr
import player
import musicInfo

import uiSelectMusic
import background

MUSIC_FILENAME_MAX_LEN = 25

if app.ENABLE_GRAPHIC_ON_OFF:
	GRAPHIC_LEVEL_MAX_NUM = 5

blockMode = 0

class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE SYSTEM OPTION DIALOG"

	def __Initialize(self):
		self.tilingMode = 0
		self.titleBar = 0
		self.changeMusicButton = 0
		self.selectMusicFile = 0
		self.ctrlMusicVolume = 0
		self.ctrlSoundVolume = 0
		self.musicListDlg = 0
		self.tilingApplyButton = 0
		self.cameraModeButtonList = []
		self.fogModeButtonList = []
		self.tilingModeButtonList = []
		self.ctrlShadowQuality = 0
		if app.ENABLE_GRAPHIC_MASK:
			self.graphicMaskButtonList = []
		if app.ENABLE_GRAPHIC_ON_OFF:
			self.effectLevel = 0
			self.effectLevelApplyButton = 0
			self.effectLevelButtonList = []
			self.dropItemLevel = 0
			self.dropItemLevelApplyButton = 0
			self.dropItemLevelButtonList = []
			self.npcNameStatusButtonList = []

	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		print " -------------------------------------- DESTROY SYSTEM OPTION DIALOG"

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("System.OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.selectMusicFile = GetObject("bgm_file")
			self.changeMusicButton = GetObject("bgm_button")
			self.ctrlMusicVolume = GetObject("music_volume_controller")
			self.ctrlSoundVolume = GetObject("sound_volume_controller")
			self.cameraModeButtonList.append(GetObject("camera_short"))
			self.cameraModeButtonList.append(GetObject("camera_long"))
			self.fogModeButtonList.append(GetObject("fog_level0"))
			self.fogModeButtonList.append(GetObject("fog_level1"))
			self.fogModeButtonList.append(GetObject("fog_level2"))
			self.tilingModeButtonList.append(GetObject("tiling_cpu"))
			self.tilingModeButtonList.append(GetObject("tiling_gpu"))
			self.tilingApplyButton=GetObject("tiling_apply")
			# self.ctrlShadowQuality = GetObject("shadow_bar")
			if app.ENABLE_GRAPHIC_MASK:
				for graphicMaskName in ('object', 'cloud', 'water', 'tree'):
					self.graphicMaskButtonList.append(GetObject('background_{:s}'.format(graphicMaskName)))

			if app.ENABLE_GRAPHIC_ON_OFF:
				for i in xrange(1, GRAPHIC_LEVEL_MAX_NUM + 1):
					self.effectLevelButtonList.append(GetObject("effect_level%d" % i))
					self.dropItemLevelButtonList.append(GetObject("dropItem_level%d" % i))
				self.effectLevelApplyButton = GetObject("effect_apply")
				self.dropItemLevelApplyButton = GetObject("dropItem_apply")
				self.npcNameStatusButtonList.append(GetObject("npcName_on"))
				self.npcNameStatusButtonList.append(GetObject("npcName_off"))

		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		self.__Load_LoadScript("uiscript/systemoptiondialog.py")
		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.ctrlMusicVolume.SetSliderPos(float(systemSetting.GetMusicVolume()))
		self.ctrlMusicVolume.SetEvent(ui.__mem_func__(self.OnChangeMusicVolume))

		self.ctrlSoundVolume.SetSliderPos(float(systemSetting.GetSoundVolume()) / 5.0)
		self.ctrlSoundVolume.SetEvent(ui.__mem_func__(self.OnChangeSoundVolume))

#		self.ctrlShadowQuality.SetSliderPos(float(systemSetting.GetShadowLevel()) / 5.0)
#		self.ctrlShadowQuality.SetEvent(ui.__mem_func__(self.OnChangeShadowQuality))

		self.changeMusicButton.SAFE_SetEvent(self.__OnClickChangeMusicButton)

		self.cameraModeButtonList[0].SAFE_SetEvent(self.__OnClickCameraModeShortButton)
		self.cameraModeButtonList[1].SAFE_SetEvent(self.__OnClickCameraModeLongButton)

		self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFogModeLevel0Button)
		self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFogModeLevel1Button)
		self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFogModeLevel2Button)

		self.tilingModeButtonList[0].SAFE_SetEvent(self.__OnClickTilingModeCPUButton)
		self.tilingModeButtonList[1].SAFE_SetEvent(self.__OnClickTilingModeGPUButton)

		self.tilingApplyButton.SAFE_SetEvent(self.__OnClickTilingApplyButton)

		self.__SetCurTilingMode()

		self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
		self.__ClickRadioButton(self.cameraModeButtonList, constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())

		if musicInfo.fieldMusic==musicInfo.METIN2THEMA:
			self.selectMusicFile.SetText(uiSelectMusic.DEFAULT_THEMA)
		else:
			self.selectMusicFile.SetText(musicInfo.fieldMusic[:MUSIC_FILENAME_MAX_LEN])

		if app.ENABLE_GRAPHIC_MASK:
			for (tabKey, tabButton) in enumerate(self.graphicMaskButtonList):
				tabButton.SetToggleUpEvent(lambda arg=tabKey: self.__OnClickGraphicMaskButton(arg, False))
				tabButton.SetToggleDownEvent(lambda arg=tabKey: self.__OnClickGraphicMaskButton(arg, True))
		if app.ENABLE_GRAPHIC_ON_OFF:
			self.__ClickRadioButton(self.effectLevelButtonList, systemSetting.GetEffectLevel())
			self.__ClickRadioButton(self.dropItemLevelButtonList, systemSetting.GetDropItemLevel())

			self.__ClickRadioButton(self.npcNameStatusButtonList, systemSetting.IsNpcNameStatus())

		if app.ENABLE_GRAPHIC_ON_OFF:
			for i in xrange(GRAPHIC_LEVEL_MAX_NUM):
				self.effectLevelButtonList[i].SAFE_SetEvent(self.__OnClickEffectLevelButton, i)
				self.dropItemLevelButtonList[i].SAFE_SetEvent(self.__OnClickDropItemLevelButton, i)

			self.npcNameStatusButtonList[0].SAFE_SetEvent(self.__OnClickNpcNameStatusButton, 0)
			self.npcNameStatusButtonList[1].SAFE_SetEvent(self.__OnClickNpcNameStatusButton, 1)

			self.effectLevelApplyButton.SAFE_SetEvent(self.__OnClickEffectApplyButton)
			self.dropItemLevelApplyButton.SAFE_SetEvent(self.__OnClickDropItemApplyButton)


			self.__RefreshGraphicMask()

	def __OnClickTilingModeCPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_3)
		self.__SetTilingMode(0)

	def __OnClickTilingModeGPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_3)
		self.__SetTilingMode(1)

	def __OnClickTilingApplyButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_TILING_EXIT)
		if 0==self.tilingMode:
			background.EnableSoftwareTiling(1)
		else:
			background.EnableSoftwareTiling(0)

		net.ExitGame()

	def __OnClickChangeMusicButton(self):
		if not self.musicListDlg:

			self.musicListDlg=uiSelectMusic.FileListDialog()
			self.musicListDlg.SAFE_SetSelectEvent(self.__OnChangeMusic)

		self.musicListDlg.Open()


	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()


	def __SetTilingMode(self, index):
		self.__ClickRadioButton(self.tilingModeButtonList, index)
		self.tilingMode=index

	def __SetCameraMode(self, index):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(index)
		self.__ClickRadioButton(self.cameraModeButtonList, index)

	def __SetFogLevel(self, index):
		constInfo.SET_FOG_LEVEL_INDEX(index)
		self.__ClickRadioButton(self.fogModeButtonList, index)

	def __OnClickCameraModeShortButton(self):
		self.__SetCameraMode(0)

	def __OnClickCameraModeLongButton(self):
		self.__SetCameraMode(1)

	def __OnClickFogModeLevel0Button(self):
		self.__SetFogLevel(0)

	def __OnClickFogModeLevel1Button(self):
		self.__SetFogLevel(1)

	def __OnClickFogModeLevel2Button(self):
		self.__SetFogLevel(2)

	def __OnChangeMusic(self, fileName):
		self.selectMusicFile.SetText(fileName[:MUSIC_FILENAME_MAX_LEN])

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		if fileName==uiSelectMusic.DEFAULT_THEMA:
			musicInfo.fieldMusic=musicInfo.METIN2THEMA
		else:
			musicInfo.fieldMusic=fileName

		musicInfo.SaveLastPlayFieldMusic()

		if musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		snd.SetMusicVolume(pos * net.GetFieldMusicVolume())
		systemSetting.SetMusicVolume(pos)

	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		snd.SetSoundVolumef(pos)
		systemSetting.SetSoundVolumef(pos)

	def OnChangeShadowQuality(self):
		pos = self.ctrlShadowQuality.GetSliderPos()
		systemSetting.SetShadowLevel(int(pos / 0.2))

	if app.ENABLE_GRAPHIC_MASK:
		def __RefreshGraphicMask(self):
			for (tabKey, tabButton) in enumerate(self.graphicMaskButtonList):
				if systemSetting.GetGraphicMaskPart(tabKey+1):
					tabButton.Down()
				else:
					tabButton.SetUp()

			background.LoadGraphicMaskSettings()
	
		def __OnClickGraphicMaskButton(self, bPart, bFlag):
			systemSetting.SetGraphicMaskPart(bPart+1, bFlag)
			self.__RefreshGraphicMask()

	if app.ENABLE_GRAPHIC_ON_OFF:
		def __OnClickEffectLevelButton(self, index):
			self.__ClickRadioButton(self.effectLevelButtonList, index)
			self.effectLevel=index

		def __OnClickEffectApplyButton(self):
			systemSetting.SetEffectLevel(self.effectLevel)

		def __OnClickDropItemLevelButton(self, index):
			self.__ClickRadioButton(self.dropItemLevelButtonList, index)
			self.dropItemLevel=index

		def __OnClickDropItemApplyButton(self):
			systemSetting.SetDropItemLevel(self.dropItemLevel)

		def __OnClickNpcNameStatusButton(self, flag):
			self.__ClickRadioButton(self.npcNameStatusButtonList, flag)
			systemSetting.SetNpcNameStatusFlag(flag)
			self.RefreshNpcNameStatus()

		def RefreshNpcNameStatus(self):
			if systemSetting.IsNpcNameStatus():
				self.npcNameStatusButtonList[0].SetUp()
				self.npcNameStatusButtonList[1].Down()
			else:
				self.npcNameStatusButtonList[0].Down()
				self.npcNameStatusButtonList[1].SetUp()


	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.__SetCurTilingMode()
		self.Hide()

	def __SetCurTilingMode(self):
		if background.IsSoftwareTiling():
			self.__SetTilingMode(0)
		else:
			self.__SetTilingMode(1)

	def __NotifyChatLine(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, text)

