QUERY_MOVIE = """WITH modified_films AS (
    SELECT
        content.film_work.id,
        content.film_work.modified
    FROM
        content.film_work
    WHERE
        content.film_work.modified > %(last_modified)s
    UNION ALL
    SELECT
        content.person_film_work.film_work_id,
        max(content.person.modified)
    FROM
        content.person
        LEFT JOIN content.person_film_work ON (content.person.id = content.person_film_work.person_id)
    WHERE
        content.person.modified >= %(last_modified)s
    GROUP BY
        1
    UNION ALL
    SELECT
        content.person_film_work.film_work_id,
        max(content.person_film_work.created)
    FROM
        content.person_film_work
    WHERE
        content.person_film_work.created > %(last_modified)s
    GROUP BY
        1
    UNION ALL
    SELECT
        content.genre_film_work.film_work_id,
        max(content.genre.modified)
    FROM
        content.genre
        LEFT OUTER JOIN content.genre_film_work ON (content.genre.id = content.genre_film_work.genre_id)
    WHERE
        content.genre.modified > %(last_modified)s
    GROUP BY
        1
    UNION ALL
    SELECT
        content.genre_film_work.film_work_id,
        max(content.genre_film_work.created)
    FROM
        content.genre_film_work
    WHERE
        content.genre_film_work.created > %(last_modified)s
    GROUP BY
        1
),
film_dates AS (
    SELECT
        id,
        max(modified) AS last_modified
FROM
    modified_films
GROUP BY
    1
)
SELECT
    content.film_work.id,
    content.film_work.title,
    content.film_work.description,
    content.film_work.creation_date,
    content.film_work.rating,
    content.film_work.type,
    film_dates.last_modified
FROM
    content.film_work
    JOIN film_dates ON (content.film_work.id = film_dates.id)
GROUP BY
    content.film_work.id,
    film_dates.last_modified
ORDER BY
    film_dates.last_modified;
"""

QUERY_PERSON = """SELECT
    content.person_film_work.film_work_id,
    content.person_film_work.person_id,
    content.person_film_work.role,
    content.person.full_name
FROM
    content.person_film_work
JOIN content.person ON (content.person.id = content.person_film_work.person_id)
WHERE content.person_film_work.film_work_id = ANY(%s)
"""

QUERY_GENRE = """SELECT
    content.genre_film_work.film_work_id,
    content.genre_film_work.genre_id,
    content.genre.name,
    content.genre.description
FROM
    content.genre_film_work
JOIN content.genre ON (content.genre.id = content.genre_film_work.genre_id)
WHERE content.genre_film_work.film_work_id = ANY(%s)
"""
