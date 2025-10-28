from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta, timezone
from trello_automacao_PE import processar_contratacoes # Importa a função correta

fuso_brasilia = timezone(timedelta(hours=-3))


# Intervalo de datas desejado
data_inicio = datetime.strptime("15/10/2025", "%d/%m/%Y")
data_fim = datetime.strptime("27/10/2025", "%d/%m/%Y").replace(hour=23, minute=59)


contratacoes = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://sislog.go.gov.br/')
    page.get_by_role('link', name='Contratações', exact=True).click()
    page.wait_for_load_state('networkidle')

    page.select_option('#comboModalidades', label='Pregão Eletrônico') # Selecionar modalidade
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
            num_pregao = texto_colunas[2]
            objeto = texto_colunas[3]
            orgao = texto_colunas[4]
            data_publicacao_str = texto_colunas[5]
            data_fim_str = texto_colunas[6]

            try:
                data_publicacao = datetime.strptime(data_publicacao_str, "%d/%m/%Y %H:%M").replace(tzinfo=fuso_brasilia)
                data_encerramento = datetime.strptime(data_fim_str, "%d/%m/%Y %H:%M").replace(tzinfo=fuso_brasilia)


                if data_inicio.date() <= data_publicacao.date() <= data_fim.date():
                    link_element = colunas.nth(1).locator('a')
                    link = link_element.get_attribute('href') or "Link não disponível"

                    # Corrige link quebrado
                    if link and not link.startswith("http"):
                        link = f"https://sislog.go.gov.br{link}"

                    contratacoes.append({
                        "num_contratacao": num_contratacao,
                        "orgao": orgao,
                        "num_pregao": num_pregao,
                        "objeto": objeto,
                        "data_inicio": data_publicacao,
                        "data_fim": data_encerramento,
                        "link": link
                    })

            except ValueError:
                print(f"Data inválida na linha {i}: {data_publicacao_str}")

# Envia para o Trello
processar_contratacoes(contratacoes)
