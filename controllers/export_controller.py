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

    @http.route('/api/export/casos', type='http', auth='user', methods=['GET'], csrf=False)
    def export_casos(self, **kwargs):
        """Download CSV of casos between start_date and end_date (YYYY-MM-DD).
        Example: /api/export/casos?start_date=2025-07-01&end_date=2025-07-31
        """
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        # fallback to current month if missing
        today = datetime.today()
        if not start_date or not end_date:
            start_date = start_date or today.replace(day=1).strftime('%Y-%m-%d')
            if today.month == 12:
                next_month = today.replace(year=today.year + 1, month=1, day=1)
            else:
                next_month = today.replace(month=today.month + 1, day=1)
            end_date = end_date or (next_month - timedelta(days=1)).strftime('%Y-%m-%d')

        start_ts = f"{start_date} 00:00:00"
        end_ts = f"{end_date} 23:59:59"

        cr = request.env.cr
        # SQL aligned to the notebook export with safe joins to names/ids we have in models
        query = """
            SELECT
                ROW_NUMBER() OVER (ORDER BY cas.case_id) - 1 AS nr,
                cas.case_id AS nr_do_caso,
                CAST(cas.created_at AS date) AS data_de_criacao,
                cas.case_status AS estado_do_caso,
                cas.case_priority AS prioridade_do_caso,
                cas.resolution_type AS tratamento_do_caso,
                cas.place_occurrence AS local_de_ocorrencia,
                created_by_name.display_name AS criado_por,
                manager_by_name.display_name AS gestor,
                case_type.name AS categoria,
                secundary_case_type.name AS subcategoria,
                case_type_classification.name AS classificacao_provisoria,
                person_involved.fullname AS nome_da_pessoa_envolvida,
                person_involved.person_type AS categoria_pessoa,
                person_involved.contact AS contacto,
                person_involved.age AS idade,
                person_involved.gender AS sexo,
                person_involved.living_relatives AS com_quem_vive,
                person_involved.victim_relationship AS relacao_com_a_vitima,
                person_involved.bairro AS bairro,
                province.name AS provincia,
                distrito.name AS distrito,
                posto.name AS posto,
                localidade.name AS localidade,
                forwarding.area_type AS tipo_de_entidade,
                referenceentity.name AS entidade_de_referencia_de_encaminhamento,
                casereference.name AS pessoa_de_contacto_de_encaminhamento,
                casereference.contact AS telefone_de_encaminhamento
            FROM linhafala_caso cas
                LEFT JOIN linhafala_person_involved person_involved ON cas.id = person_involved.case_id
                LEFT JOIN linhafala_caso_categoria case_type ON cas.case_type = case_type.id
                LEFT JOIN linhafala_caso_subcategoria secundary_case_type ON cas.secundary_case_type = secundary_case_type.id
                LEFT JOIN linhafala_caso_case_type_classification case_type_classification ON cas.case_type_classification = case_type_classification.id
                LEFT JOIN linhafala_caso_forwarding_institution forwarding ON cas.id = forwarding.case_id
                LEFT JOIN linhafala_caso_referenceentity referenceentity ON forwarding.reference_entity = referenceentity.id
                LEFT JOIN linhafala_caso_casereference casereference ON forwarding.case_reference = casereference.id
                LEFT JOIN res_users created_by ON cas.created_by = created_by.id
                LEFT JOIN res_users manager_by ON cas.manager_by = manager_by.id
                LEFT JOIN res_partner created_by_name ON created_by.partner_id = created_by_name.id
                LEFT JOIN res_partner manager_by_name ON manager_by.partner_id = manager_by_name.id
                LEFT JOIN linhafala_provincia province ON person_involved.provincia = province.id
                LEFT JOIN linhafala_distrito distrito ON person_involved.distrito = distrito.id
                LEFT JOIN linhafala_posto posto ON person_involved.posto = posto.id
                LEFT JOIN linhafala_localidade localidade ON person_involved.localidade = localidade.id
            WHERE cas.is_deleted = False
              AND cas.created_at >= %s
              AND cas.created_at <= %s
            ORDER BY cas.created_at;
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
            filename = f"CASOS_{start_date}_{end_date}.csv"
            return Response(csv_data, headers=[
                ('Content-Type', 'text/csv; charset=utf-8'),
                ('Content-Disposition', f'attachment; filename="{filename}"'),
            ])
        except Exception as e:
            _logger.exception('Failed to export casos: %s', e)
            return Response(json.dumps({'error': 'export failed'}), status=500, content_type='application/json')

    @http.route('/api/export/assistencias', type='http', auth='user', methods=['GET'], csrf=False)
    def export_assistencias(self, **kwargs):
        """Download CSV of assistências between start_date and end_date (YYYY-MM-DD).
        Example: /api/export/assistencias?start_date=2025-07-01&end_date=2025-07-31
        """
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        # fallback to current month if missing
        today = datetime.today()
        if not start_date or not end_date:
            start_date = start_date or today.replace(day=1).strftime('%Y-%m-%d')
            if today.month == 12:
                next_month = today.replace(year=today.year + 1, month=1, day=1)
            else:
                next_month = today.replace(month=today.month + 1, day=1)
            end_date = end_date or (next_month - timedelta(days=1)).strftime('%Y-%m-%d')

        start_ts = f"{start_date} 00:00:00"
        end_ts = f"{end_date} 23:59:59"

        cr = request.env.cr
        query = """
            SELECT
                ROW_NUMBER() OVER (ORDER BY callassistance.call_id) - 1 AS nr,
                callassistance.call_id AS nr_da_chamada,
                callassistance.contact AS contacto,
                callassistance.bairro AS bairro,
                prov.name AS provincia,
                dist.name AS distrito,
                post.name AS posto,
                loc.name AS localidade,
                callassistance.gender AS sexo,
                callassistance.age AS idade,
                callassistance.detailed_description AS descricao,
                CAST(callassistance.created_at AS date) AS criado_aos,
                callassistance.callcaseassistance_priority AS prioridade,
                callassistance.callcaseassistance_status AS estado,
                category.name AS tipologia,
                subcategory.name AS sub_tipologia,
                created_by.login AS criado_por,
                assistencereferall.area_type AS tipo_de_area_de_encaminhamento,
                assistencereferall.assistance_status AS estado_da_assistencia
            FROM linhafala_chamada_assistance callassistance
                LEFT JOIN linhafala_provincia prov ON callassistance.provincia = prov.id
                LEFT JOIN linhafala_distrito dist ON callassistance.distrito = dist.id
                LEFT JOIN linhafala_posto post ON callassistance.posto = post.id
                LEFT JOIN linhafala_localidade loc ON callassistance.localidade = loc.id
                LEFT JOIN linhafala_chamada_assistance_categoria category ON callassistance.category = category.id
                LEFT JOIN linhafala_chamada_assistance_subcategoria subcategory ON callassistance.subcategory = subcategory.id
                LEFT JOIN res_users created_by ON callassistance.created_by = created_by.id
                LEFT JOIN res_users reporter ON callassistance.reporter = reporter.id
                LEFT JOIN linhafala_chamada_assistance_referral assistencereferall ON callassistance.id = assistencereferall.assistance_id
            WHERE callassistance.created_at >= %s
              AND callassistance.created_at <= %s
            ORDER BY callassistance.created_at;
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
            filename = f"ASSISTENCIAS_{start_date}_{end_date}.csv"
            return Response(csv_data, headers=[
                ('Content-Type', 'text/csv; charset=utf-8'),
                ('Content-Disposition', f'attachment; filename="{filename}"'),
            ])
        except Exception as e:
            _logger.exception('Failed to export assistencias: %s', e)
            return Response(json.dumps({'error': 'export failed'}), status=500, content_type='application/json')
