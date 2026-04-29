# Bynry Backend Engineering Intern Case Study Submission

## Candidate Name
Abhinav Shingote

## Overview
This repository contains my submission for the Backend Engineering Intern case study provided by Bynry Inc.

The case study was divided into three backend-focused sections:

1. Code Review and Debugging
2. Database Design
3. API Implementation

I used Python Flask with SQLAlchemy ORM to provide a simple and practical backend-oriented solution.

---

## Part 1 - Code Review & Debugging

The provided create product API had several practical issues:

- No request validation
- No SKU uniqueness check
- Product linked directly to warehouse
- Multiple database commits causing inconsistent save possibility
- No error handling
- Negative price and quantity values not validated

I corrected the API by adding:

- basic validation
- duplicate SKU prevention
- single commit based save flow
- exception handling

---

## Part 2 - Database Design

To support a scalable B2B inventory management SaaS platform, I designed the following entities:

- Company
- Warehouse
- Product
- Inventory
- Supplier
- ProductSupplier
- InventoryTransaction

This structure allows:

- one company to manage multiple warehouses
- one product to exist in multiple warehouses
- supplier-product mapping
- inventory movement tracking

---

## Part 3 - Low Stock Alert API

Implemented endpoint:

GET /api/companies/{company_id}/alerts/low-stock

This endpoint:

- checks all warehouse inventory of a company
- compares stock with threshold
- calculates approximate days until stockout
- fetches supplier details for reordering
- returns structured JSON alert response

---

## Assumptions Made

Because the problem statement was intentionally incomplete, I made the following assumptions:

- every inventory item has a threshold value
- average daily sales is stored for simple stockout calculation
- one product can have one primary supplier mapping
- warehouse belongs to one company

---

## Tech Stack Used

- Python
- Flask
- Flask SQLAlchemy
- SQLite (for lightweight demonstration)

---

## Notes

This repository is designed as a backend case study demonstration and focuses mainly on engineering approach, schema understanding, and API logic rather than full production deployment.

---

## Submission Intent

The objective of this submission was to demonstrate backend problem-solving approach, practical schema design, and readable API implementation under incomplete business requirements.