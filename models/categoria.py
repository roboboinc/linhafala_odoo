from odoo import fields, models


class Categoria(models.Model):
    _name = "linhafala.categoria"
    _description = "Categoria"

    name = fields.Char(string="Nome de Categoria")
