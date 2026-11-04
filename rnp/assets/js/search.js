const root = document.querySelector("#site-search");
document.querySelector("#search-js-message").hidden = true;
const form = root.querySelector("form");
const input = root.querySelector("input");
const clear = root.querySelector("#search-clear");
const status = root.querySelector("#search-status");
const list = root.querySelector("#search-results");
const more = root.querySelector("#search-more");
const retry = root.querySelector("#search-retry");
let index;
let revision = 0;
let timer;
let results = [];
let shown = 0;
const pageSize = 10;

for (const control of form.elements) control.disabled = false;

function showMore(moveFocus = false) {
  const firstNew = list.children.length;
  const next = results.slice(shown, shown + pageSize);
  for (const result of next) {
    const item = document.createElement("li");
    const heading = document.createElement("h2");
    const link = document.createElement("a");
    link.href = result.url;
    link.textContent = result.meta.title || result.url;
    heading.append(link);
    const excerpt = document.createElement("p");
    // Pagefind escapes content before inserting its own <mark> tags.
    excerpt.innerHTML = result.excerpt;
    item.append(heading, excerpt);
    list.append(item);
  }
  shown += next.length;
  more.hidden = shown >= results.length;
  status.textContent = results.length
    ? `Showing ${shown} of ${results.length} result${results.length === 1 ? "" : "s"}.`
    : "No results found.";
  if (moveFocus) list.children[firstNew]?.querySelector("a").focus();
}

async function runSearch(term, current) {
  try {
    index ||= import(root.dataset.indexModule);
    const pagefind = await index;
    const response = await pagefind.search(term);
    if (current !== revision) return;
    const matches = await Promise.all(
      response.results.map((result) => result.data()),
    );
    if (current !== revision) return;
    // Pagefind can return an unrelated fragment with no matches for unknown words.
    // All indexed titles are also in the body, so genuine matches have locations.
    results = matches.filter((result) => result.locations?.length);
    shown = 0;
    showMore();
  } catch {
    if (current !== revision) return;
    status.textContent = "Search could not load. Reload search to try again.";
    retry.hidden = false;
  } finally {
    if (current === revision) list.removeAttribute("aria-busy");
  }
}

function update(immediate = false, writeUrl = true) {
  const current = ++revision;
  clearTimeout(timer);
  const term = input.value.trim();
  clear.hidden = input.value.length === 0;
  list.replaceChildren();
  list.removeAttribute("aria-busy");
  more.hidden = true;
  retry.hidden = true;
  results = [];
  shown = 0;
  if (writeUrl) {
    const url = new URL(location.href);
    if (term) url.searchParams.set("q", term);
    else url.searchParams.delete("q");
    history.replaceState(null, "", url);
  }
  if (!term) {
    status.textContent = "";
    return;
  }
  status.textContent = "Searching…";
  list.setAttribute("aria-busy", "true");
  timer = setTimeout(() => runSearch(term, current), immediate ? 0 : 200);
}

input.addEventListener("input", () => update());
form.addEventListener("submit", (event) => {
  event.preventDefault();
  update(true);
});
clear.addEventListener("click", () => {
  input.value = "";
  update(true);
  input.focus();
});
more.addEventListener("click", () => showMore(true));
retry.addEventListener("click", () => location.reload());
window.addEventListener("popstate", () => {
  input.value = new URL(location.href).searchParams.get("q") || "";
  update(true, false);
});
input.value = new URL(location.href).searchParams.get("q") || "";
update(true, false);
