SELECT rating, title FROM "movies"
INNER JOIN "ratings" on movie_id = id
WHERE year = 2010
ORDER BY rating desc, title