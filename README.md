# Rum and Popcorn
This repo contains the files used to build the website rumandpopcorn.com

It contains both the content of the site and the infrastructure config that runs it.

## Features
- **Search**: The site uses [Pagefind](https://pagefind.app/) for static site search. The search index is built automatically during the site build process and provides fast, client-side search functionality.

## Hugo Version Management
The Hugo version used across all build environments (Docker, CI/CD, and Cloudflare Pages) is managed centrally via the `.hugo-version` file in the repository root. To update the Hugo version:
1. Edit `.hugo-version` and change the version number (e.g., `0.147.6` to `0.148.0`)
2. Test the build locally using Docker
3. Commit and push the change - CI will automatically use the new version

## Running locally - devcontainer
Launch a development container - the config for which is laid out in the `.devcontainer` directory.

From within this, hop into the `rnp` directory and simply run:
```
hugo serve
```
This runs a development server, available on 127.0.0.1:1313

Note: The development server doesn't include the Pagefind search index. To test search functionality locally, build the site with:
```
hugo --gc --minify
npx -y pagefind --site public
```
Then serve the `public` directory with a static file server.

## Running locally - Docker

TODO - it'd be nice to have a 'prod' build in a local Dockerfile

## Running in AWS
Hop into the `infra` directory.

Create a virtual env if there isn't one already:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Configure your AWS cli**. 

Run `pulumi up` to get it running in AWS Amplify. This does not set up any DNS records, but should print the amplify auto generated one.