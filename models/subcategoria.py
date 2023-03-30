from odoo import fields, models


class Provincia(models.Model):
    _name = "linhafala.subcategoria"
    _description = "Subcategoria"

    name = fields.Char(string="Nome da Subcategoria")
    categoria_id = fields.Many2one("linhafala.categoria", string="Categoria")
