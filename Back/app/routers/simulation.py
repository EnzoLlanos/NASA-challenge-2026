from fastapi import APIRouter, status
from app.schemas.simulation import SimulationRequest, SimulationResponse
from app.services.climate_service import ClimateService

router = APIRouter(prefix="/api/simulation", tags=["Simulación de Rotaciones"])
climate_service = ClimateService()


@router.post(
    "",
    response_model=SimulationResponse,
    status_code=status.HTTP_200_OK,
    summary="Simular las 3 estrategias de rotación con datos NASA y catálogo de cultivos",
    description=(
        "Recibe la configuración del agricultor desde el formulario y ejecuta el ClimateService "
        "combinando los datasets climáticos (power_monthly.csv y power_daily.csv) y el dataset "
        "agronómico (crops.yaml) para devolver las 3 estrategias y la evidencia NASA."
    ),
)
def simulate_rotations(payload: SimulationRequest) -> SimulationResponse:
    return climate_service.simulate(payload)
