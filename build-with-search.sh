#!/bin/bash
# Script to build Hugo site with Pagefind search index
# This is useful for local development to test the search functionality

set -e

echo "Building Hugo site..."
cd /website
hugo

echo "Building Pagefind search index..."
npx -y pagefind --site public

echo "Build complete! Search index created in public/pagefind/"
echo "You can now run 'hugo serve' to test the site with search functionality"
