#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera uma capa editorial para um artigo do blog usando a API do Google (Gemini 3 image).
A capa sintetiza o conteúdo do artigo + traz o título, no estilo da marca (vinho/dourado/creme)."""
import os, re, json, base64, urllib.request, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_key():
    for p in [os.path.join(ROOT, "..", ".env"), os.path.join(ROOT, "..", "Prof. Rafael", ".env")]:
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                m = re.match(r"\s*GOOGLE_API_KEY\s*=\s*[\"']?([^\"'\n]+)", line)
                if m:
                    return m.group(1).strip()
    raise SystemExit("GOOGLE_API_KEY não encontrada")

PROMPT = """Create an elegant, atmospheric EDITORIAL BLOG COVER (magazine quality) for a history article.

ARTICLE THEME (synthesize this visually): "Deusas de pedra" — the female invisibility in cemetery art.
Historic Brazilian heritage cemetery as an open-air museum. The central subject is a beautiful weathered
white marble statue of a serene woman / mourning angel / classical goddess, partly covered in soft lichen,
standing among old ornate tombs and mausoleums. Melancholic, poetic, dignified mood — celebrating the
overlooked feminine figures of funerary sculpture. Soft dramatic light: golden hour glow with a faint full
moon, gentle mist, deep shadows. Cinematic, painterly, refined — NOT spooky or horror, but graceful and reverent.

ART DIRECTION / BRAND:
- Color palette: deep wine/bordeaux (#7a1f2b), warm gold (#b8893f), soft cream (#f7f1e7).
- Sophisticated, classic, feminist-historical tone. Frame the composition leaving room at the top for a title.
- Add a thin elegant gold border/frame around the cover.

TYPOGRAPHY (render this text crisply and correctly, elegant serif, gold-and-cream on the darker areas):
- Small kicker at top: "CLARISSE ISMÉRIO · PESQUISAS HISTÓRICAS"
- Large main title: "Deusas de pedra"
- Subtitle below: "A invisibilidade feminina na arte cemiterial"
The text must be perfectly spelled in Portuguese, beautifully integrated, high contrast and readable.
Overall: looks like the cover of a refined history & culture publication that makes people want to click and read."""

def gen(model, prompt, key, aspect="16:9"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"aspectRatio": aspect}},
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.load(r)
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inl = part.get("inlineData") or part.get("inline_data")
            if inl and inl.get("data"):
                return base64.b64decode(inl["data"])
    raise RuntimeError("sem imagem na resposta: " + json.dumps(data)[:600])

def main():
    key = load_key()
    out = os.path.join(ROOT, "assets", "capa-deusas-de-pedra.png")
    models = ["gemini-3-pro-image-preview", "gemini-3.1-flash-image", "gemini-2.5-flash-image"]
    last = None
    for mdl in models:
        try:
            print("Tentando", mdl, "...")
            img = gen(mdl, PROMPT, key)
            with open(out, "wb") as f:
                f.write(img)
            print(f"OK · {mdl} · {len(img)} bytes → {out}")
            return
        except Exception as e:
            last = e
            print("  falhou:", str(e)[:200])
    raise SystemExit("Todos os modelos falharam: " + str(last))

if __name__ == "__main__":
    main()
