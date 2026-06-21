const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: false,
    channel: 'chromium'
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('https://www.baidu.com');
  console.log('Browser launched and navigated to Baidu. Browser will stay open.');
  console.log('Close the browser window to exit, or press Ctrl+C in this terminal.');

  // Keep the script running - browser stays open
  // Will wait until the browser is closed by the user
  browser.on('disconnected', () => {
    console.log('Browser closed. Exiting.');
    process.exit(0);
  });
})();
