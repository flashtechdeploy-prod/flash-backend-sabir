"""Consolidate employees2 into employees table

Revision ID: consolidate_employees
Revises: merge_heads_payroll_ot_bonus_and_employees2
Create Date: 2026-01-10

This migration:
1. Adds all missing columns from employees2 to employees table
2. Migrates data from employees2 to employees
3. Updates foreign key references from employees2 to employees
4. Drops the employees2 table
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'consolidate_employees'
down_revision = '5f92d4e3bf7b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Consolidate employees2 into employees table."""
    
    # Get connection to check what columns exist
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    
    # Check if employees table exists
    tables = inspector.get_table_names()
    if 'employees' not in tables:
        # Create employees table if it doesn't exist
        op.create_table(
            'employees',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('employee_id', sa.String(100), unique=True, index=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        )
    
    existing_cols = {c['name'] for c in inspector.get_columns('employees')}
    
    # All columns that should exist in the unified employees table
    new_columns = {
        'serial_no': 'VARCHAR(100)',
        'fss_no': 'VARCHAR(100)',
        'name': 'TEXT',
        'rank': 'TEXT',
        'rank2': 'TEXT',
        'status': 'TEXT',
        'status2': 'TEXT',
        'unit': 'TEXT',
        'unit2': 'TEXT',
        'category': 'TEXT',
        'avatar_url': 'TEXT',
        'dob': 'TEXT',
        'cnic_expiry': 'TEXT',
        'documents_held': 'TEXT',
        'photo_on_doc': 'TEXT',
        'mobile_no': 'TEXT',
        'home_contact': 'TEXT',
        'verified_by_sho': 'TEXT',
        'verified_by_ssp': 'TEXT',
        'enrolled': 'TEXT',
        're_enrolled': 'TEXT',
        'village': 'TEXT',
        'post_office': 'TEXT',
        'thana': 'TEXT',
        'tehsil': 'TEXT',
        'district': 'TEXT',
        'duty_location': 'TEXT',
        'address_details': 'TEXT',
        'temp_village': 'TEXT',
        'temp_post_office': 'TEXT',
        'temp_thana': 'TEXT',
        'temp_tehsil': 'TEXT',
        'temp_district': 'TEXT',
        'temp_city': 'TEXT',
        'temp_phone': 'TEXT',
        'temp_address_details': 'TEXT',
        'police_trg_ltr_date': 'TEXT',
        'vaccination_cert': 'TEXT',
        'vol_no': 'TEXT',
        'allocation_status': 'TEXT',
        'cnic_attachment': 'TEXT',
        'domicile_attachment': 'TEXT',
        'sho_verified_attachment': 'TEXT',
        'ssp_verified_attachment': 'TEXT',
        'khidmat_verified_attachment': 'TEXT',
        'police_trg_attachment': 'TEXT',
        'photo_on_doc_attachment': 'TEXT',
        'personal_signature_attachment': 'TEXT',
        'recording_officer_signature_attachment': 'TEXT',
        'fingerprint_thumb_attachment': 'TEXT',
        'fingerprint_index_attachment': 'TEXT',
        'fingerprint_middle_attachment': 'TEXT',
        'fingerprint_ring_attachment': 'TEXT',
        'fingerprint_pinky_attachment': 'TEXT',
        'employment_agreement_attachment': 'TEXT',
        'served_in_attachment': 'TEXT',
        'vaccination_attachment': 'TEXT',
        'experience_security_attachment': 'TEXT',
        'education_attachment': 'TEXT',
        'nok_cnic_attachment': 'TEXT',
        'other_documents_attachment': 'TEXT',
        'height': 'TEXT',
        'education': 'TEXT',
        'medical_details': 'TEXT',
        'medical_discharge_cause': 'TEXT',
        'nok_name': 'TEXT',
        'nok_relationship': 'TEXT',
        'sons_count': 'TEXT',
        'daughters_count': 'TEXT',
        'brothers_count': 'TEXT',
        'sisters_count': 'TEXT',
        'served_in': 'TEXT',
        'experience_security': 'TEXT',
        'deployment_details': 'TEXT',
        'dod': 'TEXT',
        'orig_docs_received': 'TEXT',
        'salary': 'TEXT',
    }
    
    # Add missing columns to employees table
    for col_name, col_type in new_columns.items():
        if col_name not in existing_cols:
            op.add_column('employees', sa.Column(col_name, sa.Text(), nullable=True))
    
    # Create indexes for new columns
    try:
        op.create_index('ix_employees_serial_no', 'employees', ['serial_no'], unique=False)
    except Exception:
        pass
    
    try:
        op.create_index('ix_employees_fss_no', 'employees', ['fss_no'], unique=False)
    except Exception:
        pass
    
    # Check if employees2 table exists and migrate data
    if 'employees2' in tables:
        # Migrate data from employees2 to employees
        # Map columns that exist in both tables
        conn = op.get_bind()
        
        # Get employees2 columns
        emp2_cols = {c['name'] for c in inspector.get_columns('employees2')}
        
        # Common columns to copy (including created_at, updated_at if they exist)
        common_cols = emp2_cols.intersection(existing_cols.union(set(new_columns.keys())))
        common_cols.discard('id')  # Don't copy id
        
        if common_cols:
            cols_str = ', '.join(common_cols)
            # Insert data from employees2 into employees (for new records)
            conn.execute(sa.text(f"""
                INSERT INTO employees ({cols_str})
                SELECT {cols_str}
                FROM employees2
                WHERE employees2.serial_no NOT IN (SELECT serial_no FROM employees WHERE serial_no IS NOT NULL)
                OR employees2.serial_no IS NULL
            """))
    
    # Update foreign keys to reference employees table
    # PayrollSheetEntry
    try:
        op.drop_constraint('payroll_sheet_entries_employee_db_id_fkey', 'payroll_sheet_entries', type_='foreignkey')
    except Exception:
        pass
    
    try:
        op.create_foreign_key(
            'payroll_sheet_entries_employee_db_id_fkey',
            'payroll_sheet_entries', 'employees',
            ['employee_db_id'], ['id']
        )
    except Exception:
        pass
    
    # ClientSiteGuardAllocation
    try:
        op.drop_constraint('client_site_guard_allocations_employee_db_id_fkey', 'client_site_guard_allocations', type_='foreignkey')
    except Exception:
        pass
    
    try:
        op.create_foreign_key(
            'client_site_guard_allocations_employee_db_id_fkey',
            'client_site_guard_allocations', 'employees',
            ['employee_db_id'], ['id']
        )
    except Exception:
        pass
    
    # Drop employees2 table
    if 'employees2' in tables:
        op.drop_table('employees2')


def downgrade() -> None:
    """Recreate employees2 table and restore data (partial - data migration not reversed)."""
    # This is a destructive migration, downgrade will only recreate empty table
    op.create_table(
        'employees2',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('serial_no', sa.String(100), index=True),
        sa.Column('fss_no', sa.String(100), index=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )
    
    # Restore foreign keys to employees2
    try:
        op.drop_constraint('payroll_sheet_entries_employee_db_id_fkey', 'payroll_sheet_entries', type_='foreignkey')
        op.create_foreign_key(
            'payroll_sheet_entries_employee_db_id_fkey',
            'payroll_sheet_entries', 'employees2',
            ['employee_db_id'], ['id']
        )
    except Exception:
        pass
    
    try:
        op.drop_constraint('client_site_guard_allocations_employee_db_id_fkey', 'client_site_guard_allocations', type_='foreignkey')
        op.create_foreign_key(
            'client_site_guard_allocations_employee_db_id_fkey',
            'client_site_guard_allocations', 'employees2',
            ['employee_db_id'], ['id']
        )
    except Exception:
        pass
