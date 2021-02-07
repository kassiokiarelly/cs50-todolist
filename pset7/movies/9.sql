SELECT name FROM "movies"
INNER JOIN "stars" on movie_id = movies.id
INNER JOIN "people" on people.id = person_id
WHERE year = 2004
group by name
order by birth