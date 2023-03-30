from odoo import fields, models


class Provincia(models.Model):
    _name = "linhafala.provincia"
    _description = "Provincias"

    name = fields.Char(string="Nome de provincia")
