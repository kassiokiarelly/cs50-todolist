SELECT title FROM "movies"
INNER JOIN "ratings" on ratings.movie_id = movies.id
INNER JOIN "stars" on stars.movie_id = movies.id
INNER JOIN "people" on people.id = person_id
WHERE name = 'Chadwick Boseman'
order by rating desc
limit 5