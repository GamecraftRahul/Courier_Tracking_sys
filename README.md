# 📦 Courier Tracking System

A desktop-based Courier Tracking System built using **Python (Tkinter)** and **MySQL**. This application helps courier companies, logistics teams, and managers efficiently manage shipments, track delivery status, search records, and export shipment data.

---

## 🚀 Features

### Shipment Management
- Add new shipment records
- Update existing shipment details
- Delete shipment records
- Manage sender and receiver information

### Tracking & Monitoring
- Unique Tracking Number for each shipment
- Track shipment status in real time
- Update current shipment location
- Manager notes for additional tracking information

### Shipment Status Workflow
Supported shipment statuses:

- Pending
- Packaging
- Shipped
- In Transit
- Out for Delivery
- Delivered
- Returned

### Search & Filtering
- Search shipments by tracking number
- Filter shipments by status
- View all shipment records

### Data Export
- Export shipment records to CSV format
- Easy reporting and backup

### User-Friendly Interface
- Modern Tkinter GUI
- TreeView-based shipment table
- Interactive forms and status updates
- Error handling and validation

---

# 🛠️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Core Programming Language |
| Tkinter | GUI Development |
| MySQL | Database Management |
| mysql-connector-python | MySQL Connectivity |
| CSV Module | Data Export |
| Datetime Module | Date Validation |

---

# 📂 Project Structure

```text
Courier-Tracking-System/
│
├── courier_tracking.py
├── courier_tracking_system_DB.sql
├── README.md
│
└── Database
    └── shipments table
```

---

# ⚙️ Database Setup

## 1. Create Database

```sql
CREATE DATABASE courier_db;
```

## 2. Select Database

```sql
USE courier_db;
```

## 3. Run SQL Script

Import the provided SQL file:

```text
courier tracking system DB.sql
```

using MySQL Workbench or command line.

---

# 🔧 Installation

## Clone Repository

```bash
git clone https://github.com/your-username/courier-tracking-system.git
cd courier-tracking-system
```

## Install Dependencies

```bash
pip install mysql-connector-python
```

---

# 🗄️ Configure Database Connection

Open:

```python
courier_tracking.py
```

Update the database configuration:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD',
    'database': 'courier_db'
}
```

---

# ▶️ Run Application

```bash
python courier_tracking.py
```

---

# 📋 Shipment Information Stored

Each shipment record contains:

- Tracking Number
- Sender Name
- Receiver Name
- Origin
- Destination
- Package Date
- Expected Delivery Date
- Current Status
- Current Location
- Manager Notes

---

# 📤 CSV Export

The application allows exporting shipment records into CSV format for:

- Reporting
- Record Keeping
- Backup
- Data Analysis

---

# 🔒 Validation & Error Handling

The system includes:

- Required Tracking Number validation
- Date format validation (YYYY-MM-DD)
- Database connection error handling
- Duplicate record protection
- User-friendly error messages

---

# 📸 Main Functionalities

### Add Shipment
Create and store new shipment records.

### Update Shipment
Modify shipment information and delivery details.

### Delete Shipment
Remove shipment records from the database.

### Search Shipment
Find shipments using tracking numbers.

### Filter Shipments
Display shipments based on their status.

### Bulk Status Updates
Quickly update multiple shipments simultaneously.

### Export Records
Generate CSV reports from shipment data.

---

# 🎯 Future Improvements

- User Authentication System
- Barcode/QR Code Tracking
- Customer Tracking Portal
- Email Notifications
- SMS Notifications
- Delivery Agent Module
- Dashboard Analytics
- PDF Report Generation
- Cloud Database Support

---

# 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Developed using Python, Tkinter, and MySQL for efficient courier and logistics management.

⭐ If you found this project useful, consider giving it a star on GitHub.
