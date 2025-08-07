const { chromium } = require('playwright'); // ou 'firefox' ou 'webkit'

(async () => {
  // Inicia o navegador (não headless para visualização)
  const browser = await chromium.launch({ headless: false });

  // Cria um novo contexto com user agent e localização geográfica
  const context = await browser.newContext({
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    geolocation: { longitude: -47.9292, latitude: -15.7801 },
    permissions: ['geolocation']
  });

  // Abre uma nova página
  const page = await context.newPage();

  // Vai para o site do SISLOG
  await page.goto('https://sislog.go.gov.br/');

  // Aguarda o carregamento (você pode ajustar)
 // Aguarda o carregamento (você pode ajustar)
await page.waitForLoadState('domcontentloaded');

await page.getByRole('link', { name: 'Contratações', exact: true }).click();

// Seleciona "Dispensa de Licitação" no combo de modalidades (valor 7)
await page.waitForSelector('#comboModalidades', { timeout: 10000 });
await page.locator('#comboModalidades').selectOption('1');
await page.locator('#comboModalidades').click();

// Seleciona "Publicadas" no combo de status (valor 1)
await page.waitForSelector('#comboStatus', { timeout: 10000 });
await page.locator('#comboStatus').selectOption('8');
await page.locator('#comboStatus').click();

// Clica no botão "Consultar" (com o ícone de lupa)
await page.getByRole('link', { name: ' Consultar' }).click();
})();

