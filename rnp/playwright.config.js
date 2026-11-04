import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  use: { baseURL: "http://127.0.0.1:1414" },
  webServer: {
    command: "python3 -m http.server 1414 --bind 127.0.0.1 --directory public",
    url: "http://127.0.0.1:1414",
  },
});
