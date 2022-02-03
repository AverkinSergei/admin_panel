CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id UUID PRIMARY KEY,
    full_name TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id UUID PRIMARY KEY,
    person_id UUID NOT NULL,
    film_work_id UUID NOT NULL,
    role TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id UUID PRIMARY KEY,
    genre_id UUID NOT NULL,
    film_work_id UUID NOT NULL,
    created TIMESTAMP WITH TIME ZONE
);

CREATE INDEX film_work_creation_date_idx ON content.film_work (creation_date, title);

CREATE INDEX person_full_name_idx ON content.person (full_name);

CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);

CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);
