from typing import Optional, List

import fastapi
from fastapi import Depends

from models.location import Location
from models.reports import Report, ReportSubmittal
from models.validation_error import ValidationError
from fastapi import Request
from services import openweather_service, report_service
from fastapi_microsoft_identity import requires_auth, validate_scope, AuthError

router = fastapi.APIRouter()

expected_scope = "weather.read"

@router.get('/api/weather/{city}')
@requires_auth
async def weather(request:Request, loc: Location = Depends(), units: Optional[str] = 'metric'):
    try:
        validate_scope(expected_scope, request)
        return await openweather_service.get_report_async(loc.city, loc.state, loc.country, units)
    except AuthError as ae:
        return fastapi.Response(content=ae.error_msg, status_code=ae.status_code)
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    except Exception as x:
        return fastapi.Response(content=str(x), status_code=500)


@router.get('/api/reports', name='all_reports', response_model=List[Report])
async def reports_get() -> List[Report]:
    # await report_service.add_report("A", Location(city="Portland"))
    # await report_service.add_report("B", Location(city="NYC"))
    return await report_service.get_reports()


@router.post('/api/reports', name='add_report', status_code=201, response_model=Report)
async def reports_post(report_submittal: ReportSubmittal) -> Report:
    d = report_submittal.description
    loc = report_submittal.location

    return await report_service.add_report(d, loc)
