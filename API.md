# DreamHome Studio — REST API Specification

## Base URL
`http://127.0.0.1:5000/api`

---

## 1. Authentication Endpoints (`/api/auth`)

### `POST /api/auth/login`
Authenticate user credentials and initialize HTTP session.
* **Request Body**:
  ```json
  { "email": "sarah.jenkins@dreamhome.com", "password": "Designer123!Password" }
  ```
* **Response (200 OK)**:
  ```json
  { "message": "Login successful", "user": { "id": 2, "email": "sarah.jenkins@dreamhome.com", "role": "Designer" } }
  ```

### `POST /api/auth/register`
Register new account.
* **Request Body**:
  ```json
  { "email": "new.user@example.com", "password": "Password123!", "full_name": "New User", "role": "Client" }
  ```

### `GET /api/auth/me`
Retrieve active logged in user profile.

---

## 2. Projects Endpoints (`/api/projects`)

### `GET /api/projects`
List projects accessible to current user.

### `POST /api/projects`
Create a new project.
* **Request Body**:
  ```json
  { "title": "Modern Coastal Villa", "description": "Renovation", "budget_limit": 120000.0 }
  ```

---

## 3. Floorplans Endpoints (`/api/floorplans`)

### `GET /api/floorplans/<id>`
Retrieve single floorplan and canvas JSON layout.

### `POST /api/floorplans/<id>/save`
Save updated 2D canvas JSON payload and snapshot version history.

### `GET /api/floorplans/<id>/export/svg`
Export floorplan to standalone vector SVG XML file.

---

## 4. Catalog Endpoints (`/api/catalog`)

### `GET /api/catalog/furniture`
Search and filter furniture items by category, query, price.

### `GET /api/catalog/materials`
Retrieve materials catalog (flooring, paint, tiles, fabric).

---

## 5. Analytics Endpoints (`/api/analytics`)

### `GET /api/analytics/dashboard`
Retrieve dashboard KPIs, status breakdowns, and recent audit logs.

---

## 6. Admin Endpoints (`/api/admin`)

### `GET /api/admin/users`
List all registered users (Requires `Admin` role).

### `GET /api/admin/audit-logs`
Retrieve security audit logs (Requires `Admin` role).
