#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera a capa editorial do artigo 'Deusas de pedra' usando a API de imagens da OpenAI.
Sintetiza o conteúdo do artigo + título, no estilo da marca (vinho/dourado/creme)."""
import os, re, json, base64, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "capa-deusas-de-pedra.png")

def load_key():
    for p in [os.path.join(ROOT, "..", ".env"), os.path.join(ROOT, "..", "Silva.ia", "Soul Anchored", ".env")]:
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                m = re.match(r"\s*OPENAI_API_KEY\s*=\s*[\"']?([^\"'\n]+)", line)
                if m:
                    return m.group(1).strip()
    raise SystemExit("OPENAI_API_KEY não encontrada")

PROMPT = """Design an elegant, atmospheric EDITORIAL BLOG COVER (refined history & culture magazine quality), 16:9 landscape.

VISUAL THEME — synthesize this article: "Deusas de pedra" (Stone Goddesses) about the female invisibility in
cemetery art. A historic Brazilian heritage cemetery seen as an open-air museum. The central subject is a
beautiful weathered white marble statue of a serene woman / mourning angel / classical goddess, softly touched
by lichen and time, standing gracefully among ornate old tombs and mausoleums. Mood: melancholic, poetic,
dignified and reverent — honoring overlooked feminine figures of funerary sculpture. Light: warm golden-hour
glow with a faint full moon and gentle mist, deep elegant shadows. Painterly, cinematic, sophisticated.
NOT horror, NOT spooky — graceful, beautiful and noble.

BRAND ART DIRECTION:
- Color palette: deep wine/bordeaux, warm antique gold, soft cream/ivory.
- Add a thin elegant gold frame around the whole cover. Leave clear space at the top for the title.

TEXT TO RENDER (elegant classic serif, perfectly spelled in Portuguese, gold and cream, high contrast, readable):
- Small kicker line at the very top: CLARISSE ISMÉRIO · PESQUISAS HISTÓRICAS
- Large title: Deusas de pedra
- Subtitle under the title: A invisibilidade feminina na arte cemiterial

Final result: a polished, clickable cover that makes a reader want to open and read the article."""

def openai_image(key, model, prompt, size, quality=None):
    body = {"model": model, "prompt": prompt, "size": size, "n": 1}
    if quality:
        body["quality"] = quality
    if model == "dall-e-3":
        body["response_format"] = "b64_json"
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    return base64.b64decode(data["data"][0]["b64_json"])

def main():
    key = load_key()
    attempts = [
        ("gpt-image-1", "1536x1024", "high"),
        ("gpt-image-1", "1536x1024", "medium"),
        ("dall-e-3", "1792x1024", None),
    ]
    last = None
    for model, size, quality in attempts:
        try:
            print(f"Gerando com {model} ({size}, quality={quality}) ...")
            img = openai_image(key, model, PROMPT, size, quality)
            with open(OUT, "wb") as f:
                f.write(img)
            print(f"OK · {model} · {len(img)} bytes → {OUT}")
            return
        except urllib.error.HTTPError as e:
            last = e.read().decode()[:400]
            print("  falhou:", e.code, last)
        except Exception as e:
            last = str(e)[:400]
            print("  falhou:", last)
    raise SystemExit("Falhou: " + str(last))

if __name__ == "__main__":
    main()
