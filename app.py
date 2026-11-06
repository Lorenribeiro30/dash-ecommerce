from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
from dash import Dash, dcc, html, Input, Output

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / 'ecommerce_estatistica.csv')
for col in ['Nota', 'Preço', 'N_Avaliações']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
for col in ['Marca', 'Temporada']:
    df[col] = df[col].fillna('Não informado').astype(str)

app = Dash(__name__, title='Análise de E-commerce')
server = app.server
app.layout = html.Div([
    html.H1('Análise de produtos de e-commerce'),
    html.P('Explore os gráficos da análise estatística e filtre os produtos por temporada.'),
    html.Label('Temporada'),
    dcc.Dropdown(id='filtro', options=[{'label': s, 'value': s} for s in sorted(df['Temporada'].unique())], multi=True, placeholder='Todas as temporadas'),
    html.Div(id='resumo', style={'margin': '20px 0', 'fontWeight': 'bold'}),
    html.Div([dcc.Graph(id=f'g{i}') for i in range(1, 8)], style={'display':'grid','gridTemplateColumns':'repeat(auto-fit, minmax(min(100%, 490px), 1fr))','gap':'18px'}),
    html.P('Fonte: ecommerce_estatistica.csv. A análise de associação não demonstra causalidade.', style={'color':'#526176'})
], style={'maxWidth':'1450px','margin':'auto','padding':'28px','fontFamily':'Arial, sans-serif','backgroundColor':'#f4f7fb','color':'#162c44'})

def vazio(titulo):
    f = go.Figure(); f.add_annotation(text='Sem dados suficientes para esta seleção',showarrow=False); f.update_layout(title=titulo); return f

@app.callback([Output('resumo','children')] + [Output(f'g{i}','figure') for i in range(1,8)], Input('filtro','value'))
def atualizar(temporadas):
    d = df[df['Temporada'].isin(temporadas)] if temporadas else df
    h = px.histogram(d.dropna(subset=['Nota']),x='Nota', nbins=20,title='Distribuição das notas',labels={'Nota':'Nota'})
    sc = px.scatter(d.dropna(subset=['Nota','N_Avaliações']), x='Nota', y='N_Avaliações', title='Nota × número de avaliações', labels={'N_Avaliações':'Número de avaliações'})
    num = d.select_dtypes(include='number').drop(columns=['Unnamed: 0'],errors='ignore'); corr = num.corr().dropna(how='all',axis=0).dropna(how='all',axis=1)
    heat = px.imshow(corr, color_continuous_scale='RdBu_r',zmin=-1,zmax=1,title='Correlação entre variáveis numéricas',aspect='auto') if not corr.empty else vazio('Correlação entre variáveis numéricas')
    marcas=d['Marca'].value_counts().head(10).rename_axis('Marca').reset_index(name='Produtos')
    bar=px.bar(marcas,x='Produtos',y='Marca',orientation='h',title='Marcas com mais produtos (10 maiores)');bar.update_layout(yaxis={'categoryorder':'total ascending'})
    temp=d['Temporada'].value_counts().rename_axis('Temporada').reset_index(name='Produtos')
    pizza=px.pie(temp,names='Temporada',values='Produtos',title='Participação por temporada') if not temp.empty else vazio('Participação por temporada')
    precos=d['Preço'].dropna(); dens=vazio('Densidade da distribuição dos preços')
    if len(precos)>1 and precos.nunique()>1:
        x=np.linspace(precos.min(),precos.max(),200); dens=go.Figure(go.Scatter(x=x,y=gaussian_kde(precos)(x),fill='tozeroy'));dens.update_layout(title='Densidade da distribuição dos preços',xaxis_title='Preço (R$)',yaxis_title='Densidade')
    pares=d.dropna(subset=['Preço','Nota']);reg=px.scatter(pares,x='Preço',y='Nota',title='Relação entre preço e nota')
    if len(pares)>1 and pares['Preço'].nunique()>1:
        coef=np.polyfit(pares['Preço'],pares['Nota'],1);x=np.linspace(pares['Preço'].min(),pares['Preço'].max(),100);reg.add_scatter(x=x,y=np.polyval(coef,x),mode='lines',name='Tendência linear')
    figs=[h,sc,heat,bar,pizza,dens,reg]
    for f in figs: f.update_layout(template='plotly_white',margin=dict(l=45,r=30,t=65,b=55))
    return [f'{len(d)} produtos na seleção', *figs]

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
