from odoo import fields, models


class CaseTypeClassification(models.Model):
    _name = "linhafala.caso.case_type_classification"
    _description = "Classificaçäo Provisória do Caso"

    name = fields.Char(string="Nome da Classificaçäo")
    categoria_id = fields.Many2one("linhafala.caso.subcategoria", string="SubCategoria do caso")
