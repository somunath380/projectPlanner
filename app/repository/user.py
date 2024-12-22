from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from interfaces.user import UserInterface
from schemas.user import UserCreateRequestSchema, UserBase, UserGetAll, UpdateUserSchema
from utils.storge import load_data, save_data


class UserRepo(UserInterface):
    def __init__(self):
        self.filename = "users.json"
        self.team_filename = "teams.json"
    async def create_user(self, user: UserCreateRequestSchema):
        """_summary_

        Args:
            user (CreateUser): _description_
        """
        try:
            # check if user is existing
            users = await load_data(self.filename)
            existing_user = next((u for u in users if u["name"] == user.name), None)
            if existing_user:
                raise HTTPException(400, detail="user already exists")
            new_user = UserBase(id=len(users)+1, **user.model_dump())
            users.append(new_user.model_dump())
            await save_data(self.filename, users)
            return new_user
            # return JSONResponse({'success': True, "id": new_user.id}, status_code=200)
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def list_users(self):
        try:
            users = await load_data(self.filename)
            user_responses = [UserGetAll(name=user['name'], display_name=user['display_name'], created_at=user['created_at']) for user in users]
            return user_responses
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def describe_user(self, id: int):
        try:
            users = await load_data(self.filename)
            existing_user = next((u for u in users if u["id"] == id), None)
            if not existing_user:
                raise HTTPException(404, detail="user not found")
            return existing_user
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def update_user(self, update_user: UpdateUserSchema):
        try: 
            # check if the user exists or not
            users = await load_data(self.filename)
            existing_user: dict = next((u for u in users if u["id"] == update_user.id), None)
            if not existing_user:
                raise HTTPException(404, detail="user not found")
            existing_user.update(
                name= update_user.user.name,
                display_name = update_user.user.display_name
            )
            await save_data(self.filename, users)
            return JSONResponse({"success": True})
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def list_teams(self):
        try:
            teams = await load_data(self.team_filename)
            return teams
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def get_user_teams(self, id: int):
        try:
            users = await load_data(self.filename)
            existing_user = next((u for u in users if u["id"] == id), None)
            if not existing_user:
                raise HTTPException(404, detail="user not found")
            found_team = []
            all_teams = await self.list_teams()
            for team in all_teams:
                all_users_ids_of_team = [i["id"] for i in team["users"]]
                if id in all_users_ids_of_team:
                    found_team.append({
                        "name": team["name"],
                        "description": team["description"],
                        "created_on": team["created_at"]
                    })
            return JSONResponse(found_team, 200)
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))