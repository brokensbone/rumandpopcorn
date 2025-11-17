# Go version is read from .go-version file or can be overridden via build arg
ARG GO_VERSION=1.24

FROM golang:${GO_VERSION}-trixie

RUN apt-get update && apt-get install -y ca-certificates openssl git curl
RUN rm -rf /var/lib/apt/lists/*

# Download Hugo
# VARIANT can be either 'hugo' for the standard version or 'hugo_extended' for the extended version.
ARG VARIANT=hugo_extended
# VERSION is read from .hugo-version file
COPY .hugo-version /tmp/.hugo-version
RUN VERSION=$(cat /tmp/.hugo-version | tr -d '\n') && \
	ARCH=$(uname -m) && \
	if [ "$ARCH" = "aarch64" ]; then ARCH="ARM64"; elif [ "$ARCH" = "x86_64" ]; then ARCH="64bit"; else echo "Unsupported architecture"; exit 1; fi && \
	curl -L -o ${VERSION}.tar.gz https://github.com/gohugoio/hugo/releases/download/v${VERSION}/${VARIANT}_${VERSION}_Linux-${ARCH}.tar.gz && \
	tar xf ${VERSION}.tar.gz && \
	mv hugo /usr/bin/hugo

# Hugo dev server port
EXPOSE 1313

# [Optional] Uncomment this section to install additional OS packages you may want.
#
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment if you want to install more global node packages
# RUN sudo -u node npm install -g <your-package-list-here>


