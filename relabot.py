from pathlib import Path
import sys
import time
import subprocess
import os
from dotenv import load_dotenv
import telebot
from datetime import date
import glob

load_dotenv("key.env")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

pasta_downloads = Path.home() / "Downloads"

if not TOKEN:
    raise ValueError("Defina TELEGRAM_BOT_TOKEN no key.env")

bot = telebot.TeleBot(TOKEN)


def aguardar_relatorio_do_dia(pasta_downloads: str, timeout: int = 30) -> str:
    hoje = date.today().isoformat()  # Ex.: "2026-11-19"
    padrao = os.path.join(pasta_downloads, f"validade-relatorio-{hoje}*.xlsx")
    inicio = time.time()

    while time.time() - inicio < timeout:
        # Garante que não há download em andamento para o padrão de hoje
        em_andamento = glob.glob(os.path.join(pasta_downloads, f"validade-relatorio-{hoje}*.crdownload"))
        if not em_andamento:
            arquivos = [
                arq for arq in glob.glob(padrao)
                if os.path.isfile(arq) and os.path.getsize(arq) > 0
            ]
            if arquivos:
                # Se houver mais de um, pega o mais recente
                return max(arquivos, key=os.path.getmtime)

        time.sleep(0.5)

    raise FileNotFoundError(f"Arquivo do relatório de {hoje} não encontrado em {pasta_downloads}.")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Bot online! Manda um /ajuda ou qualquer texto.")


@bot.message_handler(commands=["ajuda"])
def ajuda(message):
    bot.reply_to(message, "Comandos:\n/start - Inicia\n/ajuda - Ajuda\n/relatorio Envia o Relatório mensal")

@bot.message_handler(commands=["relatorio"])
def comando_relatorio(message):
    bot.reply_to(message, "Gerando o relatório, aguarde...")

    try:
        subprocess.run([sys.executable, "webscrappe.py"], check=True)
        caminho_arquivo = aguardar_relatorio_do_dia(str(pasta_downloads), timeout=30)
        with open(caminho_arquivo, "rb") as arquivo:
            bot.send_document(message.chat.id, arquivo)

    except Exception as erro:
        bot.reply_to(message, f"Falha no processo: {erro}")


print("Bot rodando...")
bot.infinity_polling()