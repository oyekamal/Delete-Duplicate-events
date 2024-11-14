# README

## Overview

This repository provides a set of scripts to identify and delete duplicate records for users in the `analytics_analyticsevent` table of a PostgreSQL database. The process involves running a Python script to handle duplicates for the most active users over the past month. Additionally, the results of this process can be verified through SQL queries contained in the `final_queries.sql` file.

### Prerequisites
Ensure that you have the following installed and configured on your system:
- **Python 3.x** (You can check by running `python --version` in your terminal)
- **PostgreSQL** (Ensure access to the database with the appropriate credentials)
- **psycopg2** Python library for PostgreSQL (Install using `pip install psycopg2`)
- **CSV file** containing the most active users (`most_active_user_in_events_table_data.csv`)

## Setup

1. Clone this repository to your local system.

```bash
git clone https://github.com/your-repository.git
cd your-repository
```

2. Install required Python dependencies (if any).

```bash
pip install -r requirements.txt

```

3. Configure the database connection: Update the db_config dictionary in the delete_duplicate.py script with your PostgreSQL database credentials.
```bash
# Database configuration
db_config = {
    "host": "your-database-host", 
    "port": "5432", 
    "dbname": "your-database-name", 
    "user": "your-database-user", 
    "password": "your-database-password"
}
```


## Running the Script
### Step 1: Prepare the Input File

Make sure the file most_active_user_in_events_table_data.csv exists in the same directory as the Python scripts. 

### Step 2: Run the Main Python Script

To start processing and deleting duplicates for the most active users, run the following command:
```bash
python main.py
```


### Step 3: Verify Deletion with SQL Queries

After running the Python scripts, you can verify that duplicates were deleted successfully by running the SQL queries provided in final_queries.sql.