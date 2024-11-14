import csv
import psycopg2
import time
import argparse

# Database configuration
db_config = {"host": "", "port": "5432", "dbname": "", "user": "", "password": ""}


def delete_duplicates(user_id):
    """
    Delete duplicate records for a specific user_id within the last month.
    """
    query = """
    WITH duplicate_rows AS (
        SELECT id
        FROM (
            SELECT id,
                ROW_NUMBER() OVER (PARTITION BY user_ip, sent_at ORDER BY id) AS rn
            FROM public.analytics_analyticsevent
            WHERE user_id = %s
                AND sent_at >= NOW() - INTERVAL '1 month'
        ) AS ranked
        WHERE rn > 1
    )
    DELETE FROM public.analytics_analyticsevent
    WHERE id IN (SELECT id FROM duplicate_rows);
    """
    print(f"Deleting duplicates for user_id: {user_id}...")
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                print(f"Connected to the database for user_id: {user_id}")
                cursor.execute(query, (user_id,))
                conn.commit()
                print(f"Duplicates deleted for user_id: {user_id}")
    except Exception as e:
        print(f"Error deleting duplicates for user_id {user_id}: {e}")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Delete duplicate records for a given user_id."
    )
    parser.add_argument(
        "--user_id",
        type=int,
        required=True,
        help="The user_id to delete duplicates for.",
    )

    args = parser.parse_args()

    # Call the delete_duplicates function with the provided user_id
    delete_duplicates(args.user_id)
