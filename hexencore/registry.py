import shutil
from dataclasses import dataclass
@dataclass
class Tool: name:str; phase:str; tags:list; tmpl:str; timeout:int=300
class Registry:
    def __init__(self): self._t={}
    def add(self,t): self._t[t.name]=t
    def by_tag(self,tag,phase=None):
        return [t for t in self._t.values() if tag in t.tags
                and (phase is None or t.phase==phase) and shutil.which(t.tmpl.split()[0])]
REG = Registry()
REG.add(Tool("subfinder","RECON",["subdomain"],"subfinder -d {target} -silent",240))
REG.add(Tool("httpx","RECON",["probe"],"httpx -u {target} -title -tech-detect -silent",120))
REG.add(Tool("ffuf","ENUM",["content"],"ffuf -u {target}/FUZZ -w {wordlist} -mc 200,301,302,403 -s",300))
REG.add(Tool("nuclei","VULN",["cve"],"nuclei -u {target} -severity critical,high -silent -jsonl",900))
REG.add(Tool("nmap","ENUM",["port"],"nmap -sV -T4 --top-ports 200 {target}",300))
