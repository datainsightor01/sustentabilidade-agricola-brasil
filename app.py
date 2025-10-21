import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

st.set_page_config(
    page_title="Índice de Sustentabilidade Agrícola - Brasil 2023",
    layout="wide",
    page_icon="🌱"
)

st.title("Índice de Sustentabilidade Agrícola - Brasil 2023")

st.markdown("""
Este projeto apresenta o Índice de Sustentabilidade Agrícola (ISA) para cada estado brasileiro em 2023.  
O índice combina dados de vegetação nativa, uso de agrotóxicos, produtividade agrícola e eficiência de irrigação  
para avaliar o equilíbrio entre produção e preservação ambiental.

Quanto mais próximo de 1, mais sustentável é o estado.
""")

@st.cache_data
def carregar_dados():
    return pd.read_csv("sustentabilidade_agricola_brasil_ISA_2023.csv")

df = carregar_dados()

st.subheader("Dados Gerais por Estado")
st.dataframe(
    df.sort_values(by="ISA", ascending=False),
    use_container_width=True
)

st.subheader("Ranking de Sustentabilidade (ISA por Estado)")
ranking = df.sort_values(by='ISA', ascending=False)

fig_rank, ax = plt.subplots(figsize=(10, 8))
sns.barplot(
    data=ranking,
    y='Estado',
    x='ISA',
    hue='Regiao' if 'Regiao' in df.columns else None,
    dodge=False,
    palette='YlGn'
)
ax.set_title('Ranking de Sustentabilidade Agrícola - 2023')
ax.set_xlabel('Índice de Sustentabilidade Agrícola (ISA)')
ax.set_ylabel('Estado')
if 'Regiao' in df.columns:
    ax.legend(title='Região')
plt.tight_layout()
st.pyplot(fig_rank)

st.subheader("Estatísticas Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("ISA Médio", f"{df['ISA'].mean():.2f}")
col2.metric("ISA Máximo", f"{df['ISA'].max():.2f}")
col3.metric("ISA Mínimo", f"{df['ISA'].min():.2f}")

st.subheader("Mapa de Calor da Sustentabilidade Agrícola")

st.markdown("""
O mapa abaixo mostra o nível de sustentabilidade agrícola por estado.  
Quanto mais escuro o tom de verde, maior o valor do ISA.
""")

try:
    # Configurar fonte para compatibilidade
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    # Carregar dados
    df = pd.read_csv('sustentabilidade_agricola_brasil_ISA_2023.csv', encoding='utf-8')
    estados = gpd.read_file('brasil_estados.geojson')
    
    # Preparar dados para merge
    estados['name_upper'] = estados['name'].str.upper().str.strip()
    df['Estado_upper'] = df['Estado'].str.upper().str.strip()
    estados_merged = estados.merge(df, left_on='name_upper', right_on='Estado_upper', how='left')
    
    # Criar o mapa
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    
    estados_merged.plot(column='ISA', 
                       cmap='RdYlGn',
                       linewidth=1.0, 
                       edgecolor='black', 
                       legend=True, 
                       ax=ax,
                       legend_kwds={
                           'label': 'Índice de Sustentabilidade Agropecuária (ISA)',
                           'shrink': 0.8,
                           'orientation': 'horizontal',
                           'pad': 0.05
                       })
    
    # Adicionar labels nos estados
    for idx, row in estados_merged.iterrows():
        ax.annotate(text=f"{row['sigla']}\n{row['ISA']:.2f}", 
                   xy=(row['geometry'].centroid.x, row['geometry'].centroid.y),
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontsize=8,
                   color='black',
                   weight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7))
    
    plt.title('Mapa de Calor - Índice de Sustentabilidade Agropecuária (ISA) - Brasil 2023', 
             fontsize=12, pad=20, weight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    # Exibir no Streamlit
    st.pyplot(fig)
    
except Exception as e:
    st.error(f"Erro ao carregar o mapa: {e}")
    st.info("""
    **Para visualizar o mapa, certifique-se de que:**
    1. O arquivo 'brasil_estados.geojson' está na pasta do projeto
    2. O arquivo CSV está com a coluna 'Estado' correta
    3. Os nomes dos estados no CSV correspondem aos do GeoJSON
    """)

st.subheader("Conclusões")

st.markdown("""
- Estados com maior vegetação nativa e melhor eficiência na irrigação tendem a alcançar melhores índices.  
- O uso elevado de agrotóxicos ainda é o principal fator que reduz a sustentabilidade.  
- A Região Sul geralmente apresenta alta produtividade com práticas relativamente sustentáveis.  
- Já a Região Norte mantém altos níveis de vegetação, mas produtividade mais baixa.  
- Incentivos a tecnologias agrícolas limpas e otimização de irrigação são caminhos promissores para elevar o ISA nacional.
""")

st.markdown("---")
st.caption("Desenvolvido por Victor Henrique © 2025 | Projeto de Análise de Sustentabilidade Agrícola")