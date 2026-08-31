# DreamHome Studio — Database Specification

## Relational Schema Overview

The database uses SQLite (`database/dreamhome.db`) in WAL mode with full foreign key constraints and performance indexes.

---

## Core Tables

| Table Name | Primary Key | Description |
|---|---|---|
| `users` | `id` | User accounts, credentials, roles (`Designer`, `Client`, `Admin`) |
| `projects` | `id` | Interior design projects, budget limits, client & designer links |
| `floorplans` | `id` | 2D room layouts, canvas JSON payload, room dimensions |
| `floorplan_versions` | `id` | Snapshot version history points for 2D room designs |
| `furniture_catalog` | `id` | Furnishings catalog, SKU, dimensions, price, color options |
| `materials_catalog` | `id` | Surface finishes (flooring, wall paint, wallpaper, tiles) |
| `suppliers` | `id` | Manufacturers, ratings, contact info, lead times |
| `inventory_items` | `id` | Warehouse stock levels, reorder thresholds, unit costs |
| `budgets` | `id` | Project budgets, taxes, labor, margins, totals |
| `budget_line_items` | `id` | Itemized cost breakdown line items |
| `tasks` | `id` | Project tasks, priorities, status, deadlines |
| `moodboards` | `id` | Design inspiration collages, color palettes |
| `comments` | `id` | Client-designer feedback comments & 2D coordinate pins |
| `approval_requests` | `id` | Formal design approval workflow records |
| `portfolios` | `id` | Public designer showcases, views, likes |
| `notifications` | `id` | User activity alerts & notifications |
| `audit_logs` | `id` | Security audit logs, IP tracking, user action events |

---

## Indexes & Query Optimization

* `idx_users_email`: Unique lookup by email.
* `idx_projects_designer`: Designer project queries.
* `idx_projects_client`: Client project queries.
* `idx_floorplans_project`: Project floorplan listing.
* `idx_furniture_category`: Catalog filtering by room category.
* `idx_audit_user`: Audit log security filtering.
