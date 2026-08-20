const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  workers: 1,
  retries: 0,
  reporter: 'line',
  use: {
    baseURL: 'http://127.0.0.1:43821',
    browserName: 'chromium',
    acceptDownloads: true,
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure'
  },
  webServer: {
    command: 'python3 -m http.server 43821',
    url: 'http://127.0.0.1:43821',
    reuseExistingServer: false,
    timeout: 10000
  }
});
