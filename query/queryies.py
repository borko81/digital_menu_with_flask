queryies = {
        'RESTAURANT_NAME': '''SELECT obj.name_cyr from obj where obj.id = %d''',
        'SELECT': '''select KITS.NAME_CYR, KINDS.NAME, MENU.CENA, KITS.IMAGE, KITS.menu_text,
		(
		    select list(allergens.name_cyr)
		    from kits_allergens
		    inner join allergens on allergens.id = kits_allergens.allergens_id
		    where kits_allergens.kit_id = KITS.id
		    group by kits_allergens.kit_id
		)

		from KITS
		    inner join MENU
		    inner join KINDS on KINDS.ID = KITS.KIND_ID on MENU.KIT_ID = KITS.ID
		    where MENU.OBJ_ID in (select obj.id from obj where obj.kasa = %d)
		    order by 1
		''',
    'SELECT_FROM_KINDS_ID': '''
		select KITS.NAME_CYR, KINDS.NAME, MENU.CENA, KITS.IMAGE, KITS.menu_text,
		(
            select list(allergens.name_cyr)
            from kits_allergens
            inner join allergens on allergens.id = kits_allergens.allergens_id
            where kits_allergens.kit_id = KITS.id
            group by kits_allergens.kit_id
		)
		from KITS
		inner join MENU
		inner join KINDS on KINDS.ID = KITS.KIND_ID on MENU.KIT_ID = KITS.ID
		where MENU.OBJ_ID in (select obj.id from obj where obj.kasa = %d) and kinds.id = %d
		order by 1
		''',
    'TAKE_KINDS': '''
		select
		distinct(kinds.id), kinds.name, kind_icons.icon, count(*)
		from kits
		inner join kinds on kinds.id = kits.kind_id
		inner join menu
		on menu.kit_id = kits.id
		left join kind_icons on kind_icons.id = kinds.icon_id
		where MENU.OBJ_ID in (select obj.id from obj where obj.kasa = %d) and kits.kind_id is not null
		group by 1, 2, 3
		order by 2
		'''
}
