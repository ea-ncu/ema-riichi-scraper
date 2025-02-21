with ranked_scores as (
    select
        tr.player_id,
        tr.score,
        rank() over (
            partition by tr.player_id
            order by tr.score desc
        ) as score_rank,
        t.id as tournament_id
    from tournament_results tr
    join tournaments t on t.id = tr.tournament_id
    where t.date > '2022-08-28'
)
select
    rank() over (order by sum(rs.score) desc) as rank,
    p.id as player_id,
    p.first_name,
    p.last_name,
    p.country,
    count(rs.tournament_id) as tournaments_played,
    sum(rs.score) as total_top_5_score
from ranked_scores rs
join players p on p.id = rs.player_id
join tournaments t on t.id = rs.tournament_id
where rs.score_rank <= 5  -- Select only the top 5 tournaments per player
and p.country = 'gb'  -- Filter by country
group by p.id, p.first_name, p.last_name, p.country
order by total_top_5_score desc;