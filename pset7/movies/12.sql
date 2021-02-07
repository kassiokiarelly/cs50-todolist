SELECT title FROM "movies"
INNER JOIN "stars" on stars.movie_id = movies.id
INNER JOIN "people" on people.id = person_id
WHERE name = 'Johnny Depp' or name = 'Helena Bonham Carter'
group by title
having count(person_id) = 2