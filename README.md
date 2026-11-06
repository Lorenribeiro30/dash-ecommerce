# Análise de e-commerce com Dash

[Acessar a aplicação Dash](https://dash-ecommerce.onrender.com/)

Aplicação interativa em Python que lê `ecommerce_estatistica.csv` em um DataFrame pandas e apresenta os gráficos da atividade anterior: histograma de notas, dispersão de notas e avaliações, correlações, marcas, temporadas, densidade de preços e regressão linear entre preço e nota. O filtro de temporada atualiza as visualizações.

## Executar no computador

Na pasta do projeto, instale as dependências com `pip install -r requirements.txt`, execute `python app.py` e abra `http://127.0.0.1:8050` no navegador.

## Hospedagem

O GitHub armazena os arquivos, mas não executa a aplicação Dash. Para disponibilizar uma URL pública, publique o repositório em um serviço compatível com Python, utilizando `pip install -r requirements.txt` para a instalação e `gunicorn app:server` para iniciar o servidor.

A linha de tendência descreve uma relação observada e não prova causalidade.
