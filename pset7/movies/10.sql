SELECT name FROM "movies"
INNER JOIN "ratings" on ratings.movie_id = movies.id
INNER JOIN "directors" on directors.movie_id = movies.id
INNER JOIN "people" on people.id = person_id
WHERE rating >= 9