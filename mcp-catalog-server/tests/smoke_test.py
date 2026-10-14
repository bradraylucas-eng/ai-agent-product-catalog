"""Smoke test: import the data layer and assert catalog invariants."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server import list_products_impl, get_product_impl, purchase_info_impl

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data.json")
with open(DATA) as fh:
    catalog = json.load(fh)

prods = catalog["products"]
assert len(prods) == 17, f"expected 17 products, got {len(prods)}"

live = [p for p in prods if p["status"] == "live"]
assert len(live) == 4, f"expected 4 live products, got {len(live)}"
for p in live:
    assert p.get("url", "").startswith("https://bradray2.gumroad.com/l/"), f"live product missing URL: {p['name']}"

coming = [p for p in prods if p["status"] == "coming_soon"]
assert len(coming) == 13, f"expected 13 coming-soon, got {len(coming)}"
assert all("url" not in p for p in coming), "coming-soon products must not carry URLs"

info = purchase_info_impl("Source Finder Vol. 2")
assert info["url"] == "https://bradray2.gumroad.com/l/gshxcy", f"unexpected URL: {info.get('url')}"

cs = purchase_info_impl("Complete Bundle")
assert "url" not in cs, "coming-soon purchase_info must not return a URL"
assert cs["status"] == "coming_soon"

all_listed = list_products_impl()
assert len(all_listed) == 17
assert len(list_products_impl("live")) == 4
gp = get_product_impl("agentproof")
assert gp["found"] and "AgentProof" in gp["product"]["name"]

print("SMOKE TEST PASSED: 17 products, 4 live with URLs, 13 coming-soon without URLs, purchase_info OK")
