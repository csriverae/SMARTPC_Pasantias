-- Migration: Create user_invitations table
-- Compatible with PostgreSQL

CREATE TABLE IF NOT EXISTS user_invitations (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    code VARCHAR UNIQUE NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'user',
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    invited_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'expired')),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_invitations_email ON user_invitations(email);
CREATE INDEX IF NOT EXISTS idx_user_invitations_code ON user_invitations(code);
CREATE INDEX IF NOT EXISTS idx_user_invitations_tenant_id ON user_invitations(tenant_id);
CREATE INDEX IF NOT EXISTS idx_user_invitations_invited_by ON user_invitations(invited_by);
CREATE INDEX IF NOT EXISTS idx_user_invitations_status ON user_invitations(status);
CREATE INDEX IF NOT EXISTS idx_user_invitations_expires_at ON user_invitations(expires_at);

-- Add comments for documentation
COMMENT ON TABLE user_invitations IS 'User invitation system for SaaS multi-tenant application';
COMMENT ON COLUMN user_invitations.email IS 'Email address of the invited user';
COMMENT ON COLUMN user_invitations.code IS 'Unique invitation code for acceptance';
COMMENT ON COLUMN user_invitations.role IS 'Role assigned to the invited user';
COMMENT ON COLUMN user_invitations.tenant_id IS 'Tenant that owns this invitation';
COMMENT ON COLUMN user_invitations.invited_by IS 'User ID who sent the invitation';
COMMENT ON COLUMN user_invitations.status IS 'Current status of the invitation';
COMMENT ON COLUMN user_invitations.expires_at IS 'When the invitation expires';
COMMENT ON COLUMN user_invitations.created_at IS 'When the invitation was created';