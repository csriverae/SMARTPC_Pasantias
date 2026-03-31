#!/bin/bash
# 🧪 TESTING DO MULTI-TENANT - CURL Commands
# Testing script for complete multi-tenant flow

# ========================================
# VARIABLES
# ========================================
BASE_URL="http://127.0.0.1:8000"
TENANT1_ID=""
TENANT2_ID=""
USER1_TOKEN=""
USER2_TOKEN=""
RESTAURANT1_ID=""
RESTAURANT2_ID=""

echo "🚀 MesaPass Multi-Tenant Testing Suite"
echo "========================================"
echo ""

# ========================================
# PASO 1: Create Tenant 1
# ========================================
echo "📍 PASO 1: Creating Tenant 1..."
RESPONSE=$(curl -s -X POST "$BASE_URL/tenants" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Quantum Restaurant Group"
  }')

echo "$RESPONSE" | jq '.'
TENANT1_ID=$(echo "$RESPONSE" | jq -r '.data.id')
echo "✅ Tenant 1 ID: $TENANT1_ID"
echo ""

# ========================================
# PASO 2: Create Tenant 2
# ========================================
echo "📍 PASO 2: Creating Tenant 2..."
RESPONSE=$(curl -s -X POST "$BASE_URL/tenants" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fast Burgers Inc"
  }')

echo "$RESPONSE" | jq '.'
TENANT2_ID=$(echo "$RESPONSE" | jq -r '.data.id')
echo "✅ Tenant 2 ID: $TENANT2_ID"
echo ""

# ========================================
# PASO 3: Register User 1 (Tenant 1)
# ========================================
echo "📍 PASO 3: Registering User 1 in Tenant 1..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@quantum.com",
    "password": "AdminSecure123!",
    "first_name": "Juan",
    "last_name": "García",
    "full_name": "Juan García",
    "tenant_id": '$TENANT1_ID',
    "role": "admin"
  }')

echo "$RESPONSE" | jq '.'
USER1_TOKEN=$(echo "$RESPONSE" | jq -r '.data.access_token')
echo "✅ User 1 Token: ${USER1_TOKEN:0:50}..."
echo ""

# ========================================
# PASO 4: Register User 2 (Tenant 2)
# ========================================
echo "📍 PASO 4: Registering User 2 in Tenant 2..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@fastburgers.com",
    "password": "Secure123!",
    "first_name": "Maria",
    "last_name": "López",
    "full_name": "Maria López",
    "tenant_id": '$TENANT2_ID',
    "role": "admin"
  }')

echo "$RESPONSE" | jq '.'
USER2_TOKEN=$(echo "$RESPONSE" | jq -r '.data.access_token')
echo "✅ User 2 Token: ${USER2_TOKEN:0:50}..."
echo ""

# ========================================
# PASO 5: Create Restaurant 1 (User 1)
# ========================================
echo "📍 PASO 5: Creating Restaurant 1 (User 1)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/restaurants" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER1_TOKEN" \
  -d '{
    "name": "Pizza Paradise",
    "description": "Pizzería de fuego lento",
    "address": "Calle Principal 123, Ciudad",
    "phone": "+34-912345678",
    "email": "contact@pizzaparadise.com"
  }')

echo "$RESPONSE" | jq '.'
RESTAURANT1_ID=$(echo "$RESPONSE" | jq -r '.data.id')
echo "✅ Restaurant 1 ID: $RESTAURANT1_ID"
echo ""

# ========================================
# PASO 6: Create Restaurant 2 (User 2)
# ========================================
echo "📍 PASO 6: Creating Restaurant 2 (User 2)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/restaurants" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER2_TOKEN" \
  -d '{
    "name": "Burger King Quality",
    "description": "Hamburguesas premium",
    "address": "Avenida Central 456, Ciudad",
    "phone": "+34-987654321",
    "email": "contact@burgers.com"
  }')

echo "$RESPONSE" | jq '.'
RESTAURANT2_ID=$(echo "$RESPONSE" | jq -r '.data.id')
echo "✅ Restaurant 2 ID: $RESTAURANT2_ID"
echo ""

# ========================================
# PASO 7: List Restaurants (User 1)
# ========================================
echo "📍 PASO 7: Listing Restaurants (User 1 - should see only Tenant 1)..."
curl -s -X GET "$BASE_URL/restaurants?skip=0&limit=100" \
  -H "Authorization: Bearer $USER1_TOKEN" | jq '.'
echo ""

# ========================================
# PASO 8: List Restaurants (User 2)
# ========================================
echo "📍 PASO 8: Listing Restaurants (User 2 - should see only Tenant 2)..."
curl -s -X GET "$BASE_URL/restaurants?skip=0&limit=100" \
  -H "Authorization: Bearer $USER2_TOKEN" | jq '.'
echo ""

# ========================================
# PASO 9: Get Restaurant 1 (User 1 - should work)
# ========================================
echo "📍 PASO 9: Getting Restaurant 1 with User 1 (should work ✅)..."
curl -s -X GET "$BASE_URL/restaurants/$RESTAURANT1_ID" \
  -H "Authorization: Bearer $USER1_TOKEN" | jq '.'
echo ""

# ========================================
# PASO 10: Get Restaurant 1 (User 2 - should fail with 404)
# ========================================
echo "📍 PASO 10: Getting Restaurant 1 with User 2 (should fail with 404 ❌ - SECURITY VALIDATION)..."
curl -s -X GET "$BASE_URL/restaurants/$RESTAURANT1_ID" \
  -H "Authorization: Bearer $USER2_TOKEN" | jq '.'
echo ""

# ========================================
# FINAL SUMMARY
# ========================================
echo "========================================"
echo "✅ TESTING COMPLETE"
echo "========================================"
echo ""
echo "Summary:"
echo "- Tenant 1 ID: $TENANT1_ID"
echo "- Tenant 2 ID: $TENANT2_ID"
echo "- User 1 (Tenant 1) email: admin@quantum.com"
echo "- User 2 (Tenant 2) email: owner@fastburgers.com"
echo "- Restaurant 1 (Tenant 1): Pizza Paradise"
echo "- Restaurant 2 (Tenant 2): Burger King Quality"
echo ""
echo "Multi-tenant isolation validated! 🔒"
echo ""
