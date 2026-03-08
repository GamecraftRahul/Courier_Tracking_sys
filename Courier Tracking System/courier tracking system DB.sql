-- 1. Create database
CREATE DATABASE IF NOT EXISTS courier_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE courier_db;

-- 2. Create shipments table
CREATE TABLE IF NOT EXISTS shipments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tracking_no VARCHAR(30) NOT NULL UNIQUE,
    sender_name VARCHAR(100),
    receiver_name VARCHAR(100),
    origin VARCHAR(100),
    destination VARCHAR(100),
    package_date DATE,
    expected_delivery DATE,
    status ENUM('Pending','Packaging','Shipped','In Transit','Out for Delivery','Delivered','Returned') DEFAULT 'Pending',
    current_location VARCHAR(150),
    manager_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Insert 10 sample records
INSERT INTO shipments (tracking_no, sender_name, receiver_name, origin, destination, package_date, expected_delivery, status, current_location, manager_notes)
VALUES
('CR10000001','Rajesh Kumar','Asha Patel','Mumbai','Pune','2025-11-20','2025-11-22','Delivered','Pune - Local Hub','Left at front desk'),
('CR10000002','Anita Sharma','Vikram Singh','Delhi','Jaipur','2025-11-21','2025-11-25','In Transit','Jaipur - Sorting Center','Handle with care'),
('CR10000003','Sunil Verma','Priya Mehra','Bangalore','Chennai','2025-11-22','2025-11-24','Out for Delivery','Chennai - Local Vehicle','Customer expects between 10-2'),
('CR10000004','Neha Joshi','Ramesh Rao','Hyderabad','Lucknow','2025-11-19','2025-11-26','Shipped','Air Hub - Hyderabad','Delayed due to weather'),
('CR10000005','Mohan Lal','Sangeeta Rao','Kolkata','Howrah','2025-11-23','2025-11-24','Packaging','Kolkata - Warehouse','Awaiting label print'),
('CR10000006','Pooja Gupta','Arjun Kumar','Ahmedabad','Surat','2025-11-22','2025-11-23','Delivered','Surat - Customer Address','Left with neighbor'),
('CR10000007','Vandana Iyer','Karan Patel','Pune','Nashik','2025-11-24','2025-11-27','Pending','Pune - Warehouse','Pickup scheduled'),
('CR10000008','Deepak Nair','Meena Thomas','Trivandrum','Kochi','2025-11-18','2025-11-21','Returned','Kochi - Return Hub','Recipient not available'),
('CR10000009','Ritu Singh','Manish Joshi','Indore','Bhopal','2025-11-20','2025-11-22','In Transit','Bhopal - Sorting Center','No special notes'),
('CR10000010','Amit Desai','Suman Rao','Vadodara','Surat','2025-11-25','2025-11-28','Packaging','Vadodara - Warehouse','Fragile item');
