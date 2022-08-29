query_get_all = """
select
kits.id,
kits.name_cyr,
kinds.name,
case
    when kits.image is not null then '+'
    else '-'
end
from kits
inner join kinds on kinds.id = kits.kind_id
where kits.menu_text is not null
order by 3, 2
"""

query = """
update kits
set kits.image = ?, kits.tag = ?
where kits.id = ?
"""

query_for_tumbnail = """
update or insert into images values(?, ?, ?, ?)
"""

querys = {'query_get_all': query_get_all, 'query': query, 'query_for_tumb': query_for_tumbnail}