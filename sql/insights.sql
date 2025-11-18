-- 1. Top 10 bairros mais caros (preço mediano)
SELECT neighbourhood, 
       ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price), 0) AS preco_mediano
FROM listings 
WHERE price > 0 AND price < 10000
GROUP BY neighbourhood
ORDER BY preco_mediano DESC
LIMIT 10;

-- 2. Quantidade de anúncios por bairro (top 15)
SELECT neighbourhood, COUNT(*) AS total_anuncios
FROM listings
GROUP BY neighbourhood
ORDER BY total_anuncios DESC
LIMIT 15;

-- 3. Receita anual estimada média por tipo de imóvel
SELECT room_type,
       ROUND(AVG(price) * (365 - AVG(availability_365)), 0) AS receita_anual_estimada_media
FROM listings
GROUP BY room_type
ORDER BY receita_anual_estimada_media DESC;

-- 4. Hosts com mais imóveis
SELECT host_name, COUNT(*) AS total_anuncios
FROM listings
GROUP BY host_name
HAVING COUNT(*) > 30
ORDER BY total_anuncios DESC
LIMIT 10;

-- 5. Ocupação média estimada da cidade
SELECT ROUND(100 - AVG(availability_365) / 365.0 * 100, 1) || '%' AS ocupacao_media_geral
FROM listings;

-- 6. Preço médio por bairro (só bairros com +100 anúncios)
SELECT neighbourhood, 
       ROUND(AVG(price), 0) AS preco_medio,
       COUNT(*) AS total_anuncios
FROM listings
GROUP BY neighbourhood
HAVING COUNT(*) > 100
ORDER BY preco_medio DESC
LIMIT 15;
