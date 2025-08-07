const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false }); // headless: false = para ver o que está acontecendo
  const page = await browser.newPage();

  // Vai até a página principal
  await page.goto('https://sislog.go.gov.br/');

  // Clica no link "Contratações"
  await page.getByRole('link', { name: 'Contratações', exact: true }).click();

  // Espera a página carregar completamente
  await page.waitForLoadState('networkidle');

  // Seleciona a modalidade "Pregão Eletrônico"
  await page.selectOption('#comboModalidades', { label: 'Pregão Eletrônico' });

  // Seleciona o status "Em Andamento"
  await page.selectOption('#comboStatus', { label: 'Em Andamento' });

  // Aguarda meio segundo para evitar bugs de timing
  await page.waitForTimeout(500);

  // Clica no botão "Consultar"
  await page.locator('button:has-text("Consultar")').click();

  // Espera a tabela carregar (ou espera 5 segundos)
  await page.waitForTimeout(5000);

  // Você pode adicionar aqui a lógica para extrair os dados se quiser depois

  // await browser.close(); // Deixa comentado para poder ver os resultados
})();
