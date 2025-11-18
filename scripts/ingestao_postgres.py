#!/usr/bin/env python3
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://localhost/airbnb_rio')

print("Apagando tabelas antigas...")
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS listings CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS neighbourhoods CASCADE;"))
    conn.commit()
print("Tabelas apagadas! ✅")

print("Carregando bairros...")
df_bairros = pd.read_csv('dados/neighbourhoods.csv')
df_bairros.to_sql('neighbourhoods', engine, if_exists='append', index=False)
print("Bairros carregados! ✅")

print("Carregando anúncios (3-6 minutos)...")

# Colunas que REALMENTE existem no seu arquivo de outubro 2024
colunas = ['id', 'name', 'host_id', 'host_name', 'neighbourhood', 'latitude', 'longitude', 
           'room_type', 'price', 'minimum_nights', 'number_of_reviews', 'last_review', 
           'reviews_per_month', 'calculated_host_listings_count', 'availability_365', 
           'number_of_reviews_ltm', 'license']

df = pd.read_csv('dados/listings.csv.gz', compression='gzip', low_memory=False, usecols=colunas)

df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)

df.to_sql('listings', engine, if_exists='append', index=False, chunksize=5000)

print("TUDO CARREGADO COM SUCESSO!!! 🎉🎉🎉")
print(f"Total de anúncios no Rio: {len(df):,}")
