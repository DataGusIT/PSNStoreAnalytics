import pandas as pd
import os
import glob

def clean_price(price_str):
    """Converte string de preço (R$ XX,XX) para float."""
    if pd.isna(price_str): 
        return 0.0
    
    price_str = str(price_str)
    
    if 'Gratuito' in price_str or 'Incluído' in price_str: 
        return 0.0
    
    # Remove caracteres não numéricos exceto vírgula e ponto
    clean_str = price_str.replace('R$', '').replace(' ', '').strip()
    
    try:
        # Padrão brasileiro: remove ponto de milhar, substitui vírgula decimal por ponto
        clean_str = clean_str.replace('.', '').replace(',', '.')
        return float(clean_str)
    except ValueError:
        return 0.0

def clean_discount(disc_str):
    """Converte string de desconto (-XX%) para inteiro absoluto."""
    if pd.isna(disc_str) or disc_str == '0%':
        return 0
    try:
        return int(disc_str.replace('-', '').replace('%', ''))
    except ValueError:
        return 0

def calculate_original_price(row):
    """Estima o preço original baseado no preço atual e desconto."""
    if row['Desconto_Pct'] > 0:
        return row['Preco_Num'] / (1 - (row['Desconto_Pct'] / 100))
    return row['Preco_Num']

def run_etl():
    print("[INFO] Iniciando pipeline de ETL (Extract, Transform, Load)...")
    
    # Identifica o arquivo mais recente na pasta raw
    list_of_files = glob.glob('data/raw/*.csv')
    if not list_of_files:
        print("[ERROR] Nenhum arquivo encontrado em data/raw/.")
        return
    
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"[INFO] Processando arquivo: {latest_file}")
    
    df = pd.read_csv(latest_file)
    
    # 1. Limpeza e Conversão de Tipos
    df['Preco_Num'] = df['Preco_Atual'].apply(clean_price)
    df['Desconto_Pct'] = df['Desconto_Txt'].apply(clean_discount)
    
    # 2. Engenharia de Atributos (Feature Engineering)
    df['Preco_Original_Est'] = df.apply(calculate_original_price, axis=1)
    df['Economia_Reais'] = df['Preco_Original_Est'] - df['Preco_Num']
    df['Status_Promocao'] = df['Desconto_Pct'].apply(lambda x: 'Promocao' if x > 0 else 'Preco Normal')

    # 3. Persistência (Load)
    
    # A) Arquivo processado para consumo imediato (Dashboard)
    processed_path = os.path.join("data", "processed", "psn_games_clean.csv")
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.to_csv(processed_path, index=False, encoding='utf-8-sig')
    
    # B) Banco de Dados Histórico (Append Only)
    history_path = os.path.join("data", "database", "psn_history_master.csv")
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    
    if os.path.exists(history_path):
        df.to_csv(history_path, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        df.to_csv(history_path, index=False, encoding='utf-8-sig')
        
    print(f"[SUCCESS] ETL concluído. Dados processados salvos em: {processed_path}")
    print(f"[SUCCESS] Dados históricos atualizados em: {history_path}")

if __name__ == "__main__":
    run_etl()