import app
import player
import item
import ui
import localeInfo
import uiToolTip
import constInfo
import wndMgr

class CharacterDetailsUI(ui.ScriptWindow):
	def __init__(self, parent):
		self.uiCharacterStatus = parent
		ui.ScriptWindow.__init__(self)
		self.toolTip = uiToolTip.ToolTip()

		self.__LoadScript()

	def __del__(self):
		self.uiCharacterStatus = None
		self.toolTip = None
		ui.ScriptWindow.__del__(self)

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CharacterDetailsWindow.py")
		except:
			import exception
			exception.Abort("CharacterDetailsUI.__LoadScript")

		self.Width = 253 - 3

		#self.GetChild("TitleBar").CloseButtonHide()
		self.ScrollBar = self.GetChild("ScrollBar")
		self.karakterbonus		= self.GetChild("karakterbonus")
		self.istatistik		= self.GetChild("killbonus")
		self.karakterbonuspage		= self.GetChild("karakterbonuspage")
		self.istatistikpage		= self.GetChild("killbonuspage")
		self.karakterbonus.SAFE_SetEvent(self.karakterbonussayfa)
		self.istatistik.SAFE_SetEvent(self.istatistiksayfa)
		self.istatistikpage.Hide()
		self.ScrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))

		## 출력되는 UI 최대 숫자
		self.UI_MAX_COUNT = 11
		self.UI_MAX_VIEW_COUNT = 6

		## UI KEY & VALUE
		self.INFO_TEXT	= 0
		self.INFO_TOOLTIP = 1
		self.INFO_VALUE	= 2
		self.CATEGORY_STARTLINE	= -1
		self.CATEGORY_ENDLINE	= -2

		## Child 셋팅
		self.labelList		= []
		self.labelValueList	= []
		self.labelTextList	= []
		self.horizonBarList	= []
		self.horizonBarNameList = []

		for i in xrange(self.UI_MAX_COUNT):
			self.labelList.append( self.GetChild("label%s"%i) )
			self.labelValueList.append( self.GetChild("labelvalue%s"%i) )
			self.labelTextList.append( self.GetChild("labelname%s"%i) )
			self.horizonBarList.append( self.GetChild("horizontalbar%s"%i) )
			self.horizonBarNameList.append( self.GetChild("horizontalbarName%s"%i) )

		for i in xrange(self.UI_MAX_COUNT):
			self.labelTextList[i].ShowToolTip = lambda arg=i: self.__ButtonOverIn(arg)
			self.labelTextList[i].HideToolTip = lambda arg=i: self.__ButtonOverOut(arg)
		self.__Initialize()

	def __Initialize(self):
		self.InfoList = []
		self.titleBar = 0
		self.jinno_kills_obj = self.GetChild("jinno_kills")
		self.shinsoo_kills_obj = self.GetChild("shinsoo_kills")
		self.chunjo_kills_obj = self.GetChild("chunjo_kills")
		self.total_kills_obj = self.GetChild("total_kills")
		# self.total_deaths_obj = self.GetChild("total_deaths")
		# self.kd_obj = self.GetChild("kd")
		self.duels_t_obj = self.GetChild("duels_t")
		self.duels_w_obj = self.GetChild("duels_w")
		self.duels_l_obj = self.GetChild("duels_l")
		self.bosses_kills_obj = self.GetChild("bosses_kills")
		self.stones_kills_obj = self.GetChild("stones_kills")
		self.mobs_kills_obj = self.GetChild("mobs_kills")
		self.top_damage_obj = self.GetChild("top_damages")
		
		self.InfoList.append( [ localeInfo.DETAILS_CATE_1, "", self.CATEGORY_STARTLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_5, localeInfo.DETAILS_TOOLTIP_5, item.GetApplyPoint( item.APPLY_ATTBONUS_MONSTER ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_NEW1, localeInfo.DETAILS_TOOLTIP_NEW11, item.GetApplyPoint( item.APPLY_ATTBONUS_STONE ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_NEW2, localeInfo.DETAILS_TOOLTIP_NEW11, item.GetApplyPoint( item.APPLY_ATTBONUS_BOSS ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_4, localeInfo.DETAILS_TOOLTIP_4, item.GetApplyPoint( item.APPLY_ATTBONUS_UNDEAD ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_9, localeInfo.DETAILS_TOOLTIP_9, item.GetApplyPoint( item.APPLY_ATTBONUS_DEVIL ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_8, localeInfo.DETAILS_TOOLTIP_8, item.GetApplyPoint( item.APPLY_ATTBONUS_MILGYO ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_7, localeInfo.DETAILS_TOOLTIP_7, item.GetApplyPoint( item.APPLY_ATTBONUS_ANIMAL ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_3, localeInfo.DETAILS_TOOLTIP_3, item.GetApplyPoint( item.APPLY_ATTBONUS_ORC ) ] )
		self.InfoList.append( [ "", "", self.CATEGORY_ENDLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_CATE_2_2, "", self.CATEGORY_STARTLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_1, localeInfo.DETAILS_TOOLTIP_1, item.GetApplyPoint( item.APPLY_ATTBONUS_HUMAN ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_90, localeInfo.DETAILS_TOOLTIP_90, item.GetApplyPoint( item.APPLY_RESIST_HUMAN ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_36, localeInfo.DETAILS_TOOLTIP_36, item.GetApplyPoint( item.APPLY_ATTBONUS_WARRIOR ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_41, localeInfo.DETAILS_TOOLTIP_41, item.GetApplyPoint( item.APPLY_RESIST_WARRIOR ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_37, localeInfo.DETAILS_TOOLTIP_37, item.GetApplyPoint( item.APPLY_ATTBONUS_ASSASSIN ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_42, localeInfo.DETAILS_TOOLTIP_42, item.GetApplyPoint( item.APPLY_RESIST_ASSASSIN ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_38, localeInfo.DETAILS_TOOLTIP_38, item.GetApplyPoint( item.APPLY_ATTBONUS_SURA ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_43, localeInfo.DETAILS_TOOLTIP_43, item.GetApplyPoint( item.APPLY_RESIST_SURA ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_39, localeInfo.DETAILS_TOOLTIP_39, item.GetApplyPoint( item.APPLY_ATTBONUS_SHAMAN ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_44, localeInfo.DETAILS_TOOLTIP_44, item.GetApplyPoint( item.APPLY_RESIST_SHAMAN ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_45_1, localeInfo.DETAILS_TOOLTIP_44, item.GetApplyPoint( item.APPLY_ATTBONUS_CHARACTERS ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_45_2, localeInfo.DETAILS_TOOLTIP_44, item.GetApplyPoint( item.APPLY_ENCHANT_CHARACTERS ) ] )
		self.InfoList.append( [ "", "", self.CATEGORY_ENDLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_CATE_3_3, "", self.CATEGORY_STARTLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_14, localeInfo.DETAILS_TOOLTIP_14, item.GetApplyPoint( item.APPLY_NORMAL_HIT_DAMAGE_BONUS ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_16, localeInfo.DETAILS_TOOLTIP_16, item.GetApplyPoint( item.APPLY_SKILL_DAMAGE_BONUS ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_12, localeInfo.DETAILS_TOOLTIP_12, item.GetApplyPoint( item.APPLY_ATT_GRADE_BONUS ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_20, localeInfo.DETAILS_TOOLTIP_20, item.GetApplyPoint( item.APPLY_CRITICAL_PCT ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_21, localeInfo.DETAILS_TOOLTIP_21, item.GetApplyPoint( item.APPLY_PENETRATE_PCT ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_89, localeInfo.DETAILS_TOOLTIP_89, item.GetApplyPoint( item.APPLY_CAST_SPEED ) ] )
		self.InfoList.append( [ "", "", self.CATEGORY_ENDLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_CATE_4_4, "", self.CATEGORY_STARTLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_46, localeInfo.DETAILS_TOOLTIP_46, item.GetApplyPoint( item.APPLY_RESIST_SWORD ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_47, localeInfo.DETAILS_TOOLTIP_47, item.GetApplyPoint( item.APPLY_RESIST_TWOHAND ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_48, localeInfo.DETAILS_TOOLTIP_48, item.GetApplyPoint( item.APPLY_RESIST_DAGGER ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_52, localeInfo.DETAILS_TOOLTIP_52, item.GetApplyPoint( item.APPLY_RESIST_BOW ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_50, localeInfo.DETAILS_TOOLTIP_50, item.GetApplyPoint( item.APPLY_RESIST_BELL ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_51, localeInfo.DETAILS_TOOLTIP_51, item.GetApplyPoint( item.APPLY_RESIST_FAN ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_91, localeInfo.DETAILS_TOOLTIP_91, item.GetApplyPoint( item.APPLY_MAGIC_DEF_GRADE ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_63, localeInfo.DETAILS_TOOLTIP_63, item.GetApplyPoint( item.APPLY_BLOCK ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_92, localeInfo.DETAILS_TOOLTIP_92, item.GetApplyPoint( item.APPLY_DODGE ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_15, localeInfo.DETAILS_TOOLTIP_15, item.GetApplyPoint( item.APPLY_NORMAL_HIT_DEFEND_BONUS ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_17, localeInfo.DETAILS_TOOLTIP_17, item.GetApplyPoint( item.APPLY_SKILL_DEFEND_BONUS ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_13, localeInfo.DETAILS_TOOLTIP_13, item.GetApplyPoint( item.APPLY_DEF_GRADE_BONUS ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_22, localeInfo.DETAILS_TOOLTIP_22, item.GetApplyPoint( item.APPLY_ANTI_CRITICAL_PCT ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_23, localeInfo.DETAILS_TOOLTIP_23, item.GetApplyPoint( item.APPLY_ANTI_PENETRATE_PCT ) ] )
		self.InfoList.append( [ "", "", self.CATEGORY_ENDLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_CATE_4_5, "", self.CATEGORY_STARTLINE ] )
		self.InfoList.append( [ localeInfo.DETAILS_93, localeInfo.DETAILS_TOOLTIP_46, item.GetApplyPoint( item.APPLY_ENCHANT_FIRE ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_94, localeInfo.DETAILS_TOOLTIP_47, item.GetApplyPoint( item.APPLY_ENCHANT_ICE ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_95, localeInfo.DETAILS_TOOLTIP_48, item.GetApplyPoint( item.APPLY_ENCHANT_DARK ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_96, localeInfo.DETAILS_TOOLTIP_52, item.GetApplyPoint( item.APPLY_ENCHANT_ELECT ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_97, localeInfo.DETAILS_TOOLTIP_50, item.GetApplyPoint( item.APPLY_ENCHANT_WIND ) ] )
		self.InfoList.append( [ localeInfo.DETAILS_98, localeInfo.DETAILS_TOOLTIP_51, item.GetApplyPoint( item.APPLY_ENCHANT_EARTH ) ] )
		self.InfoList.append( [ "", "", self.CATEGORY_ENDLINE ] )
		self.Diff = len(self.InfoList) - self.UI_MAX_COUNT
		stepSize = 1.0 / self.Diff
		self.ScrollBar.SetScrollStep( stepSize )
		self.ScollPos = 0
		self.RefreshLabel()

	def Show(self):
		ui.ScriptWindow.Show(self)
		self.SetTop()

	def Close(self):
		self.Hide()

	def AdjustPosition(self, x, y):
		self.SetPosition(x + self.Width, y)

	def OnScroll(self):
		self.RefreshLabel()

	def Refresh(self):
		kd_zero_fix = 0
		if constInfo.KILL_STATISTICS_DATA[4] == 0:
			kd_zero_fix = 1
			
		self.jinno_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[0])
		self.shinsoo_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[1])
		self.chunjo_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[2])
		self.total_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[3])
		# self.total_deaths_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[4])
		# self.kd_obj.SetText("%.2f" % (float(constInfo.KILL_STATISTICS_DATA[3])/(kd_zero_fix+float(constInfo.KILL_STATISTICS_DATA[4]))))
		self.duels_t_obj.SetText("%i" % (constInfo.KILL_STATISTICS_DATA[5]+constInfo.KILL_STATISTICS_DATA[6]))
		self.duels_w_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[5])
		self.duels_l_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[6])
		self.bosses_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[7])
		self.stones_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[8])
		self.mobs_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[9])
		self.top_damage_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[10])
	def OnUpdate(self):
		self.Refresh()
		
	def RefreshLabel(self):
		self.ScollPos = int(self.ScrollBar.GetPos() * self.Diff)

		for i in xrange(self.UI_MAX_COUNT) :
			idx = i + self.ScollPos

			text = self.InfoList[idx][self.INFO_TEXT]
			type = self.InfoList[idx][self.INFO_VALUE]

			if type == self.CATEGORY_STARTLINE:
				self.__LabelTitleLine(i, text)
			elif type == self.CATEGORY_ENDLINE:
				self.__EmptyLine(i)
			else:
				value = player.GetStatus(type)

				self.__LabelLine(i, text, value)


	def karakterbonussayfa(self):
		self.istatistikpage.Hide()
		self.karakterbonuspage.Show()

	def istatistiksayfa(self):
		self.istatistikpage.Show()
		self.karakterbonuspage.Hide()
	def __LabelTitleLine(self, idx, text):
		self.labelList[idx].Hide()
		self.labelTextList[idx].Hide()
		self.horizonBarList[idx].Show()
		self.horizonBarNameList[idx].SetText( text )

	def __EmptyLine(self, idx):
		self.labelList[idx].Hide()
		self.labelTextList[idx].Hide()
		self.horizonBarList[idx].Hide()

	def __LabelLine(self, idx, text, value):
		self.labelList[idx].Show()
		self.labelTextList[idx].Show()
		self.horizonBarList[idx].Hide()

		self.labelTextList[idx].SetText( text )
		self.labelValueList[idx].SetText( str(value) )

	def __ButtonOverIn(self, i):
		idx = i + self.ScollPos
		tooltip = self.InfoList[idx][self.INFO_TOOLTIP]

		arglen = len(str(tooltip))
		pos_x, pos_y = wndMgr.GetMousePosition()

		self.toolTip.ClearToolTip()
		self.toolTip.SetThinBoardSize(11 * arglen)
		self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
		self.toolTip.AppendTextLine(tooltip, 0xffffff00)
		self.toolTip.Show()

	def __ButtonOverOut(self, idx):
		self.toolTip.Hide()
	def OnRunMouseWheel(self, nLen):
		if self.ScrollBar.IsShow():
			if nLen > 0:
				self.ScrollBar.OnUp()
			else:
				self.ScrollBar.OnDown()

	def OnTop(self):
		if self.uiCharacterStatus:
			self.uiCharacterStatus.SetTop()