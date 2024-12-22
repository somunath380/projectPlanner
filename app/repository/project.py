from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Dict
from pydantic import ValidationError
import json
from pathlib import Path
import aiofiles
import os

from interfaces.project import ProjectInterface
from schemas.project import *
from utils.storge import load_data, save_data, update_data


class ProjectRepo(ProjectInterface):
    def __init__(self):
        self.filename = "projects.json"
        self.teams_filename = "teams.json"
        self.users_filename = "users.json"
        self.task_filename = "tasks.json"
    
    async def list_teams(self):
        try:
            teams = await load_data(self.teams_filename)
            return teams
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def list_projects(self):
        try:
            return await load_data(self.filename)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def list_users(self):
        try:
            return await load_data(self.users_filename)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def list_tasks(self):
        try:
            return await load_data(self.task_filename)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def create_board(self, board_details: ProjectCreateRequestSchema):
        try:
            # check if board is existing
            all_projects = await self.list_projects()
            existing_project = next((p for p in all_projects if p["name"] == board_details.name), None)
            if existing_project:
                raise HTTPException(400, detail="Project already exists")
            # check team exists or not
            all_teams = await self.list_teams()
            existing_team: Dict = next((t for t in all_teams if t["id"]==board_details.team_id), None)
            if not existing_team:
                raise HTTPException(404, detail=f"No Team found of id {board_details.team_id}")
            new_project = ProjectBase(id=len(all_projects)+1, **board_details.model_dump(), teams=[{"id": board_details.team_id}])
            all_projects.append(new_project.model_dump())
            await save_data(self.filename, all_projects)
            existing_team["projects"].append({
                "id": new_project.id,
                "name": new_project.name
            })
            await update_data(self.teams_filename, existing_team, existing_team["id"])
            return new_project
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def close_board(self, project_id: GetProjectDetailsRequestSchema):
        try:
            # check if board exists
            all_projects = await self.list_projects()
            existing_project: Dict = next((p for p in all_projects if p["id"] == project_id), None)
            if not existing_project:
                raise HTTPException(404, detail="Project not exists")
            # check if all the tasks are closed
            any_open_tasks = next((task for task in existing_project["tasks"] if task["status"] != "CLOSED"), None)
            if any_open_tasks:
                raise HTTPException(404, detail="All tasks needs to be closed for closing board")
            # save closed_at
            existing_project.update(
                status = "CLOSED",
                closed_at = datetime.now(timezone.utc)
            )
            await update_data(self.filename, existing_project, existing_project["id"])
            return JSONResponse({"success": True})
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def add_task(self, added_task_data: AddTaskRequestSchema):
        try:
            # get user details
            all_users = await self.list_users()
            existing_user = next((u for u in all_users if u["id"] == added_task_data.user_id), None)
            if not existing_user:
                raise HTTPException(404, detail=f"user {added_task_data.user_id} not exists")
            # get project
            all_projects = await self.list_projects()
            existing_project = next((p for p in all_projects if p["name"] == added_task_data.name), None)
            if not existing_project:
                raise HTTPException(404, detail=f"No project found with title {added_task_data.name}")
            if existing_project["status"] == ProjectStatus.CLOSED:
                raise HTTPException(400, detail=f"Project is closed")
            # check if the user is present in the teams
            all_teams_of_project = [t["id"] for t in existing_project["teams"]]
            all_teams = await self.list_teams()
            all_users_of_project = []
            for team in all_teams:
                if team["id"] in all_teams_of_project:
                    team_user_ids = [u["id"] for u in team["users"]]
                    all_users_of_project.extend(team_user_ids)
            if added_task_data.user_id not in all_users_of_project:
                raise HTTPException(400, detail=f"{added_task_data.user_id} not present in any team of the project {added_task_data.name}")
            new_task_id = len(existing_project["tasks"]) + 1
            new_task_name = added_task_data.task_name
            new_task_description = added_task_data.description
            new_task_user_id = added_task_data.user_id
            new_task = {
                "id": new_task_id,
                "name": new_task_name,
                "description": new_task_description,
                "user_id": new_task_user_id
            }
            existing_project["tasks"].append(new_task)
            updated_project = ProjectBase(
                **existing_project
            )
            updated_project_json = updated_project.model_dump()
            # update task in projects task
            await update_data(self.filename, updated_project_json, updated_project.id)
            # create a new task in tasks
            new_task_model = TasksBase(**new_task)
            all_tasks = await self.list_tasks()
            all_tasks.append(new_task_model.model_dump())
            await save_data(self.task_filename, all_tasks)
            return new_task_model
        except ValidationError as exe:
            raise HTTPException(400, str(exe))
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def update_task_status(self, task_data: TaskStatusUpdateRequestSchema):
        try: 
            # get all tasks
            all_tasks = await self.list_tasks()
            existing_task = next((t for t in all_tasks if t["id"] == task_data.id), None)
            if not existing_task:
                raise HTTPException(404, detail=f"No task found for id {task_data.id}")
            # update the status
            existing_task["status"] = task_data.status
            await update_data(self.task_filename, existing_task, existing_task["id"])
            # get the task from the projects
            all_projects = await self.list_projects()
            for project in all_projects:
                task_ids = [t["id"] for t in project["tasks"]]
                if task_data.id not in task_ids:
                    continue
                task = next((t for t in project["tasks"] if t["id"] == task_data.id), None)
                # update that status
                task["status"] = task_data.status
                await update_data(self.filename, project, project["id"])
            return JSONResponse({"success": True}, 200)
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def list_boards(self, team_id: TeamIdRequestSchema) -> List[ListBoardResponseSchema]:
        try:
            # get all projects
            all_projects = self.list_projects()
            resp_projects = [ListBoardResponseSchema(id=project["id"], name=project["name"]) for project in all_projects if team_id in project["teams"]]
            return resp_projects
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))
    
    async def export_board(self, board_id: GetProjectDetailsRequestSchema):
        def datetime_to_string(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()  # Converts datetime to ISO 8601 format
            raise TypeError(f"Type {type(obj)} not serializable")
        temp_dir = Path("/tmp")
        temp_dir.mkdir(exist_ok=True)
        file_path = temp_dir / f"project_{board_id}.txt"
        try:
            all_projects = await self.list_projects()
            existing_project = next((p for p in all_projects if p["id"] == board_id), None)
            if not existing_project:
                raise HTTPException(404, detail=f"No project found for id {board_id}")
            
            async with aiofiles.open(file_path, mode="w") as file:
                content = json.dumps(existing_project, default=datetime_to_string, indent=4)
                await file.write(content)
            return FileResponse(
                path=file_path,
                filename=file_path.name,
                media_type="text/plain"
            )
        except HTTPException as exe:
            raise HTTPException(exe.status_code, exe.detail)
        except Exception as exe:
            raise HTTPException(500, str(exe))