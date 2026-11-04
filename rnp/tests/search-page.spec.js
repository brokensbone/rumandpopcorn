import { expect, test } from "@playwright/test";

for (const viewport of [
  { width: 1280, height: 900 },
  { width: 375, height: 812 },
]) {
  test(`search works at ${viewport.width}px`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await page.goto("/");
    if (viewport.width < 900)
      await page.locator(".mobile-menu summary").click();
    await page.getByRole("link", { name: "Search", exact: true }).click();
    await expect(page).toHaveURL(/\/search\/$/);
    for (const link of await page
      .locator('.utility-list a[href="/search/"]')
      .all()) {
      await expect(link).toHaveAttribute("aria-current", "page");
    }
    const input = page.getByRole("searchbox", { name: "Search the site" });
    await input.fill("Blackcurrants");
    await input.press("Enter");
    const link = page
      .locator("#search-results")
      .getByRole("link", { name: "Blackcurrants!", exact: true });
    await expect(link).toBeVisible();
    await expect(link).toHaveAttribute("href", "/2021/03/blackcurrants/");
    await expect(page.locator("#search-results mark").first()).toBeVisible();
    await expect(page).toHaveURL(/\?q=Blackcurrants$/);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBeTruthy();
    await link.click();
    await expect(
      page.getByRole("heading", { level: 1, name: "Blackcurrants!" }),
    ).toBeVisible();
  });
}

test("supports body matches, walks, no results, clear and direct query links", async ({
  page,
}) => {
  await page.goto("/search/?q=gooseberries");
  await expect(
    page
      .locator("#search-results")
      .getByRole("link", { name: "Blackcurrants!", exact: true }),
  ).toBeVisible();
  const input = page.getByRole("searchbox");
  await input.fill("Hartwith");
  await expect(page.locator("#search-results a").first()).toHaveAttribute(
    "href",
    "/walks/brimham-hartwith/",
  );
  await input.fill("qzxv");
  await expect(page.getByRole("status")).toHaveText(
    "No results found. Try different words.",
  );
  await expect(page.locator("#search-results li")).toHaveCount(0);
  await input.fill("Blackcurrants Hartwith");
  await expect(page.getByRole("status")).toHaveText(
    "No results found. Try different words.",
  );
  await page.getByRole("button", { name: "Clear", exact: true }).click();
  await expect(input).toBeFocused();
  await expect(input).toHaveValue("");
  await expect(page).toHaveURL(/\/search\/$/);
  await expect(page.getByRole("status")).toHaveText(
    "Enter a word or phrase to search.",
  );
});

test("loads more results and moves keyboard focus to the new results", async ({
  page,
}) => {
  await page.goto("/search/?q=film");
  const items = page.locator("#search-results li");
  await expect(items).toHaveCount(10);
  await page.getByRole("button", { name: "Show more results" }).click();
  await expect(items).toHaveCount(20);
  await expect(items.nth(10).getByRole("link")).toBeFocused();
});

test("ignores a slow search after the query changes or clears", async ({
  page,
}) => {
  await page.route("**/pagefind/pagefind.js", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 600));
    await route.continue();
  });
  await page.goto("/search/?q=film");
  await expect(page.getByRole("status")).toHaveText("Searching…");
  await page.getByRole("searchbox").fill("Hartwith");
  await expect(page.locator("#search-results a").first()).toHaveAttribute(
    "href",
    "/walks/brimham-hartwith/",
  );
  await page.getByRole("searchbox").fill("film");
  await page.getByRole("button", { name: "Clear", exact: true }).click();
  await expect(page.getByRole("status")).toHaveText(
    "Enter a word or phrase to search.",
  );
  await expect(page.locator("#search-results li")).toHaveCount(0);
});

test("shows an index load error and recovers through reload", async ({
  page,
}) => {
  await page.route("**/pagefind/**", (route) => route.abort());
  await page.goto("/search/?q=Blackcurrants");
  await expect(page.getByRole("status")).toHaveText(
    "Search could not load. Reload search to try again.",
  );
  await page.unroute("**/pagefind/**");
  await page.getByRole("button", { name: "Reload search" }).click();
  await expect(
    page
      .locator("#search-results")
      .getByRole("link", { name: "Blackcurrants!", exact: true }),
  ).toBeVisible();
});

test("keeps search out of feeds and loads its assets only on the search page", async ({
  page,
  request,
}) => {
  const searchRequests = [];
  page.on("request", (request) => {
    if (/\/pagefind\/|\/js\/search\.|\/css\/search\./.test(request.url()))
      searchRequests.push(request.url());
  });
  await page.goto("/");
  await expect(page.locator('a[href="/search/"]')).toHaveCount(2);
  expect(searchRequests).toHaveLength(0);
  for (const path of ["/sitemap.xml", "/feed.xml"]) {
    const response = await request.get(path);
    expect(response.ok()).toBeTruthy();
    expect(await response.text()).not.toMatch(
      /(?:href=["']|<loc>|<link>)[^<"']*\/search\//,
    );
  }
  await page.goto("/search/");
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute(
    "content",
    "noindex, follow",
  );
  expect(
    await page.locator("main").getAttribute("data-pagefind-body"),
  ).toBeNull();
});

test("explains the JavaScript requirement when JavaScript is disabled", async ({
  browser,
}) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto("http://127.0.0.1:1414/search/");
  await expect(
    page.getByText("Search needs JavaScript.", { exact: false }),
  ).toBeVisible();
  await expect(page.getByRole("searchbox")).toBeDisabled();
  await context.close();
});
