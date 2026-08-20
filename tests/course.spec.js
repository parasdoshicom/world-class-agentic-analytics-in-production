const { test, expect } = require('@playwright/test');

test('master course controls and downloads work end to end', async ({ page, context }) => {
  const consoleErrors = [];
  page.on('console', message => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });
  await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  await page.goto('/');

  await expect(page).toHaveTitle(/World-Class Agentic Analytics/);
  await expect(page.locator('details.reference-answer')).toHaveCount(2);
  await expect(page.locator('details.reference-answer[open]')).toHaveCount(0);

  await page.getByRole('button', { name: 'Expand walkthroughs' }).click();
  await expect(page.locator('details.workshop-note:not([open])')).toHaveCount(0);
  await expect(page.locator('details.reference-answer[open]')).toHaveCount(0);

  await page.getByRole('button', { name: 'Open workbook' }).click();
  await expect(page.locator('.artifact').first()).toBeVisible();
  await expect(page.getByRole('button', { name: 'Workbook open' })).toHaveAttribute('aria-pressed', 'true');
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThan(0);

  const copyButtons = page.locator('[data-copy-target], [data-copy-container]');
  const copyCount = await copyButtons.count();
  expect(copyCount).toBe(17);
  for (let index = 0; index < copyCount; index += 1) {
    const button = copyButtons.nth(index);
    const expectedCopy = await button.evaluate(element => {
      if (element.dataset.copyTarget) {
        return document.getElementById(element.dataset.copyTarget).textContent.trim();
      }
      return element.parentElement.querySelector('pre').textContent.trim();
    });
    await button.click();
    await expect.poll(() => page.evaluate(() => navigator.clipboard.readText())).toBe(expectedCopy);
  }

  const firstTimer = page.locator('.timer').first();
  await expect(firstTimer.locator('.timer-readout')).toHaveText('20:00');
  await firstTimer.getByRole('button', { name: 'Start' }).click();
  await expect(firstTimer.locator('.timer-readout')).toHaveText('19:59', { timeout: 2500 });
  await firstTimer.getByRole('button', { name: 'Reset' }).click();
  await expect(firstTimer.locator('.timer-readout')).toHaveText('20:00');

  const downloads = [
    ['Download the lab kit', 'agentic-analytics-workshop-lab.zip'],
    ['Download calculation CSV', 'funnel_segments.csv'],
    ['Download benchmark CSV', 'wbr_benchmark.csv']
  ];
  for (const [label, filename] of downloads) {
    const event = page.waitForEvent('download');
    await page.getByRole('link', { name: label, exact: true }).click();
    const download = await event;
    expect(download.suggestedFilename()).toBe(filename);
  }

  const exportEvent = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Export starter pack', exact: true }).click();
  const exported = await exportEvent;
  expect(exported.suggestedFilename()).toBe('agentic-analytics-production-starter-pack.md');

  expect(consoleErrors).toEqual([]);
});

test('setup preview navigates on the first click', async ({ page }) => {
  await page.goto('/#lab-kit');
  await page.getByRole('link', { name: 'Preview the data', exact: true }).click();
  await expect(page).toHaveURL(/\/examples\/workshop-data\.html$/);
  await expect(page.locator('#calculation-table tbody tr')).toHaveCount(16);
});

test('data preview loads both CSVs without browser errors', async ({ page }) => {
  const consoleErrors = [];
  page.on('console', message => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });
  await page.goto('/examples/workshop-data.html');
  await expect(page.locator('#calculation-table tbody tr')).toHaveCount(16);
  await expect(page.locator('#benchmark-table tbody tr')).toHaveCount(3);
  await expect(page.getByText('16 data rows loaded.')).toBeVisible();
  await expect(page.getByText('3 data rows loaded.')).toBeVisible();
  expect(consoleErrors).toEqual([]);
});

test('master course has no horizontal overflow on a student phone', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  const dimensions = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth
  }));
  expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.clientWidth);
  await expect(page.getByRole('link', { name: 'Skip to course content' })).toBeAttached();
});
