const { chromium } = require('playwright'); // ou 'firefox' ou 'webkit'

(async () => {
  // Inicia o navegador (não headless para visualização)
  const browser = await chromium.launch({ headless: false });

  // Cria um novo contexto com user agent e localização geográfica
  const context = await browser.newContext({
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    geolocation: { longitude: -47.9292, latitude: -15.7801 }, // Brasília
    permissions: ['geolocation']
  });

  // Abre uma nova página
  const page = await context.newPage();

  // Vai para o site do ComprasNet
  await page.goto('https://sislog.go.gov.br/');

  // Aguarda para visualizar (opcional)
  await page.waitForTimeout(5000);

  // Fecha o navegador (opcional)
  // await browser.close();
})();