from abc import abstractmethod
from typing import List

from schemas.project import *

class ProjectInterface:
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """

    # create a board
    @abstractmethod
    def create_board(self, data: ProjectCreateRequestSchema) -> ProjectCreateResponseSchema:
        """
        :param request: A json string with the board details.
        {
            "name" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """
        pass

    # close a board
    @abstractmethod
    def close_board(self, id: GetProjectDetailsRequestSchema):
        """
        :param request: A json string with the board details
        {
          "id" : "<board_id>"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """
        pass

    # add task to board
    @abstractmethod
    def add_task(self, data: AddTaskRequestSchema) -> AddTaskResponseSchema:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "title" : "<board_name>",
            "task_title": "<task_name>"
            "description" : "<description>",
            "user_id" : "<team id>"
            "creation_time" : "<date:time when task was created>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        pass

    # update the status of a task
    @abstractmethod
    def update_task_status(self, task_data: TaskStatusUpdateRequestSchema):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        pass

    # list all open boards for a team
    @abstractmethod
    def list_boards(self, id: TeamIdRequestSchema) -> List[ListBoardResponseSchema]:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        pass
    
    @abstractmethod
    def export_board(self, id: GetProjectDetailsRequestSchema):
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        pass
