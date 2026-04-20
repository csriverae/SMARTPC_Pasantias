"""Unit tests for authentication service"""
import pytest
from app.services.auth_service import AuthService
from app.core.security import verify_password, hash_password


class TestPasswordHashing:
    """Test password hashing and verification"""
    
    def test_hash_password_creates_hash(self):
        """Test that hash_password creates a valid hash"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert "$2b$" in hashed  # bcrypt hash format
    
    def test_verify_password_correct(self):
        """Test verify_password with correct password"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test verify_password with incorrect password"""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_hash_same_password_produces_different_hash(self):
        """Test that hashing same password produces different hashes"""
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2  # Should be different due to salt


class TestAuthenticationFlow:
    """Test authentication endpoints"""
    
    def test_register_user_success(self, client):
        """Test successful user registration"""
        response = client.post(
            "/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123!",
                "full_name": "New User"
            }
        )
        
        assert response.status_code == 200
        assert "user" in response.json() or "id" in response.json()
        assert response.json()["email"] == "newuser@example.com"
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        client.post(
            "/auth/register",
            json={
                "email": "user@example.com",
                "password": "SecurePass123!",
                "full_name": "User One"
            }
        )
        
        response = client.post(
            "/auth/register",
            json={
                "email": "user@example.com",
                "password": "SecurePass456!",
                "full_name": "User Two"
            }
        )
        
        assert response.status_code in [400, 409]
    
    def test_login_success(self, client):
        """Test successful login"""
        # Register user
        client.post(
            "/auth/register",
            json={
                "email": "user@example.com",
                "password": "SecurePass123!",
                "full_name": "Test User"
            }
        )
        
        # Login
        response = client.post(
            "/auth/login",
            json={
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        )
        
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "token_type" in response.json()
    
    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        client.post(
            "/auth/register",
            json={
                "email": "user@example.com",
                "password": "SecurePass123!",
                "full_name": "Test User"
            }
        )
        
        response = client.post(
            "/auth/login",
            json={
                "email": "user@example.com",
                "password": "WrongPassword456!"
            }
        )
        
        assert response.status_code in [401, 400]
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "SomePassword123!"
            }
        )
        
        assert response.status_code in [401, 404, 400]


class TestTokenValidation:
    """Test JWT token validation"""
    
    def test_access_protected_resource_with_token(self, client, authenticated_headers):
        """Test accessing protected resource with valid token"""
        response = client.get(
            "/auth/me",
            headers=authenticated_headers
        )
        
        assert response.status_code == 200
    
    def test_access_protected_resource_without_token(self, client):
        """Test accessing protected resource without token"""
        response = client.get("/auth/me")
        
        assert response.status_code == 401
    
    def test_access_protected_resource_with_invalid_token(self, client):
        """Test accessing protected resource with invalid token"""
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        assert response.status_code == 401
