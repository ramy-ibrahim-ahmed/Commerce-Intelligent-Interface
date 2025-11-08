from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import UserModel
from ..core.schemas.user import UserCreate, UserUpdate
from ..core.hash import hash_password


class UserService:
    async def _get_user_by(self, db: AsyncSession, attribute: str, value):
        stmt = select(UserModel).filter(getattr(UserModel, attribute) == value)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user(self, db: AsyncSession, user_id: int):
        return await self._get_user_by(db, "id", user_id)

    async def get_user_by_username(self, db: AsyncSession, username: str):
        return await self._get_user_by(db, "username", username)

    async def get_user_by_email(self, db: AsyncSession, email: str):
        return await self._get_user_by(db, "email", email)

    async def get_users(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[UserModel]:
        stmt = select(UserModel).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def create_user(self, db: AsyncSession, user_in: UserCreate):
        user_data = user_in.model_dump(exclude={"password"})
        hashed_password = hash_password(user_in.password)
        db_user = UserModel(**user_data, hashed_password=hashed_password)

        try:
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except Exception as e:
            await db.rollback()
            raise e

    async def update_user(self, db: AsyncSession, user_id: int, user_in: UserUpdate):
        db_user = await self.get_user(db, user_id)
        if not db_user:
            return None

        update_data = user_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            hashed_password = hash_password(update_data["password"])
            db_user.hashed_password = hashed_password
            del update_data["password"]

        for key, value in update_data.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)

        try:
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except Exception as e:
            await db.rollback()
            raise e

    async def delete_user(self, db: AsyncSession, user_id: int):
        db_user = await self.get_user(db, user_id)
        if db_user:
            try:
                await db.delete(db_user)
                await db.commit()
                return db_user
            except Exception as e:
                await db.rollback()
                raise e
        return None
