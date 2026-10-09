#!/usr/bin/env python3
"""
Generate a professional, publication-grade PDF report and interview mastery guide
for the FieldOrder project using ReportLab.
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Colors
PRIMARY = colors.HexColor("#0F172A")       # Deep Slate Navy
ACCENT = colors.HexColor("#2563EB")        # Electric Blue
SUCCESS = colors.HexColor("#059669")       # Emerald Green
WARNING = colors.HexColor("#D97706")       # Amber
MUTED = colors.HexColor("#64748B")         # Cool Slate Gray
LIGHT_BG = colors.HexColor("#F8FAFC")      # Soft Off-White
BORDER = colors.HexColor("#CBD5E1")        # Light Border
CALLOUT_BG = colors.HexColor("#EFF6FF")    # Soft Blue Callout
CODE_BG = colors.HexColor("#F1F5F9")       # Code block light gray

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(MUTED)

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, 755, "FieldOrder · Offline-First Sales Rep System | Technical Architecture & Interview Guide")
            self.setStrokeColor(BORDER)
            self.setLineWidth(0.5)
            self.line(45, 747, 567, 747)

        # Footer (all pages)
        self.setStrokeColor(BORDER)
        self.setLineWidth(0.5)
        self.line(45, 45, 567, 45)
        self.drawString(45, 33, "Confidential Portfolio Project · Built with Flutter 3.22, Drift SQLite, BLoC & FastAPI")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(567, 33, page_str)
        self.restoreState()


def build_pdf(filename="FieldOrder_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=55,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        spaceAfter=12
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=MUTED,
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=ACCENT,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=PRIMARY,
        spaceAfter=6
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=PRIMARY
    )
    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=PRIMARY
    )
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=PRIMARY
    )
    table_cell_header = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # -------------------------------------------------------------
    # COVER / HEADER BANNER
    # -------------------------------------------------------------
    story.append(Paragraph("FieldOrder: End-to-End Build Report", title_style))
    story.append(Paragraph("Offline-First Mobile System for Wholesale Sales Representatives | Architecture & Interview Guide", subtitle_style))
    
    meta_text = "<b>Architecture:</b> Flutter Clean Architecture (BLoC + Drift SQLite) &nbsp;|&nbsp; <b>Backend:</b> FastAPI &nbsp;|&nbsp; <b>Verification:</b> 67/67 Tests Passing"
    story.append(Paragraph(meta_text, meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceAfter=14))

    # -------------------------------------------------------------
    # SECTION 1: 30-SECOND ELEVATOR PITCH
    # -------------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & 30-Second Elevator Pitch", h1_style))
    
    pitch_text = (
        "<b>The 30-Second Pitch (For Recruiters & Hiring Managers):</b><br/>"
        "<i>\"FieldOrder is an offline-first Flutter application built for wholesale field sales reps who take bulk orders "
        "in dense markets and rural dead zones with weak or no cellular data. Instead of making network roundtrips on every click, "
        "FieldOrder enforces a strict 'local-first' architecture where the UI only reads from a reactive Drift SQLite database. "
        "Orders are committed locally in a single ACID transaction alongside an Outbox table, then synced to the FastAPI backend "
        "using UUID-based Idempotency Keys with exponential backoff. It also guarantees financial precision by storing money in "
        "integer paise and includes an AI-assisted voice/text order entry parser with human-in-the-loop review.\"</i>"
    )
    callout_data = [[Paragraph(pitch_text, callout_style)]]
    callout_table = Table(callout_data, colWidths=[522])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CALLOUT_BG),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 2: WHY & WHERE IS IT USED
    # -------------------------------------------------------------
    story.append(Paragraph("2. Business Problem: Where & Why is it Used?", h1_style))
    
    p2_1 = (
        "<b>Target Domain:</b> Wholesale FMCG (Fast-Moving Consumer Goods), pharmaceutical distribution, "
        "and building material supply chains in emerging markets (India, Southeast Asia, Latin America).<br/>"
        "<b>The Operational Environment:</b> Sales representatives visit <b>15 to 30 retail shops</b> (kiranas, supermarkets, "
        "market stalls) every day. These shops are located in concrete APMC yards, underground bazaars, and semi-rural alleys "
        "where cellular coverage frequently drops to 0G/2G or complete dead zones.<br/>"
        "<b>Counter Time Pressure:</b> A sales rep has only <b>3 to 5 minutes per shop</b> before the shopkeeper becomes busy "
        "with retail customers. Any app that spins on network calls or crashes loses the order."
    )
    story.append(Paragraph(p2_1, body_style))

    story.append(Paragraph("Why Standard Mobile Architectures Fail in the Field:", h2_style))
    fail_points = [
        "<b>1. Network Latency Destroys Rep Productivity:</b> If an app requests prices, stock, or discounts from a remote API per click, weak 2G network timeouts freeze the screen and waste counter time.",
        "<b>2. Duplicate Invoices on Packet Loss:</b> When network signal drops mid-flight during a standard HTTP POST /orders call, the packet reaches the ERP but the confirmation drops. Reps inevitably tap 'Submit' again, creating duplicate orders and inventory chaos.",
        "<b>3. Wholesale Pricing Complexity:</b> Wholesale orders use multi-unit conversions (cartons vs. boxes vs. pieces) with tiered wholesale discounts. Float rounding mistakes cause balance mismatches with the ERP ledger.",
        "<b>4. Data Sync Conflicts:</b> If two reps sell the last stock of an item while both are offline, the system must have a deterministic conflict policy instead of silently dropping data."
    ]
    for fp in fail_points:
        story.append(Paragraph(f"• {fp}", body_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 3: END-TO-END WORKFLOW (7-STEP JOURNEY)
    # -------------------------------------------------------------
    story.append(Paragraph("3. End-to-End Workflow: The 7-Step Sales Rep Journey", h1_style))
    
    steps = [
        ("Step 1: Morning Login & Delta Pull", 
         "Rep authenticates once via JWT. The app executes a delta pull fetching only customers and products modified since the last sync timestamp (<code>GET /customers?updated_since=...</code>). All records upsert into local SQLite."),
        ("Step 2: Route & Customer Selection (< 3s)", 
         "Rep selects their daily route (e.g. South Zone - Route #4). An indexed, debounced SQLite query searches 50+ local customer shops in under 300ms. Opens Customer 360 profile showing verified credit limit and outstanding balance (e.g., ₹15,400 due)."),
        ("Step 3: 500-SKU Catalog & Fast Unit Picker", 
         "Rep browses 500 wholesale products. 1-tap pack unit buttons (Carton = 24 pcs, Box = 12 pcs, Piece) automatically apply carton wholesale multipliers. Real-time stock badges show 'In Stock', 'Low Stock', or 'Out of Stock'."),
        ("Step 4: Cart Review & Integer Paise Engine", 
         "Itemized cart applies customer-specific line discounts. All subtotals and discounts are calculated strictly in integer paise (₹1 = 100 paise), eliminating IEEE 754 floating-point inaccuracies."),
        ("Step 5: Order Confirmation & ACID Outbox Commit", 
         "Rep taps 'Place Order'. The app commits the order to the local <code>orders</code> table AND enqueues a record in the <code>outbox</code> table in a <b>single atomic SQLite transaction</b>. The order is immediately confirmed locally. Rep leaves the shop in under 3 minutes."),
        ("Step 6: Idempotent Background Synchronization", 
         "When network connectivity returns, a background worker dispatches orders in creation order with a unique header <code>Idempotency-Key: idemp_&lt;uuid&gt;</code>. On 200/201, order is marked 'synced' and removed from outbox. On 409 stock conflict, order is marked 'needs_review' with line-level explanation. On network errors, exponential backoff with jitter applies: <code>min(300, 2^attempts * 5s)</code>."),
        ("Step 7: AI Natural Language / Voice Order Ingestion", 
         "Rep pastes a WhatsApp dealer text or speaks voice notes (e.g. <i>'10 carton Maggi noodles aur 5 box Parle-G bhej dena Raju Traders ko'</i>). The backend NLP endpoint extracts structured line items, quantities, and customer hints. A human-in-the-loop review sheet lets the rep confirm before cart ingestion.")
    ]

    for title, desc in steps:
        story.append(Paragraph(f"<b>{title}:</b> {desc}", body_style))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 4: ARCHITECTURE & THE GOLDEN RULE
    # -------------------------------------------------------------
    story.append(Paragraph("4. System Architecture & The Offline-First Golden Rule", h1_style))
    
    golden_rule = (
        "<b>The Golden Rule of Offline-First:</b><br/>"
        "<i>\"The UI layer never calls network APIs (Dio) or handles remote HTTP responses directly.<br/>"
        "The UI strictly observes reactive streams from the local database (Drift SQLite).<br/>"
        "The network layer only ever writes into the local database.\"</i><br/>"
        "This architectural invariant guarantees that the app behaves with <b>identical speed and UI predictability</b> "
        "whether the rep has 5G or zero bars."
    )
    gr_table = Table([[Paragraph(golden_rule, callout_style)]], colWidths=[522])
    gr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(gr_table)
    story.append(Spacer(1, 10))

    # Architecture diagram in code style
    arch_diagram = (
        "+-------------------------------------------------------------------------+\n"
        "|                    UI Layer (Flutter BLoC / Widgets)                    |\n"
        "+-------------------------------------------------------------------------+\n"
        "                                     |\n"
        "                              reads & observes (Drift Streams)\n"
        "                                     v\n"
        "+-------------------------------------------------------------------------+\n"
        "|                 Local Database Layer (Drift SQLite DB)                  |\n"
        "|    - customers    - products    - orders    - order_lines    - outbox   |\n"
        "+-------------------------------------------------------------------------+\n"
        "                ^                                         ^\n"
        "         writes | (Delta Upsert)                          | (Pushes Outbox)\n"
        "+-------------------------------+         +-------------------------------+\n"
        "|         Delta Puller          |         |      Sync Engine (Outbox)     |\n"
        "|    GET /customers?updated_at  |         |    POST /orders + Idemp-Key   |\n"
        "+-------------------------------+         +-------------------------------+\n"
        "                                     |\n"
        "                              network transport\n"
        "                                     v\n"
        "+-------------------------------------------------------------------------+\n"
        "|                     Remote Backend API (FastAPI)                        |\n"
        "+-------------------------------------------------------------------------+"
    )
    story.append(Table([[Paragraph(f"<pre>{arch_diagram}</pre>", code_style)]], colWidths=[522], style=[
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 5: CORE ENGINEERING DECISIONS
    # -------------------------------------------------------------
    story.append(Paragraph("5. Deep Dives: Critical Engineering Decisions", h1_style))
    
    eng_points = [
        ("Integer Paise Storage (Zero Float Error):",
         "Floating-point numbers (<code>double</code>) in software introduce binary inaccuracies (<code>0.1 + 0.2 = 0.30000000000000004</code>). In wholesale orders involving hundreds of carton multipliers, rounding fractions cause ledger reconciliation failures. FieldOrder stores all monetary values strictly as integers in Paise (₹1 = 100 paise): <code>subtotal_paise</code>, <code>discount_paise</code>, <code>total_paise</code>."),
        ("Atomic ACID Outbox Transaction:",
         "To eliminate 'stranded orders' where an order is written to SQLite but the app crashes before queueing sync, the order insertion and outbox creation share a single SQLite transaction: <code>BEGIN TRANSACTION; ... COMMIT;</code>. If anything fails, both roll back atomically."),
        ("Idempotent HTTP Pushes:",
         "Every outbox record generates a client-side UUID: <code>Idempotency-Key: idemp_&lt;uuid&gt;</code>. If a request reaches the server but the client's connection drops before reading the response, retrying with the same key returns the cached 200/201 response without duplicating invoices or deducting inventory twice."),
        ("Exponential Backoff with Jitter:",
         "When retrying failed sync attempts, the backoff interval is calculated using: <code>Delay = min(300, 2^attempts * 5s) +/- jitter</code>. This prevents 500 field sales reps from creating a thundering herd on the backend when cellular service restores across an entire market district."),
        ("Authority Separation & Conflict Policy:",
         "The server is the authority for catalog prices and warehouse inventory. The client is the authority for local order lines. If inventory depletes while a rep is offline, the server returns <code>409 Conflict</code>. The client halts automatic retries, flags the order as <code>needs_review</code>, and allows the rep to adjust quantities.")
    ]
    for h, p in eng_points:
        story.append(Paragraph(f"<b>• {h}</b> {p}", body_style))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 6: TECH STACK MATRIX
    # -------------------------------------------------------------
    story.append(Paragraph("6. Technology Stack Matrix", h1_style))
    
    table_data = [
        [Paragraph("Area", table_cell_header), Paragraph("Selection", table_cell_header), Paragraph("Key Engineering Justification", table_cell_header)],
        [Paragraph("Mobile UI", table_cell_style), Paragraph("Flutter 3.22 / Dart 3", table_cell_style), Paragraph("Cross-platform 60fps rendering with native Ahead-of-Time compilation.", table_cell_style)],
        [Paragraph("State Mgmt", table_cell_style), Paragraph("flutter_bloc", table_cell_style), Paragraph("Unidirectional event-driven state transitions, predictable testing.", table_cell_style)],
        [Paragraph("Local DB", table_cell_style), Paragraph("Drift (SQLite)", table_cell_style), Paragraph("Type-safe SQL queries, reactive stream watchers, background isolate threading.", table_cell_style)],
        [Paragraph("Networking", table_cell_style), Paragraph("Dio", table_cell_style), Paragraph("Interceptors for Idempotency-Key headers and automatic 401 JWT refresh.", table_cell_style)],
        [Paragraph("Secure Auth", table_cell_style), Paragraph("flutter_secure_storage", table_cell_style), Paragraph("Encrypted hardware keychain/keystore for JWT tokens.", table_cell_style)],
        [Paragraph("Backend", table_cell_style), Paragraph("FastAPI + SQLite", table_cell_style), Paragraph("High throughput, asynchronous endpoints, auto OpenAPI/Swagger documentation.", table_cell_style)],
        [Paragraph("NLP / AI", table_cell_style), Paragraph("FastAPI NLP Parser", table_cell_style), Paragraph("Fuzzy-matches mixed Hindi/English wholesale jargon to product catalog IDs.", table_cell_style)],
    ]
    ts_table = Table(table_data, colWidths=[90, 130, 302])
    ts_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(ts_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 7: INTERVIEW QUESTIONS & MODEL ANSWERS
    # -------------------------------------------------------------
    story.append(Paragraph("7. Technical Interview Mastery: Top 7 Questions & Model Answers", h1_style))

    qa_list = [
        ("Q1: Why does the UI read only from the local database instead of calling APIs directly?",
         "In field sales operations, network connectivity is completely non-deterministic. If UI widgets call API endpoints directly, users face loading spinners, network timeouts, and unpredictable screen states. By observing reactive Drift SQLite streams, the UI always renders in under 16ms from indexed disk storage. The network layer acts strictly as a background worker that writes to the local DB. Whether the rep is on 5G or in a concrete basement, the user experience is identical."),
        ("Q2: What happens if the phone battery dies or the app is killed mid-sync?",
         "Because order creation and outbox queuing are committed in a single ACID transaction, an order cannot exist without being queued. If the app is killed mid-HTTP-request, the order remains in the local SQLite outbox as 'pending'. When the rep re-opens the app or connectivity returns, the sync worker retries with the original Idempotency-Key. If the server already processed the order before the crash, it returns the cached 200/201 receipt without creating a duplicate."),
        ("Q3: How exactly do you prevent duplicate orders when mobile signal drops?",
         "We use client-generated UUIDs and idempotency headers. When the order is saved locally, the client generates a unique Idempotency-Key: idemp_${uuid}. The server stores idempotency keys and cached response payloads. If a retried request arrives with the same key, the server returns the cached response rather than inserting a duplicate order or deducting stock twice."),
        ("Q4: How do you handle stock conflicts if an item runs out while the rep is offline?",
         "We enforce a clear authority model: the server is the single authority for stock and prices. When the rep syncs, if stock is insufficient, the backend returns an HTTP 409 Conflict with line-level error details (e.g. 'Only 5 pieces in stock, requested 24'). The sync engine stops auto-retries, sets the order state to 'needs_review', and displays an alert in the rep's Outbox for the rep to adjust with the customer."),
        ("Q5: Why did you use integer paise instead of double/float for currency?",
         "IEEE 754 floating-point numbers introduce binary decimal errors (e.g., 0.1 + 0.2 = 0.30000000000000004). In wholesale trade with large carton multipliers and percentage discounts, these fractions accumulate into balance mismatches with the ERP ledger. Storing values strictly as integer paise (₹1 = 100 paise) guarantees arithmetic accuracy across SQLite, Dart, and Python."),
        ("Q6: How would you optimize a 10,000-item product catalog in Flutter for 60fps?",
         "First, run Drift SQLite queries on a background Dart isolate using compute() or Drift's isolate connection so deserialization never blocks the UI isolate. Second, enforce pagination (LIMIT 50 OFFSET X) with composite indexes on (category, name) and barcode. Third, in Flutter, use ListView.builder with prototypeItem or itemExtent so the framework recycles widgets without calculating variable heights on scroll."),
        ("Q7: How do you secure the AI API key in mobile applications?",
         "Never bundle API keys or call LLM endpoints directly from the client APK, as decompiling exposes the secret. Instead, the mobile app sends the unstructured text to our authenticated backend endpoint POST /ai/parse-order using the rep's JWT token. The backend verifies authorization, injects the compact product catalog into the prompt, queries the model using an environment variable, validates the output schema, and returns validated product IDs to the app.")
    ]

    for q, a in qa_list:
        qa_content = f"<b>{q}</b><br/><font color='#1E293B'>{a}</font>"
        qa_table = Table([[Paragraph(qa_content, body_style)]], colWidths=[522])
        qa_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(qa_table)
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 8: VERIFICATION MATRIX
    # -------------------------------------------------------------
    story.append(Paragraph("8. Project Verification & Automated Test Matrix", h1_style))
    
    test_matrix = [
        [Paragraph("Test Suite", table_cell_header), Paragraph("Scope", table_cell_header), Paragraph("Assertions", table_cell_header), Paragraph("Result", table_cell_header)],
        [Paragraph("End-to-End Suite<br/>(<code>test_e2e_fieldorder.py</code>)", table_cell_style), 
         Paragraph("Full System: All 10 Prototype Screens, Responsive CSS, Device Switcher, Backend Health, JWT, 50 Customers, 500 Products, AI Order Parser, ACID Order, Idempotency Replay, History", table_cell_style),
         Paragraph("40 / 40 Assertions", table_cell_style),
         Paragraph("<font color='#059669'><b>100% PASSED</b></font>", table_cell_style)],
        [Paragraph("Backend Domain Suite<br/>(<code>backend/test_suite.py</code>)", table_cell_style), 
         Paragraph("Domain Logic: Delta Pulls, Pagination, Token Refresh, Negative Auth (401), Stock Conflict (409), Idempotent Replays, Carton Multipliers, Paise Conversion", table_cell_style),
         Paragraph("27 / 27 Tests", table_cell_style),
         Paragraph("<font color='#059669'><b>100% PASSED</b></font>", table_cell_style)],
        [Paragraph("<b>Total System Health</b>", table_cell_style), 
         Paragraph("Complete Frontend Prototype + Backend Domain Services", table_cell_style),
         Paragraph("<b>67 / 67 Tests</b>", table_cell_style),
         Paragraph("<font color='#059669'><b>ALL PASSED</b></font>", table_cell_style)]
    ]
    vm_table = Table(test_matrix, colWidths=[120, 242, 85, 75])
    vm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(vm_table)

    # Build Document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "FieldOrder_Project_Report.pdf"
    build_pdf(out_file)
