from pathlib import Path

import pytest
import yaml

from nebari_workflow_controller.app import admission_controller
from nebari_workflow_controller.models import KeycloakGroup, KeycloakUser


@pytest.mark.parametrize(
    "request_file,allowed",
    sorted(
        [(str(p), True) for p in Path("./tests/test_data/requests/pass").glob("*.yaml")]
    )
    + sorted(
        [
            (str(p), False)
            for p in Path("./tests/test_data/requests/fail").glob("*.yaml")
        ]
    ),
)
def test_admission_controller(mocker, request_file, allowed):
    mocker.patch(
        "nebari_workflow_controller.app.get_keycloak_user_info",
        return_value=KeycloakUser(
            username="mocked_username",
            id="mocked_id",
            groups=[
                KeycloakGroup(**g)
                for g in [
                    {
                        "id": "3135c469-02a9-49bc-9245-f886e6317397",
                        "name": "admin",
                        "path": "/admin",
                    },
                    {
                        "id": "137d8913-e7eb-4d68-85a3-59a7a15e99fa",
                        "name": "analyst",
                        "path": "/analyst",
                    },
                ]
            ],
        ),
    )
    with open(request_file) as f:
        request = yaml.load(f, Loader=yaml.FullLoader)
    response = admission_controller(request)
    print(response)
    assert response["response"]["allowed"] == allowed
    if not allowed:
        assert response["response"]["status"]["message"]
