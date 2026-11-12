import os, asyncio, httpx
MODELS = {"V5.1 Advanced":"deepseek/deepseek-r1-0528:free","Coder":"qwen/qwen3-coder:free",
 "V4":"nousresearch/hermes-3-llama-3.1-405b:free","Vision":"meta-llama/llama-3.2-90b-vision-instruct:free",
 "Reasoner":"deepseek/deepseek-r1-0528:free"}
REF = ("i cannot","unfortunately","as an ai","i'm unable")
async def ask(prompt, model="V5.1 Advanced", tries=3):
    for m in [MODELS.get(model, MODELS["V5.1 Advanced"])] + list(MODELS.values()):
        for _ in range(tries):
            async with httpx.AsyncClient(timeout=180) as c:
                r = await c.post("https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {os.environ['OPENROUTER_KEY']}"},
                    json={"model": m, "temperature": 0.6, "messages":[{"role":"user","content":prompt}]})
            if r.status_code == 429: await asyncio.sleep(4); continue
            if r.status_code != 200: break
            t = r.json()["choices"][0]["message"]["content"]
            if any(x in t[:200].lower() for x in REF): break
            return t
    raise RuntimeError("all free models refused or throttled")
