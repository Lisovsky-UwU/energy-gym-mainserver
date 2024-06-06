import io
from typing import Dict
from datetime import timedelta
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet
from xlsxwriter.utility import xl_range
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..models import dto
from ..orm import Visit, User, Entry
from ..models import UserRole
from ..configmodule import config


class VisitsReport:

    def __init__(self, session: Session):
        self.session = session


    def to_excel_format(self, mark: str) -> str:        
        return f'~{mark}' if mark in ('?', '*') else mark
    

    def set_outer_border(self, wb: Workbook, ws: Worksheet, first_row: int, first_col: int, end_row: int, end_col: int, width = 2):
        tl_style = wb.add_format({'border': 1, 'left': width, 'top': width})
        tr_style = wb.add_format({'border': 1, 'top': width, 'right': width})
        bl_style = wb.add_format({'border': 1, 'left': width, 'bottom': width})
        br_style = wb.add_format({'border': 1, 'bottom': width, 'right': width})

        left_style = wb.add_format({'border': 1, 'left': width})
        top_style = wb.add_format({'border': 1, 'top': width})
        right_style = wb.add_format({'border': 1, 'right': width})
        bottom_style = wb.add_format({'border': 1, 'bottom': width})

        ws.conditional_format(first_row, first_col, first_row, first_col, { 'type': 'no_errors', 'format': tl_style })
        ws.conditional_format(first_row, end_col, first_row, end_col, { 'type': 'no_errors', 'format': tr_style })
        ws.conditional_format(end_row, first_col, end_row, first_col, { 'type': 'no_errors', 'format': bl_style })
        ws.conditional_format(end_row, end_col, end_row, end_col, { 'type': 'no_errors', 'format': br_style })

        ws.conditional_format(first_row, first_col, first_row, end_col, { 'type': 'no_errors', 'format': top_style })
        ws.conditional_format(first_row, end_col, end_row, end_col, { 'type': 'no_errors', 'format': right_style })
        ws.conditional_format(end_row, first_col, end_row, end_col, { 'type': 'no_errors', 'format': bottom_style })
        ws.conditional_format(first_row, first_col, end_row, first_col, { 'type': 'no_errors', 'format': left_style })


    def generate(self, data: dto.GetVisitsReportRequest) -> io.BytesIO:
        query = self.session.query(Visit) \
            .where(
                and_(
                    Visit.date >= data.startDate, Visit.date <= data.endDate,
                    Visit.deleted == False,
                    Entry.deleted == False,
                    User.role == UserRole.STUDENT,
                    User.deleted == False,
                )
            )
        if data.group:
            query.where(User.group == data.group)
        
        visits = query.join(Visit.entry_model).join(Entry.user_model).all()

        user_dict: Dict[User, Dict[str, str]] = dict()
        for visit in visits:
            user = visit.entry_model.user_model
            if user not in user_dict:
                user_dict[user] = dict()
            
            user_dict[user][visit.date.strftime('%d.%m')] = config.report.get_for_mark(visit.mark)

        user_dict = dict(sorted(user_dict.items(), key=lambda e: e[0].fullname))

        outio = io.BytesIO()

        wb = Workbook(outio, {'in_memory': True})
        ws = wb.add_worksheet('Отчет')

        head_format = wb.add_format({'bold': True, 'align': 'center', 'border': 1})
        info_format = wb.add_format({'border': 1, 'align': 'left'})
        mark_format = wb.add_format({'border': 1, 'align': 'center'})

        ws.write(0, 0, 'Студенческий', head_format)
        ws.write(0, 1, 'ФИО', head_format)
        ws.write(0, 2, 'Группа', head_format)

        for index, user in enumerate(user_dict.keys(), 1):
            ws.write(index, 0, user.student_card, info_format)
            ws.write(index, 1, user.fullname, info_format)
            ws.write(index, 2, user.group, info_format)

        cur_date = data.startDate
        col_index = 3
        while cur_date <= data.endDate:
            if cur_date.weekday() != 6:
                str_date = cur_date.strftime(config.report.format_day)
                ws.write(0, col_index, str_date, head_format)
                for row_index, (user, marks) in enumerate(user_dict.items(), 1):
                    ws.write(row_index, col_index, marks.get(str_date, ''), mark_format)
                col_index += 1
            
            cur_date += timedelta(days=1)

        ws.write(0, col_index, 'Присутствовал', head_format)
        ws.write(0, col_index + 1, 'Отсутсовал', head_format)
        ws.write(0, col_index + 2, 'Уважительная', head_format)
        ws.write(0, col_index + 3, 'Всего', head_format)
        user_count = len(user_dict.keys())

        for i in range(user_count):
            cells_range = xl_range(i+1, 3, i+1, col_index - 1)
            ws.write(i + 1, col_index, f'=COUNTIF({cells_range},"{self.to_excel_format(config.report.mark_presence)}")', mark_format)
            ws.write(i + 1, col_index + 1, f'=COUNTIF({cells_range},"{self.to_excel_format(config.report.mark_skip)}")', mark_format)
            ws.write(i + 1, col_index + 2, f'=COUNTIF({cells_range},"{self.to_excel_format(config.report.mark_valid)}")', mark_format)
            ws.write(i + 1, col_index + 3, f'=COUNTA({cells_range})', mark_format)

        self.set_outer_border(wb, ws, 0, 0, user_count, 2)
        self.set_outer_border(wb, ws, 0, 3, user_count, col_index - 1)
        self.set_outer_border(wb, ws, 0, col_index, user_count, col_index + 3)

        ws.write(user_count + 3, 0, config.report.mark_presence, mark_format)
        ws.write(user_count + 3, 1, 'Присутствовал', info_format)

        ws.write(user_count + 4, 0, config.report.mark_skip, mark_format)
        ws.write(user_count + 4, 1, 'Пропуск', info_format)

        ws.write(user_count + 5, 0, config.report.mark_valid, mark_format)
        ws.write(user_count + 5, 1, 'Уважительная', info_format)

        ws.write(user_count + 6, 0, config.report.mark_canceled, mark_format)
        ws.write(user_count + 6, 1, 'Занятие отменено', info_format)

        self.set_outer_border(wb, ws, user_count + 3, 0, user_count + 6, 1)

        ws.autofit()
        wb.close()
        outio.seek(0)

        return outio
