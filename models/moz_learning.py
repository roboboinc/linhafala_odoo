from xml.dom import ValidationErr
from odoo import api, fields, models
import uuid


class MozLearning(models.Model):
    _name = "linhafala.moz_learning"
    _description = "Formulário Moz Learning"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]

    moz_learning_id = fields.Char(
        string="ID Moz Learning", readonly=True, unique=True)
    
    call_id = fields.Many2one(
        comodel_name='linhafala.chamada', string="Chamada")

    wants_to_be_annonymous = fields.Boolean(
        "Consetimento Informado", default=True)

    fullname = fields.Char(string="Nome Completo", required=True)

    birthd_date = fields.Datetime(
        string="Data de Nascimento", widget="datetime", date_format="%d/%m/%Y %H:%M:%S")

    gender = fields.Selection(
        string='Sexo',
        selection=[
            ("male", "Masculino"),
            ("female", "Feminino"),
        ], required=True,
        help="Sexo"
    )
    have_a_phone = fields.Boolean(
        "Tem Telefone")

    contact = fields.Char(string="Contacto", widget="phone_raw",
                          size=13, min_length=9, default="+258")
    other_means_of_contact = fields.Char(string="Outro meio de Contacto")

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

    document_number = fields.Char(string="Numero do documento", widget="phone_raw",
                          size=13 )

    isVictim = fields.Boolean(
        "O Denunciante é Vítima ?")

    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Província")

    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', string="Districto")

    administrative_post = fields.Char(string="Posto Administrativo")

    locality = fields.Char(string="Localidade")

    community = fields.Char(string="Comunidade/Bairro - Escola")

    complaint_eligibility = fields.Selection(
        string='Elegibilidade da Queixa',
        selection=[
            ("Procedente", "Procedente"),
            ("Não Procedente", "Não Procedente")
        ],
        help="Elegibilidade da Queixa"
    )

    complaint_related_to = fields.Selection(
        string='Esta é uma reclamação reclacionada a',
        selection=[
            ("Ambiental", "Ambiental"),
            ("Social", "Social"),
            ("Desempenho do Projecto", "Desempenho do Projecto")
        ],
        help="Esta é uma reclamação reclacionada a"
    )

    specify = fields.Selection(
        string='Especifique',
        selection=[
            ("VBG", "VBG"),
            ("Morte", "Morte"),
            ("Corrupção", "Corrupção"),
            ("Ambiental(Geral)", "Ambiental"),
            ("Social (Geral)", "Social (Geral)"),
            ("Acidente grave", "Acidente grave"),
            ("Poluição Sonora", "Poluição Sonora"),
            ("Poluição do Ambiente", "Poluição do Ambiente"),
            ("Desempenho do projecto (Geral)", "Desempenho do projecto (Geral)"),
        ],
        help="Especifique"
    )

    type_of_vbg = fields.Selection(
        string='Qual o tipo',
        selection=[
            ("Abuso Sexual", "Abuso Sexual"),
            ("Assédio Sexual", "Assédio Sexual"),
            ("Exploração Sexual", "Exploração Sexual"),
            ("Outras formas de VBG", "Outras formas de VBG"),
        ],
        help="Qual o tipo"
    )

    level_of_urgency = fields.Selection(
        string='Nivel de urgência',
        selection=[
            ("Alto", "Alto"),
            ("Baixo", "Baixo"),
            ("Moderado", "Moderado"),
            ("Substancial", "Substancial")
        ],
        help="Nivel de urgência"
    )

    date_of_occurrence = fields.Datetime(
        string="Data de Ocorrência", widget="datetime", date_format="%d/%m/%Y %H:%M:%S")

    complaint_reception_channel = fields.Selection(
        string='Canal de recepção da reclamação',
        selection=[
            ("Email", "Email"),
            ("Formulário/Caixa", "Formulário/Caixa"),
            ("Ponto Focal Escola", "Ponto Focal Escola"),
            ("Linha Fala Criança", "Linha Fala Criança"),
            ("Ponto Focal Central", "Ponto Focal Central"),
            ("Ponto Focal Distrital de Gênero/Salvaguardas",
             " Ponto Focal Distrital de Gênero/Salvaguardas"),
            ("Ponto Focal Provincial de Gênero/Salvaguardas",
             " Ponto Focal Provincial de Gênero/Salvaguardas"),
        ],
        help="Canal de recepção da reclamação"
    )

    focal_point_name = fields.Char(
        string="Nome do ponto focal que recebeu a reclamação (caso tenha sido recebida presencialmente)")

    focal_point_contact = fields.Char(string="Contacto do ponto focal que recebeu a reclamação", widget="phone_raw",
                                      size=13, min_length=9, default="+258")

    moz_learning_details = fields.Char(string="Resumo da queixa")

    date_of_receipt = fields.Datetime(
        string="Data de recepção", widget="datetime", date_format="%d/%m/%Y %H:%M:%S")

    attachment = fields.Char(string="Anexe aqui o seu documento ou fotografia")

    process_situation = fields.Selection(
        string='Situação do processo',
        selection=[
            ("Em curso", "Em curso"),
            ("Resolvido", "Resolvido")
        ],
        help="Situação do processo"
    )

    updated_at = fields.Datetime(string='Data de actualizaçäo',
                                 default=lambda self: fields.Datetime.now(), readonly=True)

    specify_others = fields.Char(string="Especifique Outros")

    created_by = fields.Many2one(
        'res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)
