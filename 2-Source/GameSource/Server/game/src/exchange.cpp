#include "stdafx.h"
#include "../../libgame/include/grid.h"
#include "utils.h"
#include "desc.h"
#include "desc_client.h"
#include "char.h"
#include "item.h"
#include "item_manager.h"
#include "packet.h"
#include "log.h"
#include "db.h"
#include "locale_service.h"
#include "../../common/length.h"
#include "exchange.h"
#include "DragonSoul.h"
#include "questmanager.h" // @fixme150

void exchange_packet(LPCHARACTER ch, BYTE sub_header, bool is_me, DWORD arg1, TItemPos arg2, DWORD arg3, void * pvData = NULL);


void exchange_packet(LPCHARACTER ch, BYTE sub_header, bool is_me, DWORD arg1, TItemPos arg2, DWORD arg3, void * pvData)
{
	if (!ch->GetDesc())
		return;

	struct packet_exchange pack_exchg;

	pack_exchg.header 		= HEADER_GC_EXCHANGE;
	pack_exchg.sub_header 	= sub_header;
	pack_exchg.is_me		= is_me;
	pack_exchg.arg1		= arg1;
	pack_exchg.arg2		= arg2;
	pack_exchg.arg3		= arg3;

	if (sub_header == EXCHANGE_SUBHEADER_GC_ITEM_ADD && pvData)
	{
		thecore_memcpy(&pack_exchg.alSockets, ((LPITEM) pvData)->GetSockets(), sizeof(pack_exchg.alSockets));
		thecore_memcpy(&pack_exchg.aAttr, ((LPITEM) pvData)->GetAttributes(), sizeof(pack_exchg.aAttr));
	}
	else
	{
		memset(&pack_exchg.alSockets, 0, sizeof(pack_exchg.alSockets));
		memset(&pack_exchg.aAttr, 0, sizeof(pack_exchg.aAttr));
	}

	ch->GetDesc()->Packet(&pack_exchg, sizeof(pack_exchg));
}


bool CHARACTER::ExchangeStart(LPCHARACTER victim)
{
	if (this == victim)
		return false;

	if (IsObserverMode())
	{
		ChatPacket(CHAT_TYPE_INFO, LC_TEXT("관전 상태에서는 교환을 할 수 없습니다."));
		return false;
	}

	if (victim->IsNPC())
		return false;

	//PREVENT_TRADE_WINDOW
	if ( IsOpenSafebox() || GetShopOwner() || GetMyShop() || IsCubeOpen()
#ifdef __AURA_SYSTEM__
		|| IsAuraRefineWindowOpen()

#endif
		)
	{
		ChatPacket( CHAT_TYPE_INFO, LC_TEXT("다른 거래창이 열려있을경우 거래를 할수 없습니다." ) );
		return false;
	}

	if ( victim->IsOpenSafebox() || victim->GetShopOwner() || victim->GetMyShop() || victim->IsCubeOpen() 
#ifdef __AURA_SYSTEM__
		|| victim->IsAuraRefineWindowOpen()
#endif
		)
	{
		ChatPacket( CHAT_TYPE_INFO, LC_TEXT("상대방이 다른 거래중이라 거래를 할수 없습니다." ) );
		return false;
	}
	//END_PREVENT_TRADE_WINDOW
	int iDist = DISTANCE_APPROX(GetX() - victim->GetX(), GetY() - victim->GetY());


	if (iDist >= EXCHANGE_MAX_DISTANCE)
		return false;

	if (GetExchange())
		return false;

	if (victim->GetExchange())
	{
		exchange_packet(this, EXCHANGE_SUBHEADER_GC_ALREADY, 0, 0, NPOS, 0);
		return false;
	}

	if (victim->IsBlockMode(BLOCK_EXCHANGE))
	{
		ChatPacket(CHAT_TYPE_INFO, LC_TEXT("상대방이 교환 거부 상태입니다."));
		return false;
	}

	SetExchange(M2_NEW CExchange(this));
	victim->SetExchange(M2_NEW CExchange(victim));

	victim->GetExchange()->SetCompany(GetExchange());
	GetExchange()->SetCompany(victim->GetExchange());

	//
	SetExchangeTime();
	victim->SetExchangeTime();

	exchange_packet(victim, EXCHANGE_SUBHEADER_GC_START, 0, GetVID(), NPOS, 0);
	exchange_packet(this, EXCHANGE_SUBHEADER_GC_START, 0, victim->GetVID(), NPOS, 0);

	return true;
}

CExchange::CExchange(LPCHARACTER pOwner)
{
	m_pCompany = NULL;

	m_bAccept = false;

	for (int i = 0; i < EXCHANGE_ITEM_MAX_NUM; ++i)
	{
		m_apItems[i] = NULL;
		m_aItemPos[i] = NPOS;
		m_abItemDisplayPos[i] = 0;
	}

	m_lGold = 0;

	m_pOwner = pOwner;
	pOwner->SetExchange(this);

	m_pGrid = M2_NEW CGrid(4,3);
}

CExchange::~CExchange()
{
	M2_DELETE(m_pGrid);
}

bool CExchange::AddItem(TItemPos item_pos, BYTE display_pos)
{
	assert(m_pOwner != NULL && GetCompany());

	if (!item_pos.IsValidItemPosition())
		return false;


	if (item_pos.IsEquipPosition())
		return false;

	LPITEM item;

	if (!(item = m_pOwner->GetItem(item_pos)))
		return false;

	if (IS_SET(item->GetAntiFlag(), ITEM_ANTIFLAG_GIVE))
	{
		m_pOwner->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("아이템을 건네줄 수 없습니다."));
		return false;
	}

	if (true == item->isLocked())
	{
		return false;
	}


	if (item->IsExchanging())
	{
		sys_log(0, "EXCHANGE under exchanging");
		return false;
	}

	if (!m_pGrid->IsEmpty(display_pos, 1, item->GetSize()))
	{
		sys_log(0, "EXCHANGE not empty item_pos %d %d %d", display_pos, 1, item->GetSize());
		return false;
	}

	Accept(false);
	GetCompany()->Accept(false);

	for (int i = 0; i < EXCHANGE_ITEM_MAX_NUM; ++i)
	{
		if (m_apItems[i])
			continue;

		m_apItems[i]		= item;
		m_aItemPos[i]		= item_pos;
		m_abItemDisplayPos[i]	= display_pos;
		m_pGrid->Put(display_pos, 1, item->GetSize());

		item->SetExchanging(true);

		exchange_packet(m_pOwner,
				EXCHANGE_SUBHEADER_GC_ITEM_ADD,
				true,
				item->GetVnum(),
				TItemPos(RESERVED_WINDOW, display_pos),
				item->GetCount(),
				item);

		exchange_packet(GetCompany()->GetOwner(),
				EXCHANGE_SUBHEADER_GC_ITEM_ADD,
				false,
				item->GetVnum(),
				TItemPos(RESERVED_WINDOW, display_pos),
				item->GetCount(),
				item);

		sys_log(0, "EXCHANGE AddItem success %s pos(%d, %d) %d", item->GetName(), item_pos.window_type, item_pos.cell, display_pos);

		return true;
	}


	return false;
}

bool CExchange::RemoveItem(BYTE pos)
{
	if (pos >= EXCHANGE_ITEM_MAX_NUM)
		return false;

	if (!m_apItems[pos])
		return false;

	TItemPos PosOfInventory = m_aItemPos[pos];
	m_apItems[pos]->SetExchanging(false);

	m_pGrid->Get(m_abItemDisplayPos[pos], 1, m_apItems[pos]->GetSize());

	exchange_packet(GetOwner(),	EXCHANGE_SUBHEADER_GC_ITEM_DEL, true, pos, NPOS, 0);
	exchange_packet(GetCompany()->GetOwner(), EXCHANGE_SUBHEADER_GC_ITEM_DEL, false, pos, PosOfInventory, 0);

	Accept(false);
	GetCompany()->Accept(false);

	m_apItems[pos]	    = NULL;
	m_aItemPos[pos]	    = NPOS;
	m_abItemDisplayPos[pos] = 0;
	return true;
}

bool CExchange::AddGold(long gold)
{
	if (gold <= 0)
		return false;

	if (GetOwner()->GetGold() < gold)
	{

		exchange_packet(GetOwner(), EXCHANGE_SUBHEADER_GC_LESS_GOLD, 0, 0, NPOS, 0);
		return false;
	}

	if (m_lGold > 0)
		return false;

	Accept(false);
	GetCompany()->Accept(false);

	m_lGold = gold;

	exchange_packet(GetOwner(), EXCHANGE_SUBHEADER_GC_GOLD_ADD, true, m_lGold, NPOS, 0);
	exchange_packet(GetCompany()->GetOwner(), EXCHANGE_SUBHEADER_GC_GOLD_ADD, false, m_lGold, NPOS, 0);
	return true;
}


bool CExchange::Check(int * piItemCount)
{
	if (GetOwner()->GetGold() < m_lGold)
		return false;

	int item_count = 0;

	for (int i = 0; i < EXCHANGE_ITEM_MAX_NUM; ++i)
	{
		if (!m_apItems[i])
			continue;

		if (!m_aItemPos[i].IsValidItemPosition())
			return false;

		if (m_apItems[i] != GetOwner()->GetItem(m_aItemPos[i]))
			return false;

		++item_count;
	}

	*piItemCount = item_count;
	return true;
}

bool CExchange::CheckSpace()
{
	static CGrid s_grid1(INVENTORY_PAGE_COLUMN, INVENTORY_PAGE_ROW); // inven page 1
	static CGrid s_grid2(INVENTORY_PAGE_COLUMN, INVENTORY_PAGE_ROW); // inven page 2
#ifdef ENABLE_EXTEND_INVEN_SYSTEM
	static CGrid s_grid3(INVENTORY_PAGE_COLUMN, INVENTORY_PAGE_ROW); // inven page 3
	static CGrid s_grid4(INVENTORY_PAGE_COLUMN, INVENTORY_PAGE_ROW); // inven page 4
#endif

	s_grid1.Clear();
	s_grid2.Clear();
#ifdef ENABLE_EXTEND_INVEN_SYSTEM
	s_grid3.Clear();
	s_grid4.Clear();
#endif

	LPCHARACTER	victim = GetCompany()->GetOwner();
	LPITEM item;

	int i;

	for (i = 0; i < INVENTORY_PAGE_SIZE*1; ++i)
	{
		if (!(item = victim->GetInventoryItem(i)))
			continue;

		s_grid1.Put(i, 1, item->GetSize());
	}
	for (i = INVENTORY_PAGE_SIZE*1; i < INVENTORY_PAGE_SIZE*2; ++i)
	{
		if (!(item = victim->GetInventoryItem(i)))
			continue;

		s_grid2.Put(i - INVENTORY_PAGE_SIZE*1, 1, item->GetSize());
	}
#ifdef ENABLE_EXTEND_INVEN_SYSTEM
	for (i = INVENTORY_PAGE_SIZE*2; i < INVENTORY_PAGE_SIZE*3; ++i)
	{
		if (!(item = victim->GetInventoryItem(i)))
			continue;

		s_grid3.Put(i - INVENTORY_PAGE_SIZE*2, 1, item->GetSize());
	}
	for (i = INVENTORY_PAGE_SIZE*3; i < INVENTORY_PAGE_SIZE*4; ++i)
	{
		if (!(item = victim->GetInventoryItem(i)))
			continue;

		s_grid4.Put(i - INVENTORY_PAGE_SIZE*3, 1, item->GetSize());
	}
#endif


	static std::vector <WORD> s_vDSGrid(DRAGON_SOUL_INVENTORY_MAX_NUM);


	bool bDSInitialized = false;

	for (i = 0; i < EXCHANGE_ITEM_MAX_NUM; ++i)
	{
		if (!(item = m_apItems[i]))
			continue;

		if (item->IsDragonSoul())
		{
			if (!victim->DragonSoul_IsQualified())
			{
				return false;
			}
#ifdef ENABLE_SPECIAL_STORAGE
			else if (item->IsUpgradeItem())
			{
				return true;
			}
			else if (item->IsBook())
			{
				return true;
			}
			else if (item->IsStone())
			{
				return true;
			}
			else if (item->IsChest())
			{
				return true;
			}
#endif
			if (!bDSInitialized)
			{
				bDSInitialized = true;
				victim->CopyDragonSoulItemGrid(s_vDSGrid);
			}

			bool bExistEmptySpace = false;
			WORD wBasePos = DSManager::instance().GetBasePosition(item);
			if (wBasePos >= DRAGON_SOUL_INVENTORY_MAX_NUM)
				return false;

			for (int i = 0; i < DRAGON_SOUL_BOX_SIZE; i++)
			{
				WORD wPos = wBasePos + i;
				if (0 == s_vDSGrid[wPos]) // @fixme159 (wBasePos to wPos)
				{
					bool bEmpty = true;
					for (int j = 1; j < item->GetSize(); j++)
					{
						if (s_vDSGrid[wPos + j * DRAGON_SOUL_BOX_COLUMN_NUM])
						{
							bEmpty = false;
							break;
						}
					}
					if (bEmpty)
					{
						for (int j = 0; j < item->GetSize(); j++)
						{
							s_vDSGrid[wPos + j * DRAGON_SOUL_BOX_COLUMN_NUM] =  wPos + 1;
						}
						bExistEmptySpace = true;
						break;
					}
				}
				if (bExistEmptySpace)
					break;
			}
			if (!bExistEmptySpace)
				return false;
		}
		else
		{
			int iPos;

			if ((iPos = s_grid1.FindBlank(1, item->GetSize())) >= 0)
			{
				s_grid1.Put(iPos, 1, item->GetSize());
			}
			else if ((iPos = s_grid2.FindBlank(1, item->GetSize())) >= 0)
			{
				s_grid2.Put(iPos, 1, item->GetSize());
			}
#ifdef ENABLE_EXTEND_INVEN_SYSTEM
			else if ((iPos = s_grid3.FindBlank(1, item->GetSize())) >= 0)
			{
				s_grid3.Put(iPos, 1, item->GetSize());
			}
			else if ((iPos = s_grid4.FindBlank(1, item->GetSize())) >= 0)
			{
				s_grid4.Put(iPos, 1, item->GetSize());
			}
#endif
			else
				return false;
		}
	}

	return true;
}

bool CExchange::CheckSpaceDragonSoulInventory()
{
	LPCHARACTER	victim = GetCompany()->GetOwner();
	LPCHARACTER	owner = GetOwner();
	LPITEM item;

	bool elmas = false, yakut = false, yesim = false, safir = false, grena = false, onik = false;
	//Envanter//
	int elmas_1 = 0, elmas_2 = 0;
	int yakut_1 = 0, yakut_2 = 0;
	int yesim_1 = 0, yesim_2 = 0;
	int safir_1 = 0, safir_2 = 0;
	int grena_1 = 0, grena_2 = 0;
	int onik_1 = 0, onik_2 = 0;
	//Ticaret//
	int t_elmas_1 = 0, t_elmas_2 = 0;
	int t_yakut_1 = 0, t_yakut_2 = 0;
	int t_yesim_1 = 0, t_yesim_2 = 0;
	int t_safir_1 = 0, t_safir_2 = 0;
	int t_grena_1 = 0, t_grena_2 = 0;
	int t_onik_1 = 0, t_onik_2 = 0;

	for (int t = 0; t < EXCHANGE_ITEM_MAX_NUM; ++t)
	{
		if (!(item = m_apItems[t]))
			continue;

		if (item->IsDragonSoul())
		{
			if (!(owner->DragonSoul_IsQualified()))
			{
				owner->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("먼저 용혼석 퀘스트를 완료하셔야 합니다."));
				victim->ChatPacket(CHAT_TYPE_INFO, "Karsi taraf simya gorevini yapmadigi icin ticaret iptal edildi.");
				return false;
			}

			if (!(victim->DragonSoul_IsQualified()))
			{
				victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("먼저 용혼석 퀘스트를 완료하셔야 합니다."));
				owner->ChatPacket(CHAT_TYPE_INFO, "Karsi taraf simya gorevini yapmadigi icin ticaret iptal edildi.");
				return false;
			}

			DWORD item_no = item->GetVnum();
			BYTE col_type = item->GetSubType();
			if (col_type == 0)
			{
				if (!elmas) { elmas = true; }
				if (item_no >= 110000 && item_no < 113000)
				{
					owner->ChatPacket(CHAT_TYPE_INFO, "Bu itemi (%s) ticarette kullanamazsin!", item->GetName());
					victim->ChatPacket(CHAT_TYPE_INFO, "Karsi taraf ticarette kullanilamayacak item (%s) koydu!", item->GetName());
					return false;
				}
				if (item_no >= 113000 && item_no <= 113400) { t_elmas_1 += item->GetSize(); }
				if (item_no >= 114000 && item_no <= 114400) { t_elmas_2 += item->GetSize(); }
			}
			else if (col_type == 1)
			{
				if (!yakut) { yakut = true; }
				if (item_no >= 120000 && item_no < 123000)
				{
					owner->ChatPacket(CHAT_TYPE_INFO, "Bu itemi (%s) ticarette kullanamazsin!", item->GetName());
					victim->ChatPacket(CHAT_TYPE_INFO, "Karsi taraf ticarette kullanilamayacak item (%s) koydu!", item->GetName());
					return false;
				}
				if (item_no >= 123000 && item_no <= 123400) { t_yakut_1 += item->GetSize(); }
				if (item_no >= 124000 && item_no <= 124400) { t_yakut_2 += item->GetSize(); }
			}
			else if (col_type == 2)
			{
				if (!yesim) { yesim = true; }
				if (item_no >= 130000 && item_no < 133000)
				{
					owner->ChatPacket(CHAT_TYPE_INFO, "Bu itemi (%s) ticarette kullanamazsin!", item->GetName());
					victim->ChatPacket(CHAT_TYPE_INFO, "Karsi taraf ticarette kullanilamayacak item (%s) koydu!", item->GetName());
					return false;
				}
				if (item_no >= 133000 && item_no <= 133400) { t_yesim_1 += item->GetSize(); }
				if (item_no >= 134000 && item_no <= 134400) { t_yesim_2 += item->GetSize(); }
			}
			else if (col_type == 3)
			{
				if (!safir) { safir = true; }
				if (item_no >= 140000 && item_no < 143000)
				{
					owner->ChatPacket(CHAT_TYPE_INFO, "Bu itemi (%s) ticarette kullanamazsin!", item->GetName());
					victim->ChatPacket(CHAT_TYPE_INFO, "Karsi taraf ticarette kullanilamayacak item (%s) koydu!", item->GetName());
					return false;
				}
				if (item_no >= 143000 && item_no <= 143400) { t_safir_1 += item->GetSize(); }
				if (item_no >= 144000 && item_no <= 144400) { t_safir_2 += item->GetSize(); }
			}
			else if (col_type == 4)
			{
				if (!grena) { grena = true; }
				if (item_no >= 150000 && item_no < 153000)
				{
					owner->ChatPacket(CHAT_TYPE_INFO, "Bu itemi (%s) ticarette kullanamazsin!", item->GetName());
					victim->ChatPacket(CHAT_TYPE_INFO, "Karsi taraf ticarette kullanilamayacak item (%s) koydu!", item->GetName());
					return false;
				}
				if (item_no >= 153000 && item_no <= 153400) { t_grena_1 += item->GetSize(); }
				if (item_no >= 154000 && item_no <= 154400) { t_grena_2 += item->GetSize(); }
			}
			else if (col_type == 5)
			{
				if (!onik) { onik = true; }
				if (item_no >= 160000 && item_no < 163000)
				{
					owner->ChatPacket(CHAT_TYPE_INFO, "Bu itemi (%s) ticarette kullanamazsin!", item->GetName());
					victim->ChatPacket(CHAT_TYPE_INFO, "Karsi taraf ticarette kullanilamayacak item (%s) koydu!", item->GetName());
					return false;
				}
				if (item_no >= 163000 && item_no <= 163400) { t_onik_1 += item->GetSize(); }
				if (item_no >= 164000 && item_no <= 164400) { t_onik_2 += item->GetSize(); }
			}
		}
	}

	if (elmas)
	{
		if (t_elmas_1 > 0)
		{
			for (int c = 96; c < 128; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				elmas_1 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - elmas_1;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Elmas1 Tic item: %d, Env item: %d, Bos slot: %d", t_elmas_1, elmas_1, bos_slot);
			if (bos_slot < t_elmas_1) return false;
		}

		if (t_elmas_2 > 0)
		{
			for (int c = 128; c < 160; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				elmas_2 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - elmas_2;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Elmas2 Tic item: %d, Env item: %d, Bos slot: %d", t_elmas_2, elmas_2, bos_slot);
			if (bos_slot < t_elmas_2) return false;
		}
	}

	if (yakut)
	{
		if (t_yakut_1 > 0)
		{
			for (int c = 256; c < 288; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				yakut_1 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - yakut_1;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Yakut1 Tic item: %d, Env item: %d, Bos slot: %d", t_yakut_1, yakut_1, bos_slot);
			if (bos_slot < t_yakut_1) return false;
		}

		if (t_yakut_2 > 0)
		{
			for (int c = 288; c < 320; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				yakut_2 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - yakut_2;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Yakut2 Tic item: %d, Env item: %d, Bos slot: %d", t_yakut_2, yakut_2, bos_slot);
			if (bos_slot < t_yakut_2) return false;
		}
	}

	if (yesim)
	{
		if (t_yesim_1 > 0)
		{
			for (int c = 416; c < 448; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				yesim_1 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - yesim_1;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Yesim1 Tic item: %d, Env item: %d, Bos slot: %d", t_yesim_1, yesim_1, bos_slot);
			if (bos_slot < t_yesim_1) return false;
		}

		if (t_yesim_2 > 0)
		{
			for (int c = 448; c < 480; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				yesim_2 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - yesim_2;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Yesim2 Tic item: %d, Env item: %d, Bos slot: %d", t_yesim_2, yesim_2, bos_slot);
			if (bos_slot < t_yesim_2) return false;
		}
	}

	if (safir)
	{
		if (t_safir_1 > 0)
		{
			for (int c = 576; c < 608; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				safir_1 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - safir_1;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Safir1 Tic item: %d, Env item: %d, Bos slot: %d", t_safir_1, safir_1, bos_slot);
			if (bos_slot < t_safir_1) return false;
		}

		if (t_safir_2 > 0)
		{
			for (int c = 608; c < 640; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				safir_2 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - safir_2;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Safir2 Tic item: %d, Env item: %d, Bos slot: %d", t_safir_2, safir_2, bos_slot);
			if (bos_slot < t_safir_2) return false;
		}
	}

	if (grena)
	{
		if (t_grena_1 > 0)
		{
			for (int c = 736; c < 768; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				grena_1 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - grena_1;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Grena1 Tic item: %d, Env item: %d, Bos slot: %d", t_grena_1, grena_1, bos_slot);
			if (bos_slot < t_grena_1) return false;
		}

		if (t_grena_2 > 0)
		{
			for (int c = 768; c < 800; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				grena_2 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - grena_2;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Grena2 Tic item: %d, Env item: %d, Bos slot: %d", t_grena_2, grena_2, bos_slot);
			if (bos_slot < t_grena_2) return false;
		}
	}

	if (onik)
	{
		if (t_onik_1 > 0)
		{
			for (int c = 896; c < 928; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				onik_1 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - onik_1;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Onik1 Tic item: %d, Env item: %d, Bos slot: %d", t_onik_1, onik_1, bos_slot);
			if (bos_slot < t_onik_1) return false;
		}

		if (t_onik_2 > 0)
		{
			for (int c = 928; c < 960; ++c)
			{
				if (!(item = victim->GetItem(TItemPos(DRAGON_SOUL_INVENTORY, c))))
					continue;

				onik_2 += item->GetSize();
			}

			int bos_slot = DRAGON_SOUL_BOX_SIZE - onik_2;
			//victim->ChatPacket(CHAT_TYPE_INFO, "Onik2 Tic item: %d, Env item: %d, Bos slot: %d", t_onik_2, onik_2, bos_slot);
			if (bos_slot < t_onik_2) return false;
		}
	}

	return true;
}

#ifdef ENABLE_SPECIAL_STORAGE
bool CExchange::CheckSpaceUpdateInventory()
{
	static CGrid s_upp_grid1(5, 9);
	static CGrid s_upp_grid2(5, 9);
	static CGrid s_upp_grid3(5, 9);
	static CGrid s_upp_grid4(5, 9);

	s_upp_grid1.Clear();
	s_upp_grid2.Clear();
	s_upp_grid3.Clear();
	s_upp_grid4.Clear();

	LPCHARACTER victim = GetCompany()->GetOwner();
	LPITEM item;

	int i;
	for (i = 0; i < SPECIAL_INVENTORY_PAGE_SIZE; ++i)
	{
		if (!(item = victim->GetUpgradeInventoryItem(i)))
			continue;

		s_upp_grid1.Put(i, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE; i < SPECIAL_INVENTORY_PAGE_SIZE * 2; ++i)
	{
		if (!(item = victim->GetUpgradeInventoryItem(i)))
			continue;

		s_upp_grid2.Put(i - SPECIAL_INVENTORY_PAGE_SIZE, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE * 2; i < SPECIAL_INVENTORY_PAGE_SIZE * 3; ++i)
	{
		if (!(item = victim->GetUpgradeInventoryItem(i)))
			continue;

		s_upp_grid3.Put(i - SPECIAL_INVENTORY_PAGE_SIZE * 2, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE * 3; i < SPECIAL_INVENTORY_PAGE_SIZE * 4; ++i)
	{
		if (!(item = victim->GetUpgradeInventoryItem(i)))
			continue;

		s_upp_grid4.Put(i - SPECIAL_INVENTORY_PAGE_SIZE * 3, 1, item->GetSize());
	}

	for (i = 0; i < EXCHANGE_ITEM_MAX_NUM; ++i)
	{
		if (!(item = m_apItems[i]))
			continue;

		if (item->IsUpgradeItem())
		{
			int iPos = s_upp_grid1.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_upp_grid1.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_upp_grid2.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_upp_grid2.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_upp_grid3.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_upp_grid3.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_upp_grid4.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_upp_grid4.Put(iPos, 1, item->GetSize());
				continue;
			}

			return false;
		}
	}

	return true;
}

bool CExchange::CheckSpaceBookInventory()
{
	static CGrid s_book_grid1(5, 9);
	static CGrid s_book_grid2(5, 9);
	static CGrid s_book_grid3(5, 9);
	static CGrid s_book_grid4(5, 9);

	s_book_grid1.Clear();
	s_book_grid2.Clear();
	s_book_grid3.Clear();
	s_book_grid4.Clear();

	LPCHARACTER victim = GetCompany()->GetOwner();
	LPITEM item;

	int i;
	for (i = 0; i < SPECIAL_INVENTORY_PAGE_SIZE; ++i)
	{
		if (!(item = victim->GetBookInventoryItem(i)))
			continue;

		s_book_grid1.Put(i, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE; i < SPECIAL_INVENTORY_PAGE_SIZE * 2; ++i)
	{
		if (!(item = victim->GetBookInventoryItem(i)))
			continue;

		s_book_grid2.Put(i - SPECIAL_INVENTORY_PAGE_SIZE, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE * 2; i < SPECIAL_INVENTORY_PAGE_SIZE * 3; ++i)
	{
		if (!(item = victim->GetBookInventoryItem(i)))
			continue;

		s_book_grid3.Put(i - SPECIAL_INVENTORY_PAGE_SIZE * 2, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE * 3; i < SPECIAL_INVENTORY_PAGE_SIZE * 4; ++i)
	{
		if (!(item = victim->GetBookInventoryItem(i)))
			continue;

		s_book_grid4.Put(i - SPECIAL_INVENTORY_PAGE_SIZE * 3, 1, item->GetSize());
	}

	for (i = 0; i < EXCHANGE_ITEM_MAX_NUM; ++i)
	{
		if (!(item = m_apItems[i]))
			continue;

		if (item->IsBook())
		{
			int iPos = s_book_grid1.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_book_grid1.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_book_grid2.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_book_grid2.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_book_grid3.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_book_grid3.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_book_grid4.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_book_grid4.Put(iPos, 1, item->GetSize());
				continue;
			}

			return false;
		}
	}

	return true;
}

bool CExchange::CheckSpaceStoneInventory()
{
	static CGrid s_stone_grid1(5, 9);
	static CGrid s_stone_grid2(5, 9);
	static CGrid s_stone_grid3(5, 9);
	static CGrid s_stone_grid4(5, 9);

	s_stone_grid1.Clear();
	s_stone_grid2.Clear();
	s_stone_grid3.Clear();
	s_stone_grid4.Clear();

	LPCHARACTER victim = GetCompany()->GetOwner();
	LPITEM item;

	int i;
	for (i = 0; i < SPECIAL_INVENTORY_PAGE_SIZE; ++i)
	{
		if (!(item = victim->GetStoneInventoryItem(i)))
			continue;

		s_stone_grid1.Put(i, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE; i < SPECIAL_INVENTORY_PAGE_SIZE * 2; ++i)
	{
		if (!(item = victim->GetStoneInventoryItem(i)))
			continue;

		s_stone_grid2.Put(i - SPECIAL_INVENTORY_PAGE_SIZE, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE * 2; i < SPECIAL_INVENTORY_PAGE_SIZE * 3; ++i)
	{
		if (!(item = victim->GetStoneInventoryItem(i)))
			continue;

		s_stone_grid3.Put(i - SPECIAL_INVENTORY_PAGE_SIZE * 2, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE * 3; i < SPECIAL_INVENTORY_PAGE_SIZE * 4; ++i)
	{
		if (!(item = victim->GetStoneInventoryItem(i)))
			continue;

		s_stone_grid4.Put(i - SPECIAL_INVENTORY_PAGE_SIZE * 3, 1, item->GetSize());
	}

	for (i = 0; i < EXCHANGE_ITEM_MAX_NUM; ++i)
	{
		if (!(item = m_apItems[i]))
			continue;

		if (item->IsStone())
		{
			int iPos = s_stone_grid1.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_stone_grid1.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_stone_grid2.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_stone_grid2.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_stone_grid3.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_stone_grid3.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_stone_grid4.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_stone_grid4.Put(iPos, 1, item->GetSize());
				continue;
			}

			return false;
		}
	}

	return true;
}

bool CExchange::CheckSpaceChestInventory()
{
	static CGrid s_chest_grid1(5, 9);
	static CGrid s_chest_grid2(5, 9);
	static CGrid s_chest_grid3(5, 9);
	static CGrid s_chest_grid4(5, 9);

	s_chest_grid1.Clear();
	s_chest_grid2.Clear();
	s_chest_grid3.Clear();
	s_chest_grid4.Clear();

	LPCHARACTER victim = GetCompany()->GetOwner();
	LPITEM item;

	int i;
	for (i = 0; i < SPECIAL_INVENTORY_PAGE_SIZE; ++i)
	{
		if (!(item = victim->GetChestInventoryItem(i)))
			continue;

		s_chest_grid1.Put(i, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE; i < SPECIAL_INVENTORY_PAGE_SIZE * 2; ++i)
	{
		if (!(item = victim->GetChestInventoryItem(i)))
			continue;

		s_chest_grid2.Put(i - SPECIAL_INVENTORY_PAGE_SIZE, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE * 2; i < SPECIAL_INVENTORY_PAGE_SIZE * 3; ++i)
	{
		if (!(item = victim->GetChestInventoryItem(i)))
			continue;

		s_chest_grid3.Put(i - SPECIAL_INVENTORY_PAGE_SIZE * 2, 1, item->GetSize());
	}
	for (i = SPECIAL_INVENTORY_PAGE_SIZE * 3; i < SPECIAL_INVENTORY_PAGE_SIZE * 4; ++i)
	{
		if (!(item = victim->GetChestInventoryItem(i)))
			continue;

		s_chest_grid4.Put(i - SPECIAL_INVENTORY_PAGE_SIZE * 3, 1, item->GetSize());
	}

	for (i = 0; i < EXCHANGE_ITEM_MAX_NUM; ++i)
	{
		if (!(item = m_apItems[i]))
			continue;

		if (item->IsChest())
		{
			int iPos = s_chest_grid1.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_chest_grid1.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_chest_grid2.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_chest_grid2.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_chest_grid3.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_chest_grid3.Put(iPos, 1, item->GetSize());
				continue;
			}

			iPos = s_chest_grid4.FindBlank(1, item->GetSize());
			if (iPos >= 0)
			{
				s_chest_grid4.Put(iPos, 1, item->GetSize());
				continue;
			}

			return false;
		}
	}

	return true;
}
#endif

bool CExchange::Done()
{
	int		empty_pos, i;
	LPITEM	item;

	LPCHARACTER	victim = GetCompany()->GetOwner();

	for (i = 0; i < EXCHANGE_ITEM_MAX_NUM; ++i)
	{
		if (!(item = m_apItems[i]))
			continue;

		if (item->IsDragonSoul())
			empty_pos = victim->GetEmptyDragonSoulInventory(item);
#ifdef ENABLE_SPECIAL_STORAGE
		else if (item->IsUpgradeItem())
			empty_pos = victim->GetEmptyUpgradeInventory(item);
		else if (item->IsBook())
			empty_pos = victim->GetEmptyBookInventory(item);
		else if (item->IsStone())
			empty_pos = victim->GetEmptyStoneInventory(item);
		else if (item->IsChest())
			empty_pos = victim->GetEmptyChestInventory(item);
#endif
		else
			empty_pos = victim->GetEmptyInventory(item->GetSize());

		if (empty_pos < 0)
		{
			sys_err("Exchange::Done : Cannot find blank position in inventory %s <-> %s item %s",
					m_pOwner->GetName(), victim->GetName(), item->GetName());
			continue;
		}

		assert(empty_pos >= 0);

		if (item->GetVnum() == 90008 || item->GetVnum() == 90009) // VCARD
		{
			VCardUse(m_pOwner, victim, item);
			continue;
		}

		m_pOwner->SyncQuickslot(QUICKSLOT_TYPE_ITEM, item->GetCell(), 255);

		item->RemoveFromCharacter();
		if (item->IsDragonSoul())
			item->AddToCharacter(victim, TItemPos(DRAGON_SOUL_INVENTORY, empty_pos));
#ifdef ENABLE_SPECIAL_STORAGE
		else if (item->IsUpgradeItem())
			item->AddToCharacter(victim, TItemPos(UPGRADE_INVENTORY, empty_pos));
		else if (item->IsBook())
			item->AddToCharacter(victim, TItemPos(BOOK_INVENTORY, empty_pos));
		else if (item->IsStone())
			item->AddToCharacter(victim, TItemPos(STONE_INVENTORY, empty_pos));
		else if (item->IsChest())
			item->AddToCharacter(victim, TItemPos(CHEST_INVENTORY, empty_pos));
#endif
		else
			item->AddToCharacter(victim, TItemPos(INVENTORY, empty_pos));
		ITEM_MANAGER::instance().FlushDelayedSave(item);

		item->SetExchanging(false);
		{
			char exchange_buf[51];

			snprintf(exchange_buf, sizeof(exchange_buf), "%s %u %u", item->GetName(), GetOwner()->GetPlayerID(), item->GetCount());
			LogManager::instance().ItemLog(victim, item, "EXCHANGE_TAKE", exchange_buf);

			snprintf(exchange_buf, sizeof(exchange_buf), "%s %u %u", item->GetName(), victim->GetPlayerID(), item->GetCount());
			LogManager::instance().ItemLog(GetOwner(), item, "EXCHANGE_GIVE", exchange_buf);

			if (item->GetVnum() >= 80003 && item->GetVnum() <= 80007)
			{
				LogManager::instance().GoldBarLog(victim->GetPlayerID(), item->GetID(), EXCHANGE_TAKE, "");
				LogManager::instance().GoldBarLog(GetOwner()->GetPlayerID(), item->GetID(), EXCHANGE_GIVE, "");
			}
		}

		m_apItems[i] = NULL;
	}

	if (m_lGold)
	{
		GetOwner()->PointChange(POINT_GOLD, -m_lGold, true);
		victim->PointChange(POINT_GOLD, m_lGold, true);

		if (m_lGold > 1000)
		{
			char exchange_buf[51];
			snprintf(exchange_buf, sizeof(exchange_buf), "%u %s", GetOwner()->GetPlayerID(), GetOwner()->GetName());
			LogManager::instance().CharLog(victim, m_lGold, "EXCHANGE_GOLD_TAKE", exchange_buf);

			snprintf(exchange_buf, sizeof(exchange_buf), "%u %s", victim->GetPlayerID(), victim->GetName());
			LogManager::instance().CharLog(GetOwner(), m_lGold, "EXCHANGE_GOLD_GIVE", exchange_buf);
		}
	}

	m_pGrid->Clear();
	return true;
}


bool CExchange::Accept(bool bAccept)
{
	if (m_bAccept == bAccept)
		return true;

	m_bAccept = bAccept;


	if (m_bAccept && GetCompany()->m_bAccept)
	{
		int	iItemCount;

		LPCHARACTER victim = GetCompany()->GetOwner();

		//PREVENT_PORTAL_AFTER_EXCHANGE
		GetOwner()->SetExchangeTime();
		victim->SetExchangeTime();
		//END_PREVENT_PORTAL_AFTER_EXCHANGE

		// @fixme150 BEGIN
		if (quest::CQuestManager::instance().GetPCForce(GetOwner()->GetPlayerID())->IsRunning() == true)
		{
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You cannot trade if you're using quests"));
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You cannot trade if the other part using quests"));
			goto EXCHANGE_END;
		}
		else if (quest::CQuestManager::instance().GetPCForce(victim->GetPlayerID())->IsRunning() == true)
		{
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You cannot trade if you're using quests"));
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You cannot trade if the other part using quests"));
			goto EXCHANGE_END;
		}
		// @fixme150 END




		if (!Check(&iItemCount))
		{
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("돈이 부족하거나 아이템이 제자리에 없습니다."));
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("상대방의 돈이 부족하거나 아이템이 제자리에 없습니다."));
			goto EXCHANGE_END;
		}


		if (!CheckSpace())
		{
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("상대방의 소지품에 빈 공간이 없습니다."));
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("소지품에 빈 공간이 없습니다."));
			goto EXCHANGE_END;
		}

		if (!CheckSpaceDragonSoulInventory())
		{
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("karsi_tarafin_dragonsoul_enventeri_dolu"));
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("simya_envanterinde_yer_yok"));
			goto EXCHANGE_END;
		}

#ifdef ENABLE_SPECIAL_STORAGE
		if (!CheckSpaceUpdateInventory())
		{
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("karsi_tarafin_yukseltme_enventeri_dolu"));
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("yukseltme_enventerinde_yer_yok"));
			goto EXCHANGE_END;
		}

		if (!CheckSpaceBookInventory())
		{
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("karsi_tarafin_bk_enventeri_dolu"));
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("bk_enventerinde_yer_yok"));
			goto EXCHANGE_END;
		}

		if (!CheckSpaceStoneInventory())
		{
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("karsi_tarafin_tas_enventeri_dolu"));
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("tas_enventerinde_yer_yok"));
			goto EXCHANGE_END;
		}

		if (!CheckSpaceChestInventory())
		{
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("karsi_tarafin_sandik_enventeri_dolu"));
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("sandik_enventerinde_yer_yok"));
			goto EXCHANGE_END;
		}
#endif

		if (!GetCompany()->Check(&iItemCount))
		{
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("돈이 부족하거나 아이템이 제자리에 없습니다."));
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("상대방의 돈이 부족하거나 아이템이 제자리에 없습니다."));
			goto EXCHANGE_END;
		}

		if (!GetCompany()->CheckSpace())
		{
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("상대방의 소지품에 빈 공간이 없습니다."));
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("소지품에 빈 공간이 없습니다."));
			goto EXCHANGE_END;
		}

		if (!GetCompany()->CheckSpaceDragonSoulInventory())
		{
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("karsi_tarafin_dragonsoul_enventeri_dolu"));
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("simya_envanterinde_yer_yok"));
			goto EXCHANGE_END;
		}

#ifdef ENABLE_SPECIAL_STORAGE
		if (!GetCompany()->CheckSpaceUpdateInventory())
		{
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("karsi_tarafin_yukseltme_enventeri_dolu"));
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("yukseltme_enventerinde_yer_yok"));
			goto EXCHANGE_END;
		}

		if (!GetCompany()->CheckSpaceBookInventory())
		{
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("karsi_tarafin_bk_enventeri_dolu"));
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("bk_enventerinde_yer_yok"));
			goto EXCHANGE_END;
		}

		if (!GetCompany()->CheckSpaceStoneInventory())
		{
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("karsi_tarafin_tas_enventeri_dolu"));
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("tas_enventerinde_yer_yok"));
			goto EXCHANGE_END;
		}

		if (!GetCompany()->CheckSpaceChestInventory())
		{
			victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("karsi_tarafin_sandik_enventeri_dolu"));
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("sandik_enventerinde_yer_yok"));
			goto EXCHANGE_END;
		}
#endif

		if (db_clientdesc->GetSocket() == INVALID_SOCKET)
		{
			sys_err("Cannot use exchange feature while DB cache connection is dead.");
			victim->ChatPacket(CHAT_TYPE_INFO, "Unknown error");
			GetOwner()->ChatPacket(CHAT_TYPE_INFO, "Unknown error");
			goto EXCHANGE_END;
		}

		if (Done())
		{
			if (m_lGold)
				GetOwner()->Save();

			if (GetCompany()->Done())
			{
				if (GetCompany()->m_lGold)
					victim->Save();

				// INTERNATIONAL_VERSION
				GetOwner()->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("%s 님과의 교환이 성사 되었습니다."), victim->GetName());
				victim->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("%s 님과의 교환이 성사 되었습니다."), GetOwner()->GetName());
				// END_OF_INTERNATIONAL_VERSION
			}
		}

EXCHANGE_END:
		Cancel();
		return false;
	}
	else
	{

		exchange_packet(GetOwner(), EXCHANGE_SUBHEADER_GC_ACCEPT, true, m_bAccept, NPOS, 0);
		exchange_packet(GetCompany()->GetOwner(), EXCHANGE_SUBHEADER_GC_ACCEPT, false, m_bAccept, NPOS, 0);
		return true;
	}
}


void CExchange::Cancel()
{
	exchange_packet(GetOwner(), EXCHANGE_SUBHEADER_GC_END, 0, 0, NPOS, 0);
	GetOwner()->SetExchange(NULL);

	for (int i = 0; i < EXCHANGE_ITEM_MAX_NUM; ++i)
	{
		if (m_apItems[i])
			m_apItems[i]->SetExchanging(false);
	}

	if (GetCompany())
	{
		GetCompany()->SetCompany(NULL);
		GetCompany()->Cancel();
	}

	M2_DELETE(this);
}

