from odoo import fields, models


class CasoCategoria(models.Model):
    _name = "linhafala.caso.categoria"
    _description = "Categoria de Caso"

    name = fields.Char(string="Nome de Categoria")
