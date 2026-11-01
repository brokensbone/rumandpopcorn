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
Books, Films, Food & Drink, Gardening, Miscellaneous, Music and Tech. Music-library
setup articles are Tech; the original test post is Miscellaneous. Book-list pages
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
hugo && npx -y pagefind --site public
```

Pages publishes the resulting `public/` directory. The hosting configuration, custom domains, DNS records and uptime monitoring are defined in `infra/`.

GitHub Actions builds the Hugo site and checks key pages on pull requests. A separate Pulumi workflow previews infrastructure changes on pull requests and applies them after merging to `main` when `infra/`, `.hugo-version` or `.go-version` changes.

## Hugo and Go versions

`.hugo-version` defines the Hugo version used by Docker, GitHub Actions and Cloudflare Pages. `.go-version` defines the Go version used by GitHub Actions and Cloudflare Pages; the Docker build command above passes it explicitly as a build argument.

To update either version:

1. Edit the corresponding version file.
2. Rebuild the Docker image with the command above, then run the local static build.
3. Open a pull request and check CI before merging. The Pulumi deployment updates the Cloudflare Pages build environment after merge.
