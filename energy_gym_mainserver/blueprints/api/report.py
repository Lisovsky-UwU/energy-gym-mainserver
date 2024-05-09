from flask import Blueprint, request, send_file

from ...orm import SessionCtx
from ...models import dto
from ...reports import VisitsReport
from ...exceptions import LogicError


report_bl = Blueprint('report', __name__)


@report_bl.post('/visits')
def generate_report():
    data = dto.GetVisitsReportRequest.parse_obj(request.json)

    if data.endDate <= data.startDate:
        raise LogicError('Дата начала не может быть больше или равна дате окончания отчета')

    with SessionCtx() as session:
        report = VisitsReport(session).generate(data)

    return send_file(report, download_name=f'Посещения с {data.startDate.strftime("%d.%m")} по {data.endDate.strftime("%d.%m")}.xlsx')
