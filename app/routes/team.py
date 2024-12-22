from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_utils.cbv import cbv

from services.team import TeamService
from schemas.team import TeamCreateRequestSchema, GetTeamDetailsRequestSchema, \
    TeamCreateResponseSchema, TeamUpdateRequestSchema, GetTeamDetailsResponseSchema, \
        AddRemoveUsersToTeamsRequestSchema, UsersOfTeam
from typing import List

teams_router = APIRouter(prefix="/teams")

@cbv(teams_router)
class TeamController:
    def __init__(self):
        self.team_service = TeamService()
    
    # create team
    @teams_router.post("/create", response_model=TeamCreateResponseSchema)
    async def create_team(self, team: TeamCreateRequestSchema):
        try:
            return await self.team_service.create(team)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    # get all teams
    @teams_router.get("/get", response_model=List[GetTeamDetailsResponseSchema])
    async def get_all_teams(self):
        try:
            return await self.team_service.get_all_teams()
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    # get a particular team
    @teams_router.get("/get/{id}", response_model=GetTeamDetailsResponseSchema)
    async def get_team(self, id: int):
        try:
            return await self.team_service.get_team(id)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    # update team
    @teams_router.put("/update")
    async def update_team(self, data: TeamUpdateRequestSchema):
        try:
            return await self.team_service.update_team(data)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    # add users
    @teams_router.post("/add/users")
    async def add_users(self, data: AddRemoveUsersToTeamsRequestSchema):
        try:
            return await self.team_service.add_users(data)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    # remove users
    @teams_router.post("/remove/users")
    async def remove_users(self, data: AddRemoveUsersToTeamsRequestSchema):
        try:
            return await self.team_service.remove_users(data)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    # get users of a team
    @teams_router.get("/{id}/users", response_model=List[UsersOfTeam])
    async def get_users(self, id: int):
        try:
            return await self.team_service.get_users_of_team(id)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
