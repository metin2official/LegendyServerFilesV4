import localeInfo
import uiScriptLocale

LOCALE_PATH = uiScriptLocale.WINDOWS_PATH

MAINBOARD_WIDTH = 220
MAINBOARD_HEIGHT = 394#361

LABEL_START_X = 140
LABEL_START_Y = 49
LABEL_WIDTH = 50
LABEL_HEIGHT = 22
LABEL_GAP = LABEL_HEIGHT+5
LABEL_NAME_POS_X = 15
TITLE_BAR_POS_X = 40
TITLE_BAR_WIDTH = 130

window = {
	"name" : "CharacterDetailsWindow",
	"style" : ("float",),
	
	"x" : 274, #24+253-3,
	"y" : (SCREEN_HEIGHT - 398) / 2,

	"width" : MAINBOARD_WIDTH,
	"height" : MAINBOARD_HEIGHT,
	
	"children" :
	(
		## MainBoard
		{
			"name" : "MainBoard",
			"type" : "board",
			"style" : ("attach","ltr"),
			
			## CharacterWindow.py ¿µÇâ ¹ÞÀ½
			"x" : 0,
			"y" : 0,

			"width" : MAINBOARD_WIDTH,
			"height" : MAINBOARD_HEIGHT,
			
			"children" :
			(
				# Å¸ÀÌÆ²¹Ù
				{
					"name" : "ibo_adamdir",
					"type" : "image",
					"image" : "yusuf_etc/bg_boni3.png",
					"x" : 0,
					"y" : 0,
					"width" : MAINBOARD_WIDTH-20,
					"height" : MAINBOARD_HEIGHT-55,
				},
				## Å¸ÀÌÆ²¹Ù
				# {
					# "name" : "ibo_adamdir",
					# "type" : "image",
					# "image" : "yusuf_etc/boni_textfield1.tga",
					# "x" : -12,
					# "y" : 15,
					# "children" :
					# (
						# {
							# "name" : "bon", "type" : "image", "x" : 0, "y" : -20,
							# "image" : "ibowork/bon.png",
						# },
					# ),
				# },
				{
					"name" : "killbonuspage",
					"type" : "window",
					"x" : 0,
					"y" : 0,
					"width" : MAINBOARD_WIDTH,
					"height" : MAINBOARD_HEIGHT,
					"children" : 
					(
						{
							"name" : "jinno_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*0, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ 
									"name" : "jinno_text",
									"type" : "button",
									
									"x" : 0, "y" : 0,

									"text" : uiScriptLocale.KILL_STATISTICS_JINNO,
									"default_image" : "yusuf_etc/kill_blue.tga",
									"over_image" : "yusuf_etc/kill_blue.tga",
									"down_image" : "yusuf_etc/kill_blue.tga",
								},
							),
						},
						{
							"name" : "jinno_kills_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+20*0, "width" : 169-120-2, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							),
						},	

						{
							"name" : "shinsoo_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*1, "width" : 120, "height" : 24,
							
							"children" : ( 
								{
									"name" : "shinsoo_text",
									"type" : "button",
									
									"x" : 0, "y" : 0,

									"text" : uiScriptLocale.KILL_STATISTICS_SHINSOO,
									"default_image" : "yusuf_etc/kill_red.tga",
									"over_image" : "yusuf_etc/kill_red.tga",
									"down_image" : "yusuf_etc/kill_red.tga",
								},
							),
						},
						{
							"name" : "shinsoo_kills_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*1, "width" : 169-120-2, "height" : 24,
							
							"children" : ( 
								{ "name" : "shinsoo_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							),
						},		

						{
							"name" : "chunjo_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*2, "width" : 120, "height" : 24,
							
							"children" : ( 
								{
									"name" : "chunjo_text",
									"type" : "button",
									
									"x" : 0, "y" : 0,

									"text" : uiScriptLocale.KILL_STATISTICS_CHUNJO,
									"default_image" : "yusuf_etc/kill_yellow.tga",
									"over_image" : "yusuf_etc/kill_yellow.tga",
									"down_image" : "yusuf_etc/kill_yellow.tga",
								},

							),
						},
						{
							"name" : "chunjo_kills_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*2, "width" : 169-120-2, "height" : 24,
							
							"children" : ( 
								{ "name" : "chunjo_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							),
						},	

						{
							"name" : "total_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*3, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "total_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_TOTAL, "all_align" : "center", },
							),
						},
						{
							"name" : "total_kills_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*3, "width" : 169-120-2, "height" : 24,
							
							"children" : ( 
								{ "name" : "total_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							),
						},	

						# {
							# "name" : "totald_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*4, "width" : 120, "height" : 24,
							
							# "children" : ( 
								# { "name" : "total_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_TOTAL_D, "all_align" : "center", },
							# ),
						# },
						# {
							# "name" : "total_deaths_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*4, "width" : 169-120-2, "height" : 24,
							
							# "children" : ( 
								# { "name" : "total_deaths", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							# ),
						# },		

						# {
							# "name" : "kd_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*5, "width" : 120, "height" : 24,
							
							# "children" : ( 
								# { "name" : "kd_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_KD, "all_align" : "center", },
							# ),
						# },
						# {
							# "name" : "kd_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*5, "width" : 169-120-2, "height" : 24,
							
							# "children" : ( 
								# { "name" : "kd", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							# ),
						# },	

						# { 
							# "name" : "duels_title", "type":"horizontalbar", "x":15, "y":50+27*6+9, "width":169, 
							# "children" : ( { "name" : "duels_title_bar", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_PVPD_TITLE, "all_align" : "center", }, ),
						# },
						
						{
							"name" : "duels_t_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*4, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "duels_t_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_DUELS_TOTAL, "all_align" : "center", },
							),
						},
						{
							"name" : "duels_t_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*4, "width" : 169-120-2, "height" : 24,
							
							"children" : ( 
								{ "name" : "duels_t", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							),
						},					
						
						{
							"name" : "duels_w_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*5, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "duels_w_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_DUELS_W, "all_align" : "center", },
							),
						},
						{
							"name" : "duels_w_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*5, "width" : 169-120-2, "height" : 24,
							
							"children" : ( 
								{ "name" : "duels_w", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							),
						},					
						{
							"name" : "duels_l_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*6, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "duels_l_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_DUELS_L, "all_align" : "center", },
							),
						},
						{
							"name" : "duels_l_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*6, "width" : 169-120-2, "height" : 24,
							
							"children" : ( 
								{ "name" : "duels_l", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							),
						},

						# { 
							# "name" : "pvm_title", "type":"horizontalbar", "x":15, "y":50+27*10+9, "width":169, 
							# "children" : ( { "name" : "pvm_title_bar", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_PVM_TITLE, "all_align" : "center", }, ),
						# },
						{
							"name" : "mobs_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*7, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "mobs_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_MOB, "all_align" : "center", },
							),
						},
						{
							"name" : "mobs_kills_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*7, "width" : 169-120-2, "height" : 24,
							
							"children" : ( 
								{ "name" : "mobs_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							),
						},
						{
							"name" : "stones_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*8, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "stones_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_STONES, "all_align" : "center", },
							),
						},
						{
							"name" : "stones_kills_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*8, "width" : 169-120-2, "height" : 24,
							
							"children" : ( 
								{ "name" : "stones_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							),
						},
						{
							"name" : "bosses_title_bg", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*9, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "bosses_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_BOSSES, "all_align" : "center", },
							),
						},
						{
							"name" : "bosses_kills_bg", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*9, "width" : 169-120-2, "height" : 24,
							
							"children" : ( 
								{ "name" : "bosses_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							),
						},
						{
							"name" : "", "type" : "thinboard_circle", "x" : 25, "y" : 50+27*10, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_MAX, "all_align" : "center", },
							),
						},
						{
							"name" : "", "type" : "thinboard_circle", "x" : 25+120+2, "y" : 50+27*10, "width" : 169-120-2, "height" : 24,
							
							"children" : ( 
								{ "name" : "top_damages", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
							),
						},
					),
				},
				{
					"name" : "karakterbonuspage",
					"type" : "window",
					"x" : 0,
					"y" : 0,
					"width" : MAINBOARD_WIDTH,
					"height" : MAINBOARD_HEIGHT,
					"children" :
					(
						## ½ºÅ©·Ñ ¹Ù
						{
							"name" : "ScrollBar",
							"type" : "scrollbar",

							"x" : 30,
							"y" : 44,
							"size" : MAINBOARD_HEIGHT - 65,
							"horizontal_align" : "right",
						},
						{ 
							"name" : "horizontalbar0", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":48+LABEL_GAP*0, "width":TITLE_BAR_WIDTH, "height" : 24, 
							"children" : ( { "name" : "horizontalbarName0", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						},
						{ 
							"name" : "horizontalbar1", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":48+LABEL_GAP*1, "width":TITLE_BAR_WIDTH, "height" : 24,
							"children" : ( { "name" : "horizontalbarName1", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						},
						{ 
							"name" : "horizontalbar2", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":48+LABEL_GAP*2, "width":TITLE_BAR_WIDTH, "height" : 24,
							"children" : ( { "name" : "horizontalbarName2", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						},
						{ 
							"name" : "horizontalbar3", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":48+LABEL_GAP*3, "width":TITLE_BAR_WIDTH, "height" : 24,
							"children" : ( { "name" : "horizontalbarName3", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						},
						{ 
							"name" : "horizontalbar4", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":48+LABEL_GAP*4, "width":TITLE_BAR_WIDTH, "height" : 24,
							"children" : ( { "name" : "horizontalbarName4", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						},
						{ 
							"name" : "horizontalbar5", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":48+LABEL_GAP*5, "width":TITLE_BAR_WIDTH,  "height" : 24,
							"children" : ( { "name" : "horizontalbarName5", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						},
						{ 
							"name" : "horizontalbar6", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":48+LABEL_GAP*6, "width":TITLE_BAR_WIDTH, "height" : 24,
							"children" : ( { "name" : "horizontalbarName6", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						},
						{ 
							"name" : "horizontalbar7", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":48+LABEL_GAP*7, "width":TITLE_BAR_WIDTH, "height" : 24,
							"children" : ( { "name" : "horizontalbarName7", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						},
						{ 
							"name" : "horizontalbar8", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":48+LABEL_GAP*8, "width":TITLE_BAR_WIDTH, "height" : 24,
							"children" : ( { "name" : "horizontalbarName8", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						},
						{ 
							"name" : "horizontalbar9", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":48+LABEL_GAP*9, "width":TITLE_BAR_WIDTH, "height" : 24,
							"children" : ( { "name" : "horizontalbarName9", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						},
						{ 
							"name" : "horizontalbar10", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":48+LABEL_GAP*10, "width":TITLE_BAR_WIDTH, "height" : 24,
							"children" : ( { "name" : "horizontalbarName10", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						},
						# { 
							# "name" : "horizontalbar11", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":32+LABEL_GAP*11, "width":TITLE_BAR_WIDTH,
							# "children" : ( { "name" : "horizontalbarName11", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						# },
						# { 
							# "name" : "horizontalbar12", "type":"thinboard_circle", "x":TITLE_BAR_POS_X, "y":32+LABEL_GAP*12, "width":TITLE_BAR_WIDTH,
							# "children" : ( { "name" : "horizontalbarName12", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", }, ),
						# }, ## È£¸®Áð ¹Ù ³¡
						
						## ¶óº§ ##
						{
							"name" : "label0", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 50+LABEL_GAP*0, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							"children" : ( 
								{ "name" : "labelvalue0", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{
							"name" : "label1", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 50+LABEL_GAP*1, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							"children" : ( 
								{ "name" : "labelvalue1", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{
							"name" : "label2", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 50+LABEL_GAP*2, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							"children" : ( 
								{ "name" : "labelvalue2", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{
							"name" : "label3", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 50+LABEL_GAP*3, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							"children" : ( 
								{ "name" : "labelvalue3", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{
							"name" : "label4", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 50+LABEL_GAP*4, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							"children" : ( 
								{ "name" : "labelvalue4", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{
							"name" : "label5", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 50+LABEL_GAP*5, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							"children" : ( 
								{ "name" : "labelvalue5", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{
							"name" : "label6", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 50+LABEL_GAP*6, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							"children" : ( 
								{ "name" : "labelvalue6", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{
							"name" : "label7", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 50+LABEL_GAP*7, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							"children" : ( 
								{ "name" : "labelvalue7", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{
							"name" : "label8", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 50+LABEL_GAP*8, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							"children" : ( 
								{ "name" : "labelvalue8", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{
							"name" : "label9", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 50+LABEL_GAP*9, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							"children" : ( 
								{ "name" : "labelvalue9", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{
							"name" : "label10", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 50+LABEL_GAP*10, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							"children" : ( 
								{ "name" : "labelvalue10", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						# {
							# "name" : "label11", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 30+LABEL_GAP*11, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							# "children" : ( 
								# { "name" : "labelvalue11", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							# ),
						# },
						# {
							# "name" : "label12", "type" : "thinboard_circle", "x" : LABEL_START_X, "y" : 30+LABEL_GAP*12, "width" : LABEL_WIDTH, "height" : LABEL_HEIGHT,
							# "children" : ( 
								# { "name" : "labelvalue12", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							# ),
						# }, ## ¶óº§ ³¡
						
						## ¹öÆ°
						{ 
							"name" : "labelname0", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*0, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{ 
							"name" : "labelname1", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*1, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{ 
							"name" : "labelname2", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*2, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{ 
							"name" : "labelname3", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*3, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{ 
							"name" : "labelname4", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*4, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},	
						{ 
							"name" : "labelname5", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*5, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},	
						{ 
							"name" : "labelname6", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*6, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{ 
							"name" : "labelname7", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*7, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},	
						{ 
							"name" : "labelname8", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*8, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},	
						{ 
							"name" : "labelname9", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*9, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						{ 
							"name" : "labelname10", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*10, "width" : 120, "height" : 24,
							
							"children" : ( 
								{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							),
						},
						# { 
							# "name" : "labelname11", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*11, "width" : 120, "height" : 24,
							
							# "children" : ( 
								# { "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							# ),
						# },	
						# { 
							# "name" : "labelname12", "type" : "thinboard_circle", "x" : LABEL_NAME_POS_X, "y" : LABEL_START_Y+LABEL_GAP*12, "width" : 120, "height" : 24,
							
							# "children" : ( 
								# { "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align" : "center", },
							# ),
						# },
					),
				},
				{
					"name" : "karakterbonus",
					"type" : "button",

					"x" : 20,
					"y" : 10,
					"height" : 90,
					"width" : 90,
					"text" : "Bonuslar",

					"default_image" : "yusuf_etc/slot_normal.tga",
					"over_image" : "yusuf_etc/slot_active.tga",
					"down_image" : "yusuf_etc/slot_hover.tga",
				},
				{
					"name" : "killbonus",
					"type" : "button",

					"x" : 120,
					"y" : 10,
					"height" : 90,
					"width" : 90,
					"text" : "Ýstatistikler",

					"default_image" : "yusuf_etc/slot_normal.tga",
					"over_image" : "yusuf_etc/slot_active.tga",
					"down_image" : "yusuf_etc/slot_hover.tga",
				},
			),
		}, ## MainBoard End
	),
}