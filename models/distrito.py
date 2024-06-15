from odoo import fields, models


class Provincia(models.Model):
    _name = "linhafala.distrito"
    _description = "Distritos"

    name = fields.Char(string="Nome de distrito")
    provincia = fields.Many2one("linhafala.provincia", string="Provincia")
