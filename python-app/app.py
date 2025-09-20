import os
import requests
from bs4 import BeautifulSoup
import time
import pika
import json
from categorias import CATEGORIAS
import random

# ----------------------------
# Config via Environment
# ----------------------------
RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBIT_USER", "admin")
RABBIT_PASS = os.getenv("RABBIT_PASS", "admin")
EXCHANGE = os.getenv("RABBIT_EXCHANGE", "categoria_exchange")

QUEUE_TEC = os.getenv("RABBIT_QUEUE_TECNOLOGIA", "tecnologia_queue")
QUEUE_ACA = os.getenv("RABBIT_QUEUE_ACADEMIA", "academia_queue")

MAX_PAGINAS = int(os.getenv("MAX_PAGINAS", "1"))
SLEEP_BETWEEN_REQUESTS = int(os.getenv("REQUEST_SLEEP_SECS", "2"))
LOOP_SLEEP_SECS = int(os.getenv("SCRAPER_SLEEP_SECS", "5"))

HEADERS = {
    "User-Agent": os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
}

# ----------------------------
# Conexão RabbitMQ (com retry)
# ----------------------------
def get_channel():
    creds = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    params = pika.ConnectionParameters(host=RABBIT_HOST, credentials=creds, heartbeat=30)
    while True:
        try:
            conn = pika.BlockingConnection(params)
            ch = conn.channel()
            ch.exchange_declare(exchange=EXCHANGE, exchange_type='direct', durable=True)
            # declara filas e bindings
            ch.queue_declare(queue=QUEUE_TEC, durable=True)
            ch.queue_declare(queue=QUEUE_ACA, durable=True)
            ch.queue_bind(exchange=EXCHANGE, queue=QUEUE_TEC, routing_key="Tecnologia")
            ch.queue_bind(exchange=EXCHANGE, queue=QUEUE_ACA, routing_key="Academia")
            return conn, ch
        except Exception as e:
            print(f"[rabbitmq] Falha de conexão: {e}. Retentando em 5s...")
            time.sleep(5)

def publish_message(ch, routing_key, body_dict):
    ch.basic_publish(
        exchange=EXCHANGE,
        routing_key=routing_key,
        body=json.dumps(body_dict, ensure_ascii=False),
        properties=pika.BasicProperties(
            content_type="application/json",
            delivery_mode=2
        )
    )

# ----------------------------
# Scraper (igual ao seu, com ajustes)
# ----------------------------
def buscar_produtos(produto, categoria="Tecnologia", max_paginas=1, ch=None):
    produto_formatado = produto.replace(" ", "-")
    url_base = f"https://lista.mercadolivre.com.br/{produto_formatado}"

    for pagina in range(1, max_paginas + 1):
        url_final = f"{url_base}{pagina}_noindex_True"
        try:
            response = requests.get(url_final, headers=HEADERS, timeout=20)
            print(f"Buscando {url_final} → Status: {response.status_code}")
        except Exception as e:
            print("Erro na requisição:", e)
            continue

        if response.status_code != 200:
            print("Erro ao acessar a página.")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        titulos = soup.find_all("a", class_="poly-component__title")
        precos = soup.find_all("span", class_="andes-money-amount andes-money-amount--cents-superscript")
        imagens = soup.find_all("img", class_="poly-component__picture")
        estrelas = soup.find_all("span", class_="andes-visually-hidden")
        frete = soup.find_all("div", class_="poly-component__shipping")
        nomeVendedor = soup.find_all("span", class_="poly-component__seller")

        if not titulos or not precos or not imagens:
            print("Nenhum resultado encontrado.")
            continue

        # Pegando apenas o primeiro resultado (como no seu código)
        titulo = titulos[0]
        preco = precos[0]
        imagem = imagens[0]
        nome = titulo.text.strip()
        link = titulo.get("href")
        preco_valor = preco.text.strip().replace("R$", "").replace(".", "").replace(",", ".").strip()
        img_url = imagem.get("data-src") or imagem.get("src") or ""
        vendedor = nomeVendedor[0].text.strip() if nomeVendedor else "Vendedor não informado"
        estrela = estrelas[0].text.strip() if estrelas else "Sem avaliação"
        fretes = frete[0].text.strip() if frete else "Frete não informado"

        try:
            preco_float = float(preco_valor)
        except:
            preco_float = 0.0

        produto_json = {
            "titulo": nome,
            "vendedorNome": vendedor,
            "linkProduto": link,
            "preco": preco_float,
            "avaliacao": estrela,
            "imagens": img_url,
            "categoria": categoria,
            "frete": fretes
        }

        routing_key = categoria  # "Tecnologia" ou "Academia"

        try:
            publish_message(ch, routing_key, produto_json)
            print(f"[x] Produto enviado -> {produto_json}")
        except Exception as e:
            print("[publish] erro ao publicar, tentando reconectar:", e)
            return False  # força reconexão

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    return True

# ----------------------------
# Execução
# ----------------------------
if __name__ == "__main__":
    conn, ch = get_channel()
    try:
        while True:
            categoria_escolhida = random.choice(list(CATEGORIAS.keys()))
            produto_escolhido = random.choice(CATEGORIAS[categoria_escolhida])

            print(f"\n🔎 Categoria sorteada: {categoria_escolhida}")
            print(f"🔑 Palavra-chave sorteada: {produto_escolhido}\n")

            ok = buscar_produtos(produto_escolhido, categoria=categoria_escolhida, max_paginas=MAX_PAGINAS, ch=ch)

            # Se publicação falhou, reconecta
            if not ok:
                try:
                    conn.close()
                except:
                    pass
                conn, ch = get_channel()

            print(f"Aguardando {LOOP_SLEEP_SECS} segundos para próxima execução...")
            time.sleep(LOOP_SLEEP_SECS)
    finally:
        try:
            conn.close()
        except:
            pass
