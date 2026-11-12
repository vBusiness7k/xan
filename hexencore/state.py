import os, json, subprocess, tempfile, pathlib
BASE = pathlib.Path(tempfile.mkdtemp()); REPO = "xan-state"
def _g(*a): return subprocess.run(["git",*a], cwd=BASE, capture_output=True, text=True)
def open_state():
    _g("clone","-q",f"https://x:{os.environ['STATE_PAT']}@github.com/{os.environ['GH_USER']}/{REPO}.git",".")
    return BASE
def claim(t,h):
    f = BASE/"claims"/f"{t}__{h}"
    if f.exists(): return False
    f.parent.mkdir(parents=True, exist_ok=True); f.write_text("1")
    _g("add","-A"); _g("commit","-qm",f"claim {h}")
    return _g("push","-q","origin","HEAD").returncode == 0
def checkpoint(t,rows):
    p = BASE/"findings"/f"{t}.jsonl"; p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as fh:
        for r in rows: fh.write(json.dumps(r)+"\n")
    _g("add","-A"); _g("commit","-qm","ckpt"); _g("push","-q","origin","HEAD")
