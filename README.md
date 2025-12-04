# Restaurant Order Management API - Complete Setup Guide

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- Postman (for API testing)

## 🚀 Step-by-Step Setup

### Step 1: Install MySQL

1. Download MySQL from [https://dev.mysql.com/downloads/](https://dev.mysql.com/downloads/)
2. Install and note down your root password
3. Start MySQL service

### Step 2: Create Project Directory

```bash
mkdir restaurant-api
cd restaurant-api
```

### Step 3: Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Database Connection

Edit the following files and update your MySQL credentials:

**In `setup_database.py`:**
```python
connection = mysql.connector.connect(
    host='localhost',
    user='root',  # Your MySQL username
    password='YOUR_PASSWORD_HERE'  # Your MySQL password
)
```

**In `main.py`:**
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Your MySQL username
    'password': 'YOUR_PASSWORD_HERE',  # Your MySQL password
    'database': 'restaurant_db'
}
```

### Step 6: Run Database Setup Script

```bash
python setup_database.py
```


### Step 7: Start the API Server

```bash
python main.py
```


