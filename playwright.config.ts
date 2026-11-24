import { defineConfig } from "@playwright/test";

const port = 1314;

export default defineConfig({
  testDir: "tests",
  fullyParallel: true,
  reporter: [["list"], ["html", { open: "never" }]],
  use: { baseURL: `http://localhost:${port}` },
  // hugo server rewrites baseURL to localhost, so every link stays on the test server.
  webServer: {
    command: `mise exec -- hugo server --port ${port} --disableLiveReload --renderToMemory`,
    url: `http://localhost:${port}/`,
    reuseExistingServer: false,
    timeout: 60_000,
  },
});
