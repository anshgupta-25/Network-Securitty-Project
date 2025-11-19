import sqlite3

conn = sqlite3.connect('honeypot_events.db')
cur = conn.cursor()

print("\n=== DATABASE SCHEMA CHECK ===\n")

# Get all tables
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables in database:")
for table in tables:
    print(f"  ✓ {table[0]}")

print("\n=== CHECKING DATA ===\n")

# Check each table
for table in tables:
    table_name = table[0]
    count = cur.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"{table_name}: {count} rows")

print("\n=== CHECKING REQUIRED TABLES ===\n")

required_tables = ['events', 'auth_attempts', 'commands', 'sessions', 'ip_intel']
missing_tables = []

for req_table in required_tables:
    exists = cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{req_table}'").fetchone()
    if exists:
        print(f"  ✓ {req_table} - EXISTS")
    else:
        print(f"  ✗ {req_table} - MISSING")
        missing_tables.append(req_table)

if missing_tables:
    print(f"\n⚠️  ISSUE FOUND: Missing tables: {', '.join(missing_tables)}")
    print("The dashboard needs these tables for full functionality!")
else:
    print("\n✅ All required tables exist!")

conn.close()
