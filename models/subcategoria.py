from odoo import fields, models
from odoo.exceptions import UserError


class Subcategoria(models.Model):
    _name = "linhafala.subcategoria"
    _description = "Subcategoria"

    name = fields.Char(string="Nome da Subcategoria")
    categoria_id = fields.Many2one("linhafala.categoria", string="Categoria")
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar esta subcategoria. Registos existentes continuam a mostrar o nome desta versão.",
    )
    version = fields.Integer(
        string="Versão",
        default=1,
        readonly=True,
        help="Número de versão desta subcategoria.",
    )
    previous_version_id = fields.Many2one(
        comodel_name="linhafala.subcategoria",
        string="Versão Anterior",
        readonly=True,
        copy=False,
        domain="[('active', 'in', [True, False])]",
        help="A versão anterior desta subcategoria que foi substituída.",
    )
    replaced_by_ids = fields.One2many(
        comodel_name="linhafala.subcategoria",
        inverse_name="previous_version_id",
        string="Substituída Por",
        copy=False,
        help="Nova(s) versão(ões) que substituíram esta subcategoria.",
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
        self._backfill_chamada_records()

    def _backfill_chamada_records(self):
        chamada_model = self.env['linhafala.chamada']
        if not self._column_exists(chamada_model._table, 'subcategory_snapshot'):
            return
        records = chamada_model.search([
            ('subcategory_snapshot', '=', False),
            ('subcategory', '!=', False),
        ])
        for record in records:
            record.write({'subcategory_snapshot': record.subcategory.name})

    def write(self, vals):
        if 'name' not in vals:
            return super().write(vals)

        if len(self) > 1:
            raise UserError("Edite uma subcategoria de cada vez para preservar o histórico de versões.")

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
            super(Subcategoria, new_record).write(passthrough_vals)

        super(Subcategoria, record).write({'active': False})
        return True
