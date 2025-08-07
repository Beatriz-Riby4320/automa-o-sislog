from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://sislog.go.gov.br/')
    page.get_by_role('link', name='Contratações', exact=True).click()
    page.wait_for_load_state('networkidle')

    page.select_option('#comboModalidades', label='Pregão Eletrônico')
    page.dispatch_event('#comboModalidades', 'change')

    page.select_option('#comboStatus', label='Em Andamento')
    page.dispatch_event('#comboStatus', 'change')

    page.wait_for_timeout(1000)

    try:
        consultar_btn = page.get_by_role('link', name=' Consultar')
        consultar_btn.wait_for(state='visible', timeout=10000)
        consultar_btn.click()
    except Exception as e:
        print("Erro ao clicar no botão 'Consultar':", e)

    page.wait_for_timeout(5000)

    # Aqui você pode adicionar lógica para extrair os dados da tabela



