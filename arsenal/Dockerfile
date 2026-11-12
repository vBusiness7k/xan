FROM --platform=linux/amd64 kalilinux/kali-rolling
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC LANG=C.UTF-8 PIP_BREAK_SYSTEM_PACKAGES=1 PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 CHROME_PATH=/usr/bin/chromium
COPY packages.list /tmp/packages.list
RUN apt-get update \
 && xargs -a /tmp/packages.list apt-get install -y --no-install-recommends \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /usr/share/doc/* /usr/share/man/* /tmp/packages.list
RUN pip3 install --no-cache-dir curl_cffi httpx playwright mitmproxy yt-dlp certipy-ad beautifulsoup4 lxml pyjwt dnspython requests-ntlm
RUN curl -fsSL -o /usr/local/bin/kerbrute https://github.com/ropnop/kerbrute/releases/latest/download/kerbrute_linux_amd64 \
 && chmod +x /usr/local/bin/kerbrute && kerbrute --help >/dev/null
RUN useradd -m -u 1000 xan && mkdir -p /work /out /loot && chown -R xan /work /out /loot
USER xan
WORKDIR /work
COPY --chown=xan tools.list /usr/local/share/tools.list
COPY --chown=xan entrypoint.sh /usr/local/bin/entrypoint
ENTRYPOINT ["entrypoint"]
CMD ["sleep","infinity"]
