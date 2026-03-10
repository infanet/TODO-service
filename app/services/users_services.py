async def get_users(user_repositories):
    users = await user_repositories.all_users()
    return users
