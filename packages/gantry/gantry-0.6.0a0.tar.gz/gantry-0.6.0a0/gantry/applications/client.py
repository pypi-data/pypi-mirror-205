import logging

from typeguard import typechecked

from gantry.api_client import APIClient
from gantry.applications.core import Application

logger = logging.getLogger(__name__)


class ApplicationClient:
    def __init__(self, api_client: APIClient) -> None:
        self._api_client = api_client

    @typechecked
    def create_application(self, application_name: str) -> Application:
        """
        Create an empty application.
        """
        data = {
            "model_name": application_name,
        }

        res = self._api_client.request(
            "POST",
            "/api/v1/applications",
            json=data,
            raise_for_status=True,
        )
        return Application(
            name=application_name,
            api_client=self._api_client,
            id=res["data"]["id"],
        )

    @typechecked
    def get_application(self, application_name: str) -> Application:
        res = self._api_client.request(
            "GET",
            "/api/v1/applications/{}".format(application_name),
            raise_for_status=True,
        )

        return Application(
            api_client=self._api_client,
            id=res["data"]["versions"][0]["application_id"],
            name=res["data"]["func_name"],
        )

    @typechecked
    def archive_application(self, application_name: str) -> None:
        model_id = self.get_application(application_name)._id
        self._api_client.request(
            "DELETE",
            "/api/v1/applications/{}".format(model_id),
            raise_for_status=True,
        )

    @typechecked
    def delete_application(self, application_name: str) -> None:
        model_id = self.get_application(application_name)._id
        self._api_client.request(
            "POST",
            "/api/v1/applications/{}/hard_delete".format(model_id),
            raise_for_status=True,
        )
