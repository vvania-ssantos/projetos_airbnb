#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

os.makedirs('imagens', exist_ok=True)
engine = create_engine('postgresql://localhost/airbnb_rio')
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# 1. Top 10 bairros mais caros (corrigido o ROUND)
query1 = """
SELECT neighbourhood, 
       ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price)::numeric, 0) AS preco_mediano
FROM listings 
WHERE price > 0 AND price < 10000
GROUP BY neighbourhood
ORDER BY preco_mediano DESC
LIMIT 10
"""
df1 = pd.read_sql(query1, engine)
plt.figure()
sns.barplot(data=df1, y='neighbourhood', x='preco_mediano', palette='mako')
plt.title('Top 10 Bairros Mais Caros do Airbnb Rio - Preço Mediano por Noite (R$)')
plt.xlabel('Preço Mediano (R$)')
plt.ylabel('')
plt.tight_layout()
plt.savefig('imagens/top_10_bairros_caros.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Distribuição por tipo de imóvel
query2 = "SELECT room_type, COUNT(*) AS total FROM listings GROUP BY room_type ORDER BY total DESC"
df2 = pd.read_sql(query2, engine)
plt.figure()
colors = sns.color_palette('pastel')[0:len(df2)]
plt.pie(df2['total'], labels=df2['room_type'], colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('Distribuição dos Tipos de Imóvel (43.068 anúncios)')
plt.savefig('imagens/distribuicao_tipos_imovel.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Top 10 hosts com mais imóveis (gráfico extra pra ficar lindo)
query3 = """
SELECT host_name, COUNT(*) AS total_anuncios
FROM listings 
GROUP BY host_name 
HAVING COUNT(*) > 30
ORDER BY total_anuncios DESC
LIMIT 10
"""
df3 = pd.read_sql(query3, engine)
plt.figure()
sns.barplot(data=df3, y='host_name', x='total_anuncios', palette='rocket')
plt.title('Top 10 Hosts com Mais Imóveis no Rio')
plt.xlabel('Número de anúncios')
plt.ylabel('')
plt.tight_layout()
plt.savefig('imagens/top_10_hosts.png', dpi=300, bbox_inches='tight')
plt.close()

print("🎉 3 gráficos profissionais gerados na pasta imagens/ !!")
print("   → top_10_bairros_caros.png")
print("   → distribuicao_tipos_imovel.png")
print("   → top_10_hosts.png")
