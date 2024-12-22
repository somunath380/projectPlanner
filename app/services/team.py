from repository.team import TeamRepo
from schemas.team import TeamCreateRequestSchema, GetTeamDetailsRequestSchema,\
    TeamUpdateRequestSchema, AddRemoveUsersToTeamsRequestSchema

class TeamService:
    def __init__(self):
        self.team_repo = TeamRepo()
    
    async def create(self, team: TeamCreateRequestSchema):
        return await self.team_repo.create_team(team)

    async def get_all_teams(self):
        return await self.team_repo.list_teams()
    
    async def get_team(self, id: GetTeamDetailsRequestSchema):
        return await self.team_repo.describe_team(id)
    
    async def update_team(self, data: TeamUpdateRequestSchema):
        return await self.team_repo.update_team(data)
    
    async def add_users(self, data: AddRemoveUsersToTeamsRequestSchema):
        return await self.team_repo.add_users_to_team(data)
    
    async def remove_users(self, data: AddRemoveUsersToTeamsRequestSchema):
        return await self.team_repo.remove_users_from_team(data)
    
    async def get_users_of_team(self, id: GetTeamDetailsRequestSchema):
        return await self.team_repo.list_team_users(id)