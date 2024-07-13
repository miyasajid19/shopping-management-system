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

##interfaces
#interfaces![Screenshot 2024-07-13 165314](https://github.com/user-attachments/assets/16079b88-32bc-4f79-99f1-26efa9db2f28)
![Screenshot 2024-07-13 170422](https://github.com/user-attachments/assets/e091d3dd-2dc4-4208-bb16-1abbb26cce63)
![Screenshot 2024-07-13 170406](https://github.com/user-attachments/assets/8731332d-ca1e-4c33-9e53-3eefec981b1a)
![Screenshot 2024-07-13 170339](https://github.com/user-attachments/assets/0388d8bc-da18-41e7-bb62-2017c13368ad)
![Screenshot 2024-07-13 170226](https://github.com/user-attachments/assets/318e430b-9c5c-42d3-8d4a-407656f8a868)
![Screenshot 2024-07-13 170132](https://github.com/user-attachments/assets/7ba9b25f-92a3-4e86-b40f-ae97aada891d)
![Screenshot 2024-07-13 170033](https://github.com/user-attachments/assets/fb92d632-2291-41de-8006-17f439527ba9)
![Screenshot 2024-07-13 165952](https://github.com/user-attachments/assets/63d082cc-25ad-487d-a5f7-b2789b2ed5ca)
![Screenshot 2024-07-13 165910](https://github.com/user-attachments/assets/de3e58bb-36b6-42d9-87a0-018d36e6e5a4)
![Screenshot 2024-07-13 165852](https://github.com/user-attachments/assets/001f4b1f-71a5-46e9-aab3-0b9e5b4703a8)
![Screenshot 2024-07-13 165836](https://github.com/user-attachments/assets/b3d3ac9d-af1f-42cf-9298-1029ea091fcd)
![Screenshot 2024-07-13 165815](https://github.com/user-attachments/assets/4f343365-c1cc-41a7-910f-8f4bad265288)
![Screenshot 2024-07-13 165612](https://github.com/user-attachments/assets/ee72814d-f474-463a-af4c-50f79734484d)
![Screenshot 2024-07-13 165449](https://github.com/user-attachments/assets/6080528d-d2a7-4b4e-838e-7fabdfff02a0)
![Screenshot 2024-07-13 165400](https://github.com/user-attachments/assets/1ca50856-ff36-45a2-afdd-d4b58c016f61)


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
    type ENUM('customer', 'vendor')
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
