import csv
import subprocess
import time
import os

# File paths
csv_file = "most_active_user_in_events_table_data.csv"
done_file = "done.csv"
fail_file = "fail.csv"

# Load previously processed user_ids
def load_processed_user_ids(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return {row[0] for row in csv.reader(f)}
    return set()


# Run the delete_duplicate script with a timeout and track the result
def run_script_with_timeout(user_id, timeout=600):
    try:
        start_time = time.time()
        result = subprocess.run(
            ["python", "delete_duplicate.py", "--user_id", str(user_id)],
            timeout=timeout,
        )
        end_time = time.time()
        if result.returncode == 0 and (end_time - start_time) <= timeout:
            return "success"
    except subprocess.TimeoutExpired:
        pass
    return "failure"


# Main function to process each user_id
def main():
    done_user_ids = load_processed_user_ids(done_file)
    fail_user_ids = load_processed_user_ids(fail_file)

    # Process each user_id in the CSV file
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            user_id = row["user_id"]

            # Skip if already processed
            if user_id in done_user_ids or user_id in fail_user_ids:
                continue

            # Run the script and handle success or failure
            status = run_script_with_timeout(user_id)
            if status == "success":
                with open(done_file, "a", newline="") as done_f:
                    csv.writer(done_f).writerow([user_id])
                print(f"User {user_id} processed successfully.")
            else:
                with open(fail_file, "a", newline="") as fail_f:
                    csv.writer(fail_f).writerow([user_id])
                print(f"User {user_id} failed (timeout or error).")


if __name__ == "__main__":
    main()
