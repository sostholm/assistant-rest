import psycopg
import os
from datetime import datetime
from dataclasses import dataclass

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_ADDRESS = os.getenv("DATABASE_ADDRESS", "192.168.0.218")
DATABASE_NAME = os.getenv("DATABASE_NAME", "assistant_v2")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")

DSN = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{DATABASE_ADDRESS}:{DATABASE_PORT}/{DATABASE_NAME}"
)

async def register_device(
    conn: psycopg.AsyncConnection,
    device_name: str,
    device_type_id: int,
    unique_identifier: str,
    ip_address: str = None,
    mac_address: str = None,
    location: str = None,
    status: str = 'active'
) -> int:
    try:
        async with conn.cursor() as cur:
            # Insert device and return the id
            await cur.execute(
                """
                INSERT INTO devices (device_name, device_type_id, unique_identifier, ip_address, mac_address, location, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    device_name,
                    device_type_id,
                    unique_identifier,
                    ip_address,
                    mac_address,
                    location,
                    status,
                )
            )
            device_id = (await cur.fetchone())[0]

        # Commit the transaction
        await conn.commit()
        return device_id

    except psycopg.Error as e:
        print("Error occurred while registering the device.")
        print(e)
        return None

async def register_device_type(
    conn: psycopg.AsyncConnection,
    type_name: str,
    description: str = None
) -> int:
    try:
        async with conn.cursor() as cur:
            # Insert device type and return the id
            await cur.execute(
                """
                INSERT INTO device_types (type_name, description)
                VALUES (%s, %s)
                ON CONFLICT (type_name) DO UPDATE SET description = EXCLUDED.description
                RETURNING id
                """,
                (type_name, description)
            )
            device_type_id = (await cur.fetchone())[0]

        # Commit the transaction
        await conn.commit()
        return device_type_id

    except psycopg.Error as e:
        print("Error occurred while registering the device type.")
        print(e)
        return None

