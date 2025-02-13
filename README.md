# Company-Expense-Management-API

This is a **Django-based REST API** for managing employee expense claims. The application allows employees to submit their expense claims, while managers and administrators can review, approve, or reject these claims. 

## Features:
- **Role-based access control (RBAC)** for managing users and their permissions.
- **Expense claim submission, update, and management**.
- **Excel report generation** for administrators.
- Fully exposed **REST API** for all functionalities.

## Technologies Used:
- **Django**: Web framework for handling the backend.
- **Django REST Framework (DRF)**: For creating the RESTful API endpoints.
- **OpenPyXL**: To generate Excel reports for claims.

## API Endpoints Overview

The following endpoints are available for the Company Expense Management API:

### 1. `/users/`
- **Methods Supported:** `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- **Description:** Create, update, retrieve, or delete user information.
- **Permissions:**
  - Admin have full access to create, update, and delete user information
  - Employees and Managers can only edit their own data.

### 2. `/expense-claim/`
- **Methods Supported:** `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- **Description:** Submit, update, or list expense claims.
- **Permissions:**
  - Employees can submit and view their own claims; Managers can view theirs as well as their employees under their supervision
  - Admins can view all claims.

### 3. `/expense-category/`
- **Methods Supported:** `GET`, `POST`, `PUT`, `DELETE`
- **Description:** Manage expense categories (e.g., create, update, delete).
- **Permissions:** Admin only.

### 4. `/all-claim-request/`
- **Methods Supported:** `GET`, `PUT`, `PATCH`
- **Description:** View and approve/reject employee claims. This endpoint is used by managers and admins to handle claim requests.
- **Permissions:** Accessible only by managers and admins.

### 5. `/all-claim-request/view_report/`
- **Methods Supported:** `GET`
- **Description:** View a summary of all expense claims, including details like status and amount.
- **Permissions:** Admin only.

### 6. `/all-claim-request/generate_report/`
- **Methods Supported:** `GET`
- **Description:** Generate and download Excel report containing all expense claims, including details like status and amount.
- **Permissions:** Admin only.