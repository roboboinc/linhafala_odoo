from xml.dom import ValidationErr
from odoo import api, fields, models
import uuid


class GenderBasedViolence(models.Model):
    _name = "linhafala.gender_based_violence"
    _description = "Formulário de VBG (Violência Baseada no Gênero)"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]

    gender_based_violence_id = fields.Char(
        string="ID da VBG", readonly=True, unique=True)

    moz_learning_id = fields.Many2one(
        comodel_name='linhafala.moz_learning', string="Moz Learning")

    vbg_connected_project = fields.Boolean(
        "VBG está conectado ao projecto ?: ")

    signed_informed_consent = fields.Boolean(
        "Foi assinado o pedido de consentimento informado ?: ")

    attachment = fields.Char(string="Anexe a fotografia do consentimento")

    reasons_for_not_signing = fields.Char(
        string="Quais as razões para não ter assinado?")

    is_there_a_risk_of_retaliation = fields.Boolean(
        "Existe risco de retaliação?: ")

    who_does_the_victim_live_with = fields.Selection(
        string='Com quem vive o(a) vítima?',
        selection=[
            ("Pais", "Pais"),
            ("Avós", "Avós"),
            ("Tios", "Tios"),
            ("Outro", "Outro"),
            ("Não Sabe", "Não Sabe"),
        ],
        help="Com quem vive o(a) vítima?"
    )

    what_other = fields.Char(string="Qual Outro?")

    victim_occupation = fields.Selection(
        string='Ocupação do(a) vítima',
        selection=[
            ("Estudante", "Estudante"),
            ("Doméstico(a)", "Doméstico(a)"),
            ("Sem Ocupação", "Sem Ocupação"),
            ("Outro", "Outro"),
            ("Não Sabe", "Não Sabe"),
        ],
        help="Ocupação do(a) vítima"
    )

    vbg_status = fields.Selection(
        string='Estado do VBG',
        selection=[
            ("Em Curso", "Em Curso"),
            ("Resolvido", "Resolvido"),
        ],
        help="Estado do VBG"
    )
