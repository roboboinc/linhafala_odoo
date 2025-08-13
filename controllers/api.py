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
        # _logger.debug("RESPONSE: %s", vitimas_por_sexo)  # Debugging output
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
    
    @http.route('/api/statistics/age-disaggregated', type='http', auth='public', methods=['GET'], csrf=False)
    def get_age_disaggregated(self, **kwargs):
        vitimas_por_idade = request.env['linhafala.person_involved'].sudo().read_group(
            domain=[
                ('created_at', '>=', current_year_start),
                ('created_at', '<=', today),
                ('person_type', 'in', ['Contactante+Vítima', 'Vítima'])
            ],
            fields=['age', 'age:count'],
            groupby=['age']
        )
        # _logger.debug("RESPONSE: %s", vitimas_por_idade)  # Debugging output
        total = sum(rec.get('age_count', 0) for rec in vitimas_por_idade)
        data = []
        for rec in vitimas_por_idade:
            age = rec.get('age') or 'Indefinido'
            count = rec.get('age_count', 0)
            percent = (count / total * 100) if total else 0
            data.append({
                'age': age,
                'count': count,
                'percent': round(percent, 2)
            })
        return Response(
            json.dumps(data),
            content_type='application/json; charset=utf-8'
        )

    @http.route('/api/statistics/victim-by-province', type='http', auth='public', methods=['GET'], csrf=False)
    def get_victims_by_province(self, **kwargs):
        vitimas_por_provincia = request.env['linhafala.person_involved'].sudo().read_group(
            domain=[
                ('created_at', '>=', current_year_start),
                ('created_at', '<=', today),
                ('person_type', 'in', ['Contactante+Vítima', 'Vítima'])
            ],
            fields=['provincia', 'person_id:count'],
            groupby=['provincia']
        )
        total = sum(rec.get('provincia_count', 0) for rec in vitimas_por_provincia)
        data = []
        for rec in vitimas_por_provincia:
            provincia_id = rec.get('provincia')
            provincia_name = 'Indefinido'
            # Handle if provincia_id is a list/tuple or a lazy object
            if isinstance(provincia_id, (list, tuple)):
                provincia_id = provincia_id[0] if provincia_id else False
            if provincia_id and isinstance(provincia_id, int):
                provincia_record = request.env['linhafala.provincia'].sudo().browse(provincia_id)
                provincia_name = provincia_record.name or str(provincia_id)
            count = rec.get('provincia_count', 0)
            percent = (count / total * 100) if total else 0
            data.append({
                'provincia': provincia_name,
                'count': count,
                'percent': round(percent, 2)
            })
        return Response(
            json.dumps(data),
            content_type='application/json; charset=utf-8'
        )

    @http.route('/api/statistics/top-chamadas', type='http', auth='public', methods=['GET'], csrf=False)
    def get_top_chamadas(self, **kwargs):
        chamadas_grouped = request.env['linhafala.chamada'].sudo().read_group(
            domain=[
                ('created_at', '>=', current_year_start),
                ('created_at', '<=', today),
                ('is_deleted', '=', False),
                ('type_of_intervention', '!=', False)
            ],
            fields=['type_of_intervention', 'type_of_intervention:count'],
            groupby=['type_of_intervention']
        )
        total = sum(rec.get('type_of_intervention_count', 0) for rec in chamadas_grouped)
        data = []
        for rec in chamadas_grouped:
            intervention = rec.get('type_of_intervention') or 'Indefinido'
            count = rec.get('type_of_intervention_count', 0)
            percent = (count / total * 100) if total else 0
            data.append({
                'type_of_intervention': intervention,
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