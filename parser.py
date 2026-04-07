import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

def capturar_noticias(url, seletor, fonte, categoria):
    noticias_locais = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=25) # Aumentei o timeout
        soup = BeautifulSoup(response.text, 'html.parser')
        
        artigos = soup.select(seletor)[:6] 
        
        for art in artigos:
            titulo = art.get_text().strip()
            link_tag = art.find('a') if art.name != 'a' else art
            link = link_tag['href'] if link_tag and link_tag.has_attr('href') else url
            if not link.startswith('http'):
                link = url.rstrip('/') + '/' + link.lstrip('/')

            # Busca de imagem mais agressiva
            img_url = ""
            # Procura imagem dentro do bloco do artigo
            img_tag = art.select_one('img') or art.find_previous('img') or art.find_next('img')
            
            if img_tag and img_tag.has_attr('src'):
                img_url = img_tag['src']
            elif img_tag and img_tag.has_attr('data-src'):
                img_url = img_tag['data-src']

            # Se não achou imagem real, gera uma elegante baseada na categoria
            if not img_url or "base64" in img_url:
                img_url = f"https://picsum.photos/seed/{random.randint(1,1000)}/1200/600"

            if len(titulo) > 20:
                noticias_locais.append({
                    "titulo": titulo[:100],
                    "resumo": f"Radar Consuldente: Informação em tempo real via {fonte}.",
                    "cat": categoria,
                    "fonte": fonte,
                    "data": datetime.now().strftime("%H:%M"),
                    "url": link,
                    "img": img_url
                })
    except Exception as e:
        print(f"Erro em {fonte}: {e}")
    return noticias_locais

def rodar_radar():
    radar_data = []
    alvos = [
        {"url": "https://website.cfo.org.br/noticias/", "sel": "h2.entry-title", "name": "CFO", "cat": "odontologia"},
        {"url": "https://croba.org.br/noticias/", "sel": "h2.entry-title", "name": "CRO-BA", "cat": "odontologia"},
        {"url": "https://abo-ba.org.br/noticias/", "sel": ".post-title", "name": "ABO-BA", "cat": "odontologia"},
        {"url": "https://www.acordacidade.com.br/", "sel": ".entry-title", "name": "Acorda Cidade", "cat": "feira"},
        {"url": "https://g1.globo.com/ba/feira-de-santana-regiao/", "sel": ".feed-post-link", "name": "G1 Feira", "cat": "feira"},
        {"url": "https://noticias.r7.com/bahia/", "sel": ".r7-flex-listing-title", "name": "R7 Bahia", "cat": "feira"},
        {"url": "https://portaldafeira.com.br/", "sel": "h3.entry-title", "name": "Portal da Feira", "cat": "feira"},
        {"url": "https://www.jornalfolhadoestado.com/?s=Feira+de+Santana", "sel": ".entry-title", "name": "Folha Estado", "cat": "feira"}
    ]

    for alvo in alvos:
        print(f"Rastreando: {alvo['name']}")
        radar_data.extend(capturar_noticias(alvo['url'], alvo['sel'], alvo['name'], alvo['cat']))

    # Embaralha para não vir só G1 no início
    random.shuffle(radar_data)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(radar_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    rodar_radar()
