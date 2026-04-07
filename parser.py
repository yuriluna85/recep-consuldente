import json
import requests
from datetime import datetime

# Exemplo simplificado de busca e tradução
def fetch_news():
    # Aqui você conectaria com as APIs ou faria o Web Scraping
    # Para o tutorial, vamos gerar a estrutura que o seu JS espera
    news_data = [
        {
            "titulo": "Nova Descoberta na Nature Dentistry",
            "resumo": "Traduzido: Pesquisadores descobrem nova forma de regeneração dentária...",
            "cat": "pesquisa",
            "fonte": "Nature Dentistry",
            "data": datetime.now().strftime("%d/%m %H:%M"),
            "url": "https://www.nature.com/bdj"
        },
        # ... adicione a lógica para buscar os outros 14 itens aqui
    ]
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fetch_news()
