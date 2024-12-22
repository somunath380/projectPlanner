from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict

from interfaces.team import TeamInterface
from schemas.team import TeamCreateRequestSchema, TeamBase, \
    GetTeamDetailsResponseSchema, GetTeamDetailsRequestSchema, \
    TeamUpdateRequestSchema, AddRemoveUsersToTeamsRequestSchema, UsersOfTeam
from utils.storge import load_data, save_data, update_data


class TeamRepo(TeamInterface):
    def __init__(self):
        self.filename = "teams.json"
        self.users_filename = "users.json"
    
    async def list_users(self):
        try:
            users = await load_data(self.users_filename)
            return users
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def create_team(self, team: TeamCreateRequestSchema):
        try:
            # check if team is existing
            teams = await load_data(self.filename)
            existing_team = next((t for t in teams if t["name"] == team.name), None)
            if existing_team:
                raise HTTPException(400, detail="Team already exists")
            # check admin is in users or not
            all_users = await self.list_users()
            existing_user: Dict = next((u for u in all_users if u["id"]==team.admin), None)
            if not existing_user:
                raise HTTPException(404, detail=f"No user found of id {team.admin}")
            new_team = TeamBase(id=len(teams)+1, **team.model_dump(), users=[{"name": existing_user["name"], "id": existing_user["id"]}])
            teams.append(new_team.model_dump())
            await save_data(self.filename, teams)
            existing_user["teams"].append(new_team.id)
            await update_data(self.users_filename, existing_user, existing_user["id"])
            return new_team
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def list_teams(self):
        try:
            teams = await load_data(self.filename)
            team_responses = [GetTeamDetailsResponseSchema(name=team['name'], description=team['description'], created_at=team['created_at'], admin=team["admin"]) for team in teams]
            return team_responses
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def describe_team(self, id: GetTeamDetailsRequestSchema):
        try:
            teams = await load_data(self.filename)
            existing_team = next((t for t in teams if t["id"] == id), None)
            if not existing_team:
                raise HTTPException(404, detail="team not found")
            return existing_team
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def update_team(self, update_team: TeamUpdateRequestSchema):
        try: 
            # check if the team exists or not
            teams = await load_data(self.filename)
            existing_team: dict = next((t for t in teams if t["id"] == update_team.id), None)
            if not existing_team:
                raise HTTPException(404, detail="user not found")
            existing_team.update(
                name = update_team.team.name,
                description = update_team.team.description,
                admin = update_team.team.admin
            )
            await save_data(self.filename, teams)
            return JSONResponse({"success": True})
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def add_users_to_team(self, data: AddRemoveUsersToTeamsRequestSchema):
        try:
            # get the team
            teams = await load_data(self.filename)
            existing_team: dict = next((t for t in teams if t["id"] == data.id), None)
            if not existing_team:
                raise HTTPException(404, detail="team not found")
            # check if the users in request are already added to the team
            req_user_ids = set(data.users)
            all_users = await self.list_users()
            existing_team_user_ids = [u["id"] for u in existing_team["users"]]
            all_user_ids = [u["id"] for u in all_users]
            
            new_added_users = [] # have {id, name}
            not_found_users = [] # have {id}
            already_added_users = []
            
            for u in req_user_ids:
                if u not in all_user_ids:
                    not_found_users.append(u)
                else:
                    user_detail = next((i for i in all_users if i["id"] == u))
                    if u in existing_team_user_ids:
                        already_added_users.append(u)
                        continue
                    new_added_users.append({"id": user_detail["id"], "name": user_detail["name"]})
            existing_team_users: List = existing_team["users"]
            existing_team_users.extend(new_added_users)
            existing_team.update(
                users = existing_team_users
            )
            await save_data(self.filename, teams)
            # save the team in the user details
            for user in new_added_users:
                user_detail = next((i for i in all_users if i["id"] == user["id"]))
                user_detail["teams"].append(data.id)
                user_detail.update(teams = user_detail["teams"])
                await update_data(self.users_filename, user_detail, user_detail["id"])
            resp_json = {
                "success": True if new_added_users else False,
                "existing_users": already_added_users,
                "not_found_users": not_found_users,
                "added_users": new_added_users
            }
            return JSONResponse(resp_json, 200)
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def remove_users_from_team(self, data: AddRemoveUsersToTeamsRequestSchema):
        try:
            # get the team
            teams = await load_data(self.filename)
            existing_team: dict = next((t for t in teams if t["id"] == data.id), None)
            if not existing_team:
                raise HTTPException(404, detail="team not found")
            # check if the users in request are already added to the team
            req_user_ids = set(data.users)
            all_users = await self.list_users()
            existing_team_user_ids = [u["id"] for u in existing_team["users"]]
            all_user_ids = [u["id"] for u in all_users]
            
            removed_users = [] # have {id}
            not_found_users = [] # have {id}
            
            for u in req_user_ids:
                if u not in all_user_ids:
                    not_found_users.append(u)
                else:
                    user_detail = next((i for i in all_users if i["id"] == u))
                    if u not in existing_team_user_ids:
                        continue
                    removed_users.append(user_detail["id"])
            for id in removed_users:
                for user in existing_team["users"]:
                    if user["id"] == id:
                        existing_team["users"].remove(user)
            existing_team.update(
                users = existing_team["users"]
            )
            await save_data(self.filename, teams)
            # remove team from the user teams data
            for user_id in removed_users:
                user_detail = next((i for i in all_users if i["id"] == user_id))
                user_detail["teams"].remove(data.id)
                user_detail.update(teams = user_detail["teams"])
                await update_data(self.users_filename, user_detail, user_detail["id"])
            resp_json = {
                "success": True if removed_users else False,
                "not_found_users": not_found_users,
                "removed_users": removed_users
            }
            return JSONResponse(resp_json, 200)
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def list_team_users(self, id: GetTeamDetailsRequestSchema) -> List[UsersOfTeam]:
        try:
            teams = await load_data(self.filename)
            existing_team = next((t for t in teams if t["id"] == id), None)
            if not existing_team:
                raise HTTPException(404, detail="team not found")
            return existing_team["users"]
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))