from playwright.sync_api import sync_playwright
from datetime import datetime

# Define o intervalo de datas desejado
data_inicio = datetime.strptime("23/09/2025", "%d/%m/%Y")
data_fim = datetime.strptime("30/09/2025", "%d/%m/%Y")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://sislog.go.gov.br/')
    page.get_by_role('link', name='Contratações', exact=True).click()
    page.wait_for_load_state('networkidle')

    page.select_option('#comboModalidades', label='Pregão Eletrônico - SRP')
    page.dispatch_event('#comboModalidades', 'change')

    page.select_option('#comboStatus', label='Em Andamento')
    page.dispatch_event('#comboStatus', 'change')

    page.wait_for_timeout(1000)

    consultar_btn = page.get_by_role('link', name=' Consultar')
    consultar_btn.wait_for(state='visible', timeout=10000)
    consultar_btn.click()

    page.wait_for_timeout(5000)

    linhas = page.locator('table tbody tr')
    total_linhas = linhas.count()
    print(f"Total de linhas encontradas: {total_linhas}")

    for i in range(total_linhas):
        linha = linhas.nth(i)
        colunas = linha.locator('td')
        texto_colunas = [colunas.nth(j).inner_text().strip() for j in range(colunas.count())]

        if len(texto_colunas) >= 7:
            num_contratacao = texto_colunas[1]
            objeto = texto_colunas[3]                  # Objeto (coluna 4)
            data_publicacao_str = texto_colunas[5]

            try:
                data_publicacao = datetime.strptime(data_publicacao_str, "%d/%m/%Y %H:%M")
                # Compara apenas a data (sem hora)
                if data_inicio.date() <= data_publicacao.date() <= data_fim.date():
                    print(f"Nº Contratação: {num_contratacao} | Publicação: {data_publicacao_str} | Objeto: {objeto}")
            except ValueError:
                print(f"Data inválida na linha {i}: {data_publicacao_str}")