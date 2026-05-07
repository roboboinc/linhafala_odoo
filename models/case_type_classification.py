from odoo import fields, models


class CaseTypeClassification(models.Model):
    _name = "linhafala.caso.case_type_classification"
    _description = "Classificaçäo Provisória do Caso"

    name = fields.Char(string="Nome da Classificaçäo")
    categoria_id = fields.Many2one("linhafala.caso.subcategoria", string="SubCategoria do caso")
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar esta classificação. Registos existentes continuam a mostrar o nome desta versão.",
    )
    version = fields.Integer(
        string="Versão",
        default=1,
        help="Número de versão desta classificação.",
    )
    previous_version_id = fields.Many2one(
        comodel_name="linhafala.caso.case_type_classification",
        string="Versão Anterior",
        domain="[('active', 'in', [True, False])]",
        help="A versão anterior desta classificação que foi substituída.",
    )
    replaced_by_ids = fields.One2many(
        comodel_name="linhafala.caso.case_type_classification",
        inverse_name="previous_version_id",
        string="Substituída Por",
        help="Nova(s) versão(ões) que substituíram esta classificação.",
    )
