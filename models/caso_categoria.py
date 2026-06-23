from odoo import fields, models
from odoo.exceptions import UserError


class CasoCategoria(models.Model):
    _name = "linhafala.caso.categoria"
    _description = "Categoria de Caso"
    _order = "sequence, name, id"

    name = fields.Char(string="Nome de Categoria")
    sequence = fields.Integer(
        string="Sequência",
        default=10,
        help="Define a ordem de apresentação das categorias.",
    )
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar esta categoria. Registos existentes continuam a mostrar o nome desta versão.",
    )
    version = fields.Integer(
        string="Versão",
        default=1,
        readonly=True,
        help="Número de versão desta categoria.",
    )
    previous_version_id = fields.Many2one(
        comodel_name="linhafala.caso.categoria",
        string="Versão Anterior",
        readonly=True,
        copy=False,
        domain="[('active', 'in', [True, False])]",
        help="A versão anterior desta categoria que foi substituída.",
    )
    replaced_by_ids = fields.One2many(
        comodel_name="linhafala.caso.categoria",
        inverse_name="previous_version_id",
        string="Substituída Por",
        copy=False,
        help="Nova(s) versão(ões) que substituíram esta categoria.",
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
        self.env.cr.execute(
            "UPDATE %s SET active = TRUE WHERE active IS NULL" % self._table
        )
        self._backfill_case_records()

    def _backfill_case_records(self):
        case_model = self.env['linhafala.caso']
        if not self._column_exists(case_model._table, 'case_type_snapshot'):
            return
        records = case_model.search([
            ('case_type_snapshot', '=', False),
            ('case_type', '!=', False),
        ])
        for record in records:
            record.with_context(
                skip_case_person_role_validation=True,
                skip_case_priority_backfill_validation=True,
            ).write({'case_type_snapshot': record.case_type.name})

    def write(self, vals):
        if 'name' not in vals:
            return super().write(vals)

        if len(self) > 1:
            raise UserError("Edite uma categoria de cada vez para preservar o histórico de versões.")

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
            super(CasoCategoria, new_record).write(passthrough_vals)

        super(CasoCategoria, record).write({'active': False})
        return True
