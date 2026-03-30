from fastapi import APIRouter
from api.services import patient_service, observation_service
from integrations import integration_service

router = APIRouter()


@router.get("/patients")
def get_patients(
    name: str = None,
    page: int = 1,
    page_size: int = 10,
    server: str = "hapi"
):
    return patient_service.get_patients(name, page, page_size, server)


@router.get("/observations/{patient_id}")
def get_observations(
    patient_id: str,
    server: str = "hapi"
):
    return observation_service.get_observations(
        patient_id,
        server
    )


@router.get("/dashboard/patient_overview")
def patient_dashboard(server: str = "hapi"):
    """
    Endpoint to generate dashboard-ready dataset.
    """
    return integration_service.export_dashboard(server)