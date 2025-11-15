# Vian Scientific - Backend API Review & Documentation

## 1. Overall Review & Recommendations

This document provides a comprehensive review of the backend API endpoints inferred from the project's testing reports and frontend implementation. The API is well-structured, covers all required functionality, and follows RESTful principles. The separation of public, user, and admin routes is clear and enforces proper security.

Based on the review, here are some recommendations for further enhancement and production readiness:

*   **API Versioning:**
    *   **Recommendation:** Introduce API versioning (e.g., `/api/v1/...`). This is a best practice that allows you to evolve the API in the future without breaking the frontend application.

*   **Consistent Response Structure:**
    *   **Recommendation:** Standardize all API responses. A consistent format for success and error messages improves frontend development and debugging.
    *   **Success Example:** `{ "status": "success", "data": { ... } }`
    *   **Error Example:** `{ "status": "error", "message": "Invalid credentials.", "details": { ... } }`

*   **Pagination:**
    *   **Observation:** The audit log endpoint includes pagination.
    *   **Recommendation:** Ensure all endpoints that return lists (`/api/products`, `/api/admin/users`, `/api/quotes`, etc.) use a consistent pagination system (e.g., `?page=1&limit=25`). This is crucial for performance and scalability.

*   **Security - Rate Limiting:**
    *   **Recommendation:** Implement rate limiting on all endpoints, especially authentication and public-facing routes, to protect against brute-force attacks and denial-of-service (DoS) attempts.

*   **Input Validation:**
    *   **Observation:** The testing report indicates that validation (e.g., for password strength) is working.
    *   **Recommendation:** Continue to ensure that all incoming data from requests (`body`, `params`, `query`) is rigorously validated on the server-side to prevent security vulnerabilities like injection attacks.

---

## 2. Public Endpoints (No Authentication Required)

### Get All Products
*   **Endpoint:** `GET /api/products`
*   **Description:** Retrieves a list of all available products. Supports filtering by category and searching by a query string.
*   **Query Parameters:**
    *   `category` (string, optional): Slug of the category to filter by.
    *   `search` (string, optional): Search term to match against product name, description, and catalog number.
*   **Success Response (200 OK):**
    ```json
    [
      {
        "id": "product_id_1",
        "name": "HPLC Vials",
        "category": "hplc-accessories",
        "cat_no": "VS-123"
      }
    ]
    ```

### Get Single Product
*   **Endpoint:** `GET /api/products/{product_id}`
*   **Description:** Retrieves detailed information for a single product.
*   **Success Response (200 OK):**
    ```json
    {
      "id": "product_id_1",
      "name": "HPLC Vials",
      "description": "High-quality vials for all your chromatography needs.",
      "category": "hplc-accessories",
      "cat_no": "VS-123"
    }
    ```

### Get Categories
*   **Endpoint:** `GET /api/categories`
*   **Description:** Retrieves a list of all product categories.
*   **Success Response (200 OK):** `[ { "name": "HPLC Accessories", "slug": "hplc-accessories" }, ... ]`

### Get Site Content
*   **Endpoint:** `GET /api/content`
*   **Description:** Retrieves public-facing site content (e.g., for 'About Us' or 'Home' pages).
*   **Success Response (200 OK):** `[ { "page": "about", "section": "mission", "content": "Our mission is..." }, ... ]`

---

## 3. Authentication Endpoints

### Register User
*   **Endpoint:** `POST /api/auth/register`
*   **Description:** Creates a new user account.
*   **Request Body:**
    ```json
    {
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "password": "A-very-strong-password123!"
    }
    ```
*   **Success Response (201 Created):** `{ "message": "User registered successfully." }`
*   **Error Response (400 Bad Request):** `{ "message": "Email already exists." }` or `{ "message": "Password is too weak." }`

### Login User
*   **Endpoint:** `POST /api/auth/login`
*   **Description:** Authenticates a user and returns a JWT access token.
*   **Request Body:**
    ```json
    {
      "email": "john.doe@example.com",
      "password": "A-very-strong-password123!"
    }
    ```
*   **Success Response (200 OK):** `{ "access_token": "ey...", "token_type": "bearer" }`
*   **Error Response (401 Unauthorized):** `{ "message": "Invalid credentials." }`

### Forgot Password
*   **Endpoint:** `POST /api/auth/forgot-password`
*   **Description:** Sends a password reset code to the user's email if the account exists.
*   **Request Body:** `{ "email": "john.doe@example.com" }`
*   **Success Response (200 OK):** `{ "message": "Password reset email sent." }`

### Reset Password
*   **Endpoint:** `POST /api/auth/reset-password`
*   **Description:** Sets a new password for a user using a valid reset code.
*   **Request Body:**
    ```json
    {
      "email": "john.doe@example.com",
      "code": "123456",
      "new_password": "A-new-strong-password456!"
    }
    ```
*   **Success Response (200 OK):** `{ "message": "Password has been reset successfully." }`
*   **Error Response (400 Bad Request):** `{ "message": "Invalid or expired reset code." }`

---

## 4. User Endpoints (User Authentication Required)

### Get Current User
*   **Endpoint:** `GET /api/auth/me`
*   **Description:** Retrieves the profile of the currently logged-in user.
*   **Success Response (200 OK):**
    ```json
    {
      "id": "user_id_1",
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "role": "user"
    }
    ```

### Change Password
*   **Endpoint:** `POST /api/auth/change-password`
*   **Description:** Allows a logged-in user to change their own password.
*   **Request Body:**
    ```json
    {
      "current_password": "A-very-strong-password123!",
      "new_password": "A-new-strong-password456!"
    }
    ```
*   **Success Response (200 OK):** `{ "message": "Password changed successfully." }`

### Submit a Quote
*   **Endpoint:** `POST /api/quotes`
*   **Description:** Creates a new quote request from the items in the user's cart.
*   **Request Body:**
    ```json
    {
      "items": [
        { "product_id": "prod_1", "quantity": 2 },
        { "product_id": "prod_2", "quantity": 5 }
      ],
      "message": "Please provide pricing for these items."
    }
    ```
*   **Success Response (201 Created):** `{ "message": "Quote submitted successfully.", "quote_id": "quote_123" }`

### Get User's Quotes
*   **Endpoint:** `GET /api/quotes`
*   **Description:** Retrieves a list of all quotes submitted by the current user.
*   **Success Response (200 OK):** `[ { "id": "quote_123", "status": "Pending", "created_at": "...", "item_count": 2 }, ... ]`

---

## 5. Admin Endpoints (Admin Authentication Required)

### Admin: User Management
*   `GET /api/admin/users`: List all users.
*   `POST /api/admin/users`: Create a new user (admin or regular).
*   `DELETE /api/admin/users/{user_id}`: Delete a user account.
*   `PUT /api/admin/users/{user_id}`: Update user details (e.g., role, status).
    *   **Body:** `{ "is_active": false }` or `{ "role": "admin" }`
*   `POST /api/admin/users/{user_id}/reset-password`: Force a password reset for a user.

### Admin: Product Management
*   `POST /api/admin/products`: Create a new product.
*   `PUT /api/admin/products/{product_id}`: Update an existing product's details.
*   `DELETE /api/admin/products/{product_id}`: Delete a product.

### Admin: Quote Management
*   `GET /api/admin/quotes`: Get a list of all quotes from all users.
*   `PUT /api/admin/quotes/{quote_id}`: Update the status of a quote.
    *   **Body:** `{ "status": "Reviewed" }`

### Admin: Site Content Management
*   `GET /api/admin/content`: Get all editable site content.
*   `POST /api/admin/content`: Create a new editable content block.
*   `PUT /api/admin/content/{content_id}`: Update a content block.

### Admin: Audit Logs
*   `GET /api/admin/audit-logs`: Retrieve audit logs.
*   **Query Parameters:**
    *   `action` (string, optional): Filter by action type (e.g., `LOGIN_SUCCESS`).
    *   `email` (string, optional): Filter by user email.
    *   `page` (int, optional): Page number for pagination.
    *   `limit` (int, optional): Items per page.
