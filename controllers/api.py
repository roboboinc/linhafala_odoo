from odoo import http
from odoo.http import request, Response
import json
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

# Get current month range
today = datetime.today()
month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
if today.month == 12:
    next_month = today.replace(year=today.year+1, month=1, day=1)
else:
    next_month = today.replace(month=today.month+1, day=1)
month_end = next_month.replace(hour=0, minute=0, second=0, microsecond=0)
current_year_start = today.replace(year=today.year, month=1, day=1)

class ApiController(http.Controller):

    @http.route('/api/statistics/gender-disaggregated', type='http', auth='public', methods=['GET'], csrf=False)
    def get_gender_disaggregated(self, **kwargs):
        vitimas_por_sexo = request.env['linhafala.person_involved'].sudo().read_group(
            domain=[
                ('created_at', '>=', current_year_start),
                ('created_at', '<=', today),
                ('person_type', 'in', ['Contactante+Vítima', 'Vítima'])
            ],
            fields=['gender', 'gender:count'],
            groupby=['gender']
        )
        _logger.debug("RESPONSE: %s", vitimas_por_sexo)  # Debugging output
        total = sum(rec.get('gender_count', 0) for rec in vitimas_por_sexo)
        data = []
        for rec in vitimas_por_sexo:
            gender = rec.get('gender') or 'Indefinido'
            count = rec.get('gender_count', 0)
            percent = (count / total * 100) if total else 0
            data.append({
                'gender': gender,
                'count': count,
                'percent': round(percent, 2)
            })
        return Response(
            json.dumps(data),
            content_type='application/json; charset=utf-8'
        )

    @http.route('/api/statistics', type='http', auth='public', methods=['GET'], csrf=False)
    def get_statistics(self, **kwargs):

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

        chamadas_ano_count = request.env['linhafala.chamada'].sudo().search_count([
            ('created_at', '>=', current_year_start),
            ('created_at', '<=', today),
            ('is_deleted', '=', False)
        ])

        casos_ano_count = request.env['linhafala.caso'].sudo().search_count([
            ('created_at', '>=', current_year_start),
            ('created_at', '<=', today),
            ('is_deleted', '=', False)
        ])
        vitimas_ano_count = request.env['linhafala.person_involved'].sudo().search_count([
            ('created_at', '>=', current_year_start),
            ('created_at', '<=', today),
            ('person_type', 'in', ['Contactante+Vítima', 'Vítima'])
        ])
        vitimas_por_sexo_masculino = request.env['linhafala.person_involved'].sudo().search_count([
            ('created_at', '>=', current_year_start),
            ('created_at', '<=', today),
            ('person_type', 'in', ['Contactante+Vítima', 'Vítima']),
            ('gender', '=', 'Masculino')
        ])
        vitimas_por_sexo_feminino = request.env['linhafala.person_involved'].sudo().search_count([
            ('created_at', '>=', current_year_start),
            ('created_at', '<=', today),
            ('person_type', 'in', ['Contactante+Vítima', 'Vítima']),
            ('gender', '=', 'Feminino')
        ])
        chamadas_com_intervencao_ano_count = request.env['linhafala.chamada'].sudo().search_count([
            ('created_at', '>=', current_year_start),
            ('created_at', '<=', today),
            ('is_deleted', '=', False),
            ('category_status', 'in', ['Com Intervencao'])
        ])
        casos_encaminhados_ano = request.env['linhafala.caso.forwarding_institution'].sudo().search_count([
            ('created_at', '>=', current_year_start),
            ('created_at', '<=', today),
        ])
        casos_assistidos_ano = request.env['linhafala.caso.forwarding_institution'].sudo().search_count([
            ('created_at', '>=', current_year_start),
            ('created_at', '<=', today),
            ('case_status', 'in', ['Assistido'])
        ])
        casos_encerrados_ano = request.env['linhafala.caso.forwarding_institution'].sudo().search_count([
            ('created_at', '>=', current_year_start),
            ('created_at', '<=', today),
            ('case_status', 'in', ['Encerrado'])
        ])

        response_data = {
            "chamadas": chamadas_count,
            "casos": casos_count,
            "vitimas": vitimas_count,
            "month_start": month_start.strftime('%Y-%m-%d %H:%M:%S'),
            "month_end": month_end.strftime('%Y-%m-%d %H:%M:%S'),
            "current_year_start": current_year_start.strftime('%Y-%m-%d %H:%M:%S'),
            "chamadas_ano_count": chamadas_ano_count,
            "casos_ano_count": casos_ano_count,
            "vitimas_ano_count": vitimas_ano_count,
            "chamadas_com_intervencao_ano_count": chamadas_com_intervencao_ano_count,
            "casos_encaminhados_ano": casos_encaminhados_ano,
            "casos_assistidos_ano": casos_assistidos_ano,
            "casos_encerrados_ano": casos_encerrados_ano,
            "vitimas_por_sexo_masculino": vitimas_por_sexo_masculino,
            "vitimas_por_sexo_feminino": vitimas_por_sexo_feminino,
        }
        return Response(
            json.dumps(response_data),
            content_type='application/json; charset=utf-8'
        )