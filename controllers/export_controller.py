from odoo import http
from odoo.http import request, Response
import csv
import json
from io import StringIO
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class ExportController(http.Controller):

    @http.route('/api/export/chamadas', type='http', auth='user', methods=['GET'], csrf=False)
    def export_chamadas(self, **kwargs):
        """Download CSV of chamadas between start_date and end_date (YYYY-MM-DD).
        Example: /api/export/chamadas?start_date=2025-07-01&end_date=2025-07-31
        """
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        # fallback to current month if missing
        today = datetime.today()
        if not start_date or not end_date:
            start_date = start_date or today.replace(day=1).strftime('%Y-%m-%d')
            if today.month == 12:
                next_month = today.replace(year=today.year+1, month=1, day=1)
            else:
                next_month = today.replace(month=today.month+1, day=1)
            end_date = end_date or (next_month - timedelta(days=1)).strftime('%Y-%m-%d')

        # safe param timestamps
        start_ts = f"{start_date} 00:00:00"
        end_ts = f"{end_date} 23:59:59"

        cr = request.env.cr
        query = """
            SELECT
                c.call_id as nr_da_chamada,
                c.contact_type as tipo_de_contacto,
                c.how_knows_lfc as como_conheceu_a_linha,
                c.call_start as inicio_da_chamada,
                c.call_end as fim_da_chamada,
                c.detailed_description as descricao,
                cast(c.create_date as timestamp) as criado_aos,
                c.bairro,
                created_by.login as criado_por,
                prov.name as provincia,
                dist.name as distrito,
                post.name as posto,
                loc.name as localidade,
                c.age as idade_do_contactante,
                c.fullname as nome_do_contactante,
                c.gender as sexo_do_contactante,
                category_status.name as tipo_de_chamada,
                c.type_of_intervention as motivo,
                c.contact as telefone_do_contactante,
                c.id_number as tipo_documento_do_contactante,
                c.nr_identication as numero_do_documento,
                c.wants_to_be_annonymous as deseja_ser_anonimo,
                c.alternate_contact as contacto_alternativo,
                c.caller_language as lingua,
                c.on_school as estuda,
                c.grade as classe,
                c.school as nome_da_escola
            FROM linhafala_chamada c
                LEFT JOIN linhafala_provincia prov ON c.provincia = prov.id
                LEFT JOIN linhafala_distrito dist ON c.distrito = dist.id
                LEFT JOIN linhafala_posto post ON c.posto = post.id
                LEFT JOIN linhafala_localidade loc ON c.localidade = loc.id
                LEFT JOIN linhafala_categoria category_status ON c.category_status = category_status.id
                LEFT JOIN res_users created_by ON c.created_by = created_by.id
            WHERE c.is_deleted = False
              AND c.create_date >= %s
              AND c.create_date <= %s
            ORDER BY c.create_date;
        """
        try:
            cr.execute(query, (start_ts, end_ts))
            rows = cr.fetchall()
            headers = [d[0] for d in cr.description]

            sio = StringIO()
            writer = csv.writer(sio)
            writer.writerow(headers)
            for row in rows:
                writer.writerow([('' if v is None else v) for v in row])

            csv_data = sio.getvalue().encode('utf-8')
            filename = f"CHAMADAS_{start_date}_{end_date}.csv"
            return Response(csv_data, headers=[
                ('Content-Type', 'text/csv; charset=utf-8'),
                ('Content-Disposition', f'attachment; filename="{filename}"'),
            ])
        except Exception as e:
            _logger.exception('Failed to export chamadas: %s', e)
            return Response(json.dumps({'error': 'export failed'}), status=500, content_type='application/json')
