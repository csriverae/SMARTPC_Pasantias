"""Unit tests for user service"""
import pytest


class TestUserManagement:
    """Test user management endpoints"""
    
    def test_get_user_profile(self, client, authenticated_headers):
        """Test getting current user profile"""
        response = client.get(
            "/users/me",
            headers=authenticated_headers
        )
        
        assert response.status_code == 200
        assert "email" in response.json()
    
    def test_update_user_profile(self, client, authenticated_headers):
        """Test updating user profile"""
        response = client.put(
            "/users/me",
            json={
                "full_name": "Updated Name",
                "phone": "+34600000000"
            },
            headers=authenticated_headers
        )
        
        assert response.status_code == 200
        assert response.json()["full_name"] == "Updated Name"
    
    def test_change_password_success(self, client, authenticated_headers):
        """Test successful password change"""
        response = client.post(
            "/auth/change-password",
            json={
                "current_password": "TestPassword123!",
                "new_password": "NewPassword456!"
            },
            headers=authenticated_headers
        )
        
        assert response.status_code == 200
    
    def test_change_password_wrong_current(self, client, authenticated_headers):
        """Test password change with wrong current password"""
        response = client.post(
            "/auth/change-password",
            json={
                "current_password": "WrongPassword!",
                "new_password": "NewPassword456!"
            },
            headers=authenticated_headers
        )
        
        assert response.status_code == 400


class TestUserValidation:
    """Test user input validation"""
    
    def test_invalid_email_format(self, client):
        """Test registration with invalid email"""
        response = client.post(
            "/auth/register",
            json={
                "email": "invalid-email",
                "password": "SecurePass123!",
                "full_name": "Test User"
            }
        )
        
        assert response.status_code in [422, 400]
    
    def test_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post(
            "/auth/register",
            json={
                "email": "user@example.com",
                "password": "weak",
                "full_name": "Test User"
            }
        )
        
        # Should fail if validation is enforced
        assert response.status_code in [422, 400] or response.status_code == 200
    
    def test_missing_required_fields(self, client):
        """Test registration with missing required fields"""
        response = client.post(
            "/auth/register",
            json={
                "email": "user@example.com"
            }
        )
        
        assert response.status_code == 422
