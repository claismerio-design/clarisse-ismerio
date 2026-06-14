#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rastreia os artigos de Clarisse Ismério no Jornal Minuano e salva em JSON.
Identifica autoria pela assinatura no corpo ('Clarisse Ismério' + 'Doutora em História do Brasil')."""
import json, re, time, html, urllib.request, urllib.error, os

BASE = "https://www.jornalminuano.com.br"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124 Safari/537.36")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "artigos_minuano.json")

SEEDS = [
    "/caderno/minuanoconecta",
    "/colunistas/clarisse-ismerio",
    "/noticia/2026/05/02/vidas-educadoras",
    "/noticia/2026/05/31/uma-boneca-ou-o-deus-do-comercio-o-que-revela-uma-fachada-em-bage",
    "/noticia/2026/06/01/o-cenario-como-personagem-que-se-comunica-visualmente",
    "/noticia/2026/06/03/arvores-memoria-viva-pertencimento-e-patrimonio",
]

def fetch(path):
    url = BASE + path if path.startswith("/") else path
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        print("  ! erro", path, e)
        return ""

def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()

def is_clarisse(h):
    return ("Clarisse Ism" in h and
            ("Doutora em Hist" in h or "Historiadora" in h and "Urcamp" in h))

def parse_article(path, h):
    title = ""
    m = re.search(r'id="news-read-title"[^>]*>(.*?)</h1>', h, re.S)
    if m: title = clean(m.group(1))
    date = ""
    m = re.search(r'(\d{2}/\d{2}/\d{4})\s*às\s*(\d{2}:\d{2})', h)
    if m: date = f"{m.group(1)} {m.group(2)}"
    # corpo
    body = ""
    m = re.search(r'id="news-read-text"[^>]*>(.*?)(?:<div[^>]*id="news-read-|<footer|Leia também|id="news-read-tags)', h, re.S)
    chunk = m.group(1) if m else ""
    paras = re.findall(r"<p[^>]*>(.*?)</p>", chunk, re.S)
    CRED = re.compile(r"^(Clarisse Ism|Historiadora|Professora\b|Coordenadora\b|Integrante d|Membro d|Doutora em|Mestre em|Acadêmica|Acadêmico|Escritora\b|Pesquisadora\b)")
    cleaned = []
    for p in paras:
        t = clean(p)
        if not t: continue
        if CRED.match(t): continue          # linhas de credencial/assinatura
        if len(t.split()) <= 4: continue    # sobras curtas
        cleaned.append(t)
    body = "\n\n".join(cleaned)
    # og image se houver
    img = ""
    m = re.search(r'id="news-read-media".*?<img[^>]*src="([^"]+)"', h, re.S)
    if m: img = m.group(1)
    return {"path": path, "url": BASE + path, "title": title, "date": date,
            "body": body, "image": img, "n_paragraphs": len(cleaned)}

def noticia_links(h):
    return set(re.findall(r"/noticia/\d{4}/\d{2}/\d{2}/[a-z0-9-]+", h))

def main():
    seen, queue = set(), list(SEEDS)
    arts = {}
    fetches = 0
    while queue and fetches < 80:
        path = queue.pop(0)
        if path in seen: continue
        seen.add(path)
        h = fetch(path); fetches += 1
        time.sleep(0.4)
        if not h: continue
        listing = path.startswith("/caderno/") or path.startswith("/colunistas/")
        mine = path.startswith("/noticia/") and is_clarisse(h)
        if mine:
            a = parse_article(path, h)
            arts[path] = a
            print(f"  ✓ {a['date']}  {a['title']}  ({a['n_paragraphs']}p)")
        # expandir links de páginas dela ou de listagens
        if mine or listing:
            for ln in sorted(noticia_links(h)):
                if ln not in seen:
                    queue.append(ln)
    # ordena por data (dd/mm/yyyy)
    def keyf(a):
        m = re.match(r"(\d{2})/(\d{2})/(\d{4})", a["date"] or "01/01/1900")
        return (m.group(3), m.group(2), m.group(1)) if m else ("1900","01","01")
    out = sorted(arts.values(), key=keyf, reverse=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\n{len(out)} artigos de Clarisse salvos em {OUT}  ({fetches} páginas visitadas)")

if __name__ == "__main__":
    main()
