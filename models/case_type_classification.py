from odoo import fields, models
from odoo.exceptions import UserError


class CaseTypeClassification(models.Model):
    _name = "linhafala.caso.case_type_classification"
    _description = "Classificaçäo Provisória do Caso"

    name = fields.Char(string="Nome da Classificaçäo")
    categoria_id = fields.Many2one("linhafala.caso.subcategoria", string="SubCategoria do caso")
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar esta classificação. Registos existentes continuam a mostrar o nome desta versão.",
    )
    version = fields.Integer(
        string="Versão",
        default=1,
        readonly=True,
        help="Número de versão desta classificação.",
    )
    previous_version_id = fields.Many2one(
        comodel_name="linhafala.caso.case_type_classification",
        string="Versão Anterior",
        readonly=True,
        copy=False,
        domain="[('active', 'in', [True, False])]",
        help="A versão anterior desta classificação que foi substituída.",
    )
    replaced_by_ids = fields.One2many(
        comodel_name="linhafala.caso.case_type_classification",
        inverse_name="previous_version_id",
        string="Substituída Por",
        copy=False,
        help="Nova(s) versão(ões) que substituíram esta classificação.",
    )

    def _column_exists(self, table_name, column_name):
        self.env.cr.execute(
            """
            SELECT 1
              FROM information_schema.columns
             WHERE table_name = %s
               AND column_name = %s
            """,
            (table_name, column_name),
        )
        return bool(self.env.cr.fetchone())

    def init(self):
        self._backfill_case_records()

    def _backfill_case_records(self):
        case_model = self.env['linhafala.caso']
        if not self._column_exists(case_model._table, 'case_type_classification_snapshot'):
            return
        records = case_model.search([
            ('case_type_classification_snapshot', '=', False),
            ('case_type_classification', '!=', False),
        ])
        for record in records:
            record.with_context(
                skip_case_person_role_validation=True,
                skip_case_priority_backfill_validation=True,
            ).write({'case_type_classification_snapshot': record.case_type_classification.name})

    def write(self, vals):
        if 'name' not in vals:
            return super().write(vals)

        if len(self) > 1:
            raise UserError("Edite uma classificação de cada vez para preservar o histórico de versões.")

        record = self[0]
        new_name = (vals.get('name') or '').strip()
        if not new_name or new_name == record.name:
            return super().write(vals)

        passthrough_vals = {k: v for k, v in vals.items() if k != 'name'}
        new_record = record.copy(
            default={
                'name': new_name,
                'version': record.version + 1,
                'previous_version_id': record.id,
                'active': True,
            }
        )
        if passthrough_vals:
            super(CaseTypeClassification, new_record).write(passthrough_vals)

        super(CaseTypeClassification, record).write({'active': False})
        return True
