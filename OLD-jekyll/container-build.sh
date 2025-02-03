#!/bin/bash

echo "Running container build"
bundle install
bundle exec jekyll build
chown -R 1000:1000 _site
echo "Finished container build"
