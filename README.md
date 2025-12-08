# PSN Store Analytics - Inteligência de Mercado

> Pipeline de Engenharia de Dados automatizado para extração (Web Scraping), processamento (ETL) e análise estratégica de preços da PlayStation Store.

[![Status](https://img.shields.io/badge/Status-Concluído-success)](https://github.com/DataGusIT/psn-analytics)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33)](https://playwright.dev/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Science-150458)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Sobre o Projeto

O **PSN Store Analytics** é uma aplicação de Data Science e Engenharia de Dados desenvolvida para monitorar o ecossistema de preços da loja digital da PlayStation. O objetivo foi criar um sistema capaz de simular um analista de mercado, coletando dados em tempo real e transformando-os em insights financeiros para tomada de decisão.

Diferente de scrapers simples, este projeto implementa um pipeline completo: coleta dados de páginas dinâmicas (Single Page Applications) usando automação de navegador, realiza a limpeza e engenharia de atributos (ETL) e persiste os dados em um histórico incremental para análise de tendências e oportunidades de compra (arbitragem de preços).

## 📊 Demonstração Visual

| Distribuição de Preços | Top 10 Jogos Mais Caros | Melhores Oportunidades (%) |
| :---: | :---: | :---: |
| <img width="1021" height="573" alt="Image" src="https://github.com/user-attachments/assets/565525ed-a0e7-4733-8ab8-8adc91d1ce03" /> | <img width="1477" height="709" alt="Image" src="https://github.com/user-attachments/assets/11c1950d-42ef-481c-8557-be74fa7192b4" /> | <img width="1444" height="554" alt="Image" src="https://github.com/user-attachments/assets/7d74b7ff-64d4-46a4-befc-d559461c4dd5" /> |

## ✨ Funcionalidades

### 📡 Coleta de Dados (Web Scraping)
-   **Automação com Playwright:** Simulação de navegador real para renderizar páginas dinâmicas (JavaScript pesado) que bibliotecas comuns não conseguem acessar.
-   **Paginação Automática:** O robô percorre centenas de páginas da loja automaticamente.
-   **Tratamento de Lazy Loading:** Algoritmo de scroll e espera inteligente (`networkidle`) para garantir o carregamento de todas as imagens e preços antes da extração.

### ⚙️ Processamento (ETL)
-   **Limpeza de Dados:** Conversão de strings complexas (ex: "R$ 1.299,90") para tipos numéricos (Float) e tratamento de valores nulos.
-   **Engenharia de Atributos:** Criação de novas métricas não nativas da loja, como `Economia_Real_BRL` e `Preco_Original_Estimado`.
-   **Histórico Incremental:** Sistema de banco de dados (`.csv` append-only) que acumula dados de diferentes execuções para análise temporal.

### 📈 Analytics & Insights
-   **Ranking de Pricing:** Identificação dos produtos "Top Tier" (Premium) e distribuição de faixas de preço.
-   **Caçador de Ofertas:** Algoritmo que destaca as maiores quedas de preço percentuais e absolutas.
-   **Visualização Profissional:** Dashboards gerados com Seaborn e Matplotlib para storytelling de dados.

## Tecnologias

### Linguagem e Core
-   **Python 3.12+**
-   **Playwright** (Automação de Browser e Scraping)
-   **Glob & OS** (Gerenciamento de arquivos e sistema)

### Processamento e Análise
-   **Pandas** (Manipulação de DataFrames e ETL)
-   **NumPy** (Computação numérica)

### Visualização
-   **Matplotlib**
-   **Seaborn**
-   **Jupyter Notebook** (Ambiente de prototipagem e apresentação)

## Primeiros Passos

Este projeto requer Python instalado e as dependências listadas.

1.  **Clone o repositório**
    ```bash
    git clone https://github.com/DataGusIT/psn-analytics.git
    cd psn-analytics
    ```

2.  **Configure o Ambiente Virtual**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as Dependências**
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

4.  **Execute o Pipeline Completo**
    O arquivo `main.py` executa o scraping e o ETL sequencialmente.
    ```bash
    python src/main.py
    ```

5.  **Visualize os Resultados**
    Abra o notebook na pasta `notebooks/` para ver os gráficos gerados com os dados frescos.

## Aprendizados

Este projeto consolidou conhecimentos avançados em:

-   **Web Scraping Moderno:** Como lidar com seletores dinâmicos, Shadow DOM e estratégias anti-bot simples usando Playwright.
-   **Pipeline de Dados:** A importância de separar as camadas de extração (`raw`) e processamento (`processed`) para integridade dos dados.
-   **Tratamento de Exceções:** Criação de scripts resilientes que não falham completamente ao encontrar um dado corrompido ou erro de rede.
-   **Storytelling com Dados:** Transformação de números brutos em gráficos que respondem perguntas de negócio.

## Suporte e Contato

-   **Email**: [g.moreno.souza05@gmail.com](mailto:g.moreno.souza05@gmail.com)
-   **LinkedIn**: [Gustavo Moreno](https://www.linkedin.com/in/gustavo-moreno-8a925b26a/)

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">
  Desenvolvido por Gustavo Moreno Souza
  <br><br>
  <a href="https://www.linkedin.com/in/gustavo-moreno-8a925b26a/" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24" alt="LinkedIn"/>
  </a>
</div>
