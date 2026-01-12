# Database Schema - Table Relationships

## Visual Diagram (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                              CORE MODULE                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│   ┌──────────────┐         ┌──────────────────┐         ┌───────────────┐                                       │
│   │    users     │◄───────►│   user_roles     │◄───────►│     roles     │                                       │
│   │──────────────│         │ (junction table) │         │───────────────│                                       │
│   │ id (PK)      │         │ user_id (FK)     │         │ id (PK)       │                                       │
│   │ username     │         │ role_id (FK)     │         │ name          │                                       │
│   │ email        │         └──────────────────┘         │ description   │                                       │
│   └──────┬───────┘                                      └───────┬───────┘                                       │
│          │                                                      │                                               │
│          │                                              ┌───────▼───────────┐       ┌───────────────┐           │
│          │                                              │  role_permissions │◄─────►│  permissions  │           │
│          │                                              │ (junction table)  │       │───────────────│           │
│          │                                              │ role_id (FK)      │       │ id (PK)       │           │
│          │                                              │ permission_id (FK)│       │ key           │           │
│          │                                              └───────────────────┘       └───────────────┘           │
│          │                                                                                                      │
│   ┌──────▼───────┐                                                                                              │
│   │    files     │                                                                                              │
│   │──────────────│                                                                                              │
│   │ id (PK)      │                                                                                              │
│   │ user_id (FK) │──► users.id                                                                                  │
│   └──────────────┘                                                                                              │
│                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            HR MODULE                                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│   ┌────────────────────┐                              ┌────────────────────┐                                    │
│   │     employees      │                              │    employees2      │  (SEPARATE - NO LINK)              │
│   │────────────────────│                              │────────────────────│                                    │
│   │ id (PK)            │                              │ id (PK)            │                                    │
│   │ employee_id (UK)   │                              │ serial_no          │                                    │
│   │ first_name         │                              │ fss_no             │                                    │
│   │ last_name          │                              │ name               │                                    │
│   │ ...116 columns     │                              │ ...98 columns      │                                    │
│   └────────┬───────────┘                              └─────────┬──────────┘                                    │
│            │                                                    │                                               │
│            │ employees.id referenced by:                        │ employees2.id referenced by:                  │
│            │                                                    │                                               │
│   ┌────────▼───────────┐                              ┌─────────▼──────────────────────┐                        │
│   │ employee_documents │                              │ payroll_sheet_entries          │                        │
│   │────────────────────│                              │────────────────────────────────│                        │
│   │ employee_db_id(FK) │──► employees.id              │ employee_db_id (FK)            │──► employees2.id       │
│   └────────────────────┘                              └────────────────────────────────┘                        │
│                                                                                                                 │
│   ┌────────────────────┐                              ┌────────────────────────────────┐                        │
│   │ employee_warnings  │                              │ client_site_guard_allocations  │                        │
│   │────────────────────│                              │────────────────────────────────│                        │
│   │ employee_db_id(FK) │──► employees.id              │ employee_db_id (FK)            │──► employees2.id       │
│   └────────┬───────────┘                              └────────────────────────────────┘                        │
│            │                                                                                                    │
│   ┌────────▼───────────────────┐                                                                                │
│   │ employee_warning_documents │                                                                                │
│   │────────────────────────────│                                                                                │
│   │ warning_id (FK)            │──► employee_warnings.id                                                        │
│   └────────────────────────────┘                                                                                │
│                                                                                                                 │
│   ┌────────────────────┐      ┌────────────────────────────────┐                                                │
│   │ employee_advances  │      │ employee_advance_deductions    │                                                │
│   │────────────────────│      │────────────────────────────────│                                                │
│   │ employee_db_id(FK) │──►   │ employee_db_id (FK)            │──► employees.id                                │
│   └────────────────────┘      └────────────────────────────────┘                                                │
│                                                                                                                 │
│   ┌────────────────────┐      ┌────────────────────┐                                                            │
│   │ employees_inactive │      │   leave_periods    │  (No FKs - standalone)                                     │
│   │ (No FKs)           │      │   (No FKs)         │                                                            │
│   └────────────────────┘      └────────────────────┘                                                            │
│                                                                                                                 │
│   ┌────────────────────┐                                                                                        │
│   │    attendance      │  (No FKs - standalone)                                                                 │
│   └────────────────────┘                                                                                        │
│                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          FLEET MODULE                                                            │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│   ┌────────────────────┐                                                                                        │
│   │      vehicles      │                                                                                        │
│   │────────────────────│                                                                                        │
│   │ id (PK)            │                                                                                        │
│   │ vehicle_id (UK)    │◄─────────────────────────────┐                                                         │
│   └────────────────────┘                              │                                                         │
│                                                       │                                                         │
│   ┌────────────────────┐      ┌────────────────────┐  │                                                         │
│   │  vehicle_images    │      │ vehicle_documents  │  │                                                         │
│   │────────────────────│      │────────────────────│  │                                                         │
│   │ vehicle_id (FK)    │──────│ vehicle_id (FK)    │──┘ (both reference vehicles.vehicle_id)                    │
│   └────────────────────┘      └────────────────────┘                                                            │
│                                                                                                                 │
│   ┌──────────────────────┐    ┌────────────────────┐                                                            │
│   │ vehicle_assignments  │    │ vehicle_maintenance│  (No FKs - standalone)                                     │
│   │ (No FKs)             │    │ (No FKs)           │                                                            │
│   └──────────────────────┘    └────────────────────┘                                                            │
│                                                                                                                 │
│   ┌────────────────────┐                                                                                        │
│   │    fuel_entries    │  (No FKs - standalone)                                                                 │
│   └────────────────────┘                                                                                        │
│                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         CLIENT MODULE                                                            │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│   ┌────────────────────┐                                                                                        │
│   │      clients       │◄─────────────────────────────┬─────────────────────────────────────────────┐           │
│   │────────────────────│                              │                                             │           │
│   │ id (PK)            │                              │                                             │           │
│   └────────┬───────────┘                              │                                             │           │
│            │                                          │                                             │           │
│   ┌────────▼───────────┐      ┌────────────────────┐  │  ┌────────────────────┐  ┌────────────────┐ │           │
│   │  client_addresses  │      │  client_contacts   │  │  │  client_documents  │  │ client_invoices│ │           │
│   │────────────────────│      │────────────────────│  │  │────────────────────│  │────────────────│ │           │
│   │ client_id (FK)     │──►   │ client_id (FK)     │──┤  │ client_id (FK)     │  │ client_id (FK) │─┤           │
│   └────────────────────┘      └────────────────────┘  │  └────────────────────┘  └────────────────┘ │           │
│                                                       │                                             │           │
│   ┌────────────────────┐      ┌────────────────────┐  │                                             │           │
│   │  client_rate_cards │      │  client_contracts  │  │                                             │           │
│   │────────────────────│      │────────────────────│  │                                             │           │
│   │ client_id (FK)     │──────│ client_id (FK)     │──┘ (all reference clients.id)                  │           │
│   └────────────────────┘      └─────────┬──────────┘                                                │           │
│                                         │                                                           │           │
│   ┌────────────────────┐◄───────────────┘                                                           │           │
│   │   client_sites     │◄───────────────────────────────────────────────────────────────────────────┘           │
│   │────────────────────│                                                                                        │
│   │ id (PK)            │                                                                                        │
│   │ client_id (FK)     │──► clients.id                                                                          │
│   └────────┬───────────┘                                                                                        │
│            │                                                                                                    │
│   ┌────────▼────────────────────┐                                                                               │
│   │ client_guard_requirements   │◄──────────────────────────────┐                                               │
│   │─────────────────────────────│                               │                                               │
│   │ id (PK)                     │                               │                                               │
│   │ site_id (FK)                │──► client_sites.id            │                                               │
│   └─────────────────────────────┘                               │                                               │
│                                                                 │                                               │
│   ┌─────────────────────────────────────┐                       │                                               │
│   │ client_site_guard_allocations       │                       │                                               │
│   │─────────────────────────────────────│                       │                                               │
│   │ site_id (FK)                        │──► client_sites.id    │                                               │
│   │ contract_id (FK)                    │──► client_contracts.id│                                               │
│   │ requirement_id (FK)                 │──► client_guard_requirements.id                                       │
│   │ employee_db_id (FK)                 │──► employees2.id                                                      │
│   └─────────────────────────────────────┘                                                                       │
│                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        FINANCE MODULE                                                            │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│   ┌─────────────────────────┐                                                                                   │
│   │   finance_accounts      │◄──────────────────────────────────┬────────────────────────────────┐              │
│   │─────────────────────────│                                   │                                │              │
│   │ id (PK)                 │                                   │                                │              │
│   │ parent_id (FK, self)    │──► finance_accounts.id (self-ref) │                                │              │
│   └─────────────────────────┘                                   │                                │              │
│                                                                 │                                │              │
│   ┌─────────────────────────┐                                   │                                │              │
│   │ finance_journal_entries │◄──────────────────────────────────│────────┐                       │              │
│   │─────────────────────────│                                   │        │                       │              │
│   │ id (PK)                 │                                   │        │                       │              │
│   └────────────┬────────────┘                                   │        │                       │              │
│                │                                                │        │                       │              │
│   ┌────────────▼────────────┐                                   │        │                       │              │
│   │  finance_journal_lines  │                                   │        │                       │              │
│   │─────────────────────────│                                   │        │                       │              │
│   │ entry_id (FK)           │──► finance_journal_entries.id     │        │                       │              │
│   │ account_id (FK)         │──► finance_accounts.id ───────────┘        │                       │              │
│   │ employee_id (FK)        │──► employees.id                            │                       │              │
│   └─────────────────────────┘                                            │                       │              │
│                                                                          │                       │              │
│   ┌─────────────────────────┐                                            │                       │              │
│   │       expenses          │                                            │                       │              │
│   │─────────────────────────│                                            │                       │              │
│   │ account_id (FK)         │──► finance_accounts.id ────────────────────┼───────────────────────┘              │
│   │ journal_entry_id (FK)   │──► finance_journal_entries.id ─────────────┘                                      │
│   │ employee_id (FK)        │──► employees.id                                                                   │
│   └─────────────────────────┘                                                                                   │
│                                                                                                                 │
│   ┌─────────────────────────┐      ┌─────────────────────────┐                                                  │
│   │ payroll_sheet_entries   │      │ payroll_payment_status  │                                                  │
│   │─────────────────────────│      │─────────────────────────│                                                  │
│   │ employee_db_id (FK)     │──►   │ employee_db_id (FK)     │──► employees.id                                  │
│   └─────────────────────────┘      └─────────────────────────┘                                                  │
│          │                                                                                                      │
│          └──► employees2.id                                                                                     │
│                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       INVENTORY MODULE                                                           │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│   ══════════════════════ RESTRICTED INVENTORY ══════════════════════                                            │
│                                                                                                                 │
│   ┌────────────────────────┐                                                                                    │
│   │    restricted_items    │◄───────────────────────────────────────────────────────────────┐                   │
│   │────────────────────────│                                                                │                   │
│   │ id (PK)                │                                                                │                   │
│   │ item_code (UK)         │◄───────────────────────────────┬────────────────────┐          │                   │
│   └────────────────────────┘                                │                    │          │                   │
│                                                             │                    │          │                   │
│   ┌────────────────────────────────┐    ┌───────────────────▼────────────┐       │          │                   │
│   │ restricted_item_serial_units   │    │ restricted_item_images         │       │          │                   │
│   │────────────────────────────────│    │────────────────────────────────│       │          │                   │
│   │ id (PK)                        │    │ item_code (FK)                 │───────┤          │                   │
│   │ item_code (FK)                 │────│ (references item_code)         │       │          │                   │
│   └────────────┬───────────────────┘    └────────────────────────────────┘       │          │                   │
│                │                                                                 │          │                   │
│   ┌────────────▼───────────────────────────────┐                                 │          │                   │
│   │    restricted_item_transactions            │                                 │          │                   │
│   │────────────────────────────────────────────│                                 │          │                   │
│   │ item_code (FK)                             │──► restricted_items.item_code ──┘          │                   │
│   │ employee_id (FK)                           │──► employees.employee_id                   │                   │
│   │ serial_unit_id (FK)                        │──► restricted_item_serial_units.id         │                   │
│   └────────────────────────────────────────────┘                                            │                   │
│                                                                                             │                   │
│   ┌────────────────────────────────────────────┐                                            │                   │
│   │   restricted_item_employee_balances        │                                            │                   │
│   │────────────────────────────────────────────│                                            │                   │
│   │ employee_id (FK)                           │──► employees.employee_id                   │                   │
│   │ item_code (FK)                             │──► restricted_items.item_code ─────────────┘                   │
│   └────────────────────────────────────────────┘                                                                │
│                                                                                                                 │
│   ══════════════════════ GENERAL INVENTORY ══════════════════════                                               │
│                                                                                                                 │
│   ┌────────────────────────┐                                                                                    │
│   │    general_items       │◄───────────────────────────────────────────────────────────────┐                   │
│   │────────────────────────│                                                                │                   │
│   │ id (PK)                │                                                                │                   │
│   │ item_code (UK)         │◄───────────────────────────────┐                               │                   │
│   └────────────────────────┘                                │                               │                   │
│                                                             │                               │                   │
│   ┌────────────────────────────────────────────┐            │                               │                   │
│   │    general_item_transactions               │            │                               │                   │
│   │────────────────────────────────────────────│            │                               │                   │
│   │ item_code (FK)                             │────────────┘                               │                   │
│   │ employee_id (FK)                           │──► employees.employee_id                   │                   │
│   └────────────────────────────────────────────┘                                            │                   │
│                                                                                             │                   │
│   ┌────────────────────────────────────────────┐                                            │                   │
│   │   general_item_employee_balances           │                                            │                   │
│   │────────────────────────────────────────────│                                            │                   │
│   │ employee_id (FK)                           │──► employees.employee_id                   │                   │
│   │ item_code (FK)                             │──► general_items.item_code ────────────────┘                   │
│   └────────────────────────────────────────────┘                                                                │
│                                                                                                                 │
│   ┌────────────────────────────────┐                                                                            │
│   │   inventory_assignments_state  │  (No FKs - standalone)                                                     │
│   └────────────────────────────────┘                                                                            │
│                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Relationship Summary Table

| From Table | Column | To Table | Column | Relationship |
|------------|--------|----------|--------|--------------|
| **CORE** |
| `user_roles` | user_id | `users` | id | Many-to-Many |
| `user_roles` | role_id | `roles` | id | Many-to-Many |
| `role_permissions` | role_id | `roles` | id | Many-to-Many |
| `role_permissions` | permission_id | `permissions` | id | Many-to-Many |
| `files` | user_id | `users` | id | Many-to-One |
| **HR** |
| `employee_documents` | employee_db_id | `employees` | id | Many-to-One |
| `employee_warnings` | employee_db_id | `employees` | id | Many-to-One |
| `employee_warning_documents` | warning_id | `employee_warnings` | id | Many-to-One |
| `employee_advances` | employee_db_id | `employees` | id | Many-to-One |
| `employee_advance_deductions` | employee_db_id | `employees` | id | Many-to-One |
| `payroll_sheet_entries` | employee_db_id | `employees2` | id | Many-to-One |
| **FLEET** |
| `vehicle_images` | vehicle_id | `vehicles` | vehicle_id | Many-to-One |
| `vehicle_documents` | vehicle_id | `vehicles` | vehicle_id | Many-to-One |
| **CLIENT** |
| `client_addresses` | client_id | `clients` | id | Many-to-One |
| `client_contacts` | client_id | `clients` | id | Many-to-One |
| `client_documents` | client_id | `clients` | id | Many-to-One |
| `client_invoices` | client_id | `clients` | id | Many-to-One |
| `client_rate_cards` | client_id | `clients` | id | Many-to-One |
| `client_contracts` | client_id | `clients` | id | Many-to-One |
| `client_sites` | client_id | `clients` | id | Many-to-One |
| `client_guard_requirements` | site_id | `client_sites` | id | Many-to-One |
| `client_site_guard_allocations` | site_id | `client_sites` | id | Many-to-One |
| `client_site_guard_allocations` | contract_id | `client_contracts` | id | Many-to-One |
| `client_site_guard_allocations` | requirement_id | `client_guard_requirements` | id | Many-to-One |
| `client_site_guard_allocations` | employee_db_id | `employees2` | id | Many-to-One |
| **FINANCE** |
| `finance_accounts` | parent_id | `finance_accounts` | id | Self-Reference |
| `finance_journal_lines` | entry_id | `finance_journal_entries` | id | Many-to-One |
| `finance_journal_lines` | account_id | `finance_accounts` | id | Many-to-One |
| `finance_journal_lines` | employee_id | `employees` | id | Many-to-One |
| `expenses` | account_id | `finance_accounts` | id | Many-to-One |
| `expenses` | journal_entry_id | `finance_journal_entries` | id | Many-to-One |
| `expenses` | employee_id | `employees` | id | Many-to-One |
| `payroll_payment_status` | employee_db_id | `employees` | id | Many-to-One |
| **INVENTORY - RESTRICTED** |
| `restricted_item_serial_units` | item_code | `restricted_items` | item_code | Many-to-One |
| `restricted_item_images` | item_code | `restricted_items` | item_code | Many-to-One |
| `restricted_item_transactions` | item_code | `restricted_items` | item_code | Many-to-One |
| `restricted_item_transactions` | employee_id | `employees` | employee_id | Many-to-One |
| `restricted_item_transactions` | serial_unit_id | `restricted_item_serial_units` | id | Many-to-One |
| `restricted_item_employee_balances` | employee_id | `employees` | employee_id | Many-to-One |
| `restricted_item_employee_balances` | item_code | `restricted_items` | item_code | Many-to-One |
| **INVENTORY - GENERAL** |
| `general_item_transactions` | item_code | `general_items` | item_code | Many-to-One |
| `general_item_transactions` | employee_id | `employees` | employee_id | Many-to-One |
| `general_item_employee_balances` | employee_id | `employees` | employee_id | Many-to-One |
| `general_item_employee_balances` | item_code | `general_items` | item_code | Many-to-One |

---

## Key Observations

### employees vs employees2 Usage

| Table | Uses `employees` | Uses `employees2` |
|-------|------------------|-------------------|
| `employee_documents` | ✅ (id) | ❌ |
| `employee_warnings` | ✅ (id) | ❌ |
| `employee_advances` | ✅ (id) | ❌ |
| `employee_advance_deductions` | ✅ (id) | ❌ |
| `payroll_payment_status` | ✅ (id) | ❌ |
| `finance_journal_lines` | ✅ (id) | ❌ |
| `expenses` | ✅ (id) | ❌ |
| `restricted_item_transactions` | ✅ (employee_id) | ❌ |
| `restricted_item_employee_balances` | ✅ (employee_id) | ❌ |
| `general_item_transactions` | ✅ (employee_id) | ❌ |
| `general_item_employee_balances` | ✅ (employee_id) | ❌ |
| `payroll_sheet_entries` | ❌ | ✅ (id) |
| `client_site_guard_allocations` | ❌ | ✅ (id) |

### Standalone Tables (No Foreign Keys)
- `attendance`
- `employees_inactive`
- `leave_periods`
- `vehicle_assignments`
- `vehicle_maintenance`
- `fuel_entries`
- `inventory_assignments_state`

---

## File Locations

| Module | Path |
|--------|------|
| Core | `app/models/core/` |
| HR | `app/models/hr/` |
| Fleet | `app/models/fleet/` |
| Client | `app/models/client/` |
| Finance | `app/models/finance/` |
| Inventory | `app/models/inventory/` |
