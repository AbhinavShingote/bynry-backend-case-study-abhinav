# Additional Case Study Notes

## Part 1 - Debugging Summary
The original product creation API had issues related to:
- missing input validation
- duplicate SKU possibility
- separate commits
- no error handling
- improper warehouse-product mapping

My corrected approach focused on making the API safer while keeping it simple.

---

## Part 2 - Database Design Summary
Main entities designed:
- Company
- Warehouse
- Product
- Inventory
- Supplier
- ProductSupplier
- InventoryTransaction

This schema was designed to support:
- multiple warehouses per company
- multiple warehouse stock entries per product
- supplier mapping
- inventory tracking

---

## Part 3 - Low Stock Alert API Summary
Implemented endpoint:
GET /api/companies/{company_id}/alerts/low-stock

Main logic:
- fetch company warehouse inventory
- compare quantity with threshold
- include supplier information
- calculate approximate days until stockout

---

## Assumptions
- threshold stored in inventory
- avg daily sales available
- one primary supplier per product for simplicity

Detailed written explanation has been submitted separately in the shared case study document.