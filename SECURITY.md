# DreamHome Studio — Security Policy & Guidelines

## Security Controls

1. **Password Hashing**: PBKDF2 with HMAC SHA-256 (100,000 iterations) and unique cryptographic salt. Plain text passwords are never stored.
2. **Session Security**: HTTPOnly, SameSite=Lax session cookies.
3. **Role-Based Authorization (RBAC)**: Endpoint route protection via `@login_required` and `@role_required('Admin')` decorators.
4. **SQL Injection Prevention**: 100% parameterized SQL queries executed via `sqlite3` driver.
5. **XSS Protection**: HTML input sanitization and template auto-escaping in Jinja2 templates.
6. **Audit Logging**: Comprehensive recording of user logins, role changes, floorplan saves, and administrative operations in `audit_logs`.
