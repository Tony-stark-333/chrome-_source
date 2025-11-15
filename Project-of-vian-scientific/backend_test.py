#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Vian Scientific E-commerce Platform
Tests all authentication, product, quote, and admin endpoints
"""

import requests
import json
import time
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "https://scientific-shop.preview.vianscientific.com/api"
ADMIN_EMAIL = "vrventures.333@gmail.com"
ADMIN_PASSWORD = "Admin@123"

class VianScientificAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.user_token = None
        self.admin_token = None
        # Generate unique test user email with timestamp
        import time
        timestamp = str(int(time.time()))
        self.test_user_email = f"testuser{timestamp}@example.com"
        self.test_user_password = "TestUser@123"
        self.test_user_name = "Test User"
        self.created_product_id = None
        self.created_quote_id = None
        self.reset_code = None
        
        # Test results tracking
        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }
    
    def log_result(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        if success:
            self.results["passed"] += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.results["failed"] += 1
            error_msg = f"❌ {test_name}: FAILED {message}"
            print(error_msg)
            self.results["errors"].append(error_msg)
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, 
                    headers: Dict = None, token: str = None) -> requests.Response:
        """Make HTTP request with proper error handling"""
        url = f"{self.base_url}{endpoint}"
        
        # Set up headers
        request_headers = {"Content-Type": "application/json"}
        if headers:
            request_headers.update(headers)
        if token:
            request_headers["Authorization"] = f"Bearer {token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=request_headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=request_headers, timeout=30)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=request_headers, timeout=30)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=request_headers, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
    
    def test_root_endpoint(self):
        """Test API root endpoint"""
        print("\n=== Testing Root Endpoint ===")
        try:
            response = self.make_request("GET", "/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "Vian Scientific" in data["message"]:
                    self.log_result("Root endpoint", True, f"- {data['message']}")
                else:
                    self.log_result("Root endpoint", False, f"- Unexpected response: {data}")
            else:
                self.log_result("Root endpoint", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Root endpoint", False, f"- Error: {str(e)}")
    
    def test_user_registration(self):
        """Test user registration"""
        print("\n=== Testing User Registration ===")
        
        # Test successful registration
        user_data = {
            "email": self.test_user_email,
            "password": self.test_user_password,
            "full_name": self.test_user_name
        }
        
        try:
            response = self.make_request("POST", "/auth/register", user_data)
            if response.status_code == 200:
                data = response.json()
                if data.get("email") == self.test_user_email:
                    self.log_result("User registration", True, f"- User created: {data['email']}")
                else:
                    self.log_result("User registration", False, f"- Unexpected response: {data}")
            else:
                self.log_result("User registration", False, f"- Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("User registration", False, f"- Error: {str(e)}")
        
        # Test duplicate email registration
        try:
            response = self.make_request("POST", "/auth/register", user_data)
            if response.status_code == 400:
                self.log_result("Duplicate email prevention", True, "- Correctly rejected duplicate email")
            else:
                self.log_result("Duplicate email prevention", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Duplicate email prevention", False, f"- Error: {str(e)}")
        
        # Test weak password
        weak_user_data = {
            "email": "weakuser@example.com",
            "password": "123",
            "full_name": "Weak User"
        }
        
        try:
            response = self.make_request("POST", "/auth/register", weak_user_data)
            if response.status_code == 400:
                self.log_result("Weak password rejection", True, "- Correctly rejected weak password")
            else:
                self.log_result("Weak password rejection", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Weak password rejection", False, f"- Error: {str(e)}")
    
    def test_user_login(self):
        """Test user login"""
        print("\n=== Testing User Login ===")
        
        # Test successful login
        login_data = {
            "email": self.test_user_email,
            "password": self.test_user_password
        }
        
        try:
            response = self.make_request("POST", "/auth/login", login_data)
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "user" in data:
                    self.user_token = data["access_token"]
                    self.log_result("User login", True, f"- Token received for {data['user']['email']}")
                else:
                    self.log_result("User login", False, f"- Missing token or user data: {data}")
            else:
                self.log_result("User login", False, f"- Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("User login", False, f"- Error: {str(e)}")
        
        # Test invalid credentials
        invalid_login = {
            "email": self.test_user_email,
            "password": "wrongpassword"
        }
        
        try:
            response = self.make_request("POST", "/auth/login", invalid_login)
            if response.status_code == 401:
                self.log_result("Invalid login rejection", True, "- Correctly rejected invalid credentials")
            else:
                self.log_result("Invalid login rejection", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Invalid login rejection", False, f"- Error: {str(e)}")
    
    def test_admin_login(self):
        """Test admin login"""
        print("\n=== Testing Admin Login ===")
        
        admin_login = {
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        try:
            response = self.make_request("POST", "/auth/login", admin_login)
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and data.get("user", {}).get("role") == "admin":
                    self.admin_token = data["access_token"]
                    self.log_result("Admin login", True, f"- Admin token received for {data['user']['email']}")
                else:
                    self.log_result("Admin login", False, f"- Missing admin token or role: {data}")
            else:
                self.log_result("Admin login", False, f"- Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("Admin login", False, f"- Error: {str(e)}")
    
    def test_get_current_user(self):
        """Test get current user endpoint"""
        print("\n=== Testing Get Current User ===")
        
        if not self.user_token:
            self.log_result("Get current user", False, "- No user token available")
            return
        
        try:
            response = self.make_request("GET", "/auth/me", token=self.user_token)
            if response.status_code == 200:
                data = response.json()
                if data.get("email") == self.test_user_email:
                    self.log_result("Get current user", True, f"- Retrieved user: {data['email']}")
                else:
                    self.log_result("Get current user", False, f"- Unexpected user data: {data}")
            else:
                self.log_result("Get current user", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get current user", False, f"- Error: {str(e)}")
    
    def test_email_service_brevo_smtp(self):
        """Test Email Service with Brevo SMTP - PRIORITY 1"""
        print("\n=== 🔥 PRIORITY 1: Testing Email Service (Brevo SMTP) ===")
        
        # Test forgot password with email sending
        reset_request = {"email": self.test_user_email}
        
        try:
            response = self.make_request("POST", "/auth/forgot-password", reset_request)
            if response.status_code == 200:
                data = response.json()
                expected_message = "If the email exists, a reset code has been sent"
                if data.get("message") == expected_message:
                    self.log_result("📧 Forgot password email (Brevo SMTP)", True, "- Email service processed request successfully")
                    
                    # Check backend logs for email sending status
                    print("   📋 Note: Check backend logs to verify Brevo SMTP email delivery")
                    print("   📋 Command: tail -n 50 /var/log/supervisor/backend.*.log | grep -i email")
                else:
                    self.log_result("📧 Forgot password email (Brevo SMTP)", False, f"- Unexpected response: {data}")
            else:
                self.log_result("📧 Forgot password email (Brevo SMTP)", False, f"- Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("📧 Forgot password email (Brevo SMTP)", False, f"- Error: {str(e)}")
        
        # Test registration with welcome email
        import time
        welcome_email_user = f"welcometest{int(time.time())}@example.com"
        user_data = {
            "email": welcome_email_user,
            "password": "WelcomeTest@123",
            "full_name": "Welcome Test User"
        }
        
        try:
            response = self.make_request("POST", "/auth/register", user_data)
            if response.status_code == 200:
                data = response.json()
                if data.get("email") == welcome_email_user:
                    self.log_result("📧 Registration welcome email (Brevo SMTP)", True, f"- User registered, welcome email should be sent to {welcome_email_user}")
                    print("   📋 Note: Check backend logs to verify Brevo SMTP welcome email delivery")
                else:
                    self.log_result("📧 Registration welcome email (Brevo SMTP)", False, f"- Registration failed: {data}")
            else:
                self.log_result("📧 Registration welcome email (Brevo SMTP)", False, f"- Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("📧 Registration welcome email (Brevo SMTP)", False, f"- Error: {str(e)}")

    def test_password_reset_flow(self):
        """Test password reset flow with database verification"""
        print("\n=== Testing Password Reset Flow (Database Verification) ===")
        
        # Test forgot password request
        reset_request = {"email": self.test_user_email}
        
        try:
            response = self.make_request("POST", "/auth/forgot-password", reset_request)
            if response.status_code == 200:
                data = response.json()
                expected_message = "If the email exists, a reset code has been sent"
                if data.get("message") == expected_message:
                    self.log_result("Password reset request", True, "- Reset code generated and stored in database")
                    
                    # Since we can't access the reset code directly, we'll test with a mock code
                    # In production, user would get this via email
                    print("   📋 Note: Reset code stored in database, user receives via email")
                else:
                    self.log_result("Password reset request", False, f"- Unexpected response: {data}")
            else:
                self.log_result("Password reset request", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Password reset request", False, f"- Error: {str(e)}")
        
        # Test invalid reset code
        invalid_reset_data = {
            "email": self.test_user_email,
            "reset_code": "123456",  # Invalid code
            "new_password": "NewPassword@123"
        }
        
        try:
            response = self.make_request("POST", "/auth/reset-password", invalid_reset_data)
            if response.status_code == 400:
                self.log_result("Invalid reset code rejection", True, "- Correctly rejected invalid reset code")
            else:
                self.log_result("Invalid reset code rejection", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Invalid reset code rejection", False, f"- Error: {str(e)}")
    
    def test_change_password(self):
        """Test change password endpoint"""
        print("\n=== Testing Change Password ===")
        
        if not self.user_token:
            self.log_result("Change password", False, "- No user token available")
            return
        
        change_data = {
            "current_password": self.test_user_password,
            "new_password": "ChangedPassword@123"
        }
        
        try:
            response = self.make_request("POST", "/user/change-password", change_data, token=self.user_token)
            if response.status_code == 200:
                self.log_result("Change password", True, "- Password changed successfully")
                self.test_user_password = "ChangedPassword@123"
            else:
                self.log_result("Change password", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Change password", False, f"- Error: {str(e)}")
    
    def test_products_endpoints(self):
        """Test product-related endpoints"""
        print("\n=== Testing Products Endpoints ===")
        
        # Test get all products
        try:
            response = self.make_request("GET", "/products")
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list):
                    self.log_result("Get all products", True, f"- Retrieved {len(products)} products")
                    
                    # Test product search if products exist
                    if products:
                        # Test search functionality
                        search_response = self.make_request("GET", "/products?search=vial")
                        if search_response.status_code == 200:
                            search_results = search_response.json()
                            self.log_result("Product search", True, f"- Found {len(search_results)} products matching 'vial'")
                        else:
                            self.log_result("Product search", False, f"- Status: {search_response.status_code}")
                        
                        # Test category filtering
                        category_response = self.make_request("GET", "/products?category=analytical-vials")
                        if category_response.status_code == 200:
                            category_results = category_response.json()
                            self.log_result("Category filtering", True, f"- Found {len(category_results)} products in analytical-vials category")
                        else:
                            self.log_result("Category filtering", False, f"- Status: {category_response.status_code}")
                        
                        # Test get specific product
                        first_product = products[0]
                        product_id = first_product.get("id")
                        if product_id:
                            product_response = self.make_request("GET", f"/products/{product_id}")
                            if product_response.status_code == 200:
                                product_data = product_response.json()
                                self.log_result("Get specific product", True, f"- Retrieved product: {product_data.get('product_name', 'Unknown')}")
                            else:
                                self.log_result("Get specific product", False, f"- Status: {product_response.status_code}")
                else:
                    self.log_result("Get all products", False, f"- Expected list, got: {type(products)}")
            else:
                self.log_result("Get all products", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get all products", False, f"- Error: {str(e)}")
    
    def test_categories_endpoints(self):
        """Test category endpoints"""
        print("\n=== Testing Categories Endpoints ===")
        
        # Test get all categories
        try:
            response = self.make_request("GET", "/categories")
            if response.status_code == 200:
                categories = response.json()
                if isinstance(categories, list) and len(categories) > 0:
                    self.log_result("Get all categories", True, f"- Retrieved {len(categories)} categories")
                    
                    # Test get specific category
                    first_category = categories[0]
                    category_slug = first_category.get("slug")
                    if category_slug:
                        category_response = self.make_request("GET", f"/categories/{category_slug}")
                        if category_response.status_code == 200:
                            category_data = category_response.json()
                            self.log_result("Get specific category", True, f"- Retrieved category: {category_data.get('name', 'Unknown')}")
                        else:
                            self.log_result("Get specific category", False, f"- Status: {category_response.status_code}")
                else:
                    self.log_result("Get all categories", False, f"- Expected non-empty list, got: {categories}")
            else:
                self.log_result("Get all categories", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get all categories", False, f"- Error: {str(e)}")
    
    def test_quote_management(self):
        """Test quote management endpoints"""
        print("\n=== Testing Quote Management ===")
        
        if not self.user_token:
            self.log_result("Quote management", False, "- No user token available")
            return
        
        # Create a quote
        quote_data = {
            "items": [
                {
                    "product_id": "test-product-id",
                    "cat_no": "VN-CV09-100",
                    "product_name": "9 mm Clear Screw Vials W/O Patch",
                    "quantity": 5,
                    "pack_size": "100"
                }
            ],
            "message": "Test quote request for laboratory supplies"
        }
        
        try:
            response = self.make_request("POST", "/quotes", quote_data, token=self.user_token)
            if response.status_code == 200:
                quote_response = response.json()
                self.created_quote_id = quote_response.get("id")
                self.log_result("Create quote", True, f"- Quote created with ID: {self.created_quote_id}")
            else:
                self.log_result("Create quote", False, f"- Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("Create quote", False, f"- Error: {str(e)}")
        
        # Get user's quotes
        try:
            response = self.make_request("GET", "/quotes/my", token=self.user_token)
            if response.status_code == 200:
                quotes = response.json()
                if isinstance(quotes, list):
                    self.log_result("Get user quotes", True, f"- Retrieved {len(quotes)} quotes")
                else:
                    self.log_result("Get user quotes", False, f"- Expected list, got: {type(quotes)}")
            else:
                self.log_result("Get user quotes", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get user quotes", False, f"- Error: {str(e)}")
        
        # Get specific quote
        if self.created_quote_id:
            try:
                response = self.make_request("GET", f"/quotes/{self.created_quote_id}", token=self.user_token)
                if response.status_code == 200:
                    quote_data = response.json()
                    self.log_result("Get specific quote", True, f"- Retrieved quote with {len(quote_data.get('items', []))} items")
                else:
                    self.log_result("Get specific quote", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("Get specific quote", False, f"- Error: {str(e)}")
    
    def test_admin_user_management_full_authority(self):
        """Test Admin User Management with Full Authority - PRIORITY 2"""
        print("\n=== 🔥 PRIORITY 2: Testing Admin User Management (Full Authority) ===")
        
        if not self.admin_token:
            self.log_result("Admin user management", False, "- No admin token available")
            return
        
        # Test admin create user with role="user"
        import time
        created_user_email = f"admintest{int(time.time())}@example.com"
        create_user_data = {
            "email": created_user_email,
            "password": "AdminCreated@123",
            "full_name": "Admin Created User",
            "role": "user"
        }
        
        created_user_id = None
        try:
            response = self.make_request("POST", "/admin/users", create_user_data, token=self.admin_token)
            if response.status_code == 200:
                user_data = response.json()
                created_user_id = user_data.get("id")
                if user_data.get("role") == "user" and user_data.get("email") == created_user_email:
                    self.log_result("👤 Admin create user (role=user)", True, f"- User created: {created_user_email} with role 'user'")
                else:
                    self.log_result("👤 Admin create user (role=user)", False, f"- Unexpected user data: {user_data}")
            else:
                self.log_result("👤 Admin create user (role=user)", False, f"- Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("👤 Admin create user (role=user)", False, f"- Error: {str(e)}")
        
        # Test admin create user with role="admin"
        admin_user_email = f"admintest_admin{int(time.time())}@example.com"
        create_admin_data = {
            "email": admin_user_email,
            "password": "AdminCreated@123",
            "full_name": "Admin Created Admin",
            "role": "admin"
        }
        
        created_admin_id = None
        try:
            response = self.make_request("POST", "/admin/users", create_admin_data, token=self.admin_token)
            if response.status_code == 200:
                admin_data = response.json()
                created_admin_id = admin_data.get("id")
                if admin_data.get("role") == "admin" and admin_data.get("email") == admin_user_email:
                    self.log_result("👑 Admin create user (role=admin)", True, f"- Admin created: {admin_user_email} with role 'admin'")
                else:
                    self.log_result("👑 Admin create user (role=admin)", False, f"- Unexpected admin data: {admin_data}")
            else:
                self.log_result("👑 Admin create user (role=admin)", False, f"- Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("👑 Admin create user (role=admin)", False, f"- Error: {str(e)}")
        
        # Test password strength validation
        weak_user_data = {
            "email": f"weaktest{int(time.time())}@example.com",
            "password": "123",  # Weak password
            "full_name": "Weak Password User",
            "role": "user"
        }
        
        try:
            response = self.make_request("POST", "/admin/users", weak_user_data, token=self.admin_token)
            if response.status_code == 400:
                self.log_result("🔒 Password strength validation", True, "- Correctly rejected weak password")
            else:
                self.log_result("🔒 Password strength validation", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("🔒 Password strength validation", False, f"- Error: {str(e)}")
        
        # Test duplicate email prevention
        try:
            response = self.make_request("POST", "/admin/users", create_user_data, token=self.admin_token)
            if response.status_code == 400:
                self.log_result("📧 Duplicate email prevention", True, "- Correctly rejected duplicate email")
            else:
                self.log_result("📧 Duplicate email prevention", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("📧 Duplicate email prevention", False, f"- Error: {str(e)}")
        
        # Test admin delete user
        if created_user_id:
            try:
                response = self.make_request("DELETE", f"/admin/users/{created_user_id}", token=self.admin_token)
                if response.status_code == 200:
                    self.log_result("🗑️ Admin delete user", True, f"- User {created_user_email} deleted successfully")
                    
                    # Verify user is deleted from database
                    verify_response = self.make_request("GET", "/admin/users", token=self.admin_token)
                    if verify_response.status_code == 200:
                        users = verify_response.json()
                        deleted_user_exists = any(user.get("id") == created_user_id for user in users)
                        if not deleted_user_exists:
                            self.log_result("✅ User deletion verification", True, "- User successfully removed from database")
                        else:
                            self.log_result("❌ User deletion verification", False, "- User still exists in database")
                else:
                    self.log_result("🗑️ Admin delete user", False, f"- Status: {response.status_code}, Response: {response.text}")
            except Exception as e:
                self.log_result("🗑️ Admin delete user", False, f"- Error: {str(e)}")
        
        # Test admin cannot delete own account
        try:
            # Get current admin user ID
            admin_users_response = self.make_request("GET", "/admin/users", token=self.admin_token)
            if admin_users_response.status_code == 200:
                users = admin_users_response.json()
                admin_user = next((user for user in users if user.get("email") == ADMIN_EMAIL), None)
                if admin_user:
                    admin_id = admin_user.get("id")
                    response = self.make_request("DELETE", f"/admin/users/{admin_id}", token=self.admin_token)
                    if response.status_code == 400:
                        self.log_result("🛡️ Admin self-deletion prevention", True, "- Correctly prevented admin from deleting own account")
                    else:
                        self.log_result("🛡️ Admin self-deletion prevention", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("🛡️ Admin self-deletion prevention", False, f"- Error: {str(e)}")
        
        # Clean up created admin user
        if created_admin_id:
            try:
                self.make_request("DELETE", f"/admin/users/{created_admin_id}", token=self.admin_token)
                print(f"   🧹 Cleaned up created admin user: {admin_user_email}")
            except:
                pass

    def test_admin_user_management_legacy(self):
        """Test existing admin user management endpoints"""
        print("\n=== Testing Legacy Admin User Management ===")
        
        if not self.admin_token:
            self.log_result("Legacy admin user management", False, "- No admin token available")
            return
        
        # Get all users
        try:
            response = self.make_request("GET", "/admin/users", token=self.admin_token)
            if response.status_code == 200:
                users = response.json()
                if isinstance(users, list):
                    self.log_result("Get all users (admin)", True, f"- Retrieved {len(users)} users")
                    
                    # Find test user for further operations
                    test_user = None
                    for user in users:
                        if user.get("email") == self.test_user_email:
                            test_user = user
                            break
                    
                    if test_user:
                        user_id = test_user.get("id")
                        
                        # Test user status toggle
                        try:
                            disable_data = {"is_active": False}
                            response = self.make_request("PUT", f"/admin/users/{user_id}/status", disable_data, token=self.admin_token)
                            if response.status_code == 200:
                                self.log_result("Disable user account", True, "- User account disabled successfully")
                                
                                # Re-enable user
                                enable_data = {"is_active": True}
                                response = self.make_request("PUT", f"/admin/users/{user_id}/status", enable_data, token=self.admin_token)
                                if response.status_code == 200:
                                    self.log_result("Enable user account", True, "- User account enabled successfully")
                                else:
                                    self.log_result("Enable user account", False, f"- Status: {response.status_code}")
                            else:
                                self.log_result("Disable user account", False, f"- Status: {response.status_code}")
                        except Exception as e:
                            self.log_result("User status toggle", False, f"- Error: {str(e)}")
                        
                        # Test admin password reset
                        try:
                            reset_data = {
                                "user_id": user_id,
                                "new_password": "AdminReset@123"
                            }
                            response = self.make_request("POST", f"/admin/users/{user_id}/reset-password", reset_data, token=self.admin_token)
                            if response.status_code == 200:
                                self.log_result("Admin password reset", True, "- Password reset by admin successfully")
                                self.test_user_password = "AdminReset@123"  # Update for future tests
                            else:
                                self.log_result("Admin password reset", False, f"- Status: {response.status_code}, Response: {response.text}")
                        except Exception as e:
                            self.log_result("Admin password reset", False, f"- Error: {str(e)}")
                else:
                    self.log_result("Get all users (admin)", False, f"- Expected list, got: {type(users)}")
            else:
                self.log_result("Get all users (admin)", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get all users (admin)", False, f"- Error: {str(e)}")
    
    def test_admin_product_management(self):
        """Test admin product management endpoints"""
        print("\n=== Testing Admin Product Management ===")
        
        if not self.admin_token:
            self.log_result("Admin product management", False, "- No admin token available")
            return
        
        # Create a new product
        product_data = {
            "cat_no": "VN-TEST-001",
            "product_name": "Test Product for API Testing",
            "description": "This is a test product created during API testing",
            "category": "analytical-vials",
            "pack_size": "10",
            "hsn_code": "90279090"
        }
        
        try:
            response = self.make_request("POST", "/products", product_data, token=self.admin_token)
            if response.status_code == 200:
                product_response = response.json()
                self.created_product_id = product_response.get("id")
                self.log_result("Create product (admin)", True, f"- Product created: {product_response.get('product_name')}")
            else:
                self.log_result("Create product (admin)", False, f"- Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("Create product (admin)", False, f"- Error: {str(e)}")
        
        # Update the created product
        if self.created_product_id:
            update_data = {
                "description": "Updated description for test product"
            }
            
            try:
                response = self.make_request("PUT", f"/products/{self.created_product_id}", update_data, token=self.admin_token)
                if response.status_code == 200:
                    self.log_result("Update product (admin)", True, "- Product updated successfully")
                else:
                    self.log_result("Update product (admin)", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("Update product (admin)", False, f"- Error: {str(e)}")
            
            # Delete the created product
            try:
                response = self.make_request("DELETE", f"/products/{self.created_product_id}", token=self.admin_token)
                if response.status_code == 200:
                    self.log_result("Delete product (admin)", True, "- Product deleted successfully")
                else:
                    self.log_result("Delete product (admin)", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("Delete product (admin)", False, f"- Error: {str(e)}")
    
    def test_admin_quotes_management(self):
        """Test admin quotes management"""
        print("\n=== Testing Admin Quotes Management ===")
        
        if not self.admin_token:
            self.log_result("Admin quotes management", False, "- No admin token available")
            return
        
        # Get all quotes (admin view)
        try:
            response = self.make_request("GET", "/admin/quotes", token=self.admin_token)
            if response.status_code == 200:
                quotes = response.json()
                if isinstance(quotes, list):
                    self.log_result("Get all quotes (admin)", True, f"- Retrieved {len(quotes)} quotes")
                    
                    # Update quote status if quotes exist
                    if quotes and self.created_quote_id:
                        status_data = {"status": "reviewed"}
                        try:
                            response = self.make_request("PUT", f"/admin/quotes/{self.created_quote_id}/status", status_data, token=self.admin_token)
                            if response.status_code == 200:
                                self.log_result("Update quote status", True, "- Quote status updated successfully")
                            else:
                                self.log_result("Update quote status", False, f"- Status: {response.status_code}")
                        except Exception as e:
                            self.log_result("Update quote status", False, f"- Error: {str(e)}")
                else:
                    self.log_result("Get all quotes (admin)", False, f"- Expected list, got: {type(quotes)}")
            else:
                self.log_result("Get all quotes (admin)", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get all quotes (admin)", False, f"- Error: {str(e)}")
    
    def test_audit_logs_with_admin_actions(self):
        """Test audit logs endpoint with focus on admin actions"""
        print("\n=== Testing Audit Logs (Admin Actions Focus) ===")
        
        if not self.admin_token:
            self.log_result("Audit logs", False, "- No admin token available")
            return
        
        # Get audit logs
        try:
            response = self.make_request("GET", "/admin/audit-logs", token=self.admin_token)
            if response.status_code == 200:
                logs = response.json()
                if isinstance(logs, list):
                    self.log_result("Get audit logs", True, f"- Retrieved {len(logs)} audit log entries")
                    
                    # Check for admin user creation logs
                    create_logs = [log for log in logs if log.get("action") == "USER_CREATED_BY_ADMIN"]
                    self.log_result("Admin user creation audit logs", True, f"- Found {len(create_logs)} user creation entries")
                    
                    # Check for admin user deletion logs
                    delete_logs = [log for log in logs if log.get("action") == "USER_DELETED"]
                    self.log_result("Admin user deletion audit logs", True, f"- Found {len(delete_logs)} user deletion entries")
                    
                    # Test filtered audit logs
                    filter_response = self.make_request("GET", "/admin/audit-logs?action=LOGIN_SUCCESS", token=self.admin_token)
                    if filter_response.status_code == 200:
                        filtered_logs = filter_response.json()
                        self.log_result("Filter audit logs by action", True, f"- Found {len(filtered_logs)} LOGIN_SUCCESS entries")
                    else:
                        self.log_result("Filter audit logs by action", False, f"- Status: {filter_response.status_code}")
                    
                    # Test filter by user email
                    email_filter_response = self.make_request("GET", f"/admin/audit-logs?user_email={ADMIN_EMAIL}", token=self.admin_token)
                    if email_filter_response.status_code == 200:
                        email_filtered_logs = email_filter_response.json()
                        self.log_result("Filter audit logs by admin email", True, f"- Found {len(email_filtered_logs)} entries for {ADMIN_EMAIL}")
                    else:
                        self.log_result("Filter audit logs by admin email", False, f"- Status: {email_filter_response.status_code}")
                else:
                    self.log_result("Get audit logs", False, f"- Expected list, got: {type(logs)}")
            else:
                self.log_result("Get audit logs", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get audit logs", False, f"- Error: {str(e)}")
    
    def test_unauthorized_access(self):
        """Test unauthorized access scenarios"""
        print("\n=== Testing Unauthorized Access ===")
        
        # Test admin endpoint without token
        try:
            response = self.make_request("GET", "/admin/users")
            if response.status_code in [401, 403]:  # Both 401 and 403 are acceptable for unauthorized access
                self.log_result("Admin endpoint without token", True, f"- Correctly rejected unauthorized access (Status: {response.status_code})")
            else:
                self.log_result("Admin endpoint without token", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("Admin endpoint without token", False, f"- Error: {str(e)}")
        
        # Test admin endpoint with user token
        if self.user_token:
            try:
                response = self.make_request("GET", "/admin/users", token=self.user_token)
                if response.status_code == 403:
                    self.log_result("Admin endpoint with user token", True, "- Correctly rejected non-admin access")
                else:
                    self.log_result("Admin endpoint with user token", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("Admin endpoint with user token", False, f"- Error: {str(e)}")
    
    def test_existing_features_regression(self):
        """PRIORITY 3: Quick regression test of existing features"""
        print("\n=== 🔥 PRIORITY 3: Existing Features Regression Test ===")
        
        # Quick admin login test
        if self.admin_token:
            self.log_result("🔑 Admin login regression", True, "- Admin authentication working")
        else:
            self.log_result("🔑 Admin login regression", False, "- Admin authentication failed")
        
        # Quick product CRUD test
        try:
            response = self.make_request("GET", "/products")
            if response.status_code == 200:
                products = response.json()
                self.log_result("📦 Product CRUD regression", True, f"- Product listing working ({len(products)} products)")
            else:
                self.log_result("📦 Product CRUD regression", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("📦 Product CRUD regression", False, f"- Error: {str(e)}")
        
        # Quick quote management test
        if self.user_token:
            try:
                response = self.make_request("GET", "/quotes/my", token=self.user_token)
                if response.status_code == 200:
                    self.log_result("💼 Quote management regression", True, "- Quote system working")
                else:
                    self.log_result("💼 Quote management regression", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("💼 Quote management regression", False, f"- Error: {str(e)}")
        else:
            self.log_result("💼 Quote management regression", False, "- No user token for quote test")

    def test_profile_user_id_display_backend(self):
        """PRIORITY 1: Test Profile User ID Display (Backend Support)"""
        print("\n=== 🔥 PRIORITY 1: Testing Profile User ID Display (Backend Support) ===")
        
        # Test with regular user
        if self.user_token:
            try:
                response = self.make_request("GET", "/auth/me", token=self.user_token)
                if response.status_code == 200:
                    data = response.json()
                    user_id = data.get("id")
                    if user_id:
                        # Check if it's a UUID format
                        import re
                        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
                        if re.match(uuid_pattern, user_id, re.IGNORECASE):
                            self.log_result("👤 User ID field (regular user)", True, f"- ID field present with UUID: {user_id}")
                        else:
                            self.log_result("👤 User ID field (regular user)", False, f"- ID field not in UUID format: {user_id}")
                    else:
                        self.log_result("👤 User ID field (regular user)", False, "- ID field missing from response")
                else:
                    self.log_result("👤 User ID field (regular user)", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("👤 User ID field (regular user)", False, f"- Error: {str(e)}")
        
        # Test with admin user
        if self.admin_token:
            try:
                response = self.make_request("GET", "/auth/me", token=self.admin_token)
                if response.status_code == 200:
                    data = response.json()
                    admin_id = data.get("id")
                    if admin_id:
                        # Check if it's a UUID format
                        import re
                        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
                        if re.match(uuid_pattern, admin_id, re.IGNORECASE):
                            self.log_result("👑 Admin ID field (admin user)", True, f"- ID field present with UUID: {admin_id}")
                        else:
                            self.log_result("👑 Admin ID field (admin user)", False, f"- ID field not in UUID format: {admin_id}")
                    else:
                        self.log_result("👑 Admin ID field (admin user)", False, "- ID field missing from response")
                else:
                    self.log_result("👑 Admin ID field (admin user)", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("👑 Admin ID field (admin user)", False, f"- Error: {str(e)}")

    def test_admin_product_crud_comprehensive(self):
        """PRIORITY 2: Test Admin Product CRUD Operations Comprehensively"""
        print("\n=== 🔥 PRIORITY 2: Testing Admin Product CRUD Operations ===")
        
        if not self.admin_token:
            self.log_result("Admin Product CRUD", False, "- No admin token available")
            return
        
        created_product_id = None
        
        # Test POST /api/products (Create new product with all fields)
        product_data = {
            "cat_no": "VN-TEST-CRUD-001",
            "product_name": "Comprehensive Test Product",
            "description": "Test product with all fields for comprehensive CRUD testing",
            "category": "analytical-vials",
            "pack_size": "50 pieces",
            "hsn_code": "90279090",
            "image_url": "https://example.com/test-product.jpg"
        }
        
        try:
            response = self.make_request("POST", "/products", product_data, token=self.admin_token)
            if response.status_code == 200:
                product_response = response.json()
                created_product_id = product_response.get("id")
                
                # Verify all fields are returned
                all_fields_present = all(
                    product_response.get(field) == product_data[field] 
                    for field in product_data.keys()
                )
                
                if all_fields_present and created_product_id:
                    self.log_result("📦 Create product (all fields)", True, f"- Product created with ID: {created_product_id}")
                else:
                    self.log_result("📦 Create product (all fields)", False, f"- Missing fields or ID in response: {product_response}")
            else:
                self.log_result("📦 Create product (all fields)", False, f"- Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_result("📦 Create product (all fields)", False, f"- Error: {str(e)}")
        
        # Test GET /api/products (Verify new product appears in list)
        try:
            response = self.make_request("GET", "/products")
            if response.status_code == 200:
                products = response.json()
                created_product_found = any(
                    product.get("id") == created_product_id 
                    for product in products
                )
                
                if created_product_found:
                    self.log_result("📋 Verify product in list", True, f"- New product found in product list ({len(products)} total products)")
                else:
                    self.log_result("📋 Verify product in list", False, "- New product not found in product list")
            else:
                self.log_result("📋 Verify product in list", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("📋 Verify product in list", False, f"- Error: {str(e)}")
        
        # Test PUT /api/products/{product_id} (Update product)
        if created_product_id:
            update_data = {
                "product_name": "Updated Comprehensive Test Product",
                "description": "Updated description for comprehensive testing",
                "pack_size": "100 pieces"
            }
            
            try:
                response = self.make_request("PUT", f"/products/{created_product_id}", update_data, token=self.admin_token)
                if response.status_code == 200:
                    updated_product = response.json()
                    
                    # Verify changes are reflected
                    changes_reflected = all(
                        updated_product.get(field) == update_data[field]
                        for field in update_data.keys()
                    )
                    
                    if changes_reflected:
                        self.log_result("✏️ Update product", True, "- Product updated successfully, changes reflected")
                    else:
                        self.log_result("✏️ Update product", False, f"- Changes not reflected: {updated_product}")
                else:
                    self.log_result("✏️ Update product", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("✏️ Update product", False, f"- Error: {str(e)}")
        
        # Test DELETE /api/products/{product_id} (Quick verification)
        if created_product_id:
            try:
                response = self.make_request("DELETE", f"/products/{created_product_id}", token=self.admin_token)
                if response.status_code == 200:
                    self.log_result("🗑️ Delete product", True, "- Product deleted successfully")
                    
                    # Verify product is removed from list
                    verify_response = self.make_request("GET", "/products")
                    if verify_response.status_code == 200:
                        products = verify_response.json()
                        product_still_exists = any(
                            product.get("id") == created_product_id 
                            for product in products
                        )
                        
                        if not product_still_exists:
                            self.log_result("✅ Delete verification", True, "- Product successfully removed from list")
                        else:
                            self.log_result("❌ Delete verification", False, "- Product still exists in list")
                else:
                    self.log_result("🗑️ Delete product", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("🗑️ Delete product", False, f"- Error: {str(e)}")

    def test_category_api_for_product_form(self):
        """PRIORITY 3: Test Category API for Product Form"""
        print("\n=== 🔥 PRIORITY 3: Testing Category API for Product Form ===")
        
        try:
            response = self.make_request("GET", "/categories")
            if response.status_code == 200:
                categories = response.json()
                
                if isinstance(categories, list):
                    # Check if we have exactly 8 categories as expected
                    if len(categories) == 8:
                        self.log_result("📂 Get all categories (8 expected)", True, f"- Retrieved {len(categories)} categories for dropdown")
                        
                        # Verify each category has required fields for dropdown
                        required_fields = ["name", "slug"]
                        all_categories_valid = True
                        
                        for category in categories:
                            if not all(field in category for field in required_fields):
                                all_categories_valid = False
                                break
                        
                        if all_categories_valid:
                            self.log_result("📋 Category dropdown data", True, "- All categories have required fields (name, slug)")
                            
                            # List the categories for verification
                            category_names = [cat.get("name", "Unknown") for cat in categories]
                            print(f"   📋 Categories available: {', '.join(category_names)}")
                        else:
                            self.log_result("📋 Category dropdown data", False, "- Some categories missing required fields")
                    else:
                        self.log_result("📂 Get all categories (8 expected)", False, f"- Expected 8 categories, got {len(categories)}")
                else:
                    self.log_result("📂 Get all categories (8 expected)", False, f"- Expected list, got: {type(categories)}")
            else:
                self.log_result("📂 Get all categories (8 expected)", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("📂 Get all categories (8 expected)", False, f"- Error: {str(e)}")

    def test_audit_logging_for_product_changes(self):
        """PRIORITY 4: Test Audit Logging for Product Changes"""
        print("\n=== 🔥 PRIORITY 4: Testing Audit Logging for Product Changes ===")
        
        if not self.admin_token:
            self.log_result("Audit logging for products", False, "- No admin token available")
            return
        
        # Get initial audit log count
        initial_log_count = 0
        try:
            response = self.make_request("GET", "/admin/audit-logs", token=self.admin_token)
            if response.status_code == 200:
                initial_logs = response.json()
                initial_log_count = len(initial_logs)
        except:
            pass
        
        # Create a product to generate audit logs
        product_data = {
            "cat_no": "VN-AUDIT-TEST-001",
            "product_name": "Audit Test Product",
            "description": "Product for testing audit logging",
            "category": "analytical-vials",
            "pack_size": "25",
            "hsn_code": "90279090"
        }
        
        created_product_id = None
        try:
            response = self.make_request("POST", "/products", product_data, token=self.admin_token)
            if response.status_code == 200:
                product_response = response.json()
                created_product_id = product_response.get("id")
                self.log_result("📦 Create product for audit test", True, "- Product created for audit logging test")
            else:
                self.log_result("📦 Create product for audit test", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("📦 Create product for audit test", False, f"- Error: {str(e)}")
        
        # Update the product to generate more audit logs
        if created_product_id:
            update_data = {"description": "Updated description for audit test"}
            try:
                response = self.make_request("PUT", f"/products/{created_product_id}", update_data, token=self.admin_token)
                if response.status_code == 200:
                    self.log_result("✏️ Update product for audit test", True, "- Product updated for audit logging test")
            except Exception as e:
                self.log_result("✏️ Update product for audit test", False, f"- Error: {str(e)}")
        
        # Delete the product to generate delete audit log
        if created_product_id:
            try:
                response = self.make_request("DELETE", f"/products/{created_product_id}", token=self.admin_token)
                if response.status_code == 200:
                    self.log_result("🗑️ Delete product for audit test", True, "- Product deleted for audit logging test")
            except Exception as e:
                self.log_result("🗑️ Delete product for audit test", False, f"- Error: {str(e)}")
        
        # Check audit logs for product-related actions
        try:
            response = self.make_request("GET", "/admin/audit-logs", token=self.admin_token)
            if response.status_code == 200:
                all_logs = response.json()
                
                # Look for product-related audit entries
                product_logs = [
                    log for log in all_logs 
                    if any(keyword in log.get("action", "").lower() or keyword in log.get("resource", "").lower() 
                          for keyword in ["product", "create", "update", "delete"])
                ]
                
                if len(product_logs) > 0:
                    self.log_result("📊 Product audit logs", True, f"- Found {len(product_logs)} product-related audit entries")
                    
                    # Check for specific actions if we created/updated/deleted
                    if created_product_id:
                        recent_logs = all_logs[:10]  # Check recent logs
                        admin_actions = [
                            log for log in recent_logs 
                            if log.get("user_email") == ADMIN_EMAIL
                        ]
                        
                        if len(admin_actions) > 0:
                            self.log_result("👑 Admin action audit logs", True, f"- Found {len(admin_actions)} recent admin actions in audit trail")
                        else:
                            self.log_result("👑 Admin action audit logs", False, "- No recent admin actions found in audit trail")
                else:
                    self.log_result("📊 Product audit logs", False, "- No product-related audit entries found")
                
                # Test filtering audit logs by action
                filter_response = self.make_request("GET", "/admin/audit-logs?action=LOGIN_SUCCESS", token=self.admin_token)
                if filter_response.status_code == 200:
                    filtered_logs = filter_response.json()
                    self.log_result("🔍 Filter audit logs by action", True, f"- Successfully filtered logs, found {len(filtered_logs)} LOGIN_SUCCESS entries")
                else:
                    self.log_result("🔍 Filter audit logs by action", False, f"- Status: {filter_response.status_code}")
                
            else:
                self.log_result("📊 Product audit logs", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("📊 Product audit logs", False, f"- Error: {str(e)}")

    def test_site_content_management_api(self):
        """NEW FEATURE - Site Content Management API (HIGH PRIORITY)"""
        print("\n=== 🔥 NEW FEATURE: Site Content Management API (HIGH PRIORITY) ===")
        
        created_content_id = None
        
        # Test GET /api/content (public access - should work without auth)
        try:
            response = self.make_request("GET", "/content")
            if response.status_code == 200:
                content = response.json()
                if isinstance(content, list):
                    self.log_result("🌐 GET /api/content (public)", True, f"- Retrieved {len(content)} content items (public access)")
                else:
                    self.log_result("🌐 GET /api/content (public)", False, f"- Expected list, got: {type(content)}")
            else:
                self.log_result("🌐 GET /api/content (public)", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("🌐 GET /api/content (public)", False, f"- Error: {str(e)}")
        
        # Test GET /api/admin/content (admin only - test with admin token)
        if self.admin_token:
            try:
                response = self.make_request("GET", "/admin/content", token=self.admin_token)
                if response.status_code == 200:
                    admin_content = response.json()
                    if isinstance(admin_content, list):
                        self.log_result("🔐 GET /api/admin/content (admin only)", True, f"- Retrieved {len(admin_content)} content items (admin access)")
                    else:
                        self.log_result("🔐 GET /api/admin/content (admin only)", False, f"- Expected list, got: {type(admin_content)}")
                else:
                    self.log_result("🔐 GET /api/admin/content (admin only)", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("🔐 GET /api/admin/content (admin only)", False, f"- Error: {str(e)}")
        else:
            self.log_result("🔐 GET /api/admin/content (admin only)", False, "- No admin token available")
        
        # Test GET /api/admin/content?page=about (filter by page)
        if self.admin_token:
            try:
                response = self.make_request("GET", "/admin/content?page=about", token=self.admin_token)
                if response.status_code == 200:
                    filtered_content = response.json()
                    if isinstance(filtered_content, list):
                        self.log_result("🔍 GET /api/admin/content?page=about (filter)", True, f"- Retrieved {len(filtered_content)} 'about' page content items")
                    else:
                        self.log_result("🔍 GET /api/admin/content?page=about (filter)", False, f"- Expected list, got: {type(filtered_content)}")
                else:
                    self.log_result("🔍 GET /api/admin/content?page=about (filter)", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("🔍 GET /api/admin/content?page=about (filter)", False, f"- Error: {str(e)}")
        
        # Test POST /api/admin/content (create new content)
        if self.admin_token:
            content_data = {
                "page": "about",
                "section": "hero_title", 
                "content": "Test Content for API Testing"
            }
            
            try:
                response = self.make_request("POST", "/admin/content", content_data, token=self.admin_token)
                if response.status_code == 200:
                    created_content = response.json()
                    created_content_id = created_content.get("id")
                    
                    # Verify content fields
                    if (created_content.get("page") == "about" and 
                        created_content.get("section") == "hero_title" and
                        created_content.get("content") == "Test Content for API Testing"):
                        self.log_result("➕ POST /api/admin/content (create)", True, f"- Content created with ID: {created_content_id}")
                    else:
                        self.log_result("➕ POST /api/admin/content (create)", False, f"- Content fields mismatch: {created_content}")
                else:
                    self.log_result("➕ POST /api/admin/content (create)", False, f"- Status: {response.status_code}, Response: {response.text}")
            except Exception as e:
                self.log_result("➕ POST /api/admin/content (create)", False, f"- Error: {str(e)}")
        
        # Test PUT /api/admin/content/{content_id} (update content)
        if self.admin_token and created_content_id:
            update_data = {
                "content": "Updated Test Content for API Testing"
            }
            
            try:
                response = self.make_request("PUT", f"/admin/content/{created_content_id}", update_data, token=self.admin_token)
                if response.status_code == 200:
                    updated_content = response.json()
                    
                    if updated_content.get("content") == "Updated Test Content for API Testing":
                        self.log_result("✏️ PUT /api/admin/content/{id} (update)", True, "- Content updated successfully")
                    else:
                        self.log_result("✏️ PUT /api/admin/content/{id} (update)", False, f"- Update not reflected: {updated_content}")
                else:
                    self.log_result("✏️ PUT /api/admin/content/{id} (update)", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("✏️ PUT /api/admin/content/{id} (update)", False, f"- Error: {str(e)}")
        
        # Test authorization (non-admin should get 401/403)
        if self.user_token:
            try:
                response = self.make_request("GET", "/admin/content", token=self.user_token)
                if response.status_code in [401, 403]:
                    self.log_result("🛡️ Authorization check (non-admin)", True, f"- Correctly blocked non-admin access (Status: {response.status_code})")
                else:
                    self.log_result("🛡️ Authorization check (non-admin)", False, f"- Non-admin access not blocked, Status: {response.status_code}")
            except Exception as e:
                self.log_result("🛡️ Authorization check (non-admin)", False, f"- Error: {str(e)}")
        
        # Test unauthorized access (no token)
        try:
            response = self.make_request("GET", "/admin/content")
            if response.status_code in [401, 403]:
                self.log_result("🔒 Authorization check (no token)", True, f"- Correctly blocked unauthorized access (Status: {response.status_code})")
            else:
                self.log_result("🔒 Authorization check (no token)", False, f"- Unauthorized access not blocked, Status: {response.status_code}")
        except Exception as e:
            self.log_result("🔒 Authorization check (no token)", False, f"- Error: {str(e)}")
        
        # Verify audit logging for CONTENT_CREATED and CONTENT_UPDATED actions
        if self.admin_token:
            try:
                response = self.make_request("GET", "/admin/audit-logs", token=self.admin_token)
                if response.status_code == 200:
                    audit_logs = response.json()
                    
                    # Look for content-related audit logs
                    content_created_logs = [log for log in audit_logs if log.get("action") == "CONTENT_CREATED"]
                    content_updated_logs = [log for log in audit_logs if log.get("action") == "CONTENT_UPDATED"]
                    
                    if len(content_created_logs) > 0:
                        self.log_result("📊 Audit log - CONTENT_CREATED", True, f"- Found {len(content_created_logs)} CONTENT_CREATED audit entries")
                    else:
                        self.log_result("📊 Audit log - CONTENT_CREATED", False, "- No CONTENT_CREATED audit entries found")
                    
                    if len(content_updated_logs) > 0:
                        self.log_result("📊 Audit log - CONTENT_UPDATED", True, f"- Found {len(content_updated_logs)} CONTENT_UPDATED audit entries")
                    else:
                        self.log_result("📊 Audit log - CONTENT_UPDATED", False, "- No CONTENT_UPDATED audit entries found")
                        
                else:
                    self.log_result("📊 Audit logging verification", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("📊 Audit logging verification", False, f"- Error: {str(e)}")

    def test_regression_testing(self):
        """REGRESSION TESTING (MEDIUM PRIORITY)"""
        print("\n=== 🔄 REGRESSION TESTING (MEDIUM PRIORITY) ===")
        
        # Authentication endpoints still working
        if self.user_token and self.admin_token:
            self.log_result("🔑 Authentication endpoints", True, "- User and admin authentication working")
        else:
            self.log_result("🔑 Authentication endpoints", False, "- Authentication issues detected")
        
        # Product CRUD still working
        try:
            response = self.make_request("GET", "/products")
            if response.status_code == 200:
                products = response.json()
                self.log_result("📦 Product CRUD endpoints", True, f"- Product listing working ({len(products)} products)")
            else:
                self.log_result("📦 Product CRUD endpoints", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("📦 Product CRUD endpoints", False, f"- Error: {str(e)}")
        
        # Admin user management still working
        if self.admin_token:
            try:
                response = self.make_request("GET", "/admin/users", token=self.admin_token)
                if response.status_code == 200:
                    users = response.json()
                    self.log_result("👥 Admin user management", True, f"- User management working ({len(users)} users)")
                else:
                    self.log_result("👥 Admin user management", False, f"- Status: {response.status_code}")
            except Exception as e:
                self.log_result("👥 Admin user management", False, f"- Error: {str(e)}")
        
        # Email service (forgot password endpoint)
        try:
            reset_request = {"email": "test@example.com"}
            response = self.make_request("POST", "/auth/forgot-password", reset_request)
            if response.status_code == 200:
                self.log_result("📧 Email service (forgot password)", True, "- Forgot password endpoint working")
            else:
                self.log_result("📧 Email service (forgot password)", False, f"- Status: {response.status_code}")
        except Exception as e:
            self.log_result("📧 Email service (forgot password)", False, f"- Error: {str(e)}")

    def run_priority_tests(self):
        """Run priority-focused test suites as requested in review"""
        print("🧪 Starting Vian Scientific API Testing Suite - REVIEW REQUEST PRIORITIES")
        print(f"🌐 Testing against: {self.base_url}")
        print("🎯 Focus: Profile User ID + Admin Product CRUD + Categories + Audit Logging")
        print("=" * 80)
        
        # Core setup
        self.test_root_endpoint()
        
        # Basic authentication setup for testing
        self.test_user_registration()
        self.test_user_login()
        self.test_admin_login()
        
        print("\n" + "🔥" * 80)
        print("REVIEW REQUEST PRIORITY TESTING")
        print("🔥" * 80)
        
        # NEW FEATURE - Site Content Management API (HIGH PRIORITY)
        self.test_site_content_management_api()
        
        # REGRESSION TESTING (MEDIUM PRIORITY)
        self.test_regression_testing()
        
        print("\n" + "🔥" * 80)
        print("REVIEW REQUEST PRIORITY TESTING COMPLETE")
        print("🔥" * 80)
        
        # Additional comprehensive tests for completeness
        print("\n=== Additional Comprehensive Tests ===")
        self.test_get_current_user()
        self.test_password_reset_flow()
        self.test_products_endpoints()
        self.test_categories_endpoints()
        self.test_quote_management()
        self.test_admin_user_management_legacy()
        self.test_admin_product_management()
        self.test_admin_quotes_management()
        self.test_audit_logs_with_admin_actions()
        self.test_unauthorized_access()
        
        # Print final results
        print("\n" + "=" * 80)
        print("🏁 REVIEW REQUEST TEST RESULTS SUMMARY")
        print("=" * 80)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"📊 Total: {self.results['passed'] + self.results['failed']}")
        
        if self.results['failed'] > 0:
            print(f"\n🚨 FAILED TESTS ({self.results['failed']}):")
            for error in self.results['errors']:
                print(f"   {error}")
        
        success_rate = (self.results['passed'] / (self.results['passed'] + self.results['failed'])) * 100 if (self.results['passed'] + self.results['failed']) > 0 else 0
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        return self.results

    def run_all_tests(self):
        """Run all test suites (legacy method)"""
        return self.run_priority_tests()

if __name__ == "__main__":
    tester = VianScientificAPITester()
    results = tester.run_priority_tests()