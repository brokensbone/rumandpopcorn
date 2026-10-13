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
