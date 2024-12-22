from abc import abstractmethod
from typing import List

from schemas.team import TeamCreateRequestSchema, TeamCreateResponseSchema, \
    GetTeamDetailsResponseSchema, GetTeamDetailsRequestSchema, TeamUpdateRequestSchema, \
    AddRemoveUsersToTeamsRequestSchema, UsersOfTeam

class TeamInterface:
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
    """

    # create a team
    @abstractmethod
    def create_team(self, team: TeamCreateRequestSchema) -> TeamCreateResponseSchema:
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        pass

    # list all teams
    @abstractmethod
    def list_teams(self) -> List[GetTeamDetailsResponseSchema]:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]
        """
        pass

    # describe team
    @abstractmethod
    def describe_team(self, id: GetTeamDetailsRequestSchema) -> GetTeamDetailsResponseSchema:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }

        """
        pass

    # update team
    @abstractmethod
    def update_team(self, data: TeamUpdateRequestSchema):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }

        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        pass

    # add users to team
    @abstractmethod
    def add_users_to_team(self, data: AddRemoveUsersToTeamsRequestSchema):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        pass

    # remove users to team
    @abstractmethod
    def remove_users_from_team(self, data: AddRemoveUsersToTeamsRequestSchema):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        pass

    # list users of a team
    @abstractmethod
    def list_team_users(self, id: GetTeamDetailsRequestSchema) -> List[UsersOfTeam]:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
        """
        pass

