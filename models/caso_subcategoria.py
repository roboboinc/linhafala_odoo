from odoo import fields, models


class CasoSubcategoria(models.Model):
    _name = "linhafala.caso.subcategoria"
    _description = "Subcategoria do Caso"

    name = fields.Char(string="Nome da Subcategoria")
    categoria_id = fields.Many2one("linhafala.caso.categoria", string="Categoria do caso")
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar esta subcategoria. Registos existentes continuam a mostrar o nome desta versão.",
    )
    version = fields.Integer(
        string="Versão",
        default=1,
        help="Número de versão desta subcategoria.",
    )
    previous_version_id = fields.Many2one(
        comodel_name="linhafala.caso.subcategoria",
        string="Versão Anterior",
        domain="[('active', 'in', [True, False])]",
        help="A versão anterior desta subcategoria que foi substituída.",
    )
    replaced_by_ids = fields.One2many(
        comodel_name="linhafala.caso.subcategoria",
        inverse_name="previous_version_id",
        string="Substituída Por",
        help="Nova(s) versão(ões) que substituíram esta subcategoria.",
    )
