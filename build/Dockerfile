FROM mcr.microsoft.com/devcontainers/jekyll:1-bullseye

# Dir for build tools
RUN mkdir build
COPY container-build.sh /build/

# Dir for site code - needs mounting so we get the output
RUN mkdir workspace
WORKDIR workspace
CMD ["/build/container-build.sh"]
