import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def capturar_noticias(url, seletor, fonte, categoria):
    noticias_locais = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        artigos = soup.select(seletor)[:8] 
        
        for art in artigos:
            titulo = art.get_text().strip()
            link_tag = art.find('a') if art.name != 'a' else art
            link = link_tag['href'] if link_tag and link_tag.has_attr('href') else url
            if not link.startswith('http'):
                link = url.rstrip('/') + '/' + link.lstrip('/')

            # Lógica para Imagem Destacada (Wordpress e outros)
            img_url = "https://picsum.photos/seed/odonto/800/400" # Fallback
            
            # Tenta achar uma imagem próxima ao título ou dentro do artigo
            img_tag = art.find_previous('img') or art.find_next('img') or art.select_one('img')
            if img_tag and img_tag.has_attr('src'):
                img_url = img_tag['src']
                if not img_url.startswith('http'):
                    img_url = url.rstrip('/') + '/' + img_url.lstrip('/')

            if len(titulo) > 15:
                noticias_locais.append({
                    "titulo": titulo[:95],
                    "resumo": f"Radar Consuldente: Informação atualizada via {fonte}.",
                    "cat": categoria,
                    "fonte": fonte,
                    "data": datetime.now().strftime("%H:%M"),
                    "url": link,
                    "img": img_url
                })
    except Exception as e:
        print(f"Erro ao rastrear {fonte}: {e}")
    return noticias_locais

def rodar_radar():
    radar_data = []
    alvos = [
        {"url": "https://website.cfo.org.br/noticias/", "sel": "h2.entry-title", "name": "CFO", "cat": "odontologia"},
        {"url": "https://croba.org.br/noticias/", "sel": "h2.entry-title", "name": "CRO-BA", "cat": "odontologia"},
        {"url": "https://abo-ba.org.br/noticias/", "sel": ".post-title", "name": "ABO-BA", "cat": "odontologia"},
        {"url": "https://www.abo.org.br/noticias", "sel": ".noticia-titulo", "name": "ABO", "cat": "odontologia"},
        {"url": "https://www.acordacidade.com.br/", "sel": ".entry-title", "name": "Acorda Cidade", "cat": "feira"},
        {"url": "https://g1.globo.com/ba/feira-de-santana-regiao/", "sel": ".feed-post-link", "name": "G1 Feira", "cat": "feira"},
        {"url": "https://noticias.r7.com/bahia/", "sel": ".r7-flex-listing-title", "name": "R7 Bahia", "cat": "feira"},
        {"url": "https://portaldafeira.com.br/", "sel": "h3.entry-title", "name": "Portal da Feira", "cat": "feira"},
        {"url": "https://www.jornalfolhadoestado.com/?s=Feira+de+Santana", "sel": ".entry-title", "name": "Folha Estado", "cat": "feira"}
    ]

    for alvo in alvos:
        radar_data.extend(capturar_noticias(alvo['url'], alvo['sel'], alvo['name'], alvo['cat']))

    # Limpeza de duplicatas
    vistos = set()
    data_final = [n for n in radar_data if not (n['titulo'] in vistos or vistos.add(n['titulo']))]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_final, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    rodar_radar()
