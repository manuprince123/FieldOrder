#!/usr/bin/env python3
"""
FieldOrder End-to-End Automated Test & Verification Suite
==========================================================
Validates the complete FieldOrder system:
1. Prototype Frontend (localhost:3000):
   - All 10 screens loaded inside the phone frame
   - Sidebars and desktop inspect panels completely removed
   - Centered phone mockup with device switcher (iPhone 16 Pro / Pixel 9)
   - Floating controls (Simulate Offline, Theme toggle, Online pill)
   - Mobile responsive full-screen CSS rules
2. Backend API (localhost:8000):
   - Live server health and JWT authentication
   - 50 seeded customers with outstanding balances
   - 500 seeded product SKUs with multi-unit packing
   - Natural language AI order parser
   - Transactional order placement with idempotency
   - Idempotent duplicate prevention & sync verification
"""

import urllib.request
import urllib.error
import json
import uuid
import sys
import re
import time

FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8000"

GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

passed_count = 0
failed_count = 0

def test_assert(desc, condition, details=""):
    global passed_count, failed_count
    if condition:
        passed_count += 1
        print(f"  {GREEN}✓{RESET} {desc}")
        if details:
            print(f"    {BLUE}↳ {details}{RESET}")
    else:
        failed_count += 1
        print(f"  {RED}✗ FAIL:{RESET} {desc}")
        if details:
            print(f"    {YELLOW}↳ {details}{RESET}")

def fetch_url(url, method="GET", data=None, headers=None):
    h = headers or {}
    if data and "Content-Type" not in h:
        h["Content-Type"] = "application/json"
    body = json.dumps(data).encode("utf-8") if (data and isinstance(data, dict)) else data
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read()
            if "application/json" in content_type:
                return resp.status, json.loads(raw.decode("utf-8"))
            return resp.status, raw.decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw.decode("utf-8"))
        except Exception:
            return e.code, raw.decode("utf-8", errors="ignore")
    except Exception as e:
        return 0, str(e)

def main():
    print(f"\n{BOLD}{BLUE}========================================================================={RESET}")
    print(f"{BOLD}{BLUE}    FieldOrder Full System Automated E2E Verification Suite              {RESET}")
    print(f"{BOLD}{BLUE}========================================================================={RESET}\n")

    # ---------------------------------------------------------
    # PART 1: FRONTEND PROTOTYPE TEST (localhost:3000)
    # ---------------------------------------------------------
    print(f"{BOLD}[1/3] Testing Clean Prototype Frontend (localhost:3000)...{RESET}")

    # 1.1 Web Server Availability
    status, html = fetch_url(f"{FRONTEND_URL}/index.html")
    test_assert("Prototype HTTP server is responding (200 OK)", status == 200, f"Status: {status}")

    # 1.2 Title verification
    title_match = re.search(r"<title>(.*?)</title>", html)
    expected_title = "FieldOrder · Offline-First Sales Rep App (Personal Learning Project)"
    test_assert("Clean page title matches requirement", 
                title_match and expected_title in title_match.group(1),
                f"Title: {title_match.group(1) if title_match else 'None'}")

    # 1.3 Sidebars and tabs REMOVED verification
    test_assert("Left sidebar (.screen-flow-nav) removed", "screen-flow-nav" not in html)
    test_assert("Right sidebar (.figma-properties-panel) removed", "figma-properties-panel" not in html)
    test_assert("Top navigation tabs (.figma-tabs) removed", "figma-tabs" not in html)
    test_assert("Clean Arch Code button removed", "btn-primary-action" not in html)

    # 1.4 Center phone frame & controls exist
    test_assert("Centered phone stage (.phone-stage) present", 'class="phone-stage"' in html)
    test_assert("Phone frame (#deviceFrame) present", 'id="deviceFrame"' in html)
    test_assert("Dynamic Island present", 'class="dynamic-island"' in html)
    test_assert("Phone Status Bar present", 'class="phone-status-bar"' in html)
    test_assert("Phone Bottom Nav (#phoneBottomNav) present", 'class="phone-bottom-nav"' in html)
    test_assert("Device switch toggle (iPhone 16 Pro / Pixel 9) present", 'class="device-switch-bar"' in html)
    test_assert("Simulate Offline toggle (#btnToggleOffline) present", 'id="btnToggleOffline"' in html)
    test_assert("Light/Dark theme toggle (#btnThemeToggle) present", 'id="btnThemeToggle"' in html)
    test_assert("Online network indicator (#globalNetIndicator) present", 'id="globalNetIndicator"' in html)

    # 1.5 Verify all 10 screens exist inside the phone container
    expected_screens = [
        ("Dashboard", "screen-dashboard"),
        ("Customers", "screen-customers"),
        ("Customer 360", "screen-customer_detail"),
        ("Catalog", "screen-products"),
        ("Cart", "screen-cart"),
        ("Order Confirmation", "screen-order_confirm"),
        ("Outbox & Sync", "screen-sync_manager"),
        ("Order History", "screen-order_history"),
        ("AI Order Parser", "screen-ai_order"),
        ("Login", "screen-login")
    ]
    print(f"\n  {BOLD}Checking all 10 In-Phone Screens:{RESET}")
    for name, sid in expected_screens:
        exists = f'id="{sid}"' in html
        test_assert(f"Screen: {name} ({sid}) exists in phone container", exists)

    # 1.6 Verify CSS and Responsive Rules
    status_css, css = fetch_url(f"{FRONTEND_URL}/styles.css")
    test_assert("styles.css is served successfully (200 OK)", status_css == 200)
    test_assert("Mobile full-screen responsive rule (@media (max-width: 520px)) present", "@media (max-width: 520px)" in css)
    test_assert("Pixel 9 camera punch-hole styling present", ".pixel-frame .dynamic-island" in css)

    # 1.7 Verify JS Engine
    status_js, js = fetch_url(f"{FRONTEND_URL}/app.js")
    test_assert("app.js is served successfully (200 OK)", status_js == 200)
    test_assert("app.js contains safe navigation (navigateTo)", "function navigateTo(" in js)
    test_assert("app.js contains multi-unit pricing calculation", "units_per_carton" in js or "unit-sel" in js)

    # ---------------------------------------------------------
    # PART 2: BACKEND API TEST (localhost:8000)
    # ---------------------------------------------------------
    print(f"\n{BOLD}[2/3] Testing Backend API Services (localhost:8000)...{RESET}")

    # 2.1 Backend Health
    status, health = fetch_url(f"{BACKEND_URL}/")
    test_assert("Backend health check is online", status == 200 and health.get("status") == "online")

    # 2.2 Rep Authentication (JWT)
    login_payload = {"email": "rep@fieldorder.com", "password": "password123"}
    status, auth_data = fetch_url(f"{BACKEND_URL}/auth/login", method="POST", data=login_payload)
    test_assert("Rep authentication succeeds with JWT tokens", 
                status == 200 and "access_token" in auth_data and "refresh_token" in auth_data,
                f"Rep Name: {auth_data.get('user', {}).get('name', 'N/A')}")
    access_token = auth_data.get("access_token", "")
    auth_headers = {"Authorization": f"Bearer {access_token}"}

    # 2.3 Customers Catalog (50+ Wholesale Accounts)
    status, cust_data = fetch_url(f"{BACKEND_URL}/customers?limit=60", headers=auth_headers)
    total_cust = cust_data.get("total", len(cust_data.get("items", [])))
    test_assert(f"Customers API returns full seeded directory ({total_cust} accounts >= 50)",
                status == 200 and total_cust >= 50,
                f"Sample customer: {cust_data['items'][0]['name']} ({cust_data['items'][0]['city']})")
    first_customer = cust_data["items"][0]

    # 2.4 Products Catalog (500+ SKUs)
    status, prod_data = fetch_url(f"{BACKEND_URL}/products?limit=10", headers=auth_headers)
    total_prod = prod_data.get("total", 0)
    test_assert(f"Products API returns wholesale catalog ({total_prod} SKUs >= 500)",
                status == 200 and total_prod >= 500,
                f"Sample product: {prod_data['items'][0]['name']} [₹{prod_data['items'][0]['price']}]")
    sample_product = prod_data["items"][0]

    # 2.5 Product Search
    status, search_data = fetch_url(f"{BACKEND_URL}/products?search=Maggi", headers=auth_headers)
    test_assert("Product full-text search works ('Maggi')", 
                status == 200 and search_data.get("total", 0) >= 1)

    # 2.6 AI Natural Language Order Parser
    ai_prompt = {
        "text": "Bhai 10 carton Maggi noodles aur 5 box Parle-G urgently bhej dena kal subah",
        "customer_id": first_customer["id"]
    }
    status, ai_res = fetch_url(f"{BACKEND_URL}/ai/parse-order", method="POST", data=ai_prompt, headers=auth_headers)
    items_parsed = ai_res.get("lines", [])
    test_assert("AI Order Parser extracts items and quantities from free text",
                status == 200 and len(items_parsed) >= 1,
                f"Parsed {len(items_parsed)} items (Confidence: {items_parsed[0].get('confidence', 0):.0%})")

    # ---------------------------------------------------------
    # PART 3: END-TO-END TRANSACTION & IDEMPOTENT SYNC LIFECYCLE
    # ---------------------------------------------------------
    print(f"\n{BOLD}[3/3] Simulating Full End-to-End Sales Rep Order Cycle...{RESET}")

    # 3.1 Calculate order pricing with integer paise
    test_order_id = f"ORD-E2E-{uuid.uuid4().hex[:8]}"
    idem_key = f"idemp_{uuid.uuid4().hex[:16]}"
    
    # Pick product with ample stock (>= 50 pieces) and safe piece unit
    sample_product = next((p for p in prod_data.get("items", []) if p.get("stock_qty", 0) >= 50), prod_data["items"][0])
    
    qty = 2
    unit = "piece"
    unit_price = sample_product["price"]
    subtotal = unit_price * qty
    subtotal_paise = int(round(subtotal * 100))
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    order_payload = {
        "id": test_order_id,
        "customer_id": first_customer["id"],
        "notes": "Automated E2E Test Order via Outbox",
        "created_at": now_iso,
        "lines": [
            {
                "product_id": sample_product["id"],
                "unit": unit,
                "quantity": qty,
                "unit_price": unit_price,
                "discount": 0.0
            }
        ]
    }

    # 3.2 Place order with Idempotency Key
    order_headers = dict(auth_headers)
    order_headers["Idempotency-Key"] = idem_key
    status, placed_order = fetch_url(f"{BACKEND_URL}/orders", method="POST", data=order_payload, headers=order_headers)
    test_assert("Order submitted successfully to ERP backend (200/201 Synced)",
                status in (200, 201) and placed_order.get("status") == "synced",
                f"Server Order No: {placed_order.get('server_order_no')} | Net Total: ₹{placed_order.get('total', subtotal):,.2f}")

    # 3.3 Test Idempotency: Re-submitting identical order must return exact cached response without duplicate
    status_dup, placed_dup = fetch_url(f"{BACKEND_URL}/orders", method="POST", data=order_payload, headers=order_headers)
    test_assert("Idempotent replay detected - no duplicate order created",
                status_dup == 200 and placed_dup.get("server_order_no") == placed_order.get("server_order_no"),
                f"Replay server_order_no: {placed_dup.get('server_order_no')}")

    # 3.4 Verify order in ERP Order History
    status, history = fetch_url(f"{BACKEND_URL}/orders?limit=10", headers=auth_headers)
    orders_list = history.get("orders", [])
    found_order = any(o.get("id") == test_order_id for o in orders_list)
    test_assert("New order appears in ERP Order History",
                status == 200 and found_order,
                f"Total orders in history: {len(orders_list)}")

    # ---------------------------------------------------------
    # SUMMARY REPORT
    # ---------------------------------------------------------
    total_tests = passed_count + failed_count
    print(f"\n{BOLD}{BLUE}========================================================================={RESET}")
    if failed_count == 0:
        print(f"{BOLD}{GREEN}  ALL {total_tests} AUTOMATED TESTS PASSED SUCCESSFULLY! (100% HEALTHY)  {RESET}")
    else:
        print(f"{BOLD}{RED}  {failed_count} OF {total_tests} TESTS FAILED. PLEASE REVIEW LOGS.     {RESET}")
    print(f"{BOLD}{BLUE}========================================================================={RESET}\n")

    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
