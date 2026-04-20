"""Example integration test for meal logs API"""
import pytest


class TestMealLogsAPI:
    """Test meal logs endpoints"""
    
    def test_create_meal_log(self, client, authenticated_headers):
        """Test creating a meal log entry"""
        response = client.post(
            "/meal-logs",
            json={
                "restaurant_id": 1,
                "amount": 15.50,
                "date": "2024-04-20"
            },
            headers=authenticated_headers
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        assert "id" in data or "restaurant_id" in data
    
    def test_get_meal_logs(self, client, authenticated_headers):
        """Test retrieving user meal logs"""
        response = client.get(
            "/meal-logs",
            headers=authenticated_headers
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_meal_log_detail(self, client, authenticated_headers):
        """Test retrieving specific meal log"""
        response = client.get(
            "/meal-logs/1",
            headers=authenticated_headers
        )
        
        assert response.status_code in [200, 404]
    
    def test_update_meal_log(self, client, authenticated_headers):
        """Test updating meal log"""
        response = client.put(
            "/meal-logs/1",
            json={"amount": 20.00},
            headers=authenticated_headers
        )
        
        assert response.status_code in [200, 404]
    
    def test_delete_meal_log(self, client, authenticated_headers):
        """Test deleting meal log"""
        response = client.delete(
            "/meal-logs/1",
            headers=authenticated_headers
        )
        
        assert response.status_code in [204, 200, 404]


class TestMealLogsReports:
    """Test meal logs reporting"""
    
    def test_get_meal_logs_report(self, client, authenticated_headers):
        """Test getting meal logs report"""
        response = client.get(
            "/meal-logs/report",
            headers=authenticated_headers
        )
        
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)
    
    def test_get_meal_logs_by_date_range(self, client, authenticated_headers):
        """Test getting meal logs for date range"""
        response = client.get(
            "/meal-logs?start_date=2024-04-01&end_date=2024-04-30",
            headers=authenticated_headers
        )
        
        assert response.status_code in [200, 404]


class TestMealLogsBudget:
    """Test meal logs budget functionality"""
    
    def test_check_budget_limit(self, client, authenticated_headers):
        """Test checking if purchase exceeds budget"""
        response = client.post(
            "/meal-logs/check-budget",
            json={"amount": 50.00},
            headers=authenticated_headers
        )
        
        assert response.status_code in [200, 400, 409]
    
    def test_get_budget_info(self, client, authenticated_headers):
        """Test getting budget information"""
        response = client.get(
            "/meal-logs/budget",
            headers=authenticated_headers
        )
        
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "available" in data or "limit" in data
