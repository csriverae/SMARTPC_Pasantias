"""Complete schema with UUID and multi-tenancy

Revision ID: new_schema_001
Revises: dc7a488dc538
Create Date: 2026-04-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'new_schema_001'
down_revision: Union[str, Sequence[str], None] = 'dc7a488dc538'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to UUID and multi-tenancy."""
    
    # Drop existing tables to start fresh
    op.execute("DROP TABLE IF EXISTS alembic_version CASCADE")
    op.execute("DROP TABLE IF EXISTS meal_logs CASCADE")
    op.execute("DROP TABLE IF EXISTS invitation_codes CASCADE")
    op.execute("DROP TABLE IF EXISTS employees CASCADE")
    op.execute("DROP TABLE IF EXISTS agreements CASCADE")
    op.execute("DROP TABLE IF EXISTS restaurants CASCADE")
    op.execute("DROP TABLE IF EXISTS companies CASCADE")
    op.execute("DROP TABLE IF EXISTS user_tenants CASCADE")
    op.execute("DROP TABLE IF EXISTS users CASCADE")
    op.execute("DROP TABLE IF EXISTS tenants CASCADE")

    # TENANTS
    op.create_table(
        'tenants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Index('ix_tenants_name', 'name')
    )

    # USERS
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=True),
        sa.Column('last_name', sa.String(255), nullable=True),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Index('ix_users_email', 'email')
    )

    # USER_TENANTS (many-to-many with roles)
    op.create_table(
        'user_tenants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('user_id', 'tenant_id', name='uq_user_tenant'),
        sa.Index('ix_user_tenants_user_id', 'user_id'),
        sa.Index('ix_user_tenants_tenant_id', 'tenant_id')
    )

    # COMPANIES
    op.create_table(
        'companies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Index('ix_companies_tenant_id', 'tenant_id')
    )

    # RESTAURANTS
    op.create_table(
        'restaurants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Index('ix_restaurants_tenant_id', 'tenant_id'),
        sa.Index('ix_restaurants_name', 'name')
    )

    # AGREEMENTS (company ↔ restaurant)
    op.create_table(
        'agreements',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('company_tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('restaurant_tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('subsidy_type', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Index('ix_agreements_company_tenant_id', 'company_tenant_id'),
        sa.Index('ix_agreements_restaurant_tenant_id', 'restaurant_tenant_id')
    )

    # EMPLOYEES
    op.create_table(
        'employees',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('company_tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('cedula', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Index('ix_employees_user_id', 'user_id'),
        sa.Index('ix_employees_company_tenant_id', 'company_tenant_id')
    )

    # MEAL LOGS
    op.create_table(
        'meal_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('employee_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False),
        sa.Column('restaurant_tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('agreement_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agreements.id', ondelete='CASCADE'), nullable=True),
        sa.Column('consumed_at', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Index('ix_meal_logs_employee_id', 'employee_id'),
        sa.Index('ix_meal_logs_restaurant_tenant_id', 'restaurant_tenant_id')
    )

    # INVITATION CODES
    op.create_table(
        'invitation_codes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('code', sa.String(100), unique=True, nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(50), nullable=True),
        sa.Column('is_used', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now(), nullable=False),
        sa.Index('ix_invitation_codes_code', 'code'),
        sa.Index('ix_invitation_codes_tenant_id', 'tenant_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('invitation_codes')
    op.drop_table('meal_logs')
    op.drop_table('employees')
    op.drop_table('agreements')
    op.drop_table('restaurants')
    op.drop_table('companies')
    op.drop_table('user_tenants')
    op.drop_table('users')
    op.drop_table('tenants')
