import os, subprocess, tempfile, time, pathlib, threading
class Stream:
    def __init__(self, name):
        self.d = pathlib.Path(tempfile.mkdtemp()); self.f = self.d/f"{name}.log"; self.f.touch()
        url = f"https://x:{os.environ['STATE_PAT']}@github.com/{os.environ['GH_USER']}/xan.git"
        subprocess.run(["git","clone","-q","--depth","1","--branch","logs",url,str(self.d/"r")],capture_output=True)
        if not (self.d/"r").exists():
            subprocess.run(["git","clone","-q","--depth","1",url,str(self.d/"r")],capture_output=True)
            subprocess.run(["git","-C",str(self.d/"r"),"checkout","-q","-b","logs"],capture_output=True)
        self.r = self.d/"r"; (self.r/"latest").mkdir(exist_ok=True)
        self.stop = False; threading.Thread(target=self._loop,daemon=True).start()
    def __call__(self,m):
        with self.f.open("a") as fh: fh.write(f"{time.strftime('%H:%M:%S')} {m}\n")
    def _loop(self):
        while not self.stop:
            time.sleep(3)
            try:
                (self.r/"latest"/self.f.name).write_text(self.f.read_text())
                subprocess.run(["git","-C",str(self.r),"add","-A"],capture_output=True)
                subprocess.run(["git","-C",str(self.r),"commit","-qm","log"],capture_output=True)
                subprocess.run(["git","-C",str(self.r),"push","-q","origin","logs"],capture_output=True)
            except Exception: pass
    def close(self): self.stop = True; time.sleep(3.5)
