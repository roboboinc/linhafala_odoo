from odoo import fields, models


class CasoCategoria(models.Model):
    _name = "linhafala.caso.categoria"
    _description = "Categoria de Caso"

    name = fields.Char(string="Nome de Categoria")
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar esta categoria. Registos existentes continuam a mostrar o nome desta versão.",
    )
    version = fields.Integer(
        string="Versão",
        default=1,
        help="Número de versão desta categoria.",
    )
    previous_version_id = fields.Many2one(
        comodel_name="linhafala.caso.categoria",
        string="Versão Anterior",
        domain="[('active', 'in', [True, False])]",
        help="A versão anterior desta categoria que foi substituída.",
    )
    replaced_by_ids = fields.One2many(
        comodel_name="linhafala.caso.categoria",
        inverse_name="previous_version_id",
        string="Substituída Por",
        help="Nova(s) versão(ões) que substituíram esta categoria.",
    )
