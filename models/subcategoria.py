from odoo import fields, models


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
        help="Número de versão desta subcategoria.",
    )
    previous_version_id = fields.Many2one(
        comodel_name="linhafala.subcategoria",
        string="Versão Anterior",
        domain="[('active', 'in', [True, False])]",
        help="A versão anterior desta subcategoria que foi substituída.",
    )
    replaced_by_ids = fields.One2many(
        comodel_name="linhafala.subcategoria",
        inverse_name="previous_version_id",
        string="Substituída Por",
        help="Nova(s) versão(ões) que substituíram esta subcategoria.",
    )
