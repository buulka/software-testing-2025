const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:8080",
    viewportWidth: 1366,
    viewportHeight: 768,

    setupNodeEvents(on, config) {
    },

    video: false,
    screenshotOnRunFailure: true
  }
});
