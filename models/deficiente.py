from xml.dom import ValidationErr
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import uuid


class Deficiente(models.Model):
    _name = "linhafala.deficiente"
    _description = "Formulário Deficiente"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]

    deficiente_id = fields.Char(
        string="ID deficiente", readonly=True, unique=True)

    call_id = fields.Many2one(
        comodel_name='linhafala.chamada', string="Chamada")

    case_id = fields.Many2one(
        comodel_name='linhafala.caso', string="Caso")

    are_you_disabled = fields.Boolean(
        "E deficiente?", default=True)

    vision = fields.Selection(
        string='Tem dificuldade em ver,[mesmo quando usa os seus oculos]? Diria que',
        selection=[
            ("Não tem/tenho dificuldade", "Não tem/tenho dificuldade"),
            ("Tem/tenho alguma dificuldade", "Tem/tenho alguma dificuldade"),
            ("Tem/tenho muita dificuldade", "Tem/tenho muita dificuldade"),
            ("Não consegue/consigo de todo", "Não consegue/consigo de todo"),
            ("Recusa/Recuso-me a responder", "Recusa/Recuso-me a responder"),
            ("Não sei/não sabe", "Não sei/não sabe"),
        ]
    )

    hearing = fields.Selection(
        string='Tem dificuldade em ouvir,[mesmo quando usa aparelho(s) auditivo(s)]? Diria que',
        selection=[
            ("Não tem/tenho dificuldade", "Não tem/tenho dificuldade"),
            ("Tem/tenho alguma dificuldade", "Tem/tenho alguma dificuldade"),
            ("Tem/tenho muita dificuldade", "Tem/tenho muita dificuldade"),
            ("Não consegue/consigo de todo", "Não consegue/consigo de todo"),
            ("Recusa/Recuso-me a responder", "Recusa/Recuso-me a responder"),
            ("Não sei/não sabe", "Não sei/não sabe"),
        ]
    )

    mobility = fields.Selection(
        string='Tem dificuldade em caminhar ou subir escadas? Diria que',
        selection=[
            ("Não tem/tenho dificuldade", "Não tem/tenho dificuldade"),
            ("Tem/tenho alguma dificuldade", "Tem/tenho alguma dificuldade"),
            ("Tem/tenho muita dificuldade", "Tem/tenho muita dificuldade"),
            ("Não consegue/consigo de todo", "Não consegue/consigo de todo"),
            ("Recusa/Recuso-me a responder", "Recusa/Recuso-me a responder"),
            ("Não sei/não sabe", "Não sei/não sabe"),
        ]
    )

    cognition = fields.Selection(
        string='Tem dificuldade em lembrar-se ou concentrar-se? Diria que',
        selection=[
            ("Não tem/tenho dificuldade", "Não tem/tenho dificuldade"),
            ("Tem/tenho alguma dificuldade", "Tem/tenho alguma dificuldade"),
            ("Tem/tenho muita dificuldade", "Tem/tenho muita dificuldade"),
            ("Não consegue/consigo de todo", "Não consegue/consigo de todo"),
            ("Recusa/Recuso-me a responder", "Recusa/Recuso-me a responder"),
            ("Não sei/não sabe", "Não sei/não sabe"),
        ]
    )

    autonomous_care = fields.Selection(
        string='Tem dificuldades em cuidar de si proprio(a), como lavar o corpo inteiro ou vestir-se? Diria que',
        selection=[
            ("Não tem/tenho dificuldade", "Não tem/tenho dificuldade"),
            ("Tem/tenho alguma dificuldade", "Tem/tenho alguma dificuldade"),
            ("Tem/tenho muita dificuldade", "Tem/tenho muita dificuldade"),
            ("Não consegue/consigo de todo", "Não consegue/consigo de todo"),
            ("Recusa/Recuso-me a responder", "Recusa/Recuso-me a responder"),
            ("Não sei/não sabe", "Não sei/não sabe"),
        ]
    )

    comunication = fields.Selection(
        string='Utilizando a sua linguagem habitual, [o(a) inquirido(a)/ele/ela] tem dificuldade em comunicar, por exemplo, compreender ou ser compreendido? Diria que',
        selection=[
            ("Não tem/tenho dificuldade", "Não tem/tenho dificuldade"),
            ("Tem/tenho alguma dificuldade", "Tem/tenho alguma dificuldade"),
            ("Tem/tenho muita dificuldade", "Tem/tenho muita dificuldade"),
            ("Não consegue/consigo de todo", "Não consegue/consigo de todo"),
            ("Recusa/Recuso-me a responder", "Recusa/Recuso-me a responder"),
            ("Não sei/não sabe", "Não sei/não sabe"),
        ]
    )

    created_by = fields.Many2one(
        'res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)

    deficiency_status = fields.Selection(
        string='Estado do caso',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido", "Assistido"),
            ("Encerrado", "Encerrado"),
        ],
        help="Estado do caso"
    )