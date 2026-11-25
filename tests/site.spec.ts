import { expect, test, type Page } from "@playwright/test";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readdirSync, readFileSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";

// Every URL the Jekyll site published (live sitemap before the Hugo migration, plus the feed).
// These must keep working so old links and feed subscriptions don't break.
const legacyPaths = [
  "/",
  "/Blog/",
  "/CV/",
  "/feed.xml",
  "/blog_setup/",
  "/blog_paper_wall_model/",
  "/blog_cons_laws_ml/",
  "/blog_pandas_groupby_with_numpy/",
  "/blog_numba_slower_than_pandas/",
  "/blog_spark_args/",
  "/blog_49travel/",
  "/blog_langchain/",
  "/blog_python_decorators_style/",
  "/introduction-to-formal-methods-part-1/",
  "/introduction-to-formal-methods-part-2/",
  "/an-introduction-to-react-next-from-a-backend-engineer/",
  "/open-source-in-the-age-of-ai/",
];

const screenshotDir = process.env.SCREENSHOT_DIR ?? "test-results/screenshots";

// PaperMod links favicons the site doesn't ship; browsers request them on every page.
const ignoredRequest = (url: string) => /\/(favicon|apple-touch-icon|safari-pinned-tab)/.test(url);

async function sitemapPaths(request: Parameters<Parameters<typeof test>[1]>[0]["request"]) {
  const xml = await (await request.get("/sitemap.xml")).text();
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => new URL(m[1]).pathname);
}

function builtSitemapPaths() {
  const dir = mkdtempSync(path.join(os.tmpdir(), "hugo-sitemap-"));
  try {
    execFileSync("mise", ["exec", "--", "hugo", "--quiet", "--destination", dir]);
    const xml = readFileSync(path.join(dir, "sitemap.xml"), "utf8");
    return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => new URL(m[1]).pathname);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

function slug(p: string) {
  return p === "/" ? "home" : p.replace(/^\/|\/$/g, "").replace(/\W+/g, "_");
}

/** Opens a page and fails on HTTP errors, console errors, uncaught exceptions or failed requests. */
async function openClean(page: Page, p: string) {
  const problems: string[] = [];
  page.on("console", (m) => m.type() === "error" && problems.push(`console: ${m.text()}`));
  page.on("pageerror", (e) => problems.push(`pageerror: ${e.message}`));
  page.on("requestfailed", (r) => {
    if (!ignoredRequest(r.url())) problems.push(`failed: ${r.url()} ${r.failure()?.errorText}`);
  });
  page.on("response", (r) => {
    if (r.status() >= 400 && !ignoredRequest(r.url())) problems.push(`${r.status()}: ${r.url()}`);
  });
  const response = await page.goto(p, { waitUntil: "networkidle" });
  expect(response?.status(), `status of ${p}`).toBeLessThan(400);
  return problems;
}

test("every legacy Jekyll URL still resolves", async ({ request }) => {
  for (const p of legacyPaths) {
    const r = await request.get(p);
    expect(r.status(), p).toBe(200);
  }
});

test("sitemap covers every legacy page", async ({ request }) => {
  const paths = await sitemapPaths(request);
  for (const p of legacyPaths.filter((p) => p !== "/feed.xml")) expect(paths).toContain(p);
});

// One test per published page, read from a fresh build's sitemap so new pages are covered automatically.
for (const p of builtSitemapPaths()) {
  test(`page ${p} loads cleanly and its links and images resolve`, async ({ page, request }) => {
    const problems = await openClean(page, p);
    expect(problems, `problems on ${p}`).toEqual([]);

    await page.screenshot({ path: path.join(screenshotDir, `${slug(p)}.png`), fullPage: true });

    const origin = new URL(page.url()).origin;
    const targets = await page.evaluate(() => [
      ...[...document.querySelectorAll<HTMLAnchorElement>("a[href]")].map((a) => a.href),
      ...[...document.querySelectorAll<HTMLImageElement>("img[src]")].map((i) => i.src),
    ]);
    const internal = new Set(
      targets
        .map((t) => new URL(t))
        .filter((u) => u.origin === origin)
        .map((u) => ((u.hash = ""), u.toString())),
    );
    for (const url of internal) {
      expect((await request.get(url)).status(), `${url} linked from ${p}`).toBeLessThan(400);
    }
  });
}

test("header menu has Blog, Snacks, About, CV in order and each link works", async ({ page }) => {
  await page.goto("/");
  const items = page.locator("#menu a");
  await expect(items).toHaveText(["Blog", "Snacks", "About", "CV", "Search"]);
  for (const name of ["Blog", "Snacks", "About", "CV"]) {
    await page.goto("/");
    await page.locator("#menu a", { hasText: name }).click();
    await expect(page.locator("h1").first()).toBeVisible();
  }
});

test("home page shows the intro, social links and posts", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".home-info h1")).toHaveText("Vikram Singh");
  await expect(page.locator(".home-info a[href='/about/']")).toBeVisible();
  await expect(page.locator(".home-info .social-icons a")).toHaveCount(3);
  await expect(page.locator("article.post-entry").first()).toBeVisible();
});

test("about page has the full text and social links but no photo", async ({ page }) => {
  await page.goto("/about/");
  await expect(page.locator(".post-content")).toContainText("Max Planck Institute for Meteorology");
  await expect(page.locator(".post-content .social-icons a")).toHaveCount(3);
  await expect(page.locator(".post-content img")).toHaveCount(0);
});

test("math renders with KaTeX", async ({ page }) => {
  for (const p of ["/blog_paper_wall_model/", "/blog_cons_laws_ml/"]) {
    await page.goto(p);
    await expect(page.locator(".katex").first()).toBeVisible();
    await expect(page.locator(".post-content")).not.toContainText("$$");
  }
  // Inline math must stay inline: this post only has math inside sentences.
  await page.goto("/blog_paper_wall_model/");
  await expect(page.locator(".katex")).not.toHaveCount(0);
  await expect(page.locator(".katex-display")).toHaveCount(0);

  // This post has 7 display equations ($$ on their own lines) and the rest is inline.
  await page.goto("/blog_cons_laws_ml/");
  await expect(page.locator(".katex-display")).toHaveCount(7);
  await expect(page.locator("p > .katex").first()).toBeVisible();
  // Without KaTeX's stylesheet the math falls back to the body font and shows duplicated MathML text.
  await expect(page.locator(".katex").first()).toHaveCSS("font-family", /KaTeX_Main/);
});

test("math in a snack is styled on the snacks listing too", async ({ page }) => {
  await page.goto("/snacks/");
  const math = page.locator("article.snack .katex");
  test.skip((await math.count()) === 0, "no snack contains math");
  await expect(math.first()).toHaveCSS("font-family", /KaTeX_Main/);
});

test("mermaid diagrams render to SVG", async ({ page }) => {
  await page.goto("/an-introduction-to-react-next-from-a-backend-engineer/");
  // Mermaid renders diagrams one after another; allow for a slow machine.
  await expect(page.locator("pre.mermaid svg")).toHaveCount(3, { timeout: 20_000 });
});

test("cross-post link points at part 1", async ({ page }) => {
  await page.goto("/introduction-to-formal-methods-part-2/");
  await page.getByRole("link", { name: "Part 1", exact: true }).click();
  await expect(page).toHaveURL(/\/introduction-to-formal-methods-part-1\/$/);
});

test("Blog archive lists every post and no snacks", async ({ page, request }) => {
  await page.goto("/Blog/");
  const postPaths = legacyPaths.filter((p) => !["/", "/Blog/", "/CV/", "/feed.xml"].includes(p));
  for (const p of postPaths) await expect(page.locator(`.archive-entry a[href$='${p}']`)).toHaveCount(1);
  await expect(page.locator(".archive-entry a[href*='/snacks/']")).toHaveCount(0);
});

test("feeds are valid and separate posts from snacks", async ({ page, request }) => {
  const posts = await (await request.get("/feed.xml")).text();
  const snacks = await (await request.get("/snacks/feed.xml")).text();
  await page.goto("about:blank");
  const parse = (xml: string) =>
    page.evaluate((x) => {
      const doc = new DOMParser().parseFromString(x, "application/xml");
      return {
        error: doc.querySelector("parsererror")?.textContent ?? null,
        links: [...doc.querySelectorAll("item > link")].map((l) => new URL(l.textContent!).pathname),
      };
    }, xml);
  const p = await parse(posts);
  const s = await parse(snacks);
  expect(p.error).toBeNull();
  expect(s.error).toBeNull();
  expect(p.links).toContain("/open-source-in-the-age-of-ai/");
  expect(p.links.filter((l) => l.startsWith("/snacks/"))).toEqual([]);
  expect(s.links.every((l) => l.startsWith("/snacks/"))).toBe(true);
});

test("snacks listing shows each snack in full", async ({ page, request }) => {
  const snackPaths = (await sitemapPaths(request)).filter((p) => /^\/snacks\/.+/.test(p));
  const fullText: Record<string, string> = {};
  for (const p of snackPaths) {
    await page.goto(p);
    fullText[p] = (await page.locator(".post-content").innerText()).trim();
  }
  await page.goto("/snacks/");
  await expect(page.locator("h1")).toContainText("Snacks");
  await expect(page.locator("article.snack")).toHaveCount(snackPaths.length);
  for (const p of snackPaths) {
    const listed = page.locator("article.snack", { has: page.locator(`a[href$='${p}']`) });
    expect((await listed.locator(".post-content").innerText()).trim()).toBe(fullText[p]);
  }
  const dates = await page.locator("article.snack .post-meta span[title]").evaluateAll((spans) =>
    spans.map((s) => Date.parse(s.getAttribute("title") ?? "")),
  );
  expect(dates).toEqual([...dates].sort((a, b) => b - a));
});

// hugo.yaml takes the date from the filename first, so a differing front-matter date is silently ignored.
test("filename dates match front-matter dates", () => {
  for (const dir of ["content/posts", "content/snacks"]) {
    for (const name of readdirSync(dir)) {
      const fileDate = name.match(/^(\d{4}-\d{2}-\d{2})-/)?.[1];
      if (!fileDate) continue;
      const frontMatterDate = readFileSync(path.join(dir, name), "utf8").match(/^date:\s*(\d{4}-\d{2}-\d{2})/m)?.[1];
      expect(frontMatterDate ?? fileDate, `${dir}/${name}`).toBe(fileDate);
    }
  }
});

test("search finds posts", async ({ page }) => {
  await page.goto("/search/");
  await page.locator("#searchInput").fill("formal methods");
  await expect(page.locator("#searchResults li").first()).toContainText(/Formal Methods/i);
});
