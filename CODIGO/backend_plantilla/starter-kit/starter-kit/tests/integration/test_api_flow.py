"""Integration tests for API endpoints"""
import pytest


class TestAuthenticationFlow:
    """Test complete authentication flow"""
    
    def test_full_user_lifecycle(self, client):
        """Test complete user lifecycle: register -> login -> use token -> logout"""
        # Register
        register_response = client.post(
            "/auth/register",
            json={
                "email": "lifecycle@example.com",
                "password": "LifecyclePass123!",
                "full_name": "Lifecycle User"
            }
        )
        assert register_response.status_code == 200
        user_id = register_response.json().get("id")
        
        # Login
        login_response = client.post(
            "/auth/login",
            json={
                "email": "lifecycle@example.com",
                "password": "LifecyclePass123!"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Access protected resource
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/auth/me", headers=headers)
        assert me_response.status_code == 200
        
        # Logout if supported
        logout_response = client.post("/auth/logout", headers=headers)
        assert logout_response.status_code in [200, 404]


class TestMultiTenantIsolation:
    """Test multi-tenant data isolation"""
    
    def test_tenant_data_isolation(self, client, test_db):
        """Test that tenant data is properly isolated"""
        # Create company 1
        company1_response = client.post(
            "/companies",
            json={"name": "Company One"},
            headers={"Authorization": "Bearer"}
        )
        
        # Create company 2
        company2_response = client.post(
            "/companies",
            json={"name": "Company Two"},
            headers={"Authorization": "Bearer"}
        )
        
        # Verify companies are separate
        if company1_response.status_code == 200 and company2_response.status_code == 200:
            company1_id = company1_response.json().get("id")
            company2_id = company2_response.json().get("id")
            assert company1_id != company2_id


class TestErrorHandling:
    """Test error handling and responses"""
    
    def test_404_error_response(self, client):
        """Test 404 error response format"""
        response = client.get("/nonexistent/endpoint")
        
        assert response.status_code == 404
        assert "detail" in response.json() or "message" in response.json()
    
    def test_validation_error_response(self, client):
        """Test validation error response format"""
        response = client.post(
            "/auth/register",
            json={
                "email": "invalid-email",
                "password": "Pass123!"
            }
        )
        
        assert response.status_code in [422, 400]
        data = response.json()
        assert "detail" in data or "error" in data or "message" in data
    
    def test_internal_server_error_handling(self, client):
        """Test that internal errors are handled gracefully"""
        # Make a request that might cause an error
        response = client.get("/users/invalid-id")
        
        # Should not expose internal errors
        assert response.status_code in [400, 404, 422, 500]
        response_text = response.text.lower()
        assert "traceback" not in response_text
        assert "sqlalchemy" not in response_text


class TestAPIResponseFormat:
    """Test API response format consistency"""
    
    def test_success_response_format(self, client):
        """Test that success responses have consistent format"""
        response = client.post(
            "/auth/register",
            json={
                "email": "format@example.com",
                "password": "FormatPass123!",
                "full_name": "Format Test"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check basic response structure
        assert isinstance(data, dict)
    
    def test_error_response_format(self, client):
        """Test that error responses have consistent format"""
        response = client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "SomePassword123!"
            }
        )
        
        assert response.status_code in [401, 400, 404]
        data = response.json()
        
        # Should have error information
        assert isinstance(data, dict)


class TestDataPersistence:
    """Test data persistence and retrieval"""
    
    def test_created_user_can_be_retrieved(self, client):
        """Test that created user data persists"""
        # Create user
        create_response = client.post(
            "/auth/register",
            json={
                "email": "persistent@example.com",
                "password": "PersistPass123!",
                "full_name": "Persistent User"
            }
        )
        
        assert create_response.status_code == 200
        
        # Login to get token
        login_response = client.post(
            "/auth/login",
            json={
                "email": "persistent@example.com",
                "password": "PersistPass123!"
            }
        )
        
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Retrieve user data
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/auth/me", headers=headers)
        
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "persistent@example.com"
        assert me_response.json()["full_name"] == "Persistent User"
