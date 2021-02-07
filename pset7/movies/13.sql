select op.name from stars o
inner join people op on op.id = o.person_id
inner join (
SELECT s.movie_id FROM stars s
inner join "people" p on s.person_id = p.id
WHERE p.name = 'Kevin Bacon' and p.birth = 1958
) as k on k.movie_id = o.movie_id
where
op.name <> 'Kevin Bacon'