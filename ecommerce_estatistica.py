import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc  # Importação correta e única

# Carregar o dataset
df = pd.read_csv('ecommerce_estatistica.csv')

# 1-Histograma
fig1 = px.histogram(
    df,
    x='Nota',          # Eixo X: Valores das notas
    color='Gênero',    # Cores separadas por gênero
    nbins=30,          # Número de barras
    title='Distribuição de Notas por Gênero',
    barmode='overlay'  # Sobrepor as barras para comparação
)

# 2-Gráfico de pizza
#1. Pré-processamento (agrupar pequenas categorias)
top_marcas = df['Marca'].value_counts().nlargest(8).index
df['Marca'] = df['Marca'].where(df['Marca'].isin(top_marcas), 'Outros')

# 2. Criar o gráfico
fig2 = px.pie(df,
             names='Marca',
             values='N_Avaliações',
             hole=0.3,
             title='Distribuição de Avaliações por Marca (Top 5 + Outros)')

# 3. Formatar os textos
fig2.update_traces(
    textposition='inside',
    textinfo='percent+label',
    texttemplate='%{label}<br>%{percent:.1%}',  # Formato: 0.5% em vez de 0.00500%
    insidetextfont=dict(size=10),
    marker=dict(line=dict(color='white', width=1))
)

fig2.update_layout(
    legend=dict(orientation='h', yanchor='bottom', y=-0.2),
    margin=dict(t=50, b=50)
)


#3-Gráfico de bolha


# Converter 'Qtd_Vendidos' para numérico, tratando erros
df['Qtd_Vendidos'] = pd.to_numeric(df['Qtd_Vendidos'], errors='coerce')

# (Opcional) Verificar valores problemáticos
if df['Qtd_Vendidos'].isna().any():
    print("Valores inválidos encontrados em 'Qtd_Vendidos' e serão removidos.")
    df = df.dropna(subset=['Qtd_Vendidos'])

# Criar o gráfico de bolhas
fig3 = px.scatter(
    df,
    x='Material',
    y='Qtd_Vendidos',
    size='Qtd_Vendidos',
    color='Material',
    hover_name='Material',
    title='Vendas por Material',
    size_max=50,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Personalização
fig3.update_layout(
    xaxis_title='Material',
    yaxis_title='Quantidade Vendida (unidades)',
    plot_bgcolor='rgba(240,240,240,0.9)',
    paper_bgcolor='rgba(230,245,255,0.8)',
    title_font_size=22,
    font=dict(family="Arial", size=14)
)


# 4-Grafico Linha
# filtrando apenas as 10 principais marcas
top_marcas = df['Marca'].value_counts().nlargest(10).index  # Pegar as top 10
df_filtrado = df[df['Marca'].isin(top_marcas)]

# gráfico apenas com as marcas selecionadas
fig4 = px.line(
    df_filtrado,
    x='Temporada',  # Sugiro usar uma variável temporal se tiver
    y='Nota',
    color='Marca',
    title='Evolução das Notas das Top 10 Marcas por Temporada',
    markers=True  # Adiciona marcadores aos pontos
)

# Melhora do layout
fig4.update_layout(
    xaxis_title='Temporada',
    yaxis_title='Nota Média',
    legend_title='Marca',
    hovermode='x unified'
)




# 5-Gráfico 3D

# Leitura e conversão
df['Qtd_Vendidos'] = pd.to_numeric(df['Qtd_Vendidos'], errors='coerce')

# Remover linhas com Qtd_Vendidos ou outras colunas críticas faltando
df = df.dropna(subset=['Qtd_Vendidos', 'N_Avaliações', 'Material'])

# (Opcional) limitar número de marcas para focar em dados mais relevantes
top_marcas = df['Marca'].value_counts().nlargest(10).index
df = df[df['Marca'].isin(top_marcas)]

# Criar gráfico 3D
fig5 = px.scatter_3d(
    df,
    x='N_Avaliações',
    y='Qtd_Vendidos',
    z='Material',
    color='Material',
    size='Qtd_Vendidos',
    hover_name='Material',
    hover_data=['Marca', 'Nota'],
    title='Relação 3D: Avaliações, Vendas e Material',
    height=800,
    opacity=0.8,
    color_discrete_sequence=px.colors.qualitative.Vivid
)

fig5.update_layout(
    scene=dict(
        xaxis_title='Número de Avaliações',
        yaxis_title='Quantidade Vendida',
        zaxis_title='Material',
        xaxis=dict(backgroundcolor="rgb(240, 240, 240)"),
        yaxis=dict(backgroundcolor="rgb(240, 240, 240)"),
        zaxis=dict(backgroundcolor="rgb(240, 240, 240)"),
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    )
)

fig5.update_scenes(
    camera=dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=1.5, y=1.5, z=0.5)
    )
)




# 6-Gráfico de barra

fig6 = px.bar(
    df,
    x='Temporada',
    y='Qtd_Vendidos',
    color='Gênero',
    barmode='group',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    opacity=0.85,
    title='Quantidade Vendida por Temporada e Gênero'
)

fig6.update_layout(
    title=dict(
        text='Quantidade Vendida por Temporada e Gênero',
        font=dict(size=22, family='Arial', color='black'),
        x=0.5
    ),
    xaxis_title='Temporada',
    yaxis_title='Quantidade Vendida',
    legend_title='Gênero',
    plot_bgcolor='rgba(245, 250, 255, 1)',
    paper_bgcolor='rgba(230, 245, 250, 1)',
    font=dict(size=14, family='Arial', color='black'),
    xaxis=dict(tickangle=-45),
    bargap=0.2
)




# Cria o app
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6)
])

# Executa o app
if __name__ == '__main__':
    app.run(debug=True, port=8050)
