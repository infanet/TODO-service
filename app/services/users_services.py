from repositories import UserRepository
from schemas import UserCreate


async def get_users(user_repositories: UserRepository):
    users = await user_repositories.get_all()
    return users


async def create_user(user_repositories: UserRepository, data: UserCreate):
    user = await user_repositories.create(data)
    return user
