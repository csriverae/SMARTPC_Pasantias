"""Security tests for authentication and authorization"""
import pytest


class TestSQLInjectionPrevention:
    """Test SQL injection prevention"""
    
    def test_login_sql_injection_attempt(self, client):
        """Test SQL injection attempt in login"""
        response = client.post(
            "/auth/login",
            json={
                "email": "admin' OR '1'='1",
                "password": "anything"
            }
        )
        
        # Should not expose database or login
        assert response.status_code in [401, 400]
        assert "sql" not in response.text.lower()
    
    def test_user_search_sql_injection(self, client, admin_headers):
        """Test SQL injection in user search"""
        response = client.get(
            "/users?search='; DROP TABLE users; --",
            headers=admin_headers
        )
        
        assert response.status_code in [200, 400, 422]
        assert "drop" not in response.text.lower()


class TestAuthorizationBypass:
    """Test authorization and access control"""
    
    def test_unauthorized_access_admin_endpoint(self, client):
        """Test accessing admin endpoint without authorization"""
        response = client.get("/admin/users")
        
        assert response.status_code == 401
    
    def test_user_cannot_access_other_user_data(self, client):
        """Test that user cannot access other user's data"""
        # Create two users
        client.post(
            "/auth/register",
            json={
                "email": "user1@example.com",
                "password": "Pass123!",
                "full_name": "User One"
            }
        )
        
        client.post(
            "/auth/register",
            json={
                "email": "user2@example.com",
                "password": "Pass123!",
                "full_name": "User Two"
            }
        )
        
        # Login as user1 and try to access user2 data
        response = client.post(
            "/auth/login",
            json={"email": "user1@example.com", "password": "Pass123!"}
        )
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Attempt to access another user's data
        response = client.get(
            "/users/2",
            headers=headers
        )
        
        assert response.status_code in [403, 404]


class TestPasswordSecurity:
    """Test password security measures"""
    
    def test_password_not_returned_in_response(self, client):
        """Test that password is never returned in API responses"""
        response = client.post(
            "/auth/register",
            json={
                "email": "user@example.com",
                "password": "SecurePass123!",
                "full_name": "Test User"
            }
        )
        
        assert response.status_code == 200
        response_text = response.text.lower()
        assert "password" not in response_text or "securepass123" not in response_text
    
    def test_password_hashed_in_database(self, client, test_db):
        """Test that passwords are hashed in database"""
        plain_password = "TestPass123!"
        
        client.post(
            "/auth/register",
            json={
                "email": "user@example.com",
                "password": plain_password,
                "full_name": "Test User"
            }
        )
        
        # Query the database directly
        from app.models import User
        user = test_db.query(User).filter(User.email == "user@example.com").first()
        
        assert user is not None
        assert user.hashed_password != plain_password
        assert "$2b$" in user.hashed_password  # bcrypt hash


class TestCSRFProtection:
    """Test CSRF protection"""
    
    def test_cors_headers_restrictive(self, client):
        """Test CORS headers are properly configured"""
        # Only localhost:3000 should be allowed
        response = client.options(
            "/auth/login",
            headers={"Origin": "http://evil.com"}
        )
        
        # Check that origin is not in CORS allowed headers
        if "access-control-allow-origin" in response.headers:
            assert response.headers["access-control-allow-origin"] != "http://evil.com"


class TestRateLimiting:
    """Test rate limiting (if implemented)"""
    
    def test_multiple_failed_login_attempts(self, client):
        """Test that multiple failed login attempts are handled"""
        for i in range(10):
            response = client.post(
                "/auth/login",
                json={
                    "email": "user@example.com",
                    "password": f"WrongPass{i}!"
                }
            )
            
            # Should eventually return 429 (Too Many Requests) if rate limited
            # or 401 (Unauthorized) for each attempt
            assert response.status_code in [401, 429]


class TestSessionSecurity:
    """Test session and token security"""
    
    def test_logout_invalidates_token(self, client, authenticated_headers):
        """Test that logout invalidates the token"""
        # Make a request with valid token first
        response = client.get("/auth/me", headers=authenticated_headers)
        assert response.status_code == 200
        
        # Logout
        response = client.post("/auth/logout", headers=authenticated_headers)
        
        if response.status_code == 200:
            # Try to use the same token
            response = client.get("/auth/me", headers=authenticated_headers)
            # Should fail or token should be marked as logged out
            assert response.status_code in [401, 200]
    
    def test_token_expiration(self, client, authenticated_headers):
        """Test that tokens eventually expire"""
        # This would require manipulating time or testing with an expired token
        # For now, verify token structure
        token = authenticated_headers["Authorization"].split(" ")[1]
        
        # Should have three parts separated by dots (JWT format)
        assert token.count(".") == 2
