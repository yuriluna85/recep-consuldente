import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import time

def buscar_imagem_wp(post_json):
    """Tenta extrair a imagem destacada do JSON do WordPress"""
    try:
        # Verifica se o link da imagem está embutido no JSON (links -> wp:featuredmedia)
        if "_links" in post_json and "wp:featuredmedia" in post_json["_links"]:
            media_url = post_json["_links"]["wp:featuredmedia"][0]["href"]
            res = requests.get(media_url, timeout=10)
            return res.json()["source_url"]
    except:
        pass
    return f"https://picsum.photos/seed/{random.randint(1,1000)}/800/400"

def capturar_noticias():
    print(f"📡 Iniciando Radar Híbrido às {datetime.now().strftime('%H:%M:%S')}")
    final_news = []
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    fontes = [
        # ODONTOLOGIA
        {"nome": "CFO Federal", "json": "https://website.cfo.org.br/wp-json/wp/v2/posts", "rss": "https://website.cfo.org.br/feed/", "cat": "ODONTOLOGIA"},
        {"nome": "CRO-BA", "json": "https://croba.org.br/wp-json/wp/v2/posts", "rss": "https://croba.org.br/feed/", "cat": "ODONTOLOGIA"},
        {"nome": "ABO-BA", "json": "https://abo-ba.org.br/wp-json/wp/v2/posts", "rss": "https://abo-ba.org.br/feed/", "cat": "ODONTOLOGIA"},
        
        # FEIRA DE SANTANA
        {"nome": "Acorda Cidade", "json": "https://www.acordacidade.com.br/wp-json/wp/v2/posts", "rss": "https://www.acordacidade.com.br/feed/", "cat": "FEIRA"},
        {"nome": "Portal da Feira", "json": "https://portaldafeira.com.br/wp-json/wp/v2/posts", "rss": "https://portaldafeira.com.br/feed/", "cat": "FEIRA"},
        {"nome": "Folha do Estado", "json": "https://www.jornalfolhadoestado.com/wp-json/wp/v2/posts", "rss": "https://www.jornalfolhadoestado.com/feed/", "cat": "FEIRA"},
        
        # ESPECIAIS (G1 via RSS)
        {"nome": "G1 Feira", "json": None, "rss": "https://g1.globo.com/dynamo/ba/feira-de-santana-regiao/rss2.xml", "cat": "FEIRA"}
    ]

    for f in fontes:
        success = False
        print(f"🔎 Rastreando: {f['nome']}")

        # TENTATIVA 1: WP-JSON (Melhor qualidade)
        if f["json"]:
            try:
                res = requests.get(f["json"], headers=headers, timeout=15)
                if res.status_code == 200:
                    posts = res.json()[:6]
                    for p in posts:
                        final_news.append({
                            "titulo": p["title"]["rendered"][:95],
                            "resumo": "Clique para ler a matéria completa no portal oficial.",
                            "cat": f["cat"],
                            "fonte": f["nome"],
                            "data": datetime.now().strftime("%H:%M"),
                            "url": p["link"],
                            "img": buscar_imagem_wp(p)
                        })
                    print(f"  ✅ {f['nome']} via JSON")
                    success = True
            except: pass

        # TENTATIVA 2: RSS / Feed (Redundância)
        if not success and f["rss"]:
            try:
                res = requests.get(f["rss"], headers=headers, timeout=15)
                soup = BeautifulSoup(res.content, features="xml")
                items = soup.findAll('item')[:6]
                for i in items:
                    # Tenta extrair imagem do content:encoded ou media:content
                    img = "https://picsum.photos/seed/feira/800/400"
                    if i.find('media:content'): img = i.find('media:content')['url']
                    
                    final_news.append({
                        "titulo": i.title.text[:95],
                        "resumo": "Notícia atualizada capturada via Feed RSS.",
                        "cat": f["cat"],
                        "fonte": f["nome"],
                        "data": datetime.now().strftime("%H:%M"),
                        "url": i.link.text,
                        "img": img
                    })
                print(f"  ✅ {f['nome']} via RSS")
                success = True
            except: pass

    # Embaralhar para o Slide ficar dinâmico
    random.shuffle(final_news)

    with open('data.json', 'w', encoding='utf-8') as f_out:
        json.dump(final_news, f_out, ensure_ascii=False, indent=4)
    print(f"🚀 Radar Concluído! {len(final_news)} posts processados.")

if __name__ == "__main__":
    capturar_noticias()
