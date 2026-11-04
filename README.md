# Rum and Popcorn

Source for [rumandpopcorn.com](https://www.rumandpopcorn.com/), built with Hugo and hosted on Cloudflare Pages.

## Repository layout

- `rnp/`: site content, Hugo configuration, assets and the Chocos theme.
- `Dockerfile` and `docker-compose.yml`: local Hugo builds and development server.
- `infra/`: Pulumi configuration for Cloudflare Pages, DNS and StatusCake monitoring.
- `.github/workflows/`: pull-request checks and Pulumi preview/deployment workflows.

## Local development with Docker

Install Docker with the Compose plugin, then run these commands from the repository root:

```sh
docker compose build --build-arg GO_VERSION="$(cat .go-version)"
docker compose up
```

Open <http://localhost:1313>. Compose mounts `rnp/` into the container at `/website`; Hugo watches for edits and refreshes the site. Stop the server with Ctrl+C, and remove the container with `docker compose down`.

To generate the static site without starting the server:

```sh
docker compose run --rm website hugo --source /website --gc --minify
```

The generated files are written to `rnp/public/` on the host. Treat `rnp/public/` and `rnp/resources/` as build output; do not commit them.

The Docker image supplies Hugo Extended and Go. It does not include the Node.js tooling used by Cloudflare Pages to generate the Pagefind search index.

## Building and checking search

With Hugo Extended (`.hugo-version`) and Node.js (`.node-version`) installed,
run the same build as Cloudflare Pages from the repository root:

```sh
cd rnp
npm ci
npm run build
npx playwright install --with-deps chromium
npm run test:search
```

The build cleans Hugo's destination, generates the production site, then runs
the locked Pagefind version over `public/`. Search assets are generated in
`rnp/public/pagefind/`; neither those assets nor `node_modules/` belong in Git.
The browser checks serve that static output and query the actual search index,
including post body text and walks, while checking that archive pages and site
navigation are excluded. Python 3 supplies the test server.

Only individual HTML pages opt into indexing through `data-pagefind-body` on
their main content. Set `search: false` in front matter to exclude a utility
page (as Feeds does). Home, taxonomy, pagination and section listings, redirects,
and the plaintext Build Information output are excluded. Drafts and future posts
follow Hugo's normal production exclusions. Search assets load only on the
dedicated search page; the public navigation entry will follow separately.

The raw Pagefind API has an expected failure for an unknown single-word query
(`qzxv`) returning an unrelated result with no match locations in Pagefind.
The search page suppresses results without match locations; all indexed titles
are also in page content, so genuine matches retain their locations. Browser
tests verify the visible no-results behavior. Keep the raw API regression test
until an upstream version resolves it, then remove that expected failure and
reassess the workaround. The build pins Pagefind 1.6.0. Its published Linux
binaries currently crash with an illegal instruction on this development VM;
the production index build is verified in GitHub Actions and Cloudflare, and
the search page is checked against the deployed preview.

To inspect the built site, use `python3 -m http.server --directory public 1414`
from `rnp/`. `hugo server` alone does not generate or serve the Pagefind index.

### Unlisted search page (stage 2)

Open `/search/` on the built site or a Cloudflare preview. The page is rendered
but excluded from Hugo's page collections with `build.list: never`, has no menu
entry or category, is omitted from feeds and the sitemap, opts out of Pagefind,
and includes `noindex, follow`. It is unlisted, not access-controlled: anyone
with the URL can use it. Search is entirely local to the static site.

Queries are debounced and can also be submitted with Enter or the Search
button. The `q` parameter makes test queries shareable, for example
`/search/?q=Blackcurrants`. Clear cancels pending results and returns focus to
the input. Results appear ten at a time with a Show more results button.
An index-loading failure offers a reload; without JavaScript the page explains
the requirement. Colours follow the site's light/dark preference.

Before adding public navigation, check the preview on desktop and mobile:

- Search for `Blackcurrants` (title), `gooseberries` (body) and `Hartwith` (walk).
- Follow result links, including an older Chopping Mall `.html` URL.
- Search for `qzxv`, incompatible words, punctuation and an empty query.
- Try a broad query such as `film`, load more, and use keyboard navigation.
- Change and clear queries while results load; reload a shared query URL.
- Check light/dark modes and a narrow viewport, and simulate a failed index
  request to check the reload action.

CI covers the main search flows and verifies that the page stays unlisted.

## Image loading

Markdown images use a custom render hook that retains Hugo's page-bundle and
global-resource URL resolution. It adds intrinsic dimensions for local raster
images, asynchronous decoding, and native lazy loading at low priority.
`post-content.html` promotes the leading image in the first listing entry or
individual post to eager/high priority. Keep that promotion outside the render
hook because Hugo caches each post's rendered content across listings.

Browsers may prefetch lazy images near the viewport; distant images wait until
the reader approaches them. This works without JavaScript. The RSS-specific
render hook retains the original embedded image markup in feeds.

## Content categories

Categories are the subject grouping used across the content tree. Keep files in
their existing locations: categories do not change the configured post permalinks.
Sections remain Hugo's directory structure and existing archive URLs.

Homogeneous folders define a category once in their `_index.md`, inherited by
descendant content pages (including nested folders):

```yaml
cascade:
  params:
    categories: ["Films"]
  target:
    kind: page
```

The Films, Chopping Mall, Walks, Lists and Wine folders use this inheritance.
Wine belongs to Food & Drink. Chopping Mall retains its named archive category.
The page-kind target keeps section listing pages out of category counts. Existing
date cascades within Films continue to apply independently.

The mixed `posts/` folder has no default category: assign exactly one subject to
each post in front matter, including draft templates:

```yaml
categories: ["Films"]
```

For TOML front matter, use `categories = ["Films"]`. Subjects currently include
Books, Films, Food & Drink, Gardening, Music and Tech. Music-library
setup articles and the original test post are Tech. Book-list pages
under `lists/` remain Lists. About, Feeds and Build Information are utility pages
and intentionally have no category. Tags are independent and are not changed.

For a URL-preservation audit, capture `hugo list all` and a clean production build
on both revisions, then run:

```sh
python3 tests/check_content_urls.py before.csv after.csv before-public after-public
```

This checks draft/future source URLs too, and verifies existing output paths
(including section archives, pagination and redirects) still exist. New category
archive URLs are expected. No files, slugs, dates or permalink rules need moving
or changing to assign categories.

Existing RSS subscriptions retain their section-based membership: for example,
`posts/feed.xml` still contains Posts, and `films/feed.xml` still contains the
Films section. Category feeds such as `categories/films/feed.xml` are additional
subject-based subscriptions. The previously empty `categories/feed.xml` lists
the category terms themselves. The configured 20-item RSS limit is unchanged.

## Formatting

With uv and Node.js/npm installed, run these commands from the repository root:

```sh
uvx --from ruff==0.17.2 ruff format infra
npx --yes prettier@3.9.10 --write "rnp/assets/**/*.{css,js}" "rnp/themes/chocos/assets/{css,js}/**/*.{css,js}"
```

Run the same checks as CI:

```sh
uvx --from ruff==0.17.2 ruff format --check infra
npx --yes prettier@3.9.10 --check "rnp/assets/**/*.{css,js}" "rnp/themes/chocos/assets/{css,js}/**/*.{css,js}"
```

Ruff formats infrastructure Python; Prettier formats authored CSS and JavaScript
in the site and Chocos theme assets. Vendor files, minified files and generated
output are excluded. Hugo Go templates are outside this check because they need
additional formatter support. Keep the tool versions here and in
`.github/workflows/format.yml` in sync when upgrading.

## Production hosting and deployment

Cloudflare Pages builds the site from this GitHub repository. Pushes to `main` deploy production; pull requests get preview deployments. The build runs from `rnp/`:

```sh
npm ci && npm run build
```

Pages publishes the resulting `public/` directory. The hosting configuration, custom domains, DNS records and uptime monitoring are defined in `infra/`.

GitHub Actions builds Hugo and Pagefind and checks search in Chromium on pull requests. A separate Pulumi workflow previews infrastructure changes on pull requests and applies them after merging to `main` when `infra/`, `.hugo-version`, `.go-version` or `.node-version` changes.

`.node-version` selects Node.js for CI and both Cloudflare preview and production
builds. Both environments use the same locked dependencies and build command.
Cloudflare's build settings are managed by Pulumi: a PR previews their changes;
they take effect after merge and the Pulumi deployment. A branch preview made
before then still uses the existing unpinned build command. Rebuild that preview
after the build settings have been applied to verify the deployed configuration.

## Hugo and Go versions

`.hugo-version` defines the Hugo version used by Docker, GitHub Actions and Cloudflare Pages. `.go-version` defines the Go version used by GitHub Actions and Cloudflare Pages; the Docker build command above passes it explicitly as a build argument.

To update either version:

1. Edit the corresponding version file.
2. Rebuild the Docker image with the command above, then run the local static build.
3. Open a pull request and check CI before merging. The Pulumi deployment updates the Cloudflare Pages build environment after merge.
