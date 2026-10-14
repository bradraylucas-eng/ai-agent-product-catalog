# Agent Product Catalog — agent-discoverability pack

Machine-readable discovery assets for **Agent Products by bradray2**, Brad Lucas's line of
AI-agent tools and datasets sold on Gumroad (https://bradray2.gumroad.com).

Intended repo name: **`ai-agent-product-catalog`**
Intended GitHub Pages site: https://bradraylucas-eng.github.io/ai-agent-product-catalog/
Store: https://bradray2.gumroad.com

## What's in the pack

| Folder/file | What it is |
|---|---|
| `site/index.html` | Human + machine-readable single-page catalog. Carries an embedded schema.org `ItemList` JSON-LD with `Product` + `Offer` data for the 4 live products. |
| `site/products.json` | Standalone schema.org `ItemList` JSON-LD — live products only, each with an `Offer` (price USD, `InStock`, Gumroad URL). |
| `site/catalog.json` | Enriched catalog: store info, generated date, purchase instructions, and all 17 products (`live` / `coming_soon`; URLs only on live products). |
| `site/llms.txt` | llms.txt-format agent summary: available-now list with prices/links, coming-soon list (no links), and links to the machine files. |
| `site/llms-full.txt` | Full agent text: store intro, purchase + license notes, every product with summary. |
| `site/robots.txt` | Allows all crawlers, explicitly including GPTBot, ClaudeBot, Claude-Web, Google-Extended, PerplexityBot, CCBot; points to `sitemap.xml`. |
| `site/sitemap.xml` | Sitemap for the Pages URLs (/, llms.txt, llms-full.txt, products.json, catalog.json). |
| `mcp-catalog-server/` | Read-only MCP server (FastMCP) exposing the catalog as tools: `list_products`, `get_product`, `purchase_info`. No payments, no purchases. |

## Accuracy rules baked in

- Prices and URLs are taken exactly from `agent-catalog.json` (the authoritative source).
- Coming-soon products carry **no URLs and no Offers** anywhere in the pack.
- No sales or revenue claims appear anywhere.
- Product summaries are 1–2 sentence summaries of the published Gumroad listing copy.
- When a coming-soon product launches, regenerate the pack from the updated catalog so its URL and Offer appear everywhere.

## Publishing to GitHub Pages

1. Create repo `ai-agent-product-catalog` under the `bradraylucas-eng` org/user.
2. Copy the `site/` contents to the repo root (or `docs/`).
3. Enable GitHub Pages on the repo (branch root or `docs/`). The pages above are written against the Pages URL in the table.
4. The MCP server folder can live in the same repo as source code for tool authors.
