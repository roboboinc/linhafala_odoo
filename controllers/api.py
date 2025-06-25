from odoo import http
from odoo.http import request, Response
import json
from datetime import datetime

class ApiController(http.Controller):

    @http.route('/api/statistics', type='http', auth='public', methods=['GET'], csrf=False)
    def get_statistics(self, **kwargs):
        # Get current month range
        today = datetime.today()
        month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if today.month == 12:
            next_month = today.replace(year=today.year+1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month+1, day=1)
        month_end = next_month.replace(hour=0, minute=0, second=0, microsecond=0)

        chamadas_count = request.env['linhafala.chamada'].sudo().search_count([
            ('created_at', '>=', month_start),
            ('created_at', '<', month_end),
            ('is_deleted', '=', False)
        ])
        casos_count = request.env['linhafala.caso'].sudo().search_count([
            ('created_at', '>=', month_start),
            ('created_at', '<', month_end),
            ('is_deleted', '=', False)
        ])
        vitimas_count = request.env['linhafala.person_involved'].sudo().search_count([
            ('created_at', '>=', month_start),
            ('created_at', '<', month_end),
            ('person_type', 'in', ['Contactante+Vítima', 'Vítima'])
        ])

        response_data = {
            "chamadas": chamadas_count,
            "casos": casos_count,
            "vitimas": vitimas_count,
            "month_start": month_start.strftime('%Y-%m-%d %H:%M:%S'),
            "month_end": month_end.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return Response(
            json.dumps(response_data),
            content_type='application/json; charset=utf-8'
        )