

# **FastAPI Authentication API Docs**

This document provides API details and **cURL commands** to test authentication endpoints in your FastAPI-based Event Management API.

## **1. Register a New User**

Creates a new attendee account.

### **Endpoint:** `POST /auth/register`

**Request:**

```sh
curl -X 'POST' 'http://127.0.0.1:8000/auth/register' \
-H 'Content-Type: application/json' \
-d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "password": "securepassword"
}'
```

**Response:**

```json
{
    "message": "User registered successfully"
}
```

---

## **2. Login to Get Access Token**

Authenticate user and receive a JWT token.

### **Endpoint:** `POST /auth/login`

**Request:**

```sh
curl -X 'POST' 'http://127.0.0.1:8000/auth/login' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'username=johndoe@example.com&password=securepassword'
```

**Response:**

```json
{
    "access_token": "your_jwt_token_here",
    "token_type": "bearer"
}
```

⚠ **Save the `access_token`** from the response.

---

## **3. Get Logged-In User Info**

Fetch details of the authenticated user.

### **Endpoint:** `GET /auth/me`

**Request:**

```sh
curl -X 'GET' 'http://127.0.0.1:8000/auth/me' \
-H 'Authorization: Bearer your_jwt_token_here'
```

**Response:**

```json
{
    "attendee_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "phone_number": "",
    "event_id": null,
    "check_in_status": false
}
```

---

## **Notes**

* Replace `your_jwt_token_here` with the actual token from login.
* Ensure FastAPI server is running at `http://127.0.0.1:8000/`.
* Use `http://localhost:8000` if testing locally.

---
