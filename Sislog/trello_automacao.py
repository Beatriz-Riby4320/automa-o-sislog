# Atualização: código limpo com variáveis de ambiente
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# 🔐 Credenciais e IDs do Trello
API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")
BOARD_ID = os.getenv("BOARD_ID")
LIST_ID = os.getenv("LIST_ID")  # Aguardando Julgamento

# 🏷️ Nomes das etiquetas desejadas (corrigido para usar etiquetas existentes)
ETIQUETAS_DESEJADAS = ["SISLOG", "PE"]

def buscar_etiquetas():
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/labels?key={API_KEY}&token={TOKEN}"
    res = requests.get(url)
    return res.json()

def garantir_etiquetas():
    existentes = buscar_etiquetas()
    etiquetas_ids = []

    for nome_desejado in ETIQUETAS_DESEJADAS:
        etiqueta = next((e for e in existentes if e["name"].strip() == nome_desejado), None)
        if etiqueta:
            etiquetas_ids.append(etiqueta["id"])
        else:
            print(f"❌ Etiqueta '{nome_desejado}' não encontrada no quadro. Verifique se ela existe no Trello.")
    
    if len(etiquetas_ids) < len(ETIQUETAS_DESEJADAS):
        print("❌ Abortando: nem todas as etiquetas obrigatórias foram encontradas.")
        return None
    
    return etiquetas_ids

def criar_cartao(titulo, descricao, data_inicio, data_fim, etiquetas_ids):
    url = f"https://api.trello.com/1/cards"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "idList": LIST_ID,
        "name": titulo,
        "desc": descricao,
        "idLabels": ",".join(etiquetas_ids),
        "start": data_inicio.isoformat(),
        "due": data_fim.isoformat()
    }
    res = requests.post(url, params=params)
    if res.status_code != 200:
        print(f"❌ Erro ao criar cartão: {res.text}")
        return None
    return res.json()

def adicionar_comentario(card_id, texto):
    url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "text": texto
    }
    requests.post(url, params=params)

def processar_contratacoes(contratacoes):
    etiquetas_ids = garantir_etiquetas()
    if etiquetas_ids is None:
        return  # Aborta se etiquetas não forem encontradas

    for item in contratacoes:
        num_contratacao = item["num_contratacao"]
        orgao = item["orgao"]
        num_pregao = item["num_pregao"]
        objeto = item["objeto"]
        data_inicio = item["data_inicio"]
        data_fim = item["data_fim"]
        link = item["link"]

        titulo = f"{num_contratacao} - {orgao}"
        descricao = f"Número do Pregão: {num_pregao}\nObjeto: {objeto}"

        card = criar_cartao(titulo, descricao, data_inicio, data_fim, etiquetas_ids)
        if card and "id" in card:
            adicionar_comentario(card["id"], f"Link da contratação: {link}")
            print(f"✅ Cartão criado: {titulo}")
        else:
            print(f"❌ Falha ao criar cartão para: {titulo}")