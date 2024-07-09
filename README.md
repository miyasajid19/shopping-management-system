# SMPK Shopping Management System

## Overview
SMPK Shopping Management System is a portfolio of a typical e-commerce application utilizing CRUD (Create, Read, Update, Delete) functionality. It features two distinct interfaces: one for users and one for vendors. This code may appear somewhat disorganized and repetitive as it was written after a break and focuses more on results rather than code length.

## Features
### Login System
- **Login Form:** Asks for login credentials and signs in if a registered account is detected.
- **Vendor Interface:** 
  - Add new products
  - Read existing products
  - Update products (e.g., new image, restocked items, price changes)
  - Delete products (handled by the vendor if the product is no longer needed or outdated)
- **Customer Interface:**
  - Search for available products
  - Add products to cart or wishlist
  - View and manage cart
  - Order products from the cart (removes products from the cart upon ordering)
  - Delete products from the cart
  - View and manage wishlist (ordering from the wishlist does not remove the product)
  - View order history

## Database Schema
The backend is handled using XAMPP server, PHPMyAdmin, and a local host for the database.

### SQL Queries
```sql
-- Create database
CREATE DATABASE smpkshoppingcentre;

-- Create 'user' table
CREATE TABLE `user` (
    phone VARCHAR(30) PRIMARY KEY,
    passkey VARCHAR(255),
    type ENUM('customer', 'vendor', 'admin')
);

-- Create 'products' table
CREATE TABLE `products`(
    id VARCHAR(11) PRIMARY KEY,
    productname VARCHAR(255),
    vendor VARCHAR(255),
    price DECIMAL(10,2),
    quantity INT,
    image VARCHAR(255),
    description TEXT
);

-- Create 'customers' table
CREATE TABLE `customers` (
    id VARCHAR(255) PRIMARY KEY,
    cart VARCHAR(255),
    wishlist VARCHAR(255),
    status ENUM("ordered","delivered","not yet")
);

-- Create 'order' table
CREATE TABLE `order` (
    id VARCHAR(255),
    productid VARCHAR(11)
);
