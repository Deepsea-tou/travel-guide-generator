const { strict: assert } = require("node:assert");
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium } = require("playwright");

(async () => {
  const outputDir = fs.mkdtempSync(path.join(os.tmpdir(), "travel-roadbook-browser-"));
  const outputBase = path.join(outputDir, "guide");
  const python = fs.existsSync(".venv/bin/python") ? ".venv/bin/python" : "python3";
  execFileSync(python, ["scripts/build_roadbook.py", "tests/fixtures/v2-city-minimal.json", "--output", outputBase]);

  const defaultChrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
  const executablePath = process.env.CHROME_PATH || (fs.existsSync(defaultChrome) ? defaultChrome : undefined);
  const launchOptions = { headless: true };
  if (executablePath) launchOptions.executablePath = executablePath;
  const browser = await chromium.launch(launchOptions);
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  const pageErrors = [];
  page.on("pageerror", (error) => pageErrors.push(error.message));
  await page.goto(pathToFileURL(`${outputBase}.html`).href);

  await page.locator(".day-nav a").first().click();
  const itemCheck = page.locator(".item-check").first();
  await itemCheck.check();
  await page.reload();
  assert.equal(await page.locator(".item-check").first().isChecked(), true);

  const budget = page.locator(".budget-input").first();
  await budget.fill("321");
  assert.equal((await page.locator("#budget-total").textContent()).trim(), "321");
  await page.locator('[data-action="toggle-details"]').first().click();
  assert.equal(await page.locator(".item-details").first().isHidden(), true);
  await page.screenshot({ path: path.join(outputDir, "desktop.png"), fullPage: true });

  await page.setViewportSize({ width: 390, height: 844 });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  assert.ok(overflow <= 1, `mobile horizontal overflow: ${overflow}px`);
  await page.screenshot({ path: path.join(outputDir, "mobile.png"), fullPage: true });
  assert.deepEqual(pageErrors, []);
  await browser.close();
  process.stdout.write(`Browser smoke passed; screenshots: ${outputDir}\n`);
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
