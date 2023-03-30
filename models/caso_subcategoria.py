from odoo import fields, models


class CasoSubcategoria(models.Model):
    _name = "linhafala.caso.subcategoria"
    _description = "Subcategoria do Caso"

    name = fields.Char(string="Nome da Subcategoria")
    categoria_id = fields.Many2one("linhafala.caso.categoria", string="Categoria do caso")
