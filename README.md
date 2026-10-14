# agent-product-catalog MCP server

A read-only [Model Context Protocol](https://modelcontextprotocol.io) server exposing the
**Agent Products by bradray2** catalog — Brad Lucas's line of machine-readable AI-agent tools
and datasets sold on Gumroad (https://bradray2.gumroad.com).

It is **read-only**: it lists products and hands out purchase links + checkout instructions.
It takes no payments and completes no purchases.

## Install

```bash
pip install -r requirements.txt   # pins mcp>=1.6.0,<2 (SDK 2.x renamed FastMCP)
python server.py                  # runs over stdio
```

## Tools

- `list_products(status)` — list all 17 products; optional status filter: `"live"` or `"coming_soon"`.
- `get_product(name)` — look up one product by name (substring, case-insensitive).
- `purchase_info(name)` — live product → Gumroad URL + checkout instructions; coming-soon product → notice that no link exists yet.

## Claude Desktop config

```json
{
  "mcpServers": {
    "agent-product-catalog": {
      "command": "python",
      "args": ["/path/to/mcp-catalog-server/server.py"]
    }
  }
}
```

## Generic MCP config (stdio)

```json
{
  "command": "python",
  "args": ["server.py"],
  "cwd": "/path/to/mcp-catalog-server"
}
```

## Data

`data.json` is a copy of the enriched catalog generated 2026-10-14 (live products carry URLs;
coming-soon products carry no URLs and no offers). The server reads it at startup.

## License

MIT — © Brad Lucas. See `LICENSE`.
