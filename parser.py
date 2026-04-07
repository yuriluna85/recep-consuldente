import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import time

def buscar_imagem_wp(post_json):
    try:
        if "_links" in post_json and "wp:featuredmedia" in post_json["_links"]:
            media_url = post_json["_links"]["wp:featuredmedia"][0]["href"]
            res = requests.get(media_url, timeout=10)
            if res.status_code == 200:
                return res.json()["source_url"]
    except:
        pass
    return None

def capturar_noticias():
    print(f"📡 Radar Consuldente v1.2 - Iniciando em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    final_news = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    fontes = [
        {"nome": "CFO Federal", "json": "https://website.cfo.org.br/wp-json/wp/v2/posts", "rss": "https://website.cfo.org.br/feed/", "cat": "ODONTOLOGIA"},
        {"nome": "CRO-BA", "json": "https://croba.org.br/wp-json/wp/v2/posts", "rss": "https://croba.org.br/feed/", "cat": "ODONTOLOGIA"},
        {"nome": "ABO-BA", "json": "https://abo-ba.org.br/wp-json/wp/v2/posts", "rss": "https://abo-ba.org.br/feed/", "cat": "ODONTOLOGIA"},
        {"nome": "Acorda Cidade", "json": "https://www.acordacidade.com.br/wp-json/wp/v2/posts", "rss": "https://www.acordacidade.com.br/feed/", "cat": "FEIRA DE SANTANA"},
        {"nome": "Portal da Feira", "json": "https://portaldafeira.com.br/wp-json/wp/v2/posts", "rss": "https://portaldafeira.com.br/feed/", "cat": "FEIRA DE SANTANA"},
        {"nome": "Folha do Estado", "json": "https://www.jornalfolhadoestado.com/wp-json/wp/v2/posts", "rss": "https://www.jornalfolhadoestado.com/feed/", "cat": "FEIRA DE SANTANA"},
        {"nome": "G1 Feira", "json": None, "rss": "https://g1.globo.com/dynamo/ba/feira-de-santana-regiao/rss2.xml", "cat": "FEIRA DE SANTANA"}
    ]

    for f in fontes:
        success = False
        time.sleep(random.uniform(1, 2))
        if f["json"]:
            try:
                res = requests.get(f["json"], headers=headers, timeout=15)
                if res.status_code == 200:
                    for p in res.json()[:6]:
                        img = buscar_imagem_wp(p)
                        final_news.append({
                            "titulo": p["title"]["rendered"][:95],
                            "resumo": "Portal Oficial - Clique para ler mais.",
                            "cat": f["cat"],
                            "fonte": f["nome"],
                            "data": datetime.now().strftime("%H:%M"),
                            "url": p["link"],
                            "img": img if img else f"https://picsum.photos/seed/{random.randint(1,999)}/800/400"
                        })
                    success = True
            except: pass

        if not success and f["rss"]:
            try:
                res = requests.get(f["rss"], headers=headers, timeout=15)
                soup = BeautifulSoup(res.content, features="xml")
                for i in soup.findAll('item')[:6]:
                    final_news.append({
                        "titulo": i.title.text[:95],
                        "resumo": "Atualização via Radar Consuldente.",
                        "cat": f["cat"],
                        "fonte": f["nome"],
                        "data": datetime.now().strftime("%H:%M"),
                        "url": i.link.text,
                        "img": f"https://picsum.photos/seed/{random.randint(1,999)}/800/400"
                    })
            except: pass

    random.shuffle(final_news)
    with open('data.json', 'w', encoding='utf-8') as f_out:
        json.dump(final_news, f_out, ensure_ascii=False, indent=4)
    print("🚀 data.json atualizado com sucesso!")

if __name__ == "__main__":
    capturar_noticias()
