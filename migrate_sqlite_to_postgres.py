#!/usr/bin/env python3
"""
Migrate the existing ROBO TUNISIE SQLite database to PostgreSQL.

Usage:
    set DATABASE_URL=postgresql://...
    python migrate_sqlite_to_postgres.py

The SQLite database is read-only during migration. Existing PostgreSQL rows
are preserved by default. Use --replace to clear the four application tables
before importing.
"""

import argparse
import os
import sqlite3
import sys

import psycopg
from psycopg.rows import tuple_row


TABLES = ("clubs", "competitions", "documents", "social_links")


def create_schema(pg):
    with pg.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clubs (
                id BIGSERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                phone TEXT,
                city TEXT,
                facebook TEXT,
                instagram TEXT,
                linkedin TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS competitions (
                id BIGSERIAL PRIMARY KEY,
                club_id BIGINT NOT NULL REFERENCES clubs(id),
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT,
                challenges TEXT,
                max_participants TEXT,
                registration_deadline TEXT,
                website TEXT,
                contact_email TEXT NOT NULL,
                contact_phone TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id BIGSERIAL PRIMARY KEY,
                competition_id BIGINT NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS social_links (
                id BIGSERIAL PRIMARY KEY,
                competition_id BIGINT NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
                platform TEXT NOT NULL,
                url TEXT NOT NULL
            )
        """)


def clear_tables(pg):
    with pg.cursor() as cur:
        cur.execute("TRUNCATE social_links, documents, competitions, clubs RESTART IDENTITY CASCADE")


def copy_table(sqlite_conn, pg, table, columns):
    sqlite_cur = sqlite_conn.cursor()
    sqlite_cur.execute(f"SELECT {', '.join(columns)} FROM {table}")
    rows = sqlite_cur.fetchall()

    if not rows:
        return 0

    placeholders = ", ".join(["%s"] * len(columns))
    column_sql = ", ".join(columns)

    with pg.cursor() as cur:
        cur.executemany(
            f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})",
            rows,
        )

    return len(rows)


def reset_sequences(pg):
    with pg.cursor() as cur:
        for table in TABLES:
            cur.execute(
                f"""
                SELECT setval(
                    pg_get_serial_sequence(%s, 'id'),
                    COALESCE((SELECT MAX(id) FROM {table}), 1),
                    (SELECT COUNT(*) > 0 FROM {table})
                )
                """,
                (table,),
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sqlite",
        default="robo_tunisie.db",
        help="Path to the existing SQLite database",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete existing PostgreSQL application data before importing",
    )
    args = parser.parse_args()

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL is not set.", file=sys.stderr)
        return 1

    if not os.path.exists(args.sqlite):
        print(f"ERROR: SQLite database not found: {args.sqlite}", file=sys.stderr)
        return 1

    sqlite_conn = sqlite3.connect(args.sqlite)

    try:
        with psycopg.connect(database_url, row_factory=tuple_row) as pg:
            create_schema(pg)

            if args.replace:
                clear_tables(pg)

            # Parents first, then children.
            counts = {}
            counts["clubs"] = copy_table(
                sqlite_conn,
                pg,
                "clubs",
                ("id", "name", "email", "password", "phone", "city",
                 "facebook", "instagram", "linkedin", "created_at"),
            )
            counts["competitions"] = copy_table(
                sqlite_conn,
                pg,
                "competitions",
                ("id", "club_id", "name", "date", "location", "description",
                 "challenges", "max_participants", "registration_deadline",
                 "website", "contact_email", "contact_phone", "created_at"),
            )
            counts["documents"] = copy_table(
                sqlite_conn,
                pg,
                "documents",
                ("id", "competition_id", "title", "file_path", "file_type", "upload_date"),
            )
            counts["social_links"] = copy_table(
                sqlite_conn,
                pg,
                "social_links",
                ("id", "competition_id", "platform", "url"),
            )

            reset_sequences(pg)

            print("Migration completed successfully.")
            for table, count in counts.items():
                print(f"  {table}: {count} rows")

    finally:
        sqlite_conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
