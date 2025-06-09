import uiScriptLocale
import app

ENVANTER_ICON = "d:/ymir work/ui/"

window = {
	"name" : "SpecialStorageWindow",

	"x" : SCREEN_WIDTH - 400,
	"y" : SCREEN_HEIGHT - 37 - (328+32+150),

	"style" : ("movable", "float",),

	"width" : 200,
	"height" : 420,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 200,
			"height" : 420,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 35,
					"y" : 7,

					"width" : 160,
					"color" : "gray",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":84, "y":4, "text": "Toplu Env", "text_horizontal_align":"center" },
					),
				},

				{
					"name" : "SiralaButton",
					"type" : "button",

					"x" : 2,
					"y" : 2,

					"tooltip_text" : "Envanter Düzenleme",

					"default_image" : "d:/ymir work/ui/game/special_storage/basiliinventorybutton.tga",
					"over_image" : "d:/ymir work/ui/game/special_storage/normalinventorybutton.tga",
					"down_image" : "d:/ymir work/ui/game/special_storage/refinventorybutton.tga",
				},

				## Item Slot
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 12,
					"y" : 34,

					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 9,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},
				################---INVENTORY---################
				{
					"name" : "ScrollBar",
					"type" : "scrollbar",

					"x" : 25,
					"y" : 31,
					"size" : 364 - 70,
					"horizontal_align" : "right",
				},
				# {
					# "name" : "arka",
					# "type" : "thinboard_circle",

					# "x" : 10,
					# "y" : 94,
					# "vertical_align" : "bottom",
					# "width" : 178,
					# "height" : 52,

				# },
				# {
					# "name" : "Inventory_Tab_01",
					# "type" : "radio_button",

					# "x" : 15,
					# "y" : 295+32,

					# "default_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_01.sub",
					# "over_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_02.sub",
					# "down_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_03.sub",
					# "children" :
					# (
						# {
							# "name" : "Inventory_Tab_01_Print_2",
							# "type" : "text",

							# "x" : 0,
							# "y" : 0,

							# "all_align" : "center",
							# "text" : "I",
						# },
					# ),
				# },
				
				# {
					# "name" : "Inventory_Tab_02",
					# "type" : "radio_button",

					# "x" : 15 + 40,
					# "y" : 295+32,

					# "default_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_01.sub",
					# "over_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_02.sub",
					# "down_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_03.sub",

					# "children" :
					# (
						# {
							# "name" : "Inventory_Tab_02_Print_2",
							# "type" : "text",

							# "x" : 0,
							# "y" : 0,

							# "all_align" : "center",
							# "text" : "II",
						# },
					# ),
				# },
				# {
					# "name" : "Inventory_Tab_03",
					# "type" : "radio_button",

					# "x" : 15+40+40,
					# "y" : 295+32,

					# "default_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_01.sub",
					# "over_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_02.sub",
					# "down_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_03.sub",

					# "children" :
					# (
						# {
							# "name" : "Inventory_Tab_03_Print",
							# "type" : "text",

							# "x" : 0,
							# "y" : 0,

							# "all_align" : "center",
							# "text" : "III",
						# },
					# ),
				# },
				# {
					# "name" : "Inventory_Tab_04",
					# "type" : "radio_button",

					# "x" : 15+40+40+40,
					# "y" : 295+32,

					# "default_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_01.sub",
					# "over_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_02.sub",
					# "down_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_03.sub",

					# "children" :
					# (
						# {
							# "name" : "Inventory_Tab_04_Print",
							# "type" : "text",

							# "x" : 0,
							# "y" : 0,

							# "all_align" : "center",
							# "text" : "IV",
						# },
					# ),
				# },
				################---INVENTORY---################
				{
					"name" : "Category_Tab_01",
					"type" : "radio_button",

					"x" : 12,
					"y" : 295+32,

					"default_image" : "d:/ymir work/ui/game/special_storage/refine1.tga",
					"over_image" : "d:/ymir work/ui/game/special_storage/refine2.tga",
					"down_image" : "d:/ymir work/ui/game/special_storage/refine3.tga",
				},
					
				{
					"name" : "Category_Tab_02",
					"type" : "radio_button",

					"x" : 12+40,
					"y" : 295+32,
					"default_image" : "d:/ymir work/ui/game/special_storage/book1.tga",
					"over_image" : "d:/ymir work/ui/game/special_storage/book2.tga",
					"down_image" : "d:/ymir work/ui/game/special_storage/book3.tga",
				},
				
				{
					"name" : "Category_Tab_03",
					"type" : "radio_button",

					"x" : 12+40+40,
					"y" : 295+32,

					"default_image" : "d:/ymir work/ui/game/special_storage/stone1.tga",
					"over_image" : "d:/ymir work/ui/game/special_storage/stone2.tga",
					"down_image" : "d:/ymir work/ui/game/special_storage/stone3.tga",
				},
				{
					"name" : "Category_Tab_04",
					"type" : "radio_button",

					"x" : 12+40+40+40,
					"y" : 295+32,

					"default_image" : "d:/ymir work/ui/game/special_storage/chest1.png",
					"over_image" : "d:/ymir work/ui/game/special_storage/chest2.png",
					"down_image" : "d:/ymir work/ui/game/special_storage/chest3.png",
				},
			),
		},
	),
}
