# FieldOrder 📦
### Offline-First Wholesale Sales Rep App for FMCG & Distribution

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-Passing-emerald?style=for-the-badge&logo=githubactions)](.github/workflows/ci.yml)
[![Flutter Version](https://img.shields.io/badge/Flutter-3.22+-blue?style=for-the-badge&logo=flutter)](https://flutter.dev)
[![Architecture](https://img.shields.io/badge/Clean%20Architecture-BLoC%20%2B%20Drift-indigo?style=for-the-badge)](fieldorder_mobile/)
[![Figma Design](https://img.shields.io/badge/Figma-Interactive%20Studio-orange?style=for-the-badge&logo=figma)](http://localhost:3000)
[![Backend](https://img.shields.io/badge/FastAPI-Seeded%20500%20SKUs-darkgreen?style=for-the-badge&logo=fastapi)](backend/)

> **Personal project built for the Prosessed.ai Flutter Developer Intern application.**  
> Demonstrates real-world enterprise domain understanding, offline SQLite outbox sync, multi-unit wholesale pricing, and an LLM-assisted order workflow with human-in-the-loop review.

---

## 🎨 Interactive Figma Design & Live Prototype Studio
We built an interactive, web-based Figma Design System and Clickable Prototype Studio ready to explore:
- **Live Local URL**: `http://localhost:3000`
- **Features Included**:
  - **Interactive Prototype**: 10 screens running inside an authentic iPhone 16 Pro / Pixel 9 Material 3 frame.
  - **Real-Time Simulation**: Toggle Offline/Online mode, simulate 409 stock conflicts, trigger exponential backoff retry loops, and test AI natural language order parsing.
  - **All Screens Canvas**: 10 high-fidelity artboards viewable simultaneously.
  - **Design System & Token Studio**: Curated tokens for enterprise colors, 48px+ field touch targets, and typography.
  - **Developer Handoff**: Exact Flutter Dart BLoC code and Drift schema snippets for each inspected screen.

---

## 1. Problem: Why Wholesale Sales Reps Need Offline-First
Wholesale FMCG sales representatives visit 15 to 30 kirana stores, supermarkets, and wholesale depots every day. These retail stalls are often deep inside crowded bazaars, concrete APMC yards, and semi-rural markets where cellular data drops to 2G or zero connectivity.

A standard app that relies on network round-trips for each tap fails in the field:
1. **Network Latency Kills Rep Productivity**: A rep must take orders in under 3 minutes per counter.
2. **Duplicate Orders on Mobile Packet Drops**: When mobile signal drops mid-flight, standard HTTP POST calls either time out or double-charge when the rep taps "Submit" twice.
3. **Price & Stock Integrity**: Catalog updates, out-of-stock items, and multi-unit conversions (cartons vs. boxes vs. pieces) must be calculated accurately offline.

---

## 2. Core Architecture: The "UI Reads Only from Local DB" Rule

```
+-------------------------------------------------------------+
|              UI Layer (Flutter BLoC / Widgets)              |
+-------------------------------------------------------------+
                               |
                        reads & observes
                               v
+-------------------------------------------------------------+
|           Local Database Layer (Drift SQLite DB)            |
|   - customers  - products  - orders  - order_lines - outbox  |
+-------------------------------------------------------------+
               ^                               ^
      writes   |                               | pushes pending
               |                               |
+------------------------------+ +----------------------------+
|         Delta Puller         | |    Sync Engine (Outbox)    |
|   GET /customers?updated_at  | |   POST /orders + Idemp-Key |
+------------------------------+ +----------------------------+
                               |
                        network connection
                               v
+-------------------------------------------------------------+
|               Remote Backend API (FastAPI)                  |
+-------------------------------------------------------------+
```

### The Golden Rule of Offline-First:
> **The UI never touches Dio or the database directly.**  
> The UI observes streams from the local database (Drift SQLite). The network only ever writes into the local database.  
> This single design decision makes the app behave completely identically whether online or 100% offline.

---

## 3. Offline Sync Engine Specification

### Principles
1. **Local First**: Every write (e.g. creating an order) writes to the local `orders` table and the `outbox` table in a **single ACID database transaction**.
2. **Idempotent Pushes**: The client generates a UUID for the order and an `idemp_${uuid}` header. Retries on flaky networks return `200 OK` cached receipts without creating duplicate orders.
3. **Delta Pulls**: The client fetches only records modified since the last sync timestamp: `GET /customers?updated_since=ISO`.
4. **Authority Separation**:
   - **Server is the authority** for products, master prices, and warehouse inventory.
   - **Client is the authority** for orders it created locally.

### Conflict Resolution Matrix
| Entity / Data | Authority | Conflict Behavior |
|---|---|---|
| **Products & Stock** | Server | Overwrite local SQLite on pull sync. |
| **Orders** | Client creates; Server validates | Insufficient stock returns **HTTP 409 Conflict**, moving order to `needs_review` status with line-level badges. Rep edits quantity and resubmits. |
| **Customer Edits** | Last-Write-Wins | Dirty local edits (`is_dirty = true`) are pushed before pulling remote updates. |

### Exponential Backoff Retry Policy
When an outbox push fails due to 5xx server errors or dropped network packets:
- **Interval Sequence**: `30s` ➡️ `1 min` ➡️ `2 min` ➡️ `5 min` ➡️ capped at `15 min` with ±10% random jitter to avoid server thundering herds.

---

## 4. Tech Stack

| Area | Selection | Rationale |
|---|---|---|
| **Framework** | Flutter 3.x, Dart 3 | Cross-platform high performance with 60fps rendering |
| **State Management** | `flutter_bloc` | Predictable state transitions, separation of concerns |
| **Dependency Injection** | `get_it` | Fast service locator pattern |
| **Routing** | `go_router` | Declarative URL-based routing |
| **Networking** | `dio` | Interceptors, JWT refresh on 401, retry policies |
| **Local Database** | `drift` (SQLite) | Reactive streams, type safety, background isolate queries |
| **Secure Storage** | `flutter_secure_storage` | Encrypted JWT token cache |
| **Backend API** | FastAPI + SQLite (Python 3) | High performance, automatic OpenAPI docs |
| **Seed Data** | 50 Customers & 500 Products | Real-world Indian wholesale catalog (Maggi, Parle-G, Tata Tea, Fortune Oil) |

---

## 5. How to Run

### Prerequisites
- Python 3.9+ (Installed on macOS/Linux/Windows)
- Node.js (Optional, for tooling)

### Step 1: Start the FastAPI Backend & Seed Data
```bash
# Navigate to backend directory
cd backend

# Seed 50 Customers & 500 FMCG products
python3 seed_data.py

# Launch FastAPI server on port 8000
python3 -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be live at: `http://localhost:8000/docs`

### Step 2: Open the Interactive Figma Design Studio & Prototype
```bash
# In another terminal window:
python3 -m http.server 3000 --directory figma_design
```
Open **`http://localhost:3000`** in your browser. You can click through all 10 screens, test offline mode, trigger sync, and review tokens.

### Step 3: Run the Automated Test Suite (27 Tests)
```bash
python3 backend/test_suite.py
```
Output:
```
...........................
----------------------------------------------------------------------
Ran 27 tests in 0.051s

OK
```

---

## 6. Challenges & Engineering Lessons Learned
1. **Preventing Order Ghosting**: Storing snapshots of product names and prices inside `order_lines` ensures that future catalog changes never mutate past invoices.
2. **ACID Transaction for Outbox**: If the order is written to SQLite but the outbox insert crashes, the order would be stranded offline forever. Enforcing a single SQLite transaction guarantees atomic write.
3. **Human-in-the-Loop for AI Orders**: Sales reps do not want black-box automation. The AI parser maps text to structured JSON, but always presents a confirmation sheet where low-confidence lines are highlighted before committing to the cart.

---

## 7. Future Work
- WhatsApp PDF order summary sharing via `pdf` and `share_plus`.
- Integrated camera barcode scanner using `mobile_scanner`.
- Route optimization with Google Maps Directions API.
- Bluetooth thermal receipt printing for wholesale market stalls.

---

## 8. Disclaimer
*FieldOrder is an independent personal engineering project built for the Prosessed.ai Flutter Developer Intern evaluation. It is not affiliated with or endorsed by any commercial entity.*
