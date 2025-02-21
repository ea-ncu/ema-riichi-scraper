select
    rank() over (order by sum(tr.score) desc) as rank,
    p.first_name,
    p.last_name,
    p.country,
    count(t.id) as tournaments_played,
    sum(tr.score) as total_score
from tournament_results tr
join players p on p.id = tr.player_id
join tournaments t on t.id = tr.tournament_id
where p.country = 'gb'
and t.date > '2022-08-28'
group by p.id, p.first_name, p.last_name, p.country
order by total_score desc;