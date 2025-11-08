from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import UserService
from ..core.schemas.user import UserCreate, UserUpdate, UserPublic
from ..core.db import get_session

router = APIRouter(prefix="/users", tags=["Users"])


# 1. Add this function to create and return an instance of your service
def get_user_service() -> UserService:
    return UserService()


@router.post(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_new_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_session),
    # 2. Add the service as a dependency here
    user_service: UserService = Depends(get_user_service),
):
    # 3. Use the 'user_service' instance instead of the 'UserService' class
    existing_user = await user_service.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )

    # 3. Use the instance
    existing_user = await user_service.get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken.",
        )

    # 3. Use the instance
    user = await user_service.create_user(db=db, user_in=user_in)
    return user


@router.get("/", response_model=list[UserPublic], summary="Get a list of users")
async def read_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
    # 2. Add the service as a dependency here
    user_service: UserService = Depends(get_user_service),
):
    # 3. Use the instance
    users = await user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserPublic, summary="Get a single user by ID")
async def read_single_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
):
    db_user = await user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.patch("/{user_id}", response_model=UserPublic, summary="Update a user")
async def update_existing_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
):
    updated_user = await user_service.update_user(db, user_id=user_id, user_in=user_in)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return updated_user


@router.delete(
    "/{user_id}",
    response_model=UserPublic,
    summary="Delete a user",
)
async def delete_existing_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
):
    deleted_user = await user_service.delete_user(db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return deleted_user
