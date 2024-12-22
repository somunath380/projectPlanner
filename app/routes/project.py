from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_utils.cbv import cbv

from services.project import ProjectService
from schemas.project import *
from typing import List

projects_router = APIRouter(prefix="/projects")

@cbv(projects_router)
class TeamController:
    def __init__(self):
        self.project_service = ProjectService()
    
    # create project
    @projects_router.post("/create", response_model=ProjectCreateResponseSchema)
    async def create_team(self, project_data: ProjectCreateRequestSchema):
        try:
            return await self.project_service.create(project_data)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    @projects_router.get("/{id}/close")
    async def close_board(self, id: int):
        try:
            return await self.project_service.close_board(id)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    @projects_router.post("/add/task", response_model=AddTaskResponseSchema)
    async def add_task(self, data: AddTaskRequestSchema):
        try:
            return await self.project_service.add_task(data)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    @projects_router.post("/update/task/status")
    async def update_task_status(self, data: TaskStatusUpdateRequestSchema):
        try:
            return await self.project_service.update_task(data)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    @projects_router.get("/get/team/{id}", response_model=List[ListBoardResponseSchema])
    async def list_projects(self, id: int):
        try:
            return await self.project_service.get_boards_of_team(id)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)
    
    @projects_router.get("/export/{id}")
    async def export_project_details(self, id: int):
        try:
            return await self.project_service.export_project_details(id)
        except Exception as exe:
            raise HTTPException(exe.status_code, exe.detail)