from repository.project import ProjectRepo
from schemas.project import *

class ProjectService:
    def __init__(self):
        self.project_repo = ProjectRepo()
    
    async def create(self, project_data: ProjectCreateRequestSchema):
        return await self.project_repo.create_board(project_data)
    
    async def close_board(self, project_id: GetProjectDetailsRequestSchema):
        return await self.project_repo.close_board(project_id)
    
    async def add_task(self, data: AddTaskRequestSchema):
        return await self.project_repo.add_task(data)
    
    async def update_task(self, data: TaskStatusUpdateRequestSchema):
        return await self.project_repo.update_task_status(data)
    
    async def get_boards_of_team(self, id: TeamIdRequestSchema):
        return await self.project_repo.list_boards(id)
    
    async def export_project_details(self, id: GetProjectDetailsRequestSchema):
        return await self.project_repo.export_board(id)