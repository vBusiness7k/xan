import os, asyncio
from hexencore import stream, router
M = {"ASK":"Answer directly and tersely.","ARCHITECT":"Design the system, no code.",
 "AGENT":"Give runnable commands and code.","REVIEW":"Critique and find faults.",
 "ORCHESTRATOR":"Split into parallel workstreams with owners."}
async def main():
    log = stream.Stream("chat"); mode=os.environ.get("MODE","ASK"); model=os.environ.get("MODEL","V5.1 Advanced")
    log(f"[{mode}] {model} :: {os.environ['PROMPT'][:120]}")
    try: out = await router.ask(M.get(mode,"")+"\n\n"+os.environ["PROMPT"], model)
    except Exception as e: out = f"ERROR {e}"
    log("")
    for l in out.splitlines(): log(l)
    log.close()
asyncio.run(main())
