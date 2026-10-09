# FieldOrder 📦
### Enterprise Offline-First Mobile System for Wholesale FMCG & Distribution

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-Passing-emerald?style=for-the-badge&logo=githubactions)](.github/workflows/ci.yml)
[![Flutter Version](https://img.shields.io/badge/Flutter-3.22+-blue?style=for-the-badge&logo=flutter)](https://flutter.dev)
[![Architecture](https://img.shields.io/badge/Clean%20Architecture-BLoC%20%2B%20Drift-indigo?style=for-the-badge)](fieldorder_mobile/)
[![Backend](https://img.shields.io/badge/FastAPI-Seeded%20500%20SKUs-darkgreen?style=for-the-badge&logo=fastapi)](backend/)
[![Tests Status](https://img.shields.io/badge/Automated%20Tests-67%2F67%20Passing-success?style=for-the-badge)](test_e2e_fieldorder.py)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

> 📄 **[Download the Full Technical Report & Interview Guide (PDF)](FieldOrder_Project_Report.pdf)**  
> Comprehensive 4-page publication report covering architecture, sync engine invariants, integer-paise math, and interview Q&A.

---

## ⚡ 30-Second Elevator Pitch
> *"FieldOrder is an offline-first Flutter application built for wholesale field sales reps who take bulk orders in dense markets and rural dead zones with weak or no cellular data. Instead of making network roundtrips on every click, FieldOrder enforces a strict 'local-first' architecture where the UI only reads from a reactive Drift SQLite database. Orders are committed locally in a single ACID transaction alongside an Outbox table, then synced to the FastAPI backend using UUID-based Idempotency Keys with exponential backoff. It also guarantees financial precision by storing money in integer paise and includes an AI-assisted voice/text order entry parser with human-in-the-loop review."*

---

## 🎯 1. Business Domain: Where & Why is it Used?

### The Operational Environment
Wholesale FMCG (Fast-Moving Consumer Goods), pharmaceutical supply, and hardware distributors operate in high-velocity, low-connectivity field environments:
- **Location**: Crowded wholesale agricultural produce markets (APMC yards), dense inner-city bazaar alleys, and semi-rural distributor warehouses.
- **Physical Conditions**: Thick concrete walls and metal tin roofs that degrade cellular reception to 2G, intermittent Edge, or complete dead zones.
- **Time Pressure**: Sales reps visit **15 to 30 retail shops (kiranas, stalls) per day**. A rep has only **3 to 5 minutes** per counter before the shopkeeper turns to other customers or distributors.

### Why Standard Mobile Apps Fail in the Field:
1. **Network Latency Destroys Rep Productivity**: Standard apps make API requests for prices, stock, or discounts. When a rep stands in a dead zone, loading spinners freeze the screen and kill sales throughput.
2. **Duplicate Invoices on Packet Loss**: When mobile data drops mid-flight during a standard HTTP `POST /orders`, the request reaches the ERP but the confirmation response drops. Reps inevitably tap *"Submit"* again, creating duplicate invoices and disastrous double-deliveries.
3. **Wholesale Pricing Complexity**: Wholesale FMCG orders involve multi-unit conversions (e.g., 1 carton = 24 pieces; 1 box = 12 pieces) with tiered wholesale discounts. Float rounding mistakes cause balance mismatches with the ERP ledger.
4. **Data Sync Conflicts**: If two reps sell the last stock of an item while both are offline, the system must have a deterministic conflict policy instead of silently dropping data.

---

## 🏗️ 2. Core Architecture: The "Golden Rule"

```
+-------------------------------------------------------------------------+
|                    UI Layer (Flutter BLoC / Widgets)                    |
+-------------------------------------------------------------------------+
                                     |
                              reads & observes (Drift Streams)
                                     v
+-------------------------------------------------------------------------+
|                 Local Database Layer (Drift SQLite DB)                  |
|    - customers    - products    - orders    - order_lines    - outbox   |
+-------------------------------------------------------------------------+
                ^                                         ^
         writes | (Delta Upsert)                          | (Pushes Outbox)
+-------------------------------+         +-------------------------------+
|         Delta Puller          |         |      Sync Engine (Outbox)     |
|    GET /customers?updated_at  |         |    POST /orders + Idemp-Key   |
+-------------------------------+         +-------------------------------+
                                     |
                              network transport
                                     v
+-------------------------------------------------------------------------+
|                     Remote Backend API (FastAPI)                        |
+-------------------------------------------------------------------------+
```

### The Golden Rule of Offline-First:
> **The UI layer never calls network APIs (Dio) or handles remote HTTP responses directly.**  
> The UI observes reactive streams from the local database (Drift SQLite). The network layer only ever writes into the local database.  
> This architectural invariant guarantees that the app behaves with **identical speed and UI predictability** whether the rep has 5G or zero bars.

---

## 🔄 3. The 7-Step Field Sales Rep Workflow

```
[1. Login & Delta Pull] ──► [2. Customer Search & 360] ──► [3. Catalog & Multi-Unit Pick]
         │                              │                                  │
         ▼                              ▼                                  ▼
Morning JWT auth;             Sub-300ms indexed search;          Carton (24) / Box (12) / Piece;
pulls updated products/       views credit limits and            live stock status badges
customers into SQLite         outstanding balance (₹15.4k)

                                        │
                                        ▼
[6. Idempotent Sync]    ◄── [5. ACID Outbox Commit]    ◄── [4. Cart & Integer-Paise Math]
         │                              │                                  │
         ▼                              ▼                                  ▼
Background worker pushes      Atomic SQLite transaction:         Line discounts; strict paise math
with Idempotency-Key;         writes to 'orders' & 'outbox';     (₹1 = 100 paise) preventing
handles 409 conflicts         rep moves to next shop instantly   floating-point discrepancies
```

* **Step 7 (AI Natural Language / Voice Order Entry)**: Sales reps can paste WhatsApp messages or speak orders (*"10 carton Maggi noodles aur 5 box Parle-G bhej dena Raju Traders ko"*). The backend extracts structured line items and presents an editable sheet for rep confirmation before cart ingestion.

---

## 📱 4. All 10 Screens Overview (Full Mobile App Showcase)

FieldOrder features a complete 10-screen workflow running inside an authentic iPhone 16 Pro / Pixel 9 Material 3 frame:

| # | Screen | Key Functionality |
|---|---|---|
| **1** | **Dashboard** | Daily KPIs (Today's Orders, Bookings, Target), Sync Health card, Quick Action tiles. |
| **2** | **Customers Directory** | Sub-300ms debounced search, city filter chips (Mumbai, Pune, Bengaluru), balance badges. |
| **3** | **Customer 360** | Credit limit utilization, ₹15,400 outstanding balance, order history, 1-tap reorder. |
| **4** | **Product Catalog** | 500 wholesale SKUs, 6 categories, fast pack unit toggles (+ Carton, + Box, + Piece). |
| **5** | **Cart & Pricing Engine** | Multi-tier pack multipliers, line-item percentage discounts, integer-paise totals. |
| **6** | **Order Confirmation** | Credit verification, wholesale delivery notes, atomic outbox dispatch. |
| **7** | **Outbox & Sync Manager** | Queue status, exponential backoff timers, manual 'Sync Now', conflict inspector. |
| **8** | **Order History** | Historical bookings, synced server order numbers, line-item price snapshots. |
| **9** | **AI Order Parser** | Speech-to-text NLP parser with human-in-the-loop review sheet. |
| **10** | **Login & Rep Switcher** | JWT authentication, secure token storage, route assignment. |

---

## ⚙️ 5. Core Engineering Decisions & Deep Dives

### 1. Financial Precision: Integer Paise Storage
Floating-point numbers (`double` in Dart, `float` in Python) cannot accurately represent base-10 decimals, resulting in binary rounding errors like `0.1 + 0.2 = 0.30000000000000004`.  
- **Implementation**: Every monetary amount in FieldOrder is represented strictly as **integer Paise** ($\text{₹}1 = 100\text{ paise}$).
- **Database Schema**: `price_paise`, `subtotal_paise`, `discount_paise`, `total_paise`, `outstanding_balance_paise`.
- **Formatting**: Converted to rupees only at the UI boundary (`₹${(paise / 100).toFixed(2)}`).

### 2. ACID Transactional Outbox (Zero Stranded Orders)
To eliminate stranded offline orders (where an order is written to SQLite but the sync job crashes before queueing it):
```sql
BEGIN TRANSACTION;
INSERT INTO orders (id, customer_id, status, total_paise, created_at) VALUES (...);
INSERT INTO outbox (id, order_id, idempotency_key, attempts, next_attempt_at, status) VALUES (...);
COMMIT;
```
If the app process is terminated mid-write, SQLite rolls back completely, ensuring absolute data integrity.

### 3. Idempotent HTTP Pushes & Duplicate Prevention
- Each outbox record generates a client-side UUID: `Idempotency-Key: idemp_${uuid}`.
- If a connection drops after the server receives the order, the client retries with the **same** idempotency key.
- The server checks its `idempotency_keys` table and returns the original `200/201 Synced` cached response without creating duplicate invoices or deducting inventory twice.

### 4. Exponential Backoff with Jitter
Failed sync requests retry using exponential backoff with jitter to prevent a thundering herd on the backend when cellular service restores across an entire market district:
$$\text{Delay} = \min\left(300\text{ seconds}, 2^{\text{attempts}} \times 5\text{ seconds}\right) \pm \text{jitter}$$

### 5. Authority Separation & 409 Conflict Policy
- **Server Wins**: The ERP is the single source of truth for catalog prices and warehouse inventory.
- **Client Wins**: The client has authority over order lines and timestamps it created locally.
- **Stock Depletion**: If inventory ran out while the rep was offline, the server returns HTTP `409 Conflict` with line-level reasons. The client halts automatic retries, flags the order as `needs_review`, and allows the rep to adjust quantities with the shopkeeper.

---

## 🛠️ 6. Technology Stack Matrix

| Layer | Selection | Key Engineering Justification |
|---|---|---|
| **Mobile UI** | **Flutter 3.22+ / Dart 3** | Cross-platform 60fps rendering with native Ahead-of-Time compilation. |
| **State Management** | **`flutter_bloc`** | Unidirectional event-driven state transitions, predictable testing. |
| **Local Database** | **`drift` (SQLite)** | Type-safe SQL queries, reactive stream watchers, background isolate threading. |
| **Networking** | **`dio`** | Interceptors for Idempotency-Key headers and automatic 401 JWT refresh. |
| **Secure Cache** | **`flutter_secure_storage`** | Encrypted hardware keychain/keystore for JWT tokens. |
| **Backend API** | **FastAPI + SQLite** | High throughput, asynchronous endpoints, auto OpenAPI/Swagger documentation. |
| **AI NLP Engine** | **FastAPI NLP Parser** | Fuzzy-matches mixed Hindi/English wholesale jargon to product catalog IDs. |

---

## 🚀 7. How to Run Locally

### Prerequisites
- Python 3.9+
- Modern Web Browser (Chrome, Safari, Firefox, Edge)

### Step 1: Start the Backend & Seed Database
```bash
# Seed 50 Customers & 500 FMCG products
python3 backend/seed_data.py

# Launch FastAPI server on port 8000
python3 -m uvicorn backend.server:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation is live at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Step 2: Launch the Clean Prototype App
```bash
# In a second terminal:
python3 -m http.server 3000 --directory figma_design
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser:
- Center phone mockup with iPhone 16 Pro and Pixel 9 Material 3 toggle.
- Simulate Offline toggle and Light/Dark mode switch.
- Responsive full-screen presentation on mobile devices.

---

## 🧪 8. Automated Test Suites (67/67 Tests Passing)

Run both automated test suites with zero manual setup:

```bash
# 1. Run the Full End-to-End Test Suite (40 tests - Frontend Prototype & Backend API)
python3 test_e2e_fieldorder.py

# 2. Run the Backend Domain Unit Test Suite (27 tests)
python3 backend/test_suite.py
```

### Test Results Summary:
```text
=========================================================================
    FieldOrder Full System Automated E2E Verification Suite              
=========================================================================
[1/3] Clean Prototype Frontend: 16/16 Passed (All 10 Screens, Responsive CSS, Device Switcher)
[2/3] Backend API Services:     8/8   Passed (Health, JWT Auth, 50 Customers, 500 Products, AI NLP)
[3/3] End-to-End Order Cycle:   16/16 Passed (Paise Math, ACID Outbox, Idempotency Replay, History)
=========================================================================
  ALL 40 AUTOMATED TESTS PASSED SUCCESSFULLY! (100% HEALTHY)  
=========================================================================

backend/test_suite.py:
Ran 27 tests in 0.033s - OK (100% Passing)
```

---

## 💼 9. Interview Mastery: Top Technical Questions & Answers

<details>
<summary><b>Q1: Why does the UI read only from the local database instead of calling APIs directly?</b></summary>
<br/>
<i>"In field sales operations, network connectivity is completely non-deterministic. If UI widgets call API endpoints directly, users face loading spinners, network timeouts, and unpredictable screen states. By observing reactive Drift SQLite streams, the UI always renders in under 16ms from indexed disk storage. The network layer acts strictly as a background worker that writes to the local DB. Whether the rep is on 5G or in a concrete basement, the user experience is identical."</i>
</details>

<details>
<summary><b>Q2: What happens if the phone battery dies or the app is killed mid-sync?</b></summary>
<br/>
<i>"Because order creation and outbox queuing are committed in a single ACID transaction, an order cannot exist without being queued. If the app is killed mid-HTTP-request, the order remains in the local SQLite outbox as 'pending'. When the rep re-opens the app or connectivity returns, the sync worker retries with the original Idempotency-Key. If the server already processed the order before the crash, it returns the cached 200/201 receipt without creating a duplicate."</i>
</details>

<details>
<summary><b>Q3: How exactly do you prevent duplicate orders when mobile signal drops?</b></summary>
<br/>
<i>"We use client-generated UUIDs and idempotency headers. When the order is saved locally, the client generates a unique <code>Idempotency-Key: idemp_${uuid}</code>. The server stores idempotency keys and cached response payloads. If a retried request arrives with the same key, the server returns the cached response rather than inserting a duplicate order or deducting stock twice."</i>
</details>

<details>
<summary><b>Q4: How do you handle stock conflicts if an item runs out while the rep is offline?</b></summary>
<br/>
<i>"We enforce a clear authority model: the server is the single authority for stock and prices. When the rep syncs, if stock is insufficient, the backend returns an HTTP 409 Conflict with line-level error details (e.g. 'Only 5 pieces in stock, requested 24'). The sync engine stops auto-retries, sets the order state to 'needs_review', and displays an alert in the rep's Outbox for the rep to adjust with the customer."</i>
</details>

<details>
<summary><b>Q5: Why did you use integer paise instead of double/float for currency?</b></summary>
<br/>
<i>"IEEE 754 floating-point numbers introduce binary decimal errors (e.g., <code>0.1 + 0.2 = 0.30000000000000004</code>). In wholesale trade with large carton multipliers and percentage discounts, these fractions accumulate into balance mismatches with the ERP ledger. Storing values strictly as integer paise (₹1 = 100 paise) guarantees arithmetic accuracy across SQLite, Dart, and Python."</i>
</details>

<details>
<summary><b>Q6: How would you optimize a 10,000-item product catalog in Flutter for 60fps?</b></summary>
<br/>
<i>"First, run Drift SQLite queries on a background Dart isolate using <code>compute()</code> or Drift's isolate connection so deserialization never blocks the UI isolate. Second, enforce pagination (<code>LIMIT 50 OFFSET X</code>) with composite indexes on <code>(category, name)</code> and <code>barcode</code>. Third, in Flutter, use <code>ListView.builder</code> with <code>prototypeItem</code> or <code>itemExtent</code> so the framework recycles widgets without calculating variable heights on scroll."</i>
</details>

<details>
<summary><b>Q7: How do you secure the AI API key in mobile applications?</b></summary>
<br/>
<i>"Never bundle API keys or call LLM endpoints directly from the client APK, as decompiling exposes the secret. Instead, the mobile app sends the unstructured text to our authenticated backend endpoint <code>POST /ai/parse-order</code> using the rep's JWT token. The backend verifies authorization, injects the compact product catalog into the prompt, queries the model using an environment variable, validates the output schema, and returns validated product IDs to the app."</i>
</details>

---

## 💡 10. Engineering Lessons Learned
1. **Preventing Order Ghosting**: Storing snapshots of product names and unit prices inside `order_lines` ensures that future catalog price updates never alter historical invoices.
2. **Atomic Outbox Guarantees Zero Stranded Orders**: Wrapping local order persistence and outbox queuing in a single ACID transaction ensures that an un-synced order is never lost on crash.
3. **Integer Paise Storage Eliminates Financial Drift**: Decimal floats cause rounding discrepancies on bulk wholesale cart items; integer paise ensures 100% accounting accuracy.
4. **Human-in-the-Loop for AI Orders**: The AI parser maps text to structured JSON, but always presents a confirmation sheet where low-confidence lines are highlighted before committing to the cart.

---

## 📄 License & Disclaimer
Distributed under the MIT License. See [LICENSE](LICENSE) for details.  
*FieldOrder is an independent personal engineering portfolio project built for technical evaluation.*
