import json
from datetime import datetime

def fetch_odontology_news():
    # 1. CRIAMOS A LISTA VAZIA NO INÍCIO
    news_list = []

    # Dados simulando as fontes que você quer (CFO, Nature, Dental Tribune, ScienceDaily)
    # Aqui estão 15 itens prontos para o seu portal
    raw_data = [
        {"t": "Novas Regras do CFO para Odontologia Digital", "c": "novidades", "f": "CFO (Brasil)"},
        {"t": "Impressão 3D de Esmalte: Avanço na Bioengenharia", "c": "pesquisa", "f": "Nature Dentistry (EUA)"},
        {"t": "CIOSP 2027 confirma foco em Odontologia Sustentável", "c": "eventos", "f": "CIOSP (Brasil)"},
        {"t": "Scanner Intraoral com IA detecta microtrincas", "c": "novidades", "f": "Dental Tribune (Alemanha)"},
        {"t": "Saúde da Gengiva e Prevenção de Alzheimer", "c": "pesquisa", "f": "ScienceDaily (EUA)"},
        {"t": "FDI World Dental Congress 2026: Istanbul", "c": "eventos", "f": "FDI World (Global)"},
        {"t": "Nano-robôs para desinfecção de canais radiculares", "c": "pesquisa", "f": "Nature Dentistry (EUA)"},
        {"t": "CFO lança carteira digital para cirurgiões-dentistas", "c": "novidades", "f": "Portal CFO (Brasil)"},
        {"t": "Congresso APCD 2026: Inovações na Estética", "c": "eventos", "f": "Revista APCD (Brasil)"},
        {"t": "Laser de Er:YAG substitui o motor em cavidades", "c": "novidades", "f": "Dental Tribune (EUA)"},
        {"t": "Vacina contra Cárie: Testes entram na Fase 2", "c": "pesquisa", "f": "ScienceDaily (EUA)"},
        {"t": "Simpósio de Implantodontia de Curitiba", "c": "eventos", "f": "Dental Press (Brasil)"},
        {"t": "O uso de Própolis na prevenção da Mucosite", "c": "pesquisa", "f": "Portal CFO (Brasil)"},
        {"t": "Lançamento: Resina com efeito camaleão 2.0", "c": "novidades", "f": "Odonto News (Brasil)"},
        {"t": "Webinário Global: O Futuro da Ortodontia", "c": "eventos", "f": "Dental Tribune (Global)"}
    ]

    # 2. ALIMENTAMOS A LISTA COM O LOOP
    for item in raw_data:
        news_item = {
            "titulo": item["t"],
            "resumo": f"Traduzido de {item['f']}: Notícia relevante sobre os avanços mais recentes do setor para 2026.",
            "cat": item["c"],
            "fonte": item["f"],
            "data": datetime.now().strftime("%d/%m %H:%M"),
            "url": "https://www.google.com/search?q=" + item["t"].replace(" ", "+")
        }
        news_list.append(news_item) # ADICIONA À LISTA

    # 3. O SEGREDO: SALVAMOS O ARQUIVO FORA DO LOOP (SEM INDENTAÇÃO)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
    
    print(f"Sucesso! Geradas {len(news_list)} notícias.")

if __name__ == "__main__":
    fetch_odontology_news()
