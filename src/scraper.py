import os
import time
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

# Constante para URL de ofertas da PSN
BASE_URL_DEALS = "https://store.playstation.com/pt-br/category/3f772501-f6f8-49b7-abac-874a88ca4897"

def scrape_psn(max_pages=5):
    """
    Realiza a coleta de dados da seção de promoções da PlayStation Store.
    
    Args:
        max_pages (int): Número máximo de páginas a serem percorridas.
    """
    
    data_collection = []

    print(f"[INFO] Iniciando processo de scraping. Alvo: {BASE_URL_DEALS}")
    print(f"[INFO] Configuração: {max_pages} páginas a serem analisadas.")

    with sync_playwright() as p:
        # headless=False permite visualização para debug; alterar para True em produção
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for current_page in range(1, max_pages + 1):
            target_url = f"{BASE_URL_DEALS}/{current_page}"
            print(f"[INFO] Processando página {current_page}/{max_pages}...")
            
            try:
                page.goto(target_url)
                
                # Aguarda estabilidade de rede (networkidle) com timeout de segurança
                try:
                    page.wait_for_load_state("networkidle", timeout=5000)
                except:
                    pass 

                # Lógica de scroll para ativar lazy loading de imagens e itens
                for _ in range(5):
                    page.mouse.wheel(0, 1500)
                    time.sleep(0.5)

                # Coleta de elementos
                cards = page.query_selector_all("li")
                items_captured = 0

                for card in cards:
                    try:
                        text_content = card.inner_text()
                        
                        # Filtro primário: descarta elementos sem indicação de preço
                        if "R$" not in text_content and "Gratuito" not in text_content:
                            continue

                        # Extração: Título
                        title_el = card.query_selector("span[data-qa*='game-name']") or card.query_selector(".psw-t-body")
                        title = title_el.inner_text() if title_el else "N/A"

                        # Extração: Preço Atual
                        price_el = card.query_selector("span[data-qa*='price']")
                        price = price_el.inner_text() if price_el else "N/A"

                        # Extração: Percentual de Desconto
                        discount_el = card.query_selector("span[data-qa*='discount-badge']")
                        discount = discount_el.inner_text() if discount_el else "0%"

                        # Extração: Link do Produto
                        link_el = card.query_selector("a")
                        link = "https://store.playstation.com" + link_el.get_attribute("href") if link_el else "N/A"

                        if title and title != "N/A":
                            data_collection.append({
                                "Titulo": title,
                                "Preco_Atual": price,
                                "Desconto_Txt": discount,
                                "Link": link,
                                "Data_Coleta": datetime.now().strftime("%Y-%m-%d")
                            })
                            items_captured += 1

                    except Exception:
                        continue # Ignora erros pontuais de parsing em cards específicos
                
                print(f"   -> {items_captured} itens capturados.")
                
            except Exception as e:
                print(f"[ERROR] Falha na página {current_page}: {e}")

        browser.close()

    # Persistência dos dados
    if data_collection:
        df = pd.DataFrame(data_collection)
        # Remove duplicatas baseadas no título
        df = df.drop_duplicates(subset=['Titulo'])
        
        # Definição de diretórios e nomes de arquivo
        output_dir = os.path.join("data", "raw")
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"psn_promo_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        output_path = os.path.join(output_dir, filename)
        
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"[SUCCESS] Coleta finalizada. {len(df)} registros salvos em: {output_path}")
    else:
        print("[WARN] Nenhum dado foi coletado durante a execução.")

if __name__ == "__main__":
    scrape_psn(max_pages=5)