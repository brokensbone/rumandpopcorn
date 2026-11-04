import { expect, test } from "@playwright/test";

async function search(page, term) {
  return page.evaluate(async (term) => {
    const pagefind = await import("/pagefind/pagefind.js");
    const { results } = await pagefind.search(term);
    return Promise.all(results.map((result) => result.data()));
  }, term);
}

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test("searches the built index for post titles and body text", async ({
  page,
}) => {
  const titleResults = await search(page, "Blackcurrants");
  const result = titleResults.find((result) =>
    result.url.endsWith("/2021/03/blackcurrants/"),
  );
  expect(result).toBeDefined();
  expect(result.meta.title).toBe("Blackcurrants!");
  expect(result.excerpt).toBeTruthy();
  expect((await page.request.get(result.url)).ok()).toBeTruthy();

  const bodyResults = await search(page, "gooseberries");
  expect(
    bodyResults.some((bodyResult) => bodyResult.url === result.url),
  ).toBeTruthy();
});

test("includes walks rendered with their own layout", async ({ page }) => {
  const results = await search(page, "Hartwith");
  expect(
    results.some((result) => result.url.endsWith("/walks/brimham-hartwith/")),
  ).toBeTruthy();
});

test("unknown single words return no unrelated results", async ({ page }) => {
  test.fail(
    true,
    "Pagefind 1.5.2 returns an unrelated result; resolve before public search.",
  );
  expect(await search(page, "qzxv")).toEqual([]);
});

test("excludes navigation, archives and generated utility content", async ({
  page,
}) => {
  expect(await search(page, "Skip to content")).toHaveLength(0);
  expect(await search(page, "Blackcurrants Hartwith")).toEqual([]);
  const results = await search(page, null);
  expect(results.length).toBeGreaterThan(100);
  const urls = results.map(
    (result) => new URL(result.url, "http://localhost").pathname,
  );
  expect(new Set(urls).size).toBe(urls.length);
  expect(urls).not.toContain("/");
  expect(urls).not.toContain("/posts/");
  expect(urls).not.toContain("/walks/");
  expect(urls).not.toContain("/build/");
  expect(urls).not.toContain("/feeds/");
  expect(urls).not.toContain("/search/");
  expect(urls).not.toContain("/404.html");
  expect(urls.some((url) => /^\/(categories|tags)\//.test(url))).toBeFalsy();
  expect(urls.some((url) => /\/page\/\d+\//.test(url))).toBeFalsy();
});
