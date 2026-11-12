import hashlib, time
class Chain:
    def __init__(self, target, scope):
        self.target, self.scope = target, scope
        self.steps, self.started, self.seen, self.stall = 0, time.time(), set(), 0
    def observe(self, fp):
        k = hashlib.sha1(fp.encode()).hexdigest()
        self.stall = self.stall+1 if k in self.seen else 0; self.seen.add(k)
    @property
    def exhausted(self): return self.steps > 300 or time.time()-self.started > 7200 or self.stall >= 6
