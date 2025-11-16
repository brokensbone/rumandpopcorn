# Rum and Popcorn
This repo contains the files used to build the website rumandpopcorn.com

It contains both the content of the site and the infrastructure config that runs it.

## Running locally - devcontainer
Launch a development container - the config for which is laid out in the `.devcontainer` directory.

From within this, hop into the `rnp` directory and simply run:
```
hugo serve
```
This runs a development server, available on 127.0.0.1:1313

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