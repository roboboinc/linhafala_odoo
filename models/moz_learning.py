from xml.dom import ValidationErr
from odoo import api, fields, models
import uuid


class Moz_Learning(models.Model):
    _name = "linhafala.moz_learning"
    _description = "Formulário Moz Learning"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]

    moz_learning_id = fields.Char(string="ID Moz Learning", readonly=True)

    wants_to_be_annonymous = fields.Boolean(
        "Consetimento Informado", default=True)

    fullname = fields.Char(string="Nome Completo", required=True)

    birthd_date = fields.Datetime(string="Data de Nascimento", widget="datetime", date_format="%d/%m/%Y %H:%M:%S")

    gender = fields.Selection(
        string='Sexo',
        selection=[
            ("male", "Masculino"),
            ("female", "Feminino"),
        ], required=True,
        help="Sexo"
    )

    contact = fields.Char(string="Contacto", widget="phone_raw",
                          size=13, min_length=9, default="+258")
    
    id_number = fields.Selection(
        string='Tipo de Identificação',
        selection=[
            ("BI", "BI"),
            ("NUIT", "NUIT"),
            ("Cartão de Eleitor", "Cartão de Eleitor"),
            ("Cedula pessoal", " Cedula pessoal"),
            ("Certidão de Nascimento", " Certidão de Nascimento"),
            ("Carta de condução", "Carta de condução"),
            ("Outro", "Outro"),
        ],
        help="Tipo de documento de identificação"
    )

    isVictim = fields.Boolean(
        "O Denunciante é Vítima ?")
    
    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Província")

    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', string="Districto") 
    
    administrative_post = fields.Char(string="Posto Administrativo")

    locality = fields.Char(string="Localidade")

    community = fields.Char(string="Comunidade/Bairro - Escola")

    