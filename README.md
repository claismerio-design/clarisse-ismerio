# Site — Clarisse Ismério · Pesquisas Históricas

Site institucional da historiadora **Clarisse Ismério** (biografia, livros, ebooks, palestras e blog).
Site estático (HTML/CSS), publicado via **GitHub Pages**.

## Estrutura
- `index.html` — redireciona para o site escolhido (Opção 1).
- `opcao-1/` — **identidade visual em uso** (Clássica & Elegante). É o site real.
- `opcao-2/`, `opcao-3/` — opções de identidade visual alternativas (referência).
- `escolha.html` — tela de comparação das 3 identidades.
- `assets/` — logo, fotos e o CSS (`site.css`).
- `build.py` — gera as páginas das 3 opções a partir de templates. Rode `python3 build.py` após editar o conteúdo no `build.py`.
- `data/` — artigos do blog.
- `scripts/` — utilitários (coleta de artigos, geração de capas por IA).

## Como editar
- **Conteúdo simples (textos):** editar direto os arquivos `.html` dentro de `opcao-1/`.
- **Mudanças estruturais / em todas as páginas:** editar `build.py` e rodar `python3 build.py`.
- **Pré-visualizar localmente:** `python3 -m http.server 8123` e abrir <http://localhost:8123/>.

## Publicação
A cada `git push` na branch `main`, o GitHub Pages atualiza o site automaticamente.
