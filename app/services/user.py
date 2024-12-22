from repository.user import UserRepo
from schemas.user import UserCreateRequestSchema, UpdateUserSchema

class UserService:
    def __init__(self):
        self.user_repo = UserRepo()
    
    async def register(self, user: UserCreateRequestSchema):
        return await self.user_repo.create_user(user)

    async def get_all_users(self):
        return await self.user_repo.list_users()
    
    async def get_user(self, id):
        return await self.user_repo.describe_user(id)
    
    async def update_user(self, user: UpdateUserSchema):
        return await self.user_repo.update_user(user)
    
    async def get_teams(self, id: int):
        return await self.user_repo.get_user_teams(id)