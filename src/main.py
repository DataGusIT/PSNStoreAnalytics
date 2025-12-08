import sys
import os
import time
from datetime import datetime

# Garante que o diretório atual esteja no path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import scraper
import etl

class LoggerWriter:
    """
    Classe utilitária para redirecionar o output (print) 
    tanto para o terminal quanto para um arquivo de log.
    """
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.log = open(filepath, "a", encoding="utf-8") # 'a' para append

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # Necessário para compatibilidade com sys.stdout
        self.terminal.flush()
        self.log.flush()

def main():
    # --- CONFIGURAÇÃO DE LOGS ---
    # Cria o nome do arquivo de log com data/hora: logs/run_2023-12-07_10-30.log
    log_filename = f"run_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.log"
    log_path = os.path.join("logs", log_filename)
    
    # Garante que a pasta existe
    os.makedirs("logs", exist_ok=True)
    
    # Redireciona o print para o arquivo
    sys.stdout = LoggerWriter(log_path)
    
    # --- INÍCIO DO PROCESSO ---
    # Defina aqui quantas páginas quer ler (para teste use 5, para produção use 182)
    PAGINAS_PARA_LER = 5 
    
    start_time = time.time()
    
    print("-" * 60)
    print("PSN STORE ANALYTICS - AUTOMATION PIPELINE")
    print(f"Log File: {log_path}")
    print("-" * 60)
    
    # --- STEP 1: SCRAPING ---
    print(f"\n[STEP 1/2] Data Collection (Scraping)")
    try:
        scraper.scrape_psn(max_pages=PAGINAS_PARA_LER)
    except Exception as e:
        print(f"[CRITICAL ERROR] Falha no módulo de Scraping: {e}")
        # Se der erro, não queremos parar o log, mas podemos encerrar o script
        sys.exit(1)

    # --- STEP 2: ETL ---
    print(f"\n[STEP 2/2] Data Processing (ETL)")
    try:
        etl.run_etl()
    except Exception as e:
        print(f"[CRITICAL ERROR] Falha no módulo de ETL: {e}")
        sys.exit(1)

    # --- SUMMARY ---
    elapsed_time = time.time() - start_time
    
    print("-" * 60)
    print(f"[DONE] Pipeline finalizado com sucesso.")
    print(f"Tempo total de execução: {elapsed_time:.2f} segundos.")
    print("-" * 60)

if __name__ == "__main__":
    main()