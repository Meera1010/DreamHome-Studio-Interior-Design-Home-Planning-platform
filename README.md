# DreamHome Studio — Interior Design & Home Planning SaaS

![DreamHome Studio Banner](static/images/projects/coastal_villa.jpg)

**DreamHome Studio** is a full-featured, GitHub-ready, professional SaaS platform for **2D interior design, interactive floor planning, budget management, inventory tracking, client collaboration, and project analytics**.

Built with a modern **Python 3.11 Flask REST API**, **SQLite relational database**, **HTML5/CSS3**, and **Vanilla JavaScript** featuring a high-performance **HTML5 Canvas/SVG 2D Design Engine**.

---

## Key Features

* **User Authentication & Role-Based Access (RBAC)**: Secure PBKDF2 password hashing, session tokens, audit logging, and 3 distinct user roles (`Designer`, `Client`, `Admin`).
* **2D Interactive Room Designer**:
  * Grid overlay with snap-to-grid, pan, zoom (10% - 500%), ruler guides, and dynamic room area/perimeter calculations ($m^2$ / $sq\ ft$).
  * Interactive wall drawing tool, room enclosure detection, doors/windows placement, wall cutouts.
  * Drag-and-drop / click-to-add furniture catalog (sofas, tables, beds, lamps, plants, storage, rugs, bathroom fixtures).
  * Transform handles (drag movement, resize, 1-degree rotation, z-index layering).
  * Surface materials & wall paint color selectors.
  * Point and ambient light rendering engine with radial falloff.
  * Multi-level Undo & Redo state stack.
  * Vector SVG, high-res PNG, and JSON interchange export engines.
* **Multi-Room Projects & Version History**: Save design snapshots to database with version numbers, notes, and restore points.
* **Interior Cost Calculator & Budget Management**: Dynamic budget calculation based on room elements, furniture pricing, wall paint area, flooring costs, labor rates, sales tax, and designer margins.
* **Warehouse Inventory & Supplier Portal**: Stock tracking, reorder thresholds, supplier ratings, contact directory, purchase order generator.
* **Task Management & Timeline**: Project milestones, priority task boards, deadlines, estimated vs actual hours.
* **Client Collaboration & Approvals**: Visual pin feedback annotations on floor plans, comment threads, formal design approval workflows.
* **Analytics & SVG Charts Engine**: Dashboard KPI metrics, project status breakdowns, budget performance charts, audit logs.
* **Admin Panel**: User management, role modification, account activation/deactivation, security audit logs, database statistics.

---

## Tech Stack

* **Backend**: Python 3.11 + Flask, Werkzeug, PBKDF2 HMAC SHA-256 Auth, RESTful Blueprints.
* **Database**: SQLite (`dreamhome.db`) with complete relational schema, foreign key enforcement, WAL mode, indexes, and realistic seed data generator.
* **Frontend**: Vanilla ES6 JavaScript, HTML5 Canvas 2D API, SVG vector export, Vanilla CSS3 (Custom Properties, Glassmorphism, Responsive Grid System).
* **Testing**: Automated `unittest` & `pytest` suite with `loc_audit.py` auditing script.

---

## Build Instructions

### Installation & Build Setup

1. **Clone Repository**:
   ```bash
   git clone https://github.com/Meera1010/DreamHome-Studio-Interior-Design-Home-Planning-platform.git
   cd DreamHome-Studio-Interior-Design-Home-Planning-platform
   ```

2. **Install Dependencies & Build Environment**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Build & Seed SQLite Database**:
   ```bash
   python database/seed_data.py
   ```

3. **Initialize & Seed Database**:
   ```bash
   python database/seed_data.py
   ```

4. **Run Application Server**:
   ```bash
   python app.py
   ```
   Open browser at: `http://127.0.0.1:5000`

5. **Run Automated Test Suite**:
   ```bash
   python tests/run_tests.py
   ```

6. **Run LOC Audit**:
   ```bash
   python loc_audit.py
   ```

---

## Demo Credentials

| Role | Email | Password |
|---|---|---|
| **Admin** | `admin@dreamhome.com` | `Admin123!Password` |
| **Designer** | `sarah.jenkins@dreamhome.com` | `Designer123!Password` |
| **Client** | `john.doe@gmail.com` | `Client123!Password` |

---

## License

Distributed under the MIT License.
