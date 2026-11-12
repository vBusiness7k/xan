import os, subprocess, argparse, time
from hexencore import state, stream
from hexencore.registry import REG
W = "/usr/share/seclists/Discovery/Web-Content/common.txt"
DEAD = time.time() + 5.5*3600
log = lambda m: None
def run(c,t=300):
    log(f"$ {c}")
    try:
        p = subprocess.run(c,shell=True,capture_output=True,text=True,timeout=t)
        if p.returncode: log(f"  ! rc={p.returncode} {(p.stderr or '')[:200]}")
        return (p.stdout or "")[:4000]
    except subprocess.TimeoutExpired: log("  ! timeout"); return ""
def shrink(o,cap=40):
    s,k = set(),[]
    for l in o.splitlines():
        l=l.strip()
        if l and l not in s:
            s.add(l); k.append(l)
            if len(k)>=cap: break
    return k
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--shard",type=int); ap.add_argument("--of",type=int)
    a=ap.parse_args(); global log; log=stream.Stream(str(a.shard-1))
    t=os.environ["TARGET"]; b=state.open_state(); hf=b/"hosts"/f"{t}.txt"
    log(f"shard {a.shard}/{a.of} -> {t}"); hs=[]
    for _ in range(30):
        if hf.exists() and hf.read_text().strip(): hs=hf.read_text().split(); break
        time.sleep(10)
    hs = hs or [t]; mine=[h for i,h in enumerate(hs) if i % a.of == a.shard-1]
    log(f"{len(hs)} hosts, {len(mine)} mine")
    for h in mine:
        if time.time()>DEAD: log("deadline"); break
        if not state.claim(t,h): log(f"skip {h}"); continue
        log(f"=== {h}")
        for ph,tag in (("RECON","subdomain"),("RECON","probe"),("ENUM","content"),("VULN","cve")):
            tl=REG.by_tag(tag,ph)[:1]
            if not tl: continue
            p=tl[0]; tgt=t if tag=="subdomain" else h
            rows=shrink(run(p.tmpl.format(target=tgt,wordlist=W),p.timeout))
            log(f"  {p.name}: {len(rows)}")
            if rows: state.checkpoint(t,[{"host":h,"phase":ph,"tool":p.name,"at":time.strftime("%FT%TZ"),"items":rows}])
            for r in rows[:6]: log(f"    {r[:150]}")
    log("done"); log.close()
if __name__=="__main__": main()
