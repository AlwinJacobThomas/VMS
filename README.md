# Vendor Management System (VMS)

## Overview
The Vendor Management System (VMS) is a Django-based application that allows users to manage vendors, track purchase orders, and evaluate vendor performance metrics. This README provides instructions for setting up the project and using its API endpoints.

## Setup Instructions
Follow these steps to set up and run the Vendor Management System locally:

1. **Clone the repository:**
    ```bash
    git clone <repository_url>
    ```

2. **Navigate to the project directory:**
    ```bash
    cd VMS
    ```

3. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment:**

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```

    - On Linux/MacOS:
        ```bash
        source venv/bin/activate
        ```

5. **Install the project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

6. **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

7. **Create a superuser to access the Django admin panel:**
    ```bash
    python manage.py createsuperuser
    ```

8. **Start the development server:**
    ```bash
    python manage.py runserver
    ```

9. **Access the application in your web browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)**    

# Vendors Endpoints

## Retrieve All Vendors
- **URL:** `/api/vendors/`
- **Method:** GET
- **Description:** Retrieves a list of all vendors.
- **Response:** JSON array containing details of all vendors.

## Retrieve Single Vendor
- **URL:** `/api/vendors/<vendor_id>/`
- **Method:** GET
- **Description:** Retrieves details of a single vendor identified by vendor_id.
- **Response:** JSON object containing details of the vendor.

# Purchase Orders Endpoints

## Retrieve All Purchase Orders
- **URL:** `/api/purchase_orders/`
- **Method:** GET
- **Description:** Retrieves a list of all purchase orders.
- **Response:** JSON array containing details of all purchase orders.

## Retrieve Single Purchase Order
- **URL:** `/api/purchase_orders/<po_id>/`
- **Method:** GET
- **Description:** Retrieves details of a single purchase order identified by po_id.
- **Response:** JSON object containing details of the purchase order.

## Acknowledge Purchase Order
- **URL:** `/api/purchase_orders/<po_id>/acknowledge/`
- **Method:** POST
- **Description:** Acknowledges a purchase order identified by po_id, updating its acknowledgment date.
- **Request Body:** Empty or may contain additional acknowledgment details.
- **Response:** Success message indicating that the purchase order was acknowledged successfully.

# Vendor Performance Endpoints

## Retrieve Vendor Performance
- **URL:** `/api/vendors/<vendor_id>/performance/`
- **Method:** GET
- **Description:** Retrieves historical performance metrics of a vendor identified by vendor_id.
- **Response:** JSON object containing historical performance metrics such as on-time delivery rate, quality rating average, average response time, and fulfillment rate.

# Models

## Vendor Model
- Represents a vendor with fields for name, contact details, address, vendor code, on-time delivery rate, quality rating average, average response time, and fulfillment rate.

## PurchaseOrder Model
- Represents a purchase order with fields for purchase order number, vendor, order date, delivery date, items, quantity, status, quality rating, issue date, and acknowledgment date.

## HistoricalPerformance Model
- Represents historical performance metrics with fields for vendor, date, on-time delivery rate, quality rating average, average response time, and fulfillment rate.

# Signals

## update_matrices Signal
- Updates various metrics such as quality rating average, on-time delivery rate, average response time, and fulfillment rate for vendors whenever a purchase order is saved.

## update_fulfillment_rate Signal
- Updates the fulfillment rate for vendors whenever the status of a purchase order is changed.

# Serializers

## VendorSerializer
- Serializes vendor data for API interaction.

## PurchaseOrderSerializer
- Serializes purchase order data for API interaction.

## HistoricalPerformanceSerializer
- Serializes historical performance data for API interaction.

# URLs

## Vendors URLs
- Defines URL patterns for vendor-related endpoints.

## VMS URLs
- Includes Vendors URLs to route API requests to the appropriate views.
