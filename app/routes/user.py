from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_utils.cbv import cbv
from services.user import UserService
from schemas.user import UserCreateRequestSchema, UserGetAll, UserCreateResponseSchema, UserGetResponse, UpdateUserSchema
from typing import List

user_router = APIRouter(prefix="/users")

@cbv(user_router)
class UserController:
    def __init__(self):
        self.user_service = UserService()
    
    # create user
    @user_router.post("/create", response_model=UserCreateResponseSchema)
    async def create_user(self, user: UserCreateRequestSchema):
        try:
            return await self.user_service.register(user)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    # get all users
    @user_router.get("/get", response_model=List[UserGetAll])
    async def get_all_users(self):
        try:
            return await self.user_service.get_all_users()
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    # get a particular user
    @user_router.get("/get/{id}", response_model=UserGetResponse)
    async def get_user(self, id: int):
        try:
            return await self.user_service.get_user(id)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    # update user
    @user_router.put("/update")
    async def update_user(self, user: UpdateUserSchema):
        try:
            return await self.user_service.update_user(user)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    # get user teams
    @user_router.get("/{id}/teams")
    async def get_teams(self, id: int):
        try:
            return await self.user_service.get_teams(id)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
