import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import asyncpg

from project.app.config import settings


class PostgresRepository:
    def __init__(self) -> None:
        self._pool: Optional[asyncpg.Pool] = None
        self._pool_lock = asyncio.Lock()

    async def _init_pool(self) -> asyncpg.Pool:
        try:
            pool = await asyncpg.create_pool(dsn=settings.DATABASE_URL, min_size=1, max_size=5)
        except Exception as exc:  # pragma: no cover - defensive message
            raise RuntimeError(
                "Failed to connect to PostgreSQL. Verify the DATABASE_URL environment variable."
            ) from exc
        async with pool.acquire() as conn:
            await self._ensure_schema(conn)
        return pool

    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            async with self._pool_lock:
                if self._pool is None:
                    self._pool = await self._init_pool()
        return self._pool

    @staticmethod
    async def _ensure_schema(conn: asyncpg.Connection) -> None:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id TEXT PRIMARY KEY,
                nombre_usuario VARCHAR(255) NOT NULL,
                display_name VARCHAR(255),
                email VARCHAR(255) NOT NULL,
                contrasena VARCHAR(255),
                photo_url TEXT,
                fecha_registro TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS grupos (
                id UUID PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                descripcion TEXT,
                creador_id TEXT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                fecha_actualizacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS grupo_de_usuarios (
                id_grupo UUID NOT NULL REFERENCES grupos(id) ON DELETE CASCADE,
                id_usuario TEXT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                PRIMARY KEY (id_grupo, id_usuario)
            );
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS productos (
                id UUID PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                estado VARCHAR(50) NOT NULL,
                asignado_a TEXT REFERENCES usuarios(id),
                id_grupo UUID NOT NULL REFERENCES grupos(id) ON DELETE CASCADE,
                cantidad INTEGER NOT NULL DEFAULT 1,
                notas TEXT,
                preset VARCHAR(255),
                fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                fecha_actualizacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mensajes (
                id UUID PRIMARY KEY,
                id_usuario TEXT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                id_grupo UUID NOT NULL REFERENCES grupos(id) ON DELETE CASCADE,
                contenido TEXT NOT NULL,
                fecha_envio TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )

    @staticmethod
    def _safe_uuid(value: str) -> Optional[uuid.UUID]:
        try:
            return uuid.UUID(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _user_record_to_dict(record: asyncpg.Record) -> dict:
        return {
            "id": record["id"],
            "username": record["nombre_usuario"],
            "displayName": record["display_name"],
            "email": record["email"],
            "photoURL": record["photo_url"],
            "createdAt": record["fecha_registro"],
        }

    @staticmethod
    def _group_record_to_dict(record: asyncpg.Record, members: List[str]) -> dict:
        return {
            "id": str(record["id"]),
            "name": record["nombre"],
            "description": record["descripcion"],
            "ownerId": record["creador_id"],
            "members": members,
            "createdAt": record["fecha_creacion"],
            "updatedAt": record["fecha_actualizacion"],
        }

    @staticmethod
    def _product_record_to_dict(record: asyncpg.Record) -> dict:
        return {
            "id": str(record["id"]),
            "groupId": str(record["id_grupo"]),
            "name": record["nombre"],
            "assigneeUserId": record["asignado_a"],
            "status": record["estado"],
            "quantity": record["cantidad"],
            "notes": record["notas"],
            "preset": record["preset"],
            "createdAt": record["fecha_creacion"],
            "updatedAt": record["fecha_actualizacion"],
        }

    @staticmethod
    def _message_record_to_dict(record: asyncpg.Record) -> dict:
        return {
            "id": str(record["id"]),
            "groupId": str(record["id_grupo"]),
            "userId": record["id_usuario"],
            "text": record["contenido"],
            "createdAt": record["fecha_envio"],
        }

    async def _fetch_group_members(self, conn: asyncpg.Connection, group_id: uuid.UUID) -> List[str]:
        rows = await conn.fetch(
            """
            SELECT id_usuario
            FROM grupo_de_usuarios
            WHERE id_grupo = $1
            ORDER BY id_usuario
            """,
            group_id,
        )
        return [row["id_usuario"] for row in rows]

    async def create_user(self, user_id: str, user_data: Dict[str, Any]) -> dict:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                INSERT INTO usuarios (id, nombre_usuario, display_name, email, contrasena, photo_url)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (id) DO UPDATE SET
                    nombre_usuario = EXCLUDED.nombre_usuario,
                    display_name = EXCLUDED.display_name,
                    email = EXCLUDED.email,
                    photo_url = EXCLUDED.photo_url
                RETURNING id, nombre_usuario, display_name, email, photo_url, fecha_registro;
                """,
                user_id,
                user_data.get("username"),
                user_data.get("displayName"),
                user_data.get("email"),
                user_data.get("password"),
                user_data.get("photoURL"),
            )
        return self._user_record_to_dict(record)

    async def get_user(self, user_id: str) -> Optional[dict]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                SELECT id, nombre_usuario, display_name, email, photo_url, fecha_registro
                FROM usuarios
                WHERE id = $1
                """,
                user_id,
            )
        if record is None:
            return None
        return self._user_record_to_dict(record)

    async def create_group(self, group_data: Dict[str, Any]) -> dict:
        pool = await self._get_pool()
        group_id = uuid.uuid4()
        now = datetime.utcnow()
        members = set(group_data.get("members") or [])
        members.add(group_data["ownerId"])
        async with pool.acquire() as conn:
            async with conn.transaction():
                record = await conn.fetchrow(
                    """
                    INSERT INTO grupos (id, nombre, descripcion, creador_id, fecha_creacion, fecha_actualizacion)
                    VALUES ($1, $2, $3, $4, $5, $5)
                    RETURNING id, nombre, descripcion, creador_id, fecha_creacion, fecha_actualizacion;
                    """,
                    group_id,
                    group_data["name"],
                    group_data.get("description"),
                    group_data["ownerId"],
                    now,
                )
                for member_id in members:
                    await conn.execute(
                        """
                        INSERT INTO grupo_de_usuarios (id_grupo, id_usuario)
                        VALUES ($1, $2)
                        ON CONFLICT DO NOTHING;
                        """,
                        group_id,
                        member_id,
                    )
                members_list = await self._fetch_group_members(conn, group_id)
        return self._group_record_to_dict(record, members_list)

    async def get_group(self, group_id: str) -> Optional[dict]:
        group_uuid = self._safe_uuid(group_id)
        if group_uuid is None:
            return None
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                SELECT id, nombre, descripcion, creador_id, fecha_creacion, fecha_actualizacion
                FROM grupos
                WHERE id = $1
                """,
                group_uuid,
            )
            if record is None:
                return None
            members = await self._fetch_group_members(conn, group_uuid)
        return self._group_record_to_dict(record, members)

    async def update_group(self, group_id: str, update_data: Dict[str, Any]) -> Optional[dict]:
        group_uuid = self._safe_uuid(group_id)
        if group_uuid is None:
            return None

        updates: List[str] = []
        values: List[Any] = []
        index = 1

        if "name" in update_data:
            updates.append(f"nombre = ${index}")
            values.append(update_data["name"])
            index += 1
        if "description" in update_data:
            updates.append(f"descripcion = ${index}")
            values.append(update_data["description"])
            index += 1

        updates.append(f"fecha_actualizacion = ${index}")
        values.append(datetime.utcnow())

        set_clause = ", ".join(updates)
        query = f"UPDATE grupos SET {set_clause} WHERE id = ${index + 1}"
        values.append(group_uuid)

        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(query, *values)

        return await self.get_group(group_id)

    async def delete_group(self, group_id: str) -> bool:
        group_uuid = self._safe_uuid(group_id)
        if group_uuid is None:
            return False
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                DELETE FROM grupos
                WHERE id = $1
                """,
                group_uuid,
            )
        return True

    async def list_user_groups(self, user_id: str) -> List[dict]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT g.id, g.nombre, g.descripcion, g.creador_id, g.fecha_creacion, g.fecha_actualizacion
                FROM grupos g
                JOIN grupo_de_usuarios gu ON gu.id_grupo = g.id
                WHERE gu.id_usuario = $1
                ORDER BY g.fecha_creacion DESC
                """,
                user_id,
            )
            result = []
            for record in records:
                members = await self._fetch_group_members(conn, record["id"])
                result.append(self._group_record_to_dict(record, members))
        return result

    async def add_member_to_group(self, group_id: str, user_id: str) -> Optional[dict]:
        group_uuid = self._safe_uuid(group_id)
        if group_uuid is None:
            return None
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    """
                    INSERT INTO grupo_de_usuarios (id_grupo, id_usuario)
                    VALUES ($1, $2)
                    ON CONFLICT DO NOTHING;
                    """,
                    group_uuid,
                    user_id,
                )
                await conn.execute(
                    """
                    UPDATE grupos
                    SET fecha_actualizacion = $1
                    WHERE id = $2
                    """,
                    datetime.utcnow(),
                    group_uuid,
                )
        return await self.get_group(group_id)

    async def remove_member_from_group(self, group_id: str, user_id: str) -> Optional[dict]:
        group_uuid = self._safe_uuid(group_id)
        if group_uuid is None:
            return None
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    """
                    DELETE FROM grupo_de_usuarios
                    WHERE id_grupo = $1 AND id_usuario = $2
                    """,
                    group_uuid,
                    user_id,
                )
                await conn.execute(
                    """
                    UPDATE grupos
                    SET fecha_actualizacion = $1
                    WHERE id = $2
                    """,
                    datetime.utcnow(),
                    group_uuid,
                )
        return await self.get_group(group_id)

    async def create_product(self, product_data: Dict[str, Any]) -> dict:
        pool = await self._get_pool()
        product_id = uuid.uuid4()
        group_uuid = self._safe_uuid(product_data["groupId"])
        if group_uuid is None:
            raise ValueError("Invalid groupId")
        now = datetime.utcnow()
        async with pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                INSERT INTO productos (
                    id, nombre, estado, asignado_a, id_grupo, cantidad, notas, preset, fecha_creacion, fecha_actualizacion
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $9)
                RETURNING id, nombre, estado, asignado_a, id_grupo, cantidad, notas, preset, fecha_creacion, fecha_actualizacion;
                """,
                product_id,
                product_data["name"],
                product_data.get("status", "pending"),
                product_data.get("assigneeUserId"),
                group_uuid,
                product_data.get("quantity", 1),
                product_data.get("notes"),
                product_data.get("preset"),
                now,
            )
        return self._product_record_to_dict(record)

    async def get_product(self, product_id: str) -> Optional[dict]:
        product_uuid = self._safe_uuid(product_id)
        if product_uuid is None:
            return None
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                SELECT id, nombre, estado, asignado_a, id_grupo, cantidad, notas, preset,
                       fecha_creacion, fecha_actualizacion
                FROM productos
                WHERE id = $1
                """,
                product_uuid,
            )
        if record is None:
            return None
        return self._product_record_to_dict(record)

    async def update_product(self, product_id: str, update_data: Dict[str, Any]) -> Optional[dict]:
        product_uuid = self._safe_uuid(product_id)
        if product_uuid is None:
            return None

        field_map = {
            "name": "nombre",
            "status": "estado",
            "assigneeUserId": "asignado_a",
            "quantity": "cantidad",
            "notes": "notas",
            "preset": "preset",
        }

        updates: List[str] = []
        values: List[Any] = []
        index = 1

        for key, column in field_map.items():
            if key in update_data:
                updates.append(f"{column} = ${index}")
                values.append(update_data[key])
                index += 1

        updates.append(f"fecha_actualizacion = ${index}")
        values.append(datetime.utcnow())

        set_clause = ", ".join(updates)
        query = f"UPDATE productos SET {set_clause} WHERE id = ${index + 1}"
        values.append(product_uuid)

        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(query, *values)

        return await self.get_product(product_id)

    async def delete_product(self, product_id: str) -> bool:
        product_uuid = self._safe_uuid(product_id)
        if product_uuid is None:
            return False
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                DELETE FROM productos
                WHERE id = $1
                """,
                product_uuid,
            )
        return True

    async def list_group_products(self, group_id: str) -> List[dict]:
        group_uuid = self._safe_uuid(group_id)
        if group_uuid is None:
            return []
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT id, nombre, estado, asignado_a, id_grupo, cantidad, notas, preset,
                       fecha_creacion, fecha_actualizacion
                FROM productos
                WHERE id_grupo = $1
                ORDER BY fecha_creacion DESC
                """,
                group_uuid,
            )
        return [self._product_record_to_dict(record) for record in records]

    async def create_chat_message(self, message_data: Dict[str, Any]) -> dict:
        pool = await self._get_pool()
        message_id = uuid.uuid4()
        group_uuid = self._safe_uuid(message_data["groupId"])
        if group_uuid is None:
            raise ValueError("Invalid groupId")
        now = datetime.utcnow()
        async with pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                INSERT INTO mensajes (id, id_usuario, id_grupo, contenido, fecha_envio)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id, id_usuario, id_grupo, contenido, fecha_envio;
                """,
                message_id,
                message_data["userId"],
                group_uuid,
                message_data["text"],
                now,
            )
        return self._message_record_to_dict(record)

    async def list_group_messages(self, group_id: str, limit: int = 100) -> List[dict]:
        group_uuid = self._safe_uuid(group_id)
        if group_uuid is None:
            return []
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT id, id_usuario, id_grupo, contenido, fecha_envio
                FROM mensajes
                WHERE id_grupo = $1
                ORDER BY fecha_envio DESC
                LIMIT $2
                """,
                group_uuid,
                limit,
            )
        messages = [self._message_record_to_dict(record) for record in records]
        messages.reverse()
        return messages


repo = PostgresRepository()
