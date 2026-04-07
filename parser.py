import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Simulação de tradução simples para manter o código leve e funcional no GitHub
def traduzir_titulo(texto):
    # Dicionário de termos comuns para uma tradução "nerd" rápida
    termos = {
        "Research": "Pesquisa", "Study": "Estudo", "New": "Novo", 
        "Health": "Saúde", "Dentistry": "Odontologia", "Digital": "Digital",
        "Market": "Mercado", "Congress": "Congresso", "Surgery": "Cirurgia"
    }
    for eng, pt in termos.items():
        texto = texto.replace(eng, pt)
    return texto

def capturar_noticias(url, seletor, fonte, categoria):
    noticias_locais = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Seleciona os links/manchetes (limitando a 5 por fonte para não sobrecarregar)
        artigos = soup.select(seletor)[:5]
        
        for art in artigos:
            titulo_original = art.get_text().strip()
            link = art.find('a')['href'] if art.find('a') else url
            
            # Ajuste de links relativos
            if not link.startswith('http'):
                link = url.rstrip('/') + '/' + link.lstrip('/')

            titulo_pt = traduzir_titulo(titulo_original)
            
            noticias_locais.append({
                "titulo": titulo_pt[:95],
                "resumo": f"Radar Consuldente: Nova atualização capturada em {fonte}. Clique para ler o artigo completo na fonte original.",
                "cat": categoria,
                "fonte": fonte,
                "data": datetime.now().strftime("%d/%m %H:%M"),
                "url": link,
                "img": f"https://picsum.photos/seed/{titulo_original[:5]}/400/250" # Imagem única por título
            })
    except Exception as e:
        print(f"Erro ao rastrear {fonte}: {e}")
    return noticias_locais

def rodar_radar():
    print(f"📡 Iniciando Radar às {datetime.now()}...")
    radar_data = []
    
    # Configuração dos alvos (Site, Seletor CSS, Nome, Categoria)
    alvos = [
        {"url": "https://website.cfo.org.br/noticias/", "sel": ".post-title", "name": "CFO Brasil", "cat": "novidades"},
        {"url": "https://www.dental-tribune.com/news/", "sel": ".article-title", "name": "Dental Tribune", "cat": "novidades"},
        {"url": "https://www.nature.com/bdj/research-articles", "sel": "article h3", "name": "Nature Dentistry", "cat": "pesquisa"}
    ]

    for alvo in alvos:
        print(f"Buscando em {alvo['name']}...")
        radar_data.extend(capturar_noticias(alvo['url'], alvo['sel'], alvo['name'], alvo['cat']))

    # Salva o arquivo que o index.html vai ler
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(radar_data, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Radar finalizado! {len(radar_data)} notícias indexadas.")

if __name__ == "__main__":
    rodar_radar()
