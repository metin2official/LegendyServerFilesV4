import uiScriptLocale
import app

ROOT_PATH = "d:/ymir work/ui/public/"

TEMPORARY_X = +13
TEXT_TEMPORARY_X = -10
BUTTON_TEMPORARY_X = 5
PVP_X = -10

LINE_LABEL_X 	= 25
LINE_DATA_X 	= 90
LINE_BEGIN	= 40
LINE_STEP	= 0
SMALL_BUTTON_WIDTH 	= 35
MIDDLE_BUTTON_WIDTH 	= 65

if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
	window = {
		"name" : "SystemOptionDialog",
		"style" : ("movable", "float",),

		"x" : 0,
		"y" : 0,

		"width" : 305,
		"height" : 500,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",

				"x" : 0,
				"y" : 0,

				"width" : 305,
				"height" : 500,

				"children" :
				(
					## Title
					{
						"name" : "titlebar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 8,

						"width" : 284,
						"color" : "gray",

						"children" :
						(
							{
							"name":"titlename", "type":"text", "x":0, "y":3,
							"horizontal_align":"center", "text_horizontal_align":"center",
							"text": uiScriptLocale.SYSTEMOPTION_TITLE,
							 },
						),
					},


					## Music
					{
						"name" : "music_name",
						"type" : "text",

						"x" : 30,
						"y" : 75,

						"text" : uiScriptLocale.OPTION_MUSIC,
					},

					{
						"name" : "music_volume_controller",
						"type" : "sliderbar",

						"x" : 110,
						"y" : 75,
					},

					{
						"name" : "bgm_button",
						"type" : "button",

						"x" : 20,
						"y" : 100,

						"text" : uiScriptLocale.OPTION_MUSIC_CHANGE,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "bgm_file",
						"type" : "text",

						"x" : 100,
						"y" : 102,

						"text" : uiScriptLocale.OPTION_MUSIC_DEFAULT_THEMA,
					},

					## Sound
					{
						"name" : "sound_name",
						"type" : "text",

						"x" : 30,
						"y" : 50,

						"text" : uiScriptLocale.OPTION_SOUND,
					},

					{
						"name" : "sound_volume_controller",
						"type" : "sliderbar",

						"x" : 110,
						"y" : 50,
					},

					{
						"name" : "camera_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 135+2,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE,
					},

					{
						"name" : "camera_short",
						"type" : "radio_button",

						"x" : 110,
						"y" : 135,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "camera_long",
						"type" : "radio_button",

						"x" : 110+70,
						"y" : 135,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "fog_mode",
						"type" : "text",

						"x" : 30,
						"y" : 160+2,

						"text" : uiScriptLocale.OPTION_FOG,
					},

					{
						"name" : "fog_level0",
						"type" : "radio_button",

						"x" : 110,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_DENSE,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "fog_level1",
						"type" : "radio_button",

						"x" : 110+50,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_MIDDLE,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "fog_level2",
						"type" : "radio_button",

						"x" : 110 + 100,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_LIGHT,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "tiling_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 185+2,

						"text" : uiScriptLocale.OPTION_TILING,
					},

					{
						"name" : "tiling_cpu",
						"type" : "radio_button",

						"x" : 110,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_CPU,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "tiling_gpu",
						"type" : "radio_button",

						"x" : 110+50,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_GPU,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "tiling_apply",
						"type" : "button",

						"x" : 110+100,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_APPLY,

						"default_image" : ROOT_PATH + "middle_Button_01.sub",
						"over_image" : ROOT_PATH + "middle_Button_02.sub",
						"down_image" : ROOT_PATH + "middle_Button_03.sub",
					},

					{
						"name" : "night_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 210,

						"text" : uiScriptLocale.OPTION_NIGHT_MODE,
					},

					{
						"name" : "night_mode_on",
						"type" : "radio_button",

						"x" : 110,
						"y" : 210,

						"text" : uiScriptLocale.OPTION_NIGHT_MODE_ON,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "night_mode_off",
						"type" : "radio_button",

						"x" : 110+50,
						"y" : 210,

						"text" : uiScriptLocale.OPTION_NIGHT_MODE_OFF,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "snow_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 235,

						"text" : uiScriptLocale.OPTION_SNOW_MODE,
					},

					{
						"name" : "snow_mode_on",
						"type" : "radio_button",

						"x" : 110,
						"y" : 235,

						"text" : uiScriptLocale.OPTION_SNOW_MODE_ON,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "snow_mode_off",
						"type" : "radio_button",

						"x" : 110+50,
						"y" : 235,

						"text" : uiScriptLocale.OPTION_SNOW_MODE_OFF,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "snow_texture_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 260,

						"text" : uiScriptLocale.OPTION_SNOW_TEXTURE_MODE,
					},

					{
						"name" : "snow_texture_mode_on",
						"type" : "radio_button",

						"x" : 110,
						"y" : 260,

						"text" : uiScriptLocale.OPTION_SNOW_TEXTURE_MODE_ON,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "snow_texture_mode_off",
						"type" : "radio_button",

						"x" : 110+50,
						"y" : 260,

						"text" : uiScriptLocale.OPTION_SNOW_TEXTURE_MODE_OFF,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

	#				{
	#					"name" : "shadow_mode",
	#					"type" : "text",

	#					"x" : 30,
	#					"y" : 210,

	#					"text" : uiScriptLocale.OPTION_SHADOW,
	#				},

	#				{
	#					"name" : "shadow_bar",
	#					"type" : "sliderbar",

	#					"x" : 110,
	#					"y" : 210,
	#				},
				),
			},
		),
	}
else:
	window = {
		"name" : "SystemOptionDialog",
		"style" : ("movable", "float",),

		"x" : 0,
		"y" : 0,

		"width" : 305,
		"height" : 500,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",

				"x" : 0,
				"y" : 0,

				"width" : 305,
				"height" : 500,

				"children" :
				(
					## Title
					{
						"name" : "titlebar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 8,

						"width" : 284,
						"color" : "gray",

						"children" :
						(
							{
							"name":"titlename", "type":"text", "x":0, "y":3,
							"horizontal_align":"center", "text_horizontal_align":"center",
							"text": uiScriptLocale.SYSTEMOPTION_TITLE,
							 },
						),
					},


					## Music
					{
						"name" : "music_name",
						"type" : "text",

						"x" : 30,
						"y" : 75,

						"text" : uiScriptLocale.OPTION_MUSIC,
					},

					{
						"name" : "music_volume_controller",
						"type" : "sliderbar",

						"x" : 110,
						"y" : 75,
					},

					{
						"name" : "bgm_button",
						"type" : "button",

						"x" : 20,
						"y" : 100,

						"text" : uiScriptLocale.OPTION_MUSIC_CHANGE,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "bgm_file",
						"type" : "text",

						"x" : 100,
						"y" : 102,

						"text" : uiScriptLocale.OPTION_MUSIC_DEFAULT_THEMA,
					},

					## Sound
					{
						"name" : "sound_name",
						"type" : "text",

						"x" : 30,
						"y" : 50,

						"text" : uiScriptLocale.OPTION_SOUND,
					},

					{
						"name" : "sound_volume_controller",
						"type" : "sliderbar",

						"x" : 110,
						"y" : 50,
					},

					{
						"name" : "camera_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 135+2,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE,
					},

					{
						"name" : "camera_short",
						"type" : "radio_button",

						"x" : 110,
						"y" : 135,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "camera_long",
						"type" : "radio_button",

						"x" : 110+70,
						"y" : 135,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "fog_mode",
						"type" : "text",

						"x" : 30,
						"y" : 160+2,

						"text" : uiScriptLocale.OPTION_FOG,
					},

					{
						"name" : "fog_level0",
						"type" : "radio_button",

						"x" : 110,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_DENSE,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "fog_level1",
						"type" : "radio_button",

						"x" : 110+50,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_MIDDLE,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "fog_level2",
						"type" : "radio_button",

						"x" : 110 + 100,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_LIGHT,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},




					{
						"name" : "background_object",
						"type" : "toggle_button",

						"x" : LINE_DATA_X+SMALL_BUTTON_WIDTH*0,
						"y" : 220,#asagÄ± artar yukarÄ± azalÄ±r

						"text" : "Bina",
						"tooltip_text" :  "Bina & Köprü Göster/Gizle",

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},
				
					{
						"name" : "background_cloud",
						"type" : "toggle_button",

						"x" : LINE_DATA_X+10+SMALL_BUTTON_WIDTH*1,
						"y" : 220,#asagÄ± artar yukarÄ± azalÄ±r

						"text" : "Bulut",
						"tooltip_text" :  "Bulut Göster/Gizle",

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "background_tree",
						"type" : "toggle_button",

						"x" : LINE_DATA_X+20+SMALL_BUTTON_WIDTH*2,
						"y" : 220,#asagÄ± artar yukarÄ± azalÄ±r

						"text" : "Aðaç",
						"tooltip_text" :  "Aðaç & Çiçek Göster/Gizle",

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},
					{
						"name" : "background_water",
						"type" : "toggle_button",

						"x" : LINE_DATA_X+30+SMALL_BUTTON_WIDTH*3,
						"y" : 220,#asagÄ± artar yukarÄ± azalÄ±r

						"text" : "Deniz",
						"tooltip_text" :  "Su & Ateþ Göster/Gizle",

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},


					{
						"name" : "effect_level",
						"type" : "text",
	
						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 185+2+20+25+25+25,
	
						"text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL, 
					},
					{
						"name" : "effect_level1",
						"type" : "radio_button",
	
						"x" : 110,
						"y" : 185+20+25+25+25,
	
						"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL1,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL1_TOOLTIP,
	
						"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
						"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
						"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
					},
					{
						"name" : "effect_level2",
						"type" : "radio_button",
	
						"x" : 110 + 20,
						"y" : 185+20+25+25+25,
	
						"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL2,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL2_TOOLTIP,
	
						"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
						"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
						"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
					},
					{
						"name" : "effect_level3",
						"type" : "radio_button",
	
						"x" : 110 + 40,
						"y" : 185+20+25+25+25,
	
						"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL3,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL3_TOOLTIP,
	
						"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
						"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
						"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
					},
					{
						"name" : "effect_level4",
						"type" : "radio_button",
	
						"x" : 110 + 60,
						"y" : 185+20+25+25+25,
	
						"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL4,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL4_TOOLTIP,
	
						"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
						"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
						"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
					},
					{
						"name" : "effect_level5",
						"type" : "radio_button",
	
						"x" : 110 + 80,
						"y" : 185+20+25+25+25,
	
						"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL5,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL5_TOOLTIP,
	
						"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
						"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
						"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
					},
					{
						"name" : "effect_apply",
						"type" : "button",
	
						"x" : 110+105,
						"y" : 185+20+25+25+25,
	
						"text" : uiScriptLocale.GRAPHICONOFF_EFFECT_APPLY,
	
						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},
					
					## Drop Item
					{
						"name" : "dropItem_level",
						"type" : "text",
	
						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 185+20+25+25+25+25,
	
						"text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL, 
					},
					{
						"name" : "dropItem_level1",
						"type" : "radio_button",
	
						"x" : 110,
						"y" : 185+20+25+25+25+25,
	
						"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL1,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL1_TOOLTIP, 
	
						"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
						"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
						"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
					},
					{
						"name" : "dropItem_level2",
						"type" : "radio_button",
	
						"x" : 110 + 20,
						"y" : 185+20+25+25+25+25,
	
						"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL2,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL2_TOOLTIP, 
	
						"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
						"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
						"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
					},
					{
						"name" : "dropItem_level3",
						"type" : "radio_button",
	
						"x" : 110 + 40,
						"y" : 185+20+25+25+25+25,
	
						"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL3,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL3_TOOLTIP, 
	
						"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
						"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
						"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
					},
					{
						"name" : "dropItem_level4",
						"type" : "radio_button",
	
						"x" : 110 + 60,
						"y" : 185+20+25+25+25+25,
	
						"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL4,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL4_TOOLTIP, 
	
						"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
						"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
						"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
					},
					{
						"name" : "dropItem_level5",
						"type" : "radio_button",
	
						"x" : 110 + 80,
						"y" : 185+20+25+25+25+25,
	
						"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL5,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL5_TOOLTIP, 
	
						"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
						"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
						"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
					},
					{
						"name" : "dropItem_apply",
						"type" : "button",
	
						"x" : 110+105,
						"y" : 185+20+25+25+25+25,
	
						"text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_APPLY,
	
						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},
					
					## NPC Name
					{
						"name" : "npcName_status",
						"type" : "text",
	
						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 185+2+20+25+25+25+25+25,
	
						"text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS,
					},
					{
						"name" : "npcName_on",
						"type" : "radio_button",
	
						"x" : 110,
						"y" : 185+20+25+25+25+25+25,
	
						"text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_ON,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_ON_TOOLTIP,
	
						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},
					{
						"name" : "npcName_off",
						"type" : "radio_button",
	
						"x" : 110 + 50,
						"y" : 185+20+25+25+25+25+25,
	
						"text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_OFF,
						"tooltip_text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_OFF_TOOLTIP,  
	
						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},



					{
						"name" : "tiling_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 185+2,

						"text" : uiScriptLocale.OPTION_TILING,
					},

					{
						"name" : "tiling_cpu",
						"type" : "radio_button",

						"x" : 110,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_CPU,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "tiling_gpu",
						"type" : "radio_button",

						"x" : 110+50,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_GPU,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "tiling_apply",
						"type" : "button",

						"x" : 110+100,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_APPLY,

						"default_image" : ROOT_PATH + "middle_Button_01.sub",
						"over_image" : ROOT_PATH + "middle_Button_02.sub",
						"down_image" : ROOT_PATH + "middle_Button_03.sub",
					},


	#				{
	#					"name" : "shadow_mode",
	#					"type" : "text",

	#					"x" : 30,
	#					"y" : 210,

	#					"text" : uiScriptLocale.OPTION_SHADOW,
	#				},

	#				{
	#					"name" : "shadow_bar",
	#					"type" : "sliderbar",

	#					"x" : 110,
	#					"y" : 210,
	#				},
				),
			},
		),
	}
