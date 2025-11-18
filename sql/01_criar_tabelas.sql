-- Apaga se já existir
DROP TABLE IF EXISTS listings CASCADE;
DROP TABLE IF EXISTS neighbourhoods CASCADE;

-- Tabela de bairros
CREATE TABLE neighbourhoods (
    neighbourhood_group VARCHAR,
    neighbourhood VARCHAR PRIMARY KEY
);

-- Tabela principal de anúncios
CREATE TABLE listings (
    id BIGINT PRIMARY KEY,
    name TEXT,
    host_id BIGINT,
    host_name TEXT,
    neighbourhood VARCHAR REFERENCES neighbourhoods(neighbourhood),
    latitude FLOAT,
    longitude FLOAT,
    room_type VARCHAR,
    price NUMERIC,
    minimum_nights INT,
    number_of_reviews INT,
    last_review DATE,
    reviews_per_month FLOAT,
    calculated_host_listings_count INT,
    availability_365 INT,
    number_of_reviews_ltm INT,
    license VARCHAR,
    host_is_superhost CHAR(1)
);
