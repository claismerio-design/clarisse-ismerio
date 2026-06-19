#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera os 3 sites (opções de identidade visual) da Clarisse Ismério.
Cada opção é um site completo navegável com as mesmas abas do site de referência."""
import os, shutil, json, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# TEMAS
# ----------------------------------------------------------------------------
THEMES = {
    "opcao-1": {
        "cls": "t1", "nome": "Clássica & Elegante",
        "fonts": '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,400;1,500&family=Playfair+Display:wght@500;600;700;800&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">',
    },
    "opcao-2": {
        "cls": "t2", "nome": "Moderna & Vibrante",
        "fonts": '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">',
    },
    "opcao-3": {
        "cls": "t3", "nome": "Sofisticada & Noturna",
        "fonts": '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,400;1,500&family=Marcellus&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">',
    },
}

# Abas (iguais à referência marydelpriore)
NAV = [
    ("index.html", "Início"),
    ("sobre.html", "Sobre"),
    ("midia.html", "Na Mídia"),
    ("livros.html", "Livros"),
    ("palestras.html", "Palestras"),
    ("videos.html", "Vídeos"),
    ("blog.html", "Blog"),
    ("contato.html", "Contato"),
]

IMG = "assets"

# ----------------------------------------------------------------------------
# CSS  (um arquivo, três temas via classe no body)
# ----------------------------------------------------------------------------
CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:var(--f-body);background:var(--bg);color:var(--text);line-height:1.7;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{font-family:var(--f-head);font-weight:var(--head-w);line-height:1.14}
em{font-family:var(--f-italic);font-style:italic;color:var(--gold-strong)}
a{color:inherit;text-decoration:none}
img{display:block;max-width:100%}
.wrap{max-width:1180px;margin:0 auto;padding:0 28px}
.kicker{font-size:.76rem;letter-spacing:var(--ks);text-transform:uppercase;color:var(--gold-strong);font-weight:600;display:block;margin-bottom:14px}

/* THEME TOKENS */
body.t1{--bg:#fbf7ef;--bg-alt:#f7f1e7;--surface:#fbf7ef;--text:#2c2420;--text-soft:#5b524c;
  --primary:#7a1f2b;--primary-dark:#5c1620;--accent:#c84b6a;--gold:#b8893f;--gold-strong:#a8771f;--gold-light:#d9b56a;
  --border:rgba(184,137,63,.28);--nav-bg:rgba(251,247,239,.92);--hero-bg:linear-gradient(135deg,#5c1620,#7a1f2b);--hero-text:#f7f1e7;
  --radius:3px;--radius-lg:5px;--f-head:'Playfair Display',serif;--f-body:'Jost',sans-serif;--f-italic:'Cormorant Garamond',serif;--head-w:700;--ks:.26em}
body.t2{--bg:#fff6f8;--bg-alt:#fdeef2;--surface:#ffffff;--text:#2a0e16;--text-soft:#6b5860;
  --primary:#b51b3b;--primary-dark:#8e1430;--accent:#e0507e;--gold:#e0a942;--gold-strong:#c98e1f;--gold-light:#f0c674;
  --border:rgba(224,80,126,.18);--nav-bg:rgba(255,246,248,.9);--hero-bg:linear-gradient(120deg,#b51b3b,#d63268,#e0507e);--hero-text:#ffffff;
  --radius:18px;--radius-lg:24px;--f-head:'Fraunces',serif;--f-body:'Manrope',sans-serif;--f-italic:'Fraunces',serif;--head-w:600;--ks:.12em}
body.t3{--bg:#1a060c;--bg-alt:#260810;--surface:#1f0a11;--text:#e8d9cf;--text-soft:#b89aa0;
  --primary:#8e1a32;--primary-dark:#3a0d18;--accent:#d05c7e;--gold:#d8af5f;--gold-strong:#d8af5f;--gold-light:#ecd29a;
  --border:rgba(216,175,95,.22);--nav-bg:rgba(26,6,12,.85);--hero-bg:radial-gradient(ellipse at 70% 0%,#4a1020,#1a060c 60%);--hero-text:#f3e9d8;
  --radius:3px;--radius-lg:4px;--f-head:'Marcellus',serif;--f-body:'Outfit',sans-serif;--f-italic:'Cormorant Garamond',serif;--head-w:400;--ks:.3em}

/* NAV */
header.nav{position:sticky;top:0;z-index:50;background:var(--nav-bg);backdrop-filter:blur(10px);border-bottom:1px solid var(--border)}
.nav-inner{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:14px 28px;max-width:1180px;margin:0 auto}
.brand{display:flex;align-items:center;gap:13px;white-space:nowrap}
.brand-logo{width:50px;height:50px;border-radius:50%;object-fit:cover;border:2px solid var(--gold);box-shadow:0 2px 10px rgba(122,31,43,.25);flex:none}
body.t3 .brand-logo{box-shadow:0 0 16px rgba(216,175,95,.35)}
.brand-name{display:flex;flex-direction:column;line-height:1.05;font-family:var(--f-head);font-weight:var(--head-w);font-size:1.3rem;color:var(--primary);letter-spacing:.02em}
.brand-name small{font-family:var(--f-body);font-weight:400;font-size:.6rem;letter-spacing:.22em;text-transform:uppercase;color:var(--gold-strong);margin-top:3px}
body.t2 .brand-name{color:var(--primary)}
body.t3 .brand-name{color:var(--gold-light)}
.brand-name b{color:var(--gold-strong);font-weight:inherit}
body.t3 .brand-name b{color:var(--accent)}
nav.menu ul{display:flex;gap:22px;list-style:none;align-items:center;flex-wrap:wrap;justify-content:flex-end}
nav.menu a{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text-soft);transition:color .2s;white-space:nowrap}
nav.menu a:hover,nav.menu a.active{color:var(--primary)}
body.t3 nav.menu a:hover,body.t3 nav.menu a.active{color:var(--gold-light)}
nav.menu a.cta{background:var(--primary);color:#fff;padding:9px 16px;border-radius:var(--radius);font-size:.74rem}
body.t2 nav.menu a.cta{background:var(--hero-bg);border-radius:30px}
body.t3 nav.menu a.cta{background:transparent;border:1px solid var(--gold);color:var(--gold-light)}

/* BUTTONS */
.btn{display:inline-block;padding:14px 26px;border-radius:var(--radius);font-size:.82rem;letter-spacing:.08em;text-transform:uppercase;font-weight:600;transition:.2s;cursor:pointer}
body.t2 .btn{border-radius:30px;letter-spacing:.04em}
.btn-gold{background:linear-gradient(135deg,var(--gold),var(--gold-strong));color:#2a1606}
.btn-gold:hover{filter:brightness(1.07);transform:translateY(-2px)}
.btn-ghost{border:1px solid var(--gold);color:var(--hero-text)}
.btn-ghost:hover{background:rgba(216,175,95,.14)}
.btn-line{border:1px solid var(--primary);color:var(--primary)}
.btn-line:hover{background:var(--primary);color:#fff}

/* HERO (home) */
.hero{position:relative;overflow:hidden;background:var(--hero-bg);color:var(--hero-text)}
.hero::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 82% 18%,rgba(216,175,95,.20),transparent 55%)}
.hero-grid{position:relative;display:grid;grid-template-columns:1.08fr .92fr;gap:48px;align-items:center;padding:84px 0}
.hero h1{font-size:4rem;margin-bottom:20px}
.hero .lead{font-family:var(--f-italic);font-style:italic;font-size:1.5rem;max-width:30ch;margin-bottom:28px;opacity:.95}
.hero .roles{font-size:.82rem;letter-spacing:.08em;text-transform:uppercase;opacity:.85;margin-bottom:32px}
.hero .btns{display:flex;gap:14px;flex-wrap:wrap}
.portrait{position:relative}
.portrait img{width:100%;border-radius:var(--radius-lg);box-shadow:0 30px 60px rgba(0,0,0,.4)}
.portrait .frame{position:absolute;inset:-12px;border:1px solid var(--gold);border-radius:var(--radius-lg);z-index:-1}
body.t2 .portrait .frame{border-style:dashed;inset:-14px;border-color:rgba(255,255,255,.5)}
.moon{display:none;position:absolute;top:54px;right:7%;width:150px;height:150px;border-radius:50%;background:radial-gradient(circle at 40% 38%,#fff8e7,#e9d6a8 55%,#caa85f);box-shadow:0 0 70px 18px rgba(236,210,154,.25);z-index:0}
body.t3 .moon{display:block}

/* PAGE HEADER (páginas internas) */
.phead{position:relative;overflow:hidden;background:var(--hero-bg);color:var(--hero-text);padding:64px 0 58px;text-align:center}
.phead::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 80% 10%,rgba(216,175,95,.18),transparent 55%)}
.phead h1{position:relative;font-size:3rem;margin-bottom:10px}
.phead p{position:relative;font-family:var(--f-italic);font-style:italic;font-size:1.3rem;opacity:.92}
.crumb{position:relative;font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;opacity:.7;margin-bottom:16px}

/* STATS */
.stats{background:var(--bg-alt);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;padding:42px 0;text-align:center}
.stat .num{font-family:var(--f-head);font-size:2.6rem;color:var(--primary)}
body.t3 .stat .num{color:var(--gold-light)}
.stat .lbl{font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:var(--text-soft)}

/* SECTIONS */
section.block{padding:84px 0}
section.alt{background:var(--bg-alt)}
.sec-head{text-align:center;max-width:640px;margin:0 auto 52px}
.sec-head h2{font-size:2.5rem;color:var(--primary)}
body.t3 .sec-head h2{color:var(--text)}
.rule{width:54px;height:2px;background:var(--gold);margin:16px auto 0}

/* SPLIT (texto + imagem) */
.split{display:grid;grid-template-columns:.9fr 1.1fr;gap:54px;align-items:center}
.split.rev{grid-template-columns:1.1fr .9fr}
.split img.full{width:100%;border-radius:var(--radius-lg);box-shadow:0 22px 46px rgba(0,0,0,.18)}
.split h2{font-size:2.3rem;color:var(--primary);margin-bottom:20px}
body.t3 .split h2{color:var(--text)}
.split p{color:var(--text-soft);margin-bottom:15px}
.sign{font-family:var(--f-italic);font-style:italic;font-size:1.6rem;color:var(--gold-strong);margin-top:6px}

/* CARDS GRID */
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:30px}
.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:30px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;transition:.25s}
.card:hover{transform:translateY(-6px);box-shadow:0 22px 46px rgba(0,0,0,.18)}

/* BOOK */
.book .cover{aspect-ratio:3/4;background:linear-gradient(160deg,var(--primary),var(--primary-dark));display:flex;flex-direction:column;justify-content:flex-end;padding:24px;color:#f7ecd9;position:relative}
.book .cover::before{content:"";position:absolute;inset:13px;border:1px solid rgba(216,175,95,.45)}
.book .cover .ano{position:relative;font-size:.7rem;letter-spacing:.18em;color:var(--gold-light)}
.book .cover .tit{position:relative;font-family:var(--f-head);font-size:1.35rem;margin-top:6px;line-height:1.16}
.book .meta{padding:20px 22px}
.book .meta p{font-size:.88rem;color:var(--text-soft);margin-bottom:14px}
.book .meta .price{font-family:var(--f-head);color:var(--primary);font-size:1.2rem;margin-bottom:12px}
body.t3 .book .meta .price{color:var(--gold-light)}

/* SARAU feature */
.sarau{position:relative;overflow:hidden;background:linear-gradient(135deg,#2a1418,var(--primary-dark));color:#f3e9df}
body.t3 .sarau{background:radial-gradient(ellipse at 30% 20%,#4a1020,#1a060c 62%)}
.sarau .split{padding:84px 0}
.sarau h2{color:#fff}
.sarau p{color:#ecdcdf}

/* VIDEO */
.video{position:relative;border-radius:var(--radius-lg);overflow:hidden;background:var(--surface);border:1px solid var(--border)}
.video .thumb{aspect-ratio:16/9;background-size:cover;background-position:center;position:relative}
.video .thumb::after{content:"▶";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:1.6rem;color:#fff;background:rgba(58,13,24,.42)}
.video .cap{padding:16px 18px}
.video .cap h4{font-size:1.05rem;margin-bottom:4px}
.video .cap span{font-size:.8rem;color:var(--text-soft)}

/* MÍDIA cards */
.mcard{padding:26px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg)}
.mcard .src{font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-strong);margin-bottom:10px}
.mcard h4{font-size:1.25rem;color:var(--primary);margin-bottom:8px}
body.t3 .mcard h4{color:var(--text)}
.mcard p{font-size:.9rem;color:var(--text-soft);margin-bottom:14px}
.mcard a{font-size:.76rem;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-strong);border-bottom:1px solid var(--gold)}

/* BLOG (formato referência) */
.post{display:grid;grid-template-columns:.92fr 1.08fr;gap:34px;align-items:center;padding:32px 0;border-bottom:1px solid var(--border)}
.post:first-of-type{border-top:1px solid var(--border)}
.post .thumb{aspect-ratio:2/1;border-radius:var(--radius-lg);background-size:cover;background-position:center;border:1px solid var(--border)}
.post .cat{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold-strong)}
.post h3{font-family:var(--f-head);font-size:1.6rem;color:var(--primary);margin:8px 0 8px}
body.t3 .post h3{color:var(--text)}
.post .by{font-size:.82rem;color:var(--text-soft);margin-bottom:10px}
.post p{color:var(--text-soft);margin-bottom:12px}
.post .saiba{font-size:.76rem;letter-spacing:.1em;text-transform:uppercase;color:var(--primary);font-weight:600;border-bottom:1px solid var(--gold);padding-bottom:2px}
body.t3 .post .saiba{color:var(--gold-light)}

/* ARTIGO (página individual) */
.art-top{padding-top:34px}
.crumb-link{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--text-soft);margin-bottom:18px}
.crumb-link a{color:var(--gold-strong);border-bottom:1px solid var(--border)}
.article{max-width:760px;margin:0 auto}
.art-meta{font-size:.85rem;color:var(--text-soft);text-transform:uppercase;letter-spacing:.08em;margin:22px 0 0;text-align:center}
.art-meta b{color:var(--primary)}
body.t3 .art-meta b{color:var(--gold-light)}

/* CAPA EDITORIAL (foto + degradê + moldura + título) */
.cover-design{position:relative;aspect-ratio:16/9;max-height:460px;border-radius:var(--radius-lg);overflow:hidden;
  background-size:cover;background-position:center 22%;display:flex;align-items:flex-end;
  box-shadow:0 26px 54px rgba(0,0,0,.32)}
.cover-design::before{content:"";position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(40,10,16,.15) 0%,rgba(50,12,20,.30) 40%,rgba(58,13,24,.92) 100%)}
.cover-frame{position:absolute;inset:14px;border:1px solid rgba(216,175,95,.65);border-radius:calc(var(--radius-lg) - 2px);z-index:2;pointer-events:none}
.cover-txt{position:relative;z-index:3;padding:40px 44px;max-width:80%}
.cover-kicker{display:block;font-family:var(--f-body);font-size:.74rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-light);margin-bottom:12px}
.cover-title{display:block;font-family:var(--f-head);font-weight:var(--head-w);font-size:2.7rem;line-height:1.08;color:#fff7ec;text-shadow:0 2px 18px rgba(0,0,0,.4)}
.cover-sub{display:inline-block;margin-top:14px;font-family:var(--f-italic);font-style:italic;font-size:1.15rem;color:#f0d9c7}
.art-body{margin-top:36px;font-size:1.12rem;line-height:1.85}
.art-body p{margin-bottom:1.25em;color:var(--text)}
body.t1 .art-body,body.t2 .art-body{color:#3a322c}
.art-body p:first-of-type::first-letter{font-family:var(--f-head);font-size:3.4rem;line-height:.8;float:left;margin:6px 12px 0 0;color:var(--primary)}
body.t3 .art-body p:first-of-type::first-letter{color:var(--gold-light)}
.art-foot{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;margin-top:40px;padding-top:26px;border-top:1px solid var(--border)}
.art-src{font-size:.82rem;color:var(--text-soft);border-bottom:1px solid var(--gold)}
.art-src:hover{color:var(--primary)}

/* CTA box */
.ctabox{background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;padding:60px 40px;border-radius:var(--radius-lg);text-align:center;position:relative;overflow:hidden}
.ctabox::before{content:"";position:absolute;inset:16px;border:1px solid rgba(216,175,95,.5);border-radius:var(--radius);pointer-events:none}
body.t2 .ctabox::before{display:none}
.ctabox h2{position:relative;font-size:2.2rem;margin-bottom:14px}
.ctabox p{position:relative;max-width:48ch;margin:0 auto 24px;opacity:.95}

/* CONTACT */
.form{display:grid;gap:16px;max-width:560px}
.form input,.form textarea{width:100%;padding:13px 15px;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);color:var(--text);font-family:var(--f-body);font-size:.95rem}
.form textarea{min-height:130px;resize:vertical}
.info-list{list-style:none;display:grid;gap:14px}
.info-list li{display:flex;gap:12px;align-items:flex-start;color:var(--text-soft)}
.info-list b{color:var(--text);font-family:var(--f-head);font-weight:var(--head-w)}

.center{text-align:center}
.mt40{margin-top:40px}
.lead-list{list-style:none;display:grid;gap:14px;margin-top:10px}
.lead-list li{padding-left:26px;position:relative;color:var(--text-soft)}
.lead-list li::before{content:"❦";position:absolute;left:0;color:var(--gold-strong)}

/* FOOTER */
footer.foot{background:var(--primary-dark);color:#e7d6cf;padding:58px 0 26px}
body.t2 footer.foot{background:#2a0e16}
body.t3 footer.foot{background:#14060a;border-top:1px solid var(--border)}
.foot-grid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:40px;padding-bottom:36px;border-bottom:1px solid rgba(216,175,95,.22)}
.brand-f-row{display:flex;align-items:center;gap:14px;margin-bottom:14px}
.foot-logo{width:54px;height:54px;border-radius:50%;object-fit:cover;border:2px solid var(--gold);flex:none}
footer .brand-f{font-family:var(--f-head);font-size:1.6rem;color:#fff;margin:0}
body.t3 footer .brand-f{color:var(--gold-light)}
footer h4{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-light);margin-bottom:15px}
footer ul{list-style:none}
footer li{margin-bottom:9px;font-size:.9rem}
footer li a:hover{color:var(--gold-light)}
.copy{text-align:center;padding-top:22px;font-size:.8rem;opacity:.7}

/* SWITCHER flutuante (alterna identidade visual) */
.switcher{position:fixed;bottom:18px;right:18px;z-index:200;display:flex;align-items:center;gap:8px;
  background:rgba(20,6,10,.9);backdrop-filter:blur(8px);border:1px solid var(--gold);border-radius:40px;
  padding:8px 12px;box-shadow:0 12px 30px rgba(0,0,0,.4)}
.switcher .sw-lbl{font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:#e7d6cf;padding:0 4px}
.switcher .sw-opt{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:.82rem;font-weight:700;color:#e7d6cf;border:1px solid rgba(216,175,95,.4);transition:.2s;font-family:var(--f-body)}
.switcher .sw-opt:hover{border-color:var(--gold);color:#fff}
.switcher .sw-opt.cur{background:linear-gradient(135deg,var(--gold),var(--gold-strong));color:#2a1606;border-color:transparent}
.switcher .sw-home{margin-left:2px;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  color:#caa85f;font-size:1rem;text-decoration:none}
.switcher .sw-home:hover{color:#fff}
@media(max-width:560px){.switcher{bottom:12px;right:12px;padding:6px 10px;gap:5px}.switcher .sw-lbl{display:none}}

@media(max-width:880px){
  .hero-grid,.split,.split.rev,.grid3,.grid2,.foot-grid{grid-template-columns:1fr}
  .hero h1{font-size:2.7rem}.phead h1{font-size:2.2rem}
  .stats-grid{grid-template-columns:repeat(2,1fr);gap:28px}
  nav.menu ul{display:none}
  .portrait{order:-1;max-width:340px;margin:0 auto}
  .moon{width:96px;height:96px;top:18px}
}
"""

# ----------------------------------------------------------------------------
# PARTIALS
# ----------------------------------------------------------------------------
def nav(active, cls):
    items = ""
    for href, label in NAV:
        a = ' active' if href == active else ''
        cta = ' cta' if href == 'contato.html' else ''
        items += f'<li><a class="{(a+cta).strip()}" href="{href}">{label}</a></li>'
    return f'''<header class="nav"><div class="nav-inner">
  <a class="brand" href="index.html">
    <img class="brand-logo" src="{IMG}/logo.jpeg" alt="Logotipo Clarisse Ismério — Pesquisas Históricas">
    <span class="brand-name">Clarisse <b>Ismério</b><small>Pesquisas Históricas</small></span>
  </a>
  <nav class="menu"><ul>{items}</ul></nav>
</div></header>'''

def footer():
    cols = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV[1:6])
    return f'''<footer class="foot"><div class="wrap">
  <div class="foot-grid">
    <div>
      <div class="brand-f-row">
        <img class="foot-logo" src="{IMG}/logo.jpeg" alt="Logotipo Clarisse Ismério">
        <p class="brand-f">Clarisse Ismério</p>
      </div>
      <p style="max-width:34ch;font-size:.9rem">Historiadora, pesquisadora e criadora do Sarau Noturno. Pesquisas históricas, livros, palestras e cultura.</p>
    </div>
    <div><h4>Navegação</h4><ul>{cols}</ul></div>
    <div><h4>Contato</h4><ul>
      <li>Bagé · Rio Grande do Sul</li>
      <li>claismerio@gmail.com</li>
      <li>@clarisseismerio</li>
    </ul></div>
  </div>
  <p class="copy">© 2026 Clarisse Ismério · Pesquisas Históricas. Todos os direitos reservados.</p>
</div></footer>'''

def page(theme, active, title, body):
    t = THEMES[theme]
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · Clarisse Ismério</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{t["fonts"]}
<link rel="stylesheet" href="assets/site.css">
</head>
<body class="{t["cls"]}">
{nav(active, t["cls"])}
{body}
{footer()}
</body>
</html>'''

def phead(title, sub):
    return f'''<section class="phead"><div class="moon"></div><div class="wrap">
  <p class="crumb">Clarisse Ismério</p>
  <h1>{title}</h1><p>{sub}</p>
</div></section>'''

STATS = '''<div class="stats"><div class="wrap stats-grid">
  <div class="stat"><div class="num">30+</div><div class="lbl">Anos de pesquisa</div></div>
  <div class="stat"><div class="num">8</div><div class="lbl">Livros &amp; coletâneas</div></div>
  <div class="stat"><div class="num">17</div><div class="lbl">Anos de Sarau Noturno</div></div>
  <div class="stat"><div class="num">100+</div><div class="lbl">Palestras &amp; aulas</div></div>
</div></div>'''

BOOKS = [
    ("Mulher: a Moral e o Imaginário", "Ediurcamp · 2018", "O universo feminino e suas representações entre 1889 e 1930.", "R$ 59"),
    ("Sarau Noturno", "Ediurcamp · 2021", "Educação patrimonial e arte cemiterial sob o olhar da sensibilidade.", "R$ 64"),
    ("Pequenos Detalhes de Bagé", "Ediurcamp · 2019", "As histórias e os detalhes que constroem a identidade de Bagé.", "R$ 49"),
]

def book_card(b, with_price=True):
    tit, ano, desc, preco = b
    price = f'<div class="price">{preco}</div>' if with_price else ''
    return f'''<div class="card book">
  <div class="cover"><span class="ano">{ano}</span><span class="tit">{tit}</span></div>
  <div class="meta"><p>{desc}</p>{price}<a class="btn btn-gold" href="#">Comprar</a></div>
</div>'''

# --- Artigos reais (coluna do Jornal Minuano, extraídos em data/artigos_minuano.json) ---
# categoria + ilustração (fotos dela como placeholder até termos capas próprias)
# Só fotos limpas dela como fundo de capa (a ilustração do Sarau tem texto embutido — fica na home).
ART_META = {
    "vidas-educadoras": ("Mulheres na História", "clarisse-mesa.jpeg"),
    "uma-boneca-ou-o-deus-do-comercio-o-que-revela-uma-fachada-em-bage": ("Patrimônio", "clarisse-retrato.jpeg"),
    "arte-cemiterial": ("Patrimônio & Memória", "clarisse-mesa.jpeg"),
    "deusas-de-pedra-a-invisibilidade-feminina-na-arte-cemiterial": ("Mulheres na História", "clarisse-retrato.jpeg"),
    "do-luto-a-elegancia-as-origens-historicas-do-pretinho-basico": ("História da Moda", "clarisse-mesa.jpeg"),
    "a-maternidade-na-perspectiva-historica-representacoes-papeis-e-transformacoes": ("Mulheres na História", "clarisse-retrato.jpeg"),
    "um-conto-de-duas-amigas-escrita-memoria-e-sororidade": ("Memória & Sororidade", "clarisse-mesa.jpeg"),
}
# capas geradas por IA (slug -> arquivo em assets) — sobrescrevem a ilustração placeholder
ART_COVER = {}

MESES = {"01":"janeiro","02":"fevereiro","03":"março","04":"abril","05":"maio","06":"junho",
         "07":"julho","08":"agosto","09":"setembro","10":"outubro","11":"novembro","12":"dezembro"}

def _slug(path): return path.rstrip("/").split("/")[-1]

def _excerpt(body, n=30):
    w = body.replace("\n", " ").split()
    return " ".join(w[:n]) + ("…" if len(w) > n else "")

def _data_ext(d):
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", d or "")
    return f"{int(m.group(1))} de {MESES[m.group(2)]} de {m.group(3)}" if m else d

def load_articles():
    with open(os.path.join(ROOT, "data", "artigos_minuano.json"), encoding="utf-8") as f:
        raw = json.load(f)
    arts = []
    for a in raw:
        slug = _slug(a["path"])
        cat, img = ART_META.get(slug, ("Coluna", "clarisse-retrato.jpeg"))
        arts.append({
            "slug": slug, "title": a["title"], "date": a["date"], "data_ext": _data_ext(a["date"]),
            "cat": cat, "img": ART_COVER.get(slug, img), "excerpt": _excerpt(a["body"]),
            "body": a["body"], "file": f"artigo-{slug}.html", "source": a["url"],
        })
    return arts  # JSON já vem ordenado por data desc

ARTICLES = load_articles()

def post_html(a):
    return f'''<article class="post">
  <div class="thumb" style="background-image:url('{IMG}/{a["img"]}')"></div>
  <div><span class="cat">{a["cat"]}</span><h3>{a["title"]}</h3>
  <p class="by">Por Clarisse Ismério · {a["data_ext"]}</p><p>{a["excerpt"]}</p>
  <a class="saiba" href="{a["file"]}">Saiba mais</a></div>
</article>'''

# ----------------------------------------------------------------------------
# PÁGINAS
# ----------------------------------------------------------------------------
def page_home(theme):
    books = "".join(book_card(b, False) for b in BOOKS)
    posts = "".join(post_html(p) for p in ARTICLES[:3])
    body = f'''
<section class="hero"><div class="moon"></div><div class="wrap hero-grid">
  <div>
    <span class="kicker" style="color:var(--gold-light)">Historiadora · Pesquisadora · Escritora</span>
    <h1>História, memória &amp; <em>sensibilidades</em></h1>
    <p class="lead">Pesquisas históricas que dão voz à memória, ao feminino e ao patrimônio da Campanha.</p>
    <p class="roles">Doutora em História do Brasil · Criadora do Sarau Noturno</p>
    <div class="btns"><a class="btn btn-gold" href="livros.html">Conheça os livros</a><a class="btn btn-ghost" href="contato.html">Contratar palestra</a></div>
  </div>
  <div class="portrait"><div class="frame"></div><img src="{IMG}/clarisse-retrato.jpeg" alt="Clarisse Ismério"></div>
</div></section>
{STATS}
<section class="block"><div class="wrap split">
  <div class="portrait"><div class="frame"></div><img class="full" src="{IMG}/clarisse-mesa.jpeg" alt="Clarisse Ismério"></div>
  <div>
    <span class="kicker">Sobre</span>
    <h2>Uma vida dedicada à história do Brasil</h2>
    <p>Nascida em São Gabriel (RS), Clarisse Ismério é historiadora formada pela PUCRS, com mestrado e doutorado em História do Brasil. Há mais de três décadas pesquisa o universo feminino, a cultura e o patrimônio.</p>
    <p>É autora de <em>Mulher: a Moral e o Imaginário</em>, <em>Sarau Noturno</em> e <em>Pequenos Detalhes de Bagé</em>.</p>
    <a class="btn btn-line" href="sobre.html">Conhecer a trajetória</a>
  </div>
</div></section>
<section class="block alt"><div class="wrap">
  <div class="sec-head"><span class="kicker">Publicações</span><h2>Livros &amp; ebooks</h2><div class="rule"></div></div>
  <div class="grid3">{books}</div>
  <div class="center mt40"><a class="btn btn-line" href="livros.html">Ver todos os livros</a></div>
</div></section>
<section class="sarau"><div class="wrap split rev">
  <div>
    <span class="kicker" style="color:var(--gold-light)">Projeto cultural</span>
    <h2>O <em>Sarau Noturno</em></h2>
    <p>Criado em 2008 a partir da pesquisa de arte cemiterial no Cemitério da Santa Casa de Bagé, é hoje um dos projetos de educação patrimonial mais singulares do Rio Grande do Sul.</p>
    <p>Une comunidade, universidade e turismo em torno da memória, da estética e da sensibilidade cultural.</p>
    <a class="btn btn-gold" href="contato.html">Leve o Sarau à sua cidade</a>
  </div>
  <img class="full" src="{IMG}/sarau-noturno.jpeg" alt="Sarau Noturno">
</div></section>
<section class="block"><div class="wrap">
  <div class="sec-head"><span class="kicker">Coluna &amp; reflexões</span><h2>Do blog</h2><div class="rule"></div></div>
  {posts}
  <div class="center mt40"><a class="btn btn-gold" href="blog.html">Ver todas as colunas</a></div>
</div></section>'''
    return page(theme, "index.html", "Início", body)

def page_sobre(theme):
    body = phead("Sobre Clarisse", "Historiadora, pesquisadora e criadora do Sarau Noturno") + f'''
<section class="block"><div class="wrap split">
  <div class="portrait"><div class="frame"></div><img class="full" src="{IMG}/clarisse-retrato.jpeg" alt="Clarisse Ismério"></div>
  <div>
    <span class="kicker">Trajetória</span>
    <h2>Mais de 30 anos dando voz à memória</h2>
    <p>Nascida em São Gabriel (RS) em 1967, Clarisse Ismério graduou-se em História pela PUCRS, onde concluiu também o mestrado (1995) e o doutorado (1999) em História do Brasil.</p>
    <p>Dedica-se à pesquisa do universo feminino, da cultura e do patrimônio. É professora e atuou na coordenação dos cursos de Pedagogia e História da Urcamp.</p>
    <p class="sign">Clarisse Ismério</p>
  </div>
</div></section>
{STATS}
<section class="block alt"><div class="wrap split rev">
  <div>
    <span class="kicker">Pesquisa &amp; atuação</span>
    <h2>Áreas de pesquisa</h2>
    <ul class="lead-list">
      <li>História do Brasil e história das mulheres</li>
      <li>Educação patrimonial e arte cemiterial</li>
      <li>Memória, cultura e sensibilidades</li>
      <li>História regional da Campanha e de Bagé</li>
    </ul>
    <a class="btn btn-line mt40" href="livros.html" style="margin-top:24px">Ver publicações</a>
  </div>
  <img class="full" src="{IMG}/clarisse-mesa.jpeg" alt="Clarisse Ismério em seu gabinete">
</div></section>'''
    return page(theme, "sobre.html", "Sobre", body)

def page_midia(theme):
    cards = ""
    midia = [
        ("Jornal Minuano", "Coluna de Clarisse Ismério", "Reflexões sobre história, memória e o universo feminino, publicadas no Jornal Minuano, Coluna no Caderno Minuano Conecta, Jornal Minuano.", "https://www.jornalminuano.com.br/caderno/minuanoconecta", "Acessar caderno →"),
        ("Jornal Minuano", "Publicações no Minuano Conecta", "Artigos assinados por Clarisse Ismério com foco em patrimônio, memória, história das mulheres e sensibilidades.", "blog.html", "Ver no site →"),
        ("Urcamp", "Cultura, Memória e Patrimônio", "Registros institucionais da atuação de Clarisse Ismério em projetos, pesquisa e extensão ligados ao patrimônio cultural.", "https://urcamp.edu.br/", "Acessar portal →"),
        ("Urcamp", "Notícias da Urcamp", "Portal de notícias da universidade com cobertura institucional de ações acadêmicas, culturais e patrimoniais.", "https://urcamp.edu.br/busca/news", "Ver notícias →"),
    ]
    for src, tit, desc, href, label in midia:
        extra = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        cards += f'''<div class="mcard"><div class="src">{src}</div><h4>{tit}</h4><p>{desc}</p><a href="{href}"{extra}>{label}</a></div>'''
    posts = "".join(post_html(p) for p in ARTICLES)
    body = phead("Na Mídia", "Clarisse Ismério na imprensa e nos espaços culturais") + f'''
<section class="block"><div class="wrap"><div class="grid2">{cards}</div></div></section>
<section class="block alt"><div class="wrap">
  <div class="sec-head"><span class="kicker">Minuano Conecta</span><h2>Todas as publicações</h2><div class="rule"></div></div>
  {posts}
</div></section>'''
    return page(theme, "midia.html", "Na Mídia", body)

def page_livros(theme):
    books = "".join(book_card(b, True) for b in BOOKS)
    body = phead("Livros &amp; Ebooks", "Pesquisas históricas em forma de livro") + f'''
<section class="block"><div class="wrap">
  <div class="grid3">{books}</div>
</div></section>
<section class="block alt"><div class="wrap">
  <div class="sec-head"><span class="kicker">Organização</span><h2>Coletâneas organizadas</h2><div class="rule"></div></div>
  <ul class="lead-list" style="max-width:680px;margin:0 auto">
    <li><b>Nem tudo são rosas</b> — preconceitos, lutas e conquistas femininas (2021)</li>
    <li><b>Patrimônio Cultural</b> — simbolismos, intertextualidades e polifonias (2021)</li>
    <li><b>Educação em suas múltiplas faces e sensibilidades</b> (2020)</li>
    <li><b>História de Bagé: novos olhares</b> — vol. 1 (2022) e vol. 2 (2023)</li>
  </ul>
</div></section>'''
    return page(theme, "livros.html", "Livros", body)

def page_palestras(theme):
    body = phead("Palestras", "Conteúdo rigoroso e envolvente para o seu evento") + f'''
<section class="block"><div class="wrap split">
  <div>
    <span class="kicker">Temas</span>
    <h2>Sobre o que Clarisse fala</h2>
    <ul class="lead-list">
      <li>História das mulheres e o universo feminino</li>
      <li>Educação patrimonial e o Sarau Noturno</li>
      <li>Memória, cultura e sensibilidades</li>
      <li>História do Brasil e da Campanha gaúcha</li>
      <li>A história como ferramenta de transformação</li>
    </ul>
  </div>
  <img class="full" src="{IMG}/sarau-noturno.jpeg" alt="Sarau Noturno">
</div></section>
<section class="block alt"><div class="wrap">
  <div class="sec-head"><span class="kicker">Para quem</span><h2>Onde levar</h2><div class="rule"></div></div>
  <div class="grid3">
    <div class="mcard"><h4>Escolas &amp; universidades</h4><p>Aulas magnas, formações de professores e mediações culturais.</p></div>
    <div class="mcard"><h4>Eventos &amp; festivais</h4><p>Palestras e contações para públicos amplos, em torno da memória e da cultura.</p></div>
    <div class="mcard"><h4>Empresas &amp; instituições</h4><p>Encontros sobre patrimônio, identidade e história regional.</p></div>
  </div>
</div></section>
<section class="block"><div class="wrap"><div class="ctabox">
  <h2>Quer levar uma palestra à sua cidade?</h2>
  <p>Conte sobre o seu evento e o público. Retornamos com temas, formatos e disponibilidade.</p>
  <a class="btn btn-gold" href="contato.html">Solicitar uma palestra</a>
</div></div></section>'''
    return page(theme, "palestras.html", "Palestras", body)

def page_videos(theme):
    vids = [
        ("Sarau Noturno — o documentário", "Projeto cultural", "sarau-noturno.jpeg"),
        ("Mulheres na história do Brasil", "Palestra", "clarisse-mesa.jpeg"),
        ("Arte cemiterial e memória", "Pesquisa", "sarau-noturno.jpeg"),
        ("Pequenos detalhes de Bagé", "Entrevista", "clarisse-retrato.jpeg"),
        ("Educação patrimonial na prática", "Aula aberta", "clarisse-mesa.jpeg"),
        ("Sensibilidades e história", "Conversa", "sarau-noturno.jpeg"),
    ]
    cards = ""
    for tit, cat, img in vids:
        cards += f'''<div class="video"><div class="thumb" style="background-image:url('{IMG}/{img}')"></div>
        <div class="cap"><h4>{tit}</h4><span>{cat}</span></div></div>'''
    body = phead("Vídeos", "Palestras, entrevistas e registros do Sarau Noturno") + f'''
<section class="block"><div class="wrap"><div class="grid3">{cards}</div></div></section>'''
    return page(theme, "videos.html", "Vídeos", body)

def page_blog(theme):
    posts = "".join(post_html(p) for p in ARTICLES)
    body = phead("Blog", "Coluna no Jornal Minuano · reflexões e crônicas históricas") + f'''
<section class="block"><div class="wrap">{posts}</div></section>'''
    return page(theme, "blog.html", "Blog", body)

def cover_block(a, tag="div"):
    """Capa editorial: foto de fundo + degradê + moldura dourada + título (estilo capa de revista)."""
    return f'''<{tag} class="cover-design" style="background-image:url('{IMG}/{a["img"]}')">
  <div class="cover-frame"></div>
  <div class="cover-txt">
    <span class="cover-kicker">Clarisse Ismério · Pesquisas Históricas</span>
    <span class="cover-title">{a["title"]}</span>
    <span class="cover-sub">{a["cat"]}</span>
  </div>
</{tag}>'''

def page_artigo(theme, a):
    paras = "".join(f"<p>{p}</p>" for p in a["body"].split("\n\n") if p.strip())
    related = [x for x in ARTICLES if x["slug"] != a["slug"]][:2]
    rel = "".join(post_html(x) for x in related)
    body = f'''
<section class="art-top"><div class="wrap">
  <p class="crumb-link"><a href="blog.html">Blog</a> · {a["cat"]}</p>
  {cover_block(a)}
  <p class="art-meta">Por <b>Clarisse Ismério</b> · {a["data_ext"]}</p>
</div></section>
<section class="block" style="padding-top:30px"><div class="wrap article">
  <div class="art-body">{paras}</div>
  <div class="art-foot">
    <a class="btn btn-line" href="blog.html">← Voltar ao blog</a>
    <a class="art-src" href="{a["source"]}" target="_blank" rel="noopener">Publicado originalmente no Jornal Minuano ↗</a>
  </div>
</div></section>
<section class="block alt"><div class="wrap">
  <div class="sec-head"><span class="kicker">Continue lendo</span><h2>Outras colunas</h2><div class="rule"></div></div>
  {rel}
</div></section>'''
    return page(theme, "blog.html", a["title"], body)

def page_contato(theme):
    body = phead("Contato", "Palestras, parcerias, imprensa e aquisição de livros") + f'''
<section class="block"><div class="wrap split">
  <div>
    <span class="kicker">Fale com Clarisse</span>
    <h2>Envie uma mensagem</h2>
    <form class="form" onsubmit="return false">
      <input type="text" placeholder="Seu nome">
      <input type="email" placeholder="Seu e-mail">
      <input type="text" placeholder="Assunto (palestra, livro, imprensa...)">
      <textarea placeholder="Sua mensagem"></textarea>
      <button class="btn btn-gold" type="submit">Enviar mensagem</button>
    </form>
  </div>
  <div>
    <span class="kicker">Informações</span>
    <h2>Onde encontrar</h2>
    <ul class="info-list">
      <li><span>📍</span><div><b>Cidade</b><br>Bagé · Rio Grande do Sul</div></li>
      <li><span>✉️</span><div><b>E-mail</b><br>claismerio@gmail.com</div></li>
      <li><span>📷</span><div><b>Instagram</b><br>@clarisseismerio</div></li>
      <li><span>📰</span><div><b>Coluna</b><br>Jornal Minuano</div></li>
    </ul>
  </div>
</div></section>'''
    return page(theme, "contato.html", "Contato", body)

BUILDERS = {
    "index.html": page_home, "sobre.html": page_sobre, "midia.html": page_midia,
    "livros.html": page_livros, "palestras.html": page_palestras, "videos.html": page_videos,
    "blog.html": page_blog, "contato.html": page_contato,
}

# ----------------------------------------------------------------------------
# BUILD
# ----------------------------------------------------------------------------
# Identidade visual em uso (Clássica & Elegante). Site único, gerado na raiz.
THEME = "opcao-1"

def main():
    with open(os.path.join(ROOT, "assets", "site.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    for fname, builder in BUILDERS.items():
        with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
            f.write(builder(THEME))
    for a in ARTICLES:
        with open(os.path.join(ROOT, a["file"]), "w", encoding="utf-8") as f:
            f.write(page_artigo(THEME, a))
    print(f"  site: {len(BUILDERS) + len(ARTICLES)} páginas ({len(ARTICLES)} artigos) na raiz")
    print("OK")

if __name__ == "__main__":
    main()
