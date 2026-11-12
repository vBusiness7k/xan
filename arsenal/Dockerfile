FROM --platform=linux/amd64 kalilinux/kali-rolling
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC LANG=C.UTF-8 PIP_BREAK_SYSTEM_PACKAGES=1 PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 CHROME_PATH=/usr/bin/chromium

RUN apt-get update && apt-get install -y --no-install-recommends \
      kali-linux-headless metasploit-framework \
      seclists wordlists \
      rustscan gobuster feroxbuster wfuzz dirb nikto wpscan whatweb \
      netexec impacket-scripts responder bettercap \
      enum4linux smbclient ldap-utils snmp \
      chisel ligolo-ng proxychains4 tor \
      kerbrute evil-winrm certipy bloodhound.py \
      ssh-audit testssl.sh sslscan \
      theharvester dnsrecon fierce recon-ng \
      chromium ffmpeg libimage-exiftool-perl \
      jq curl git python3-pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /usr/share/doc/* /usr/share/man/*

RUN pip3 install --no-cache-dir \
      curl_cffi httpx playwright mitmproxy yt-dlp \
      beautifulsoup4 lxml pyjwt dnspython requests-ntlm

RUN useradd -m -u 1000 xan && mkdir -p /work /out /loot && chown -R xan /work /out /loot
USER xan
WORKDIR /work
COPY --chown=xan tools.list /usr/local/share/tools.list
COPY --chown=xan entrypoint.sh /usr/local/bin/entrypoint
ENTRYPOINT ["entrypoint"]
CMD ["sleep", "infinity"]
