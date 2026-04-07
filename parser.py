import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import time
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import time

def buscar_imagem_wp(post_json, session):
    try:
        if "_links" in post_json and "wp:featuredmedia" in post_json["_links"]:
            media_url = post_json["_links"]["wp:featuredmedia"][0]["href"]
            res = session.get(media_url, timeout=10)
            if res.status_code == 200:
                return res.json()["source_url"]
    except:
        pass
    return None

def capturar_noticias():
    print(f"📡 Radar Consuldente v1.1 - Iniciando varredura em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    final_news = []
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    })

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
        print(f"🔎 Analisando: {f['nome']}")
        success = False
        time.sleep(random.uniform(2, 4)) 

        if f["json"]:
            try:
                res = session.get(f["json"], timeout=20)
                if res.status_code == 200:
                    for p in res.json()[:7]:
                        img = buscar_imagem_wp(p, session)
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
                    print(f"  ✅ JSON OK")
            except: pass

        if not success and f["rss"]:
            try:
                res = session.get(f["rss"], timeout=20)
                soup = BeautifulSoup(res.content, features="xml")
                for i in soup.findAll('item')[:7]:
                    final_news.append({
                        "titulo": i.title.text[:95],
                        "resumo": "Atualização via Radar Consuldente.",
                        "cat": f["cat"],
                        "fonte": f["nome"],
                        "data": datetime.now().strftime("%H:%M"),
                        "url": i.link.text,
                        "img": f"https://picsum.photos/seed/{random.randint(1,999)}/800/400"
                    })
                print(f"  ✅ RSS OK")
            except: print(f"  ❌ Falha em {f['nome']}")

    random.shuffle(final_news)
    with open('data.json', 'w', encoding='utf-8') as f_out:
        json.dump(final_news, f_out, ensure_ascii=False, indent=4)
    print(f"🏁 Fim. {len(final_news)} notícias salvas.")

if __name__ == "__main__":
    capturar_noticias()
def buscar_imagem_wp(post_json, session):
    try:
        if "_links" in post_json and "wp:featuredmedia" in post_json["_links"]:
            media_url = post_json["_links"]["wp:featuredmedia"][0]["href"]
            res = session.get(media_url, timeout=10)
            if res.status_code == 200:
                return res.json()["source_url"]
    except:
        pass
    return None

def capturar_noticias():
    print(f"📡 Radar Consuldente v5.0 - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    final_news = []
    
    # Sessão persistente para manter cookies e simular melhor um humano
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
    })

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
        print(f"🔎 Analisando: {f['nome']}")
        success = False
        time.sleep(random.uniform(2, 4)) # Delay para não ser banido

        # TENTATIVA 1: JSON
        if f["json"]:
            try:
                res = session.get(f["json"], timeout=20)
                if res.status_code == 200:
                    for p in res.json()[:7]:
                        img = buscar_imagem_wp(p, session)
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
                    print(f"  ✅ JSON OK")
            except: pass

        # TENTATIVA 2: RSS (Se JSON falhar)
        if not success and f["rss"]:
            try:
                res = session.get(f["rss"], timeout=20)
                soup = BeautifulSoup(res.content, features="xml")
                for i in soup.findAll('item')[:7]:
                    final_news.append({
                        "titulo": i.title.text[:95],
                        "resumo": "Atualização via Radar Consuldente.",
                        "cat": f["cat"],
                        "fonte": f["nome"],
                        "data": datetime.now().strftime("%H:%M"),
                        "url": i.link.text,
                        "img": f"https://picsum.photos/seed/{random.randint(1,999)}/800/400"
                    })
                print(f"  ✅ RSS OK")
            except: print(f"  ❌ Falha total em {f['nome']}")

    random.shuffle(final_news)
    with open('data.json', 'w', encoding='utf-8') as f_out:
        json.dump(final_news, f_out, ensure_ascii=False, indent=4)
    print(f"🏁 Fim. {len(final_news)} notícias salvas.")

if __name__ == "__main__":
    capturar_noticias()
