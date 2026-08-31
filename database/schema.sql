-- DreamHome Studio Relational SQLite Schema Definition
-- Includes full schema tables, constraints, foreign keys, indexes, and triggers

PRAGMA foreign_keys = ON;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('Designer', 'Client', 'Admin')),
    avatar_url TEXT,
    phone VARCHAR(30),
    company VARCHAR(100),
    bio TEXT,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    client_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    designer_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(30) DEFAULT 'Planning' CHECK (status IN ('Planning', 'In Design', 'Pending Approval', 'Approved', 'In Progress', 'Completed', 'Archived')),
    budget_limit DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(10) DEFAULT 'USD',
    cover_image TEXT,
    target_completion_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. Floorplans Table
CREATE TABLE IF NOT EXISTS floorplans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    room_type VARCHAR(50) DEFAULT 'Living Room',
    width_m DECIMAL(6, 2) DEFAULT 8.00,
    height_m DECIMAL(6, 2) DEFAULT 6.00,
    grid_size_cm INTEGER DEFAULT 20,
    scale_factor DECIMAL(5, 2) DEFAULT 50.00,
    canvas_data_json TEXT,
    thumbnail_url TEXT,
    version_number INTEGER DEFAULT 1,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. Floorplan Versions Table
CREATE TABLE IF NOT EXISTS floorplan_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    floorplan_id INTEGER NOT NULL REFERENCES floorplans(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    title VARCHAR(100),
    notes TEXT,
    canvas_data_json TEXT NOT NULL,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. Furniture Catalog Table
CREATE TABLE IF NOT EXISTS furniture_catalog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50),
    sku VARCHAR(50) UNIQUE NOT NULL,
    brand VARCHAR(100),
    width_cm DECIMAL(6, 2) NOT NULL,
    depth_cm DECIMAL(6, 2) NOT NULL,
    height_cm DECIMAL(6, 2) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    color_options_json TEXT,
    material VARCHAR(50),
    texture_url TEXT,
    thumbnail_url TEXT,
    default_z_index INTEGER DEFAULT 1,
    is_customizable INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 6. Materials Catalog Table
CREATE TABLE IF NOT EXISTS materials_catalog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('Flooring', 'Wall Paint', 'Wallpaper', 'Fabric', 'Tile', 'Wood', 'Metal', 'Glass', 'Stone')),
    texture_url TEXT,
    pattern_type VARCHAR(50) DEFAULT 'solid',
    color_hex VARCHAR(10) DEFAULT '#FFFFFF',
    price_per_sqm DECIMAL(8, 2) NOT NULL,
    roughness DECIMAL(3, 2) DEFAULT 0.50,
    opacity DECIMAL(3, 2) DEFAULT 1.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 7. Suppliers Table
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name VARCHAR(120) NOT NULL,
    contact_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(30),
    website VARCHAR(200),
    address TEXT,
    rating DECIMAL(3, 2) DEFAULT 4.50,
    lead_time_days INTEGER DEFAULT 7,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 8. Inventory Items Table
CREATE TABLE IF NOT EXISTS inventory_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    furniture_id INTEGER REFERENCES furniture_catalog(id) ON DELETE CASCADE,
    supplier_id INTEGER REFERENCES suppliers(id) ON DELETE CASCADE,
    quantity_in_stock INTEGER DEFAULT 0,
    reorder_level INTEGER DEFAULT 5,
    unit_cost DECIMAL(10, 2) NOT NULL,
    bin_location VARCHAR(50),
    status VARCHAR(30) DEFAULT 'In Stock' CHECK (status IN ('In Stock', 'Low Stock', 'Out of Stock', 'On Order')),
    last_restocked_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 9. Budgets Table
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER UNIQUE NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    total_estimated DECIMAL(12, 2) DEFAULT 0.00,
    total_spent DECIMAL(12, 2) DEFAULT 0.00,
    tax_rate DECIMAL(5, 4) DEFAULT 0.0850,
    labor_cost DECIMAL(10, 2) DEFAULT 0.00,
    designer_margin DECIMAL(5, 4) DEFAULT 0.1500,
    notes TEXT,
    status VARCHAR(30) DEFAULT 'Draft' CHECK (status IN ('Draft', 'Submitted', 'Approved', 'Exceeded')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 10. Budget Line Items Table
CREATE TABLE IF NOT EXISTS budget_line_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    budget_id INTEGER NOT NULL REFERENCES budgets(id) ON DELETE CASCADE,
    item_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    item_type VARCHAR(30) DEFAULT 'Furniture' CHECK (item_type IN ('Furniture', 'Material', 'Labor', 'Shipping', 'Fee', 'Custom')),
    unit_price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER DEFAULT 1,
    total_price DECIMAL(12, 2) NOT NULL,
    supplier_id INTEGER REFERENCES suppliers(id) ON DELETE SET NULL,
    status VARCHAR(30) DEFAULT 'Estimated' CHECK (status IN ('Estimated', 'Ordered', 'Purchased', 'Cancelled')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 11. Tasks Table
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
    priority VARCHAR(20) DEFAULT 'Medium' CHECK (priority IN ('Low', 'Medium', 'High', 'Urgent')),
    status VARCHAR(30) DEFAULT 'To Do' CHECK (status IN ('To Do', 'In Progress', 'Under Review', 'Completed')),
    due_date DATE,
    estimated_hours DECIMAL(5, 2) DEFAULT 0.00,
    actual_hours DECIMAL(5, 2) DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 12. Moodboards Table
CREATE TABLE IF NOT EXISTS moodboards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(120) NOT NULL,
    description TEXT,
    layout_json TEXT,
    color_palette_json TEXT,
    tags VARCHAR(200),
    created_by INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 13. Comments & Annotations Table
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    floorplan_id INTEGER REFERENCES floorplans(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    pos_x DECIMAL(8, 2),
    pos_y DECIMAL(8, 2),
    comment_text TEXT NOT NULL,
    status VARCHAR(30) DEFAULT 'Open' CHECK (status IN ('Open', 'Resolved', 'Archived')),
    parent_id INTEGER REFERENCES comments(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 14. Approval Requests Table
CREATE TABLE IF NOT EXISTS approval_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    floorplan_id INTEGER REFERENCES floorplans(id) ON DELETE CASCADE,
    requested_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    approved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    status VARCHAR(30) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected', 'Revision Requested')),
    client_notes TEXT,
    reviewer_notes TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    decided_at DATETIME
);

-- 15. Portfolios Table
CREATE TABLE IF NOT EXISTS portfolios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    designer_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    cover_image TEXT,
    tags VARCHAR(200),
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    is_public INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 16. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(120) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(30) DEFAULT 'Info' CHECK (type IN ('Info', 'Success', 'Warning', 'Danger', 'Approval')),
    is_read INTEGER DEFAULT 0,
    target_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 17. Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER,
    details_json TEXT,
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- INDEXES for Query Optimization
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_projects_designer ON projects(designer_id);
CREATE INDEX IF NOT EXISTS idx_projects_client ON projects(client_id);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_floorplans_project ON floorplans(project_id);
CREATE INDEX IF NOT EXISTS idx_furniture_sku ON furniture_catalog(sku);
CREATE INDEX IF NOT EXISTS idx_furniture_category ON furniture_catalog(category);
CREATE INDEX IF NOT EXISTS idx_materials_category ON materials_catalog(category);
CREATE INDEX IF NOT EXISTS idx_budget_line_items_budget ON budget_line_items(budget_id);
CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_comments_project ON comments(project_id);
CREATE INDEX IF NOT EXISTS idx_comments_floorplan ON comments(floorplan_id);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
