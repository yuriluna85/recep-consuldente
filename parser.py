import json
from datetime import datetime

def fetch_odontology_news():
    # Esta lista vai armazenar as 15 notícias
    news_list = []

    # Aqui simulamos a estrutura das fontes que você quer
    # No futuro, você pode usar 'requests' para pegar dados reais desses sites
    sources = [
        {"nome": "Portal CFO (Brasil)", "url": "https://website.cfo.org.br/"},
        {"nome": "Dental Tribune (Global)", "url": "https://www.dental-tribune.com/"},
        {"nome": "Nature Dentistry (EUA)", "url": "https://www.nature.com/bdj"},
        {"nome": "ScienceDaily (EUA)", "url": "https://www.sciencedaily.com/news/health_medicine/dentistry/"}
    ]

    # Categorias que o seu index.html reconhece
    categories = ["pesquisa", "eventos", "novidades"]

    # Loop para gerar 15 notícias (5 de cada categoria para teste)
    for i in range(1, 16):
        source = sources[i % len(sources)]
        category = categories[i % len(categories)]
        
        item = {
            "titulo": f"Notícia {i}: Avanço em {category.capitalize()} na Odontologia",
            "resumo": f"Traduzido de {source['nome']}: Pesquisa recente demonstra novas técnicas de atendimento clínico e biotecnologia aplicada.",
            "cat": category,
            "fonte": source['nome'],
            "data": datetime.now().strftime("%d/%m %H:%M"),
            "url": source['url']
        }
        news_list.append(item)

    # O segredo está aqui: salvamos a LISTA completa (news_list) e não apenas um item
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
    
    print(f"Sucesso! {len(news_list)} notícias foram salvas no data.json.")

if __name__ == "__main__":
    fetch_odontology_news()
