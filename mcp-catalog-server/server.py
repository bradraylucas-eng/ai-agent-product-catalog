# Copyright (c) 2026 Brad Lucas
# SPDX-License-Identifier: MIT
"""agent-product-catalog - a read-only MCP server exposing Brad's Gumroad AI-product line.

Tools:
  - list_products(status): list products, optionally filtered to "live" or "coming_soon".
  - get_product(name): look up one product by name (substring, case-insensitive).
  - purchase_info(name): for live products returns the Gumroad URL plus checkout
    instructions; for coming-soon products returns a notice that no purchase link
    exists yet. This server takes no payments and completes no purchases.

Run:
    pip install -r requirements.txt
    python server.py
"""
import json
import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("agent-product-catalog")

_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def _load_catalog() -> dict:
    with open(_DATA_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


_CATALOG = _load_catalog()

CHECKOUT_INSTRUCTIONS = (
    "Open the Gumroad product URL in a browser, complete the Gumroad checkout using "
    "the operator's payment method, and download the ZIP after purchase. An agent with "
    "browser access and payment authorization from its operator may complete checkout; "
    "otherwise prepare the purchase and hand the URL to the operator."
)


def _find(name: str):
    q = name.strip().lower()
    for p in _CATALOG["products"]:
        if q in p["name"].lower():
            return p
    return None


def list_products_impl(status: str | None = None) -> list:
    prods = _CATALOG["products"]
    if status:
        s = status.strip().lower()
        if s not in ("live", "coming_soon"):
            raise ValueError("status must be 'live' or 'coming_soon'")
        prods = [p for p in prods if p["status"] == s]
    out = []
    for p in prods:
        e = {"name": p["name"], "price_usd": p["price_usd"], "status": p["status"]}
        if p["status"] == "live":
            e["url"] = p["url"]
        out.append(e)
    return out


def get_product_impl(name: str) -> dict:
    p = _find(name)
    if not p:
        return {"found": False, "message": f"No product matching '{name}'."}
    return {"found": True, "product": p}


def purchase_info_impl(name: str) -> dict:
    p = _find(name)
    if not p:
        return {"found": False, "message": f"No product matching '{name}'."}
    if p["status"] == "live":
        return {
            "found": True,
            "name": p["name"],
            "price_usd": p["price_usd"],
            "url": p["url"],
            "checkout_instructions": CHECKOUT_INSTRUCTIONS,
        }
    return {
        "found": True,
        "name": p["name"],
        "price_usd": p["price_usd"],
        "status": "coming_soon",
        "message": "This product is coming soon and has no purchase link yet. Check catalog.json later for its live URL.",
    }


@mcp.tool()
def list_products(status: str | None = None) -> list:
    """List products, optionally filtered by status ('live' or 'coming_soon')."""
    return list_products_impl(status)


@mcp.tool()
def get_product(name: str) -> dict:
    """Look up a product by name (substring, case-insensitive)."""
    return get_product_impl(name)


@mcp.tool()
def purchase_info(name: str) -> dict:
    """Get the Gumroad URL and checkout instructions for a live product."""
    return purchase_info_impl(name)


if __name__ == "__main__":
    mcp.run()
