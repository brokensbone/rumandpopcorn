# Build Information Page

This directory contains the configuration for generating a build information page at `/build/index.txt`.

## Usage

To build the site with the environment variable list:

```bash
# Generate the environment variable data file
./generate-env-data.sh

# Build the site
hugo
```

The build information page will be available at `public/build/index.txt`.

## How It Works

1. **`generate-env-data.sh`**: This script captures all environment variable names at build time and stores them in `data/envvars.json`.

2. **`layouts/_default/single.plaintext`**: The template reads the environment variable names from the data file and displays them in two sections:
   - **With values**: Shows `name=value` for important variables (configured in the template)
   - **Names only**: Shows just the names of all other available environment variables

3. **Dynamic discovery**: When new environment variables are added, they will automatically appear in the "names only" section after running `generate-env-data.sh`.

## Customization

To show values for additional environment variables, edit the `$detailedVars` list in `layouts/_default/single.plaintext`.
