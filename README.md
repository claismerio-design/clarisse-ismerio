# Site — Clarisse Ismério · Pesquisas Históricas

Site institucional da historiadora **Clarisse Ismério** (biografia, livros, ebooks, palestras e blog).
Site estático (HTML/CSS), publicado via **GitHub Pages**.

## Estrutura
- `index.html`, `sobre.html`, `livros.html`, `palestras.html`, `midia.html`, `videos.html`, `blog.html`, `contato.html` — páginas do site.
- `artigo-*.html` — páginas dos artigos do blog.
- `assets/` — logo, fotos e o CSS (`site.css`).
- `build.py` — gera todas as páginas a partir de templates. Rode `python3 build.py` após editar.
- `data/` — artigos do blog.
- `scripts/` — utilitários (coleta de artigos, geração de capas por IA).

## Como editar
- **Conteúdo simples (textos):** editar direto os arquivos `.html` na raiz.
- **Mudanças estruturais / em todas as páginas:** editar `build.py` e rodar `python3 build.py`.
- **Pré-visualizar localmente:** `python3 -m http.server 8123` e abrir <http://localhost:8123/>.

## Publicação
A cada `git push` na branch `main`, o GitHub Pages atualiza o site automaticamente.
