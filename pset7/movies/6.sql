SELECT avg(rating) as avg FROM "movies"
inner join "ratings" on movie_id = id
WHERE year = 2012