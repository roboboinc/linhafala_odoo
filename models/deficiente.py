from xml.dom import ValidationErr
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import uuid

class Deficiente():
    _name = "linhafala.deficiente"
    _description = "Formulario Deficiente"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    deficiente_id = fields.Char(
        string= "ID deficiente", readonly=True, unique=True)
    
    are_you_disabled = fields.Boolean(
        "E deficiente?", default=False)
    
    vision = fields.Selection(
        string = '[O(a) inquirido(a)/ele/ela] tem dificuldade em ver,[mesmo quando usa os seus oculos]? Diria que',
        selection=[
            ("Não tem/tenho dificuldade","Não tem/tenho dificuldade")
            ("Tem/tenho alguma dificuldade","Tem/tenho alguma dificuldade")
            ("Tem/tenho muita dificuldade","Tem/tenho muita dificuldade")
            ("Não consegue/consigo de todo","Não consegue/consigo de todo")
            ("Recusa/Recuso-me a responder","Recusa/Recuso-me a responder")
            ("Não sei/não sabe","Não sei/não sabe")
        ],
    )

    hearing = fields.Selection(
        string = '[O(a) inquirido(a)/ele/ela] tem dificuldade em ouvir,[mesmo quando usa aparelho(s) auditivo(s)]? Diria que',
        selection=[
            ("Não tem/tenho dificuldade","Não tem/tenho dificuldade")
            ("Tem/tenho alguma dificuldade","Tem/tenho alguma dificuldade")
            ("Tem/tenho muita dificuldade","Tem/tenho muita dificuldade")
            ("Não consegue/consigo de todo","Não consegue/consigo de todo")
            ("Recusa/Recuso-me a responder","Recusa/Recuso-me a responder")
            ("Não sei/não sabe","Não sei/não sabe")
        ],
    )

    mobility = fields.Selection(
        string = '[O(a) inquirido(a)/ele/ela] tem dificuldade em caminhar ou subir escadas? Diria que',
        selection=[
            ("Não tem/tenho dificuldade","Não tem/tenho dificuldade")
            ("Tem/tenho alguma dificuldade","Tem/tenho alguma dificuldade")
            ("Tem/tenho muita dificuldade","Tem/tenho muita dificuldade")
            ("Não consegue/consigo de todo","Não consegue/consigo de todo")
            ("Recusa/Recuso-me a responder","Recusa/Recuso-me a responder")
            ("Não sei/não sabe","Não sei/não sabe")
        ],
    )

    cognition = fields.Selection(
        string = '[O(a) inquirido(a)/ele/ela] tem dificuldade em lembrar-se ou concentrar-se? Diria que',
        selection=[
            ("Não tem/tenho dificuldade","Não tem/tenho dificuldade")
            ("Tem/tenho alguma dificuldade","Tem/tenho alguma dificuldade")
            ("Tem/tenho muita dificuldade","Tem/tenho muita dificuldade")
            ("Não consegue/consigo de todo","Não consegue/consigo de todo")
            ("Recusa/Recuso-me a responder","Recusa/Recuso-me a responder")
            ("Não sei/não sabe","Não sei/não sabe")
        ],
    )

    autonomous_care = fields.Selection(
        string = '[O(a) inquirido(a)/ele/ela] tem dificuldades em cuidar de si proprio(a), como lavar o corpo inteiro ou vestir-se? Diria que',
        selection=[
            ("Não tem/tenho dificuldade","Não tem/tenho dificuldade")
            ("Tem/tenho alguma dificuldade","Tem/tenho alguma dificuldade")
            ("Tem/tenho muita dificuldade","Tem/tenho muita dificuldade")
            ("Não consegue/consigo de todo","Não consegue/consigo de todo")
            ("Recusa/Recuso-me a responder","Recusa/Recuso-me a responder")
            ("Não sei/não sabe","Não sei/não sabe")
        ],
    )

    comunication = fields.Selection(
        string = 'Utilizando a sua linguagem habitual, [o(a) inquirido(a)/ele/ela] tem dificuldade em comunicar, por exemplo, compreender ou ser compreendido? Diria que',
        selection=[
            ("Não tem/tenho dificuldade","Não tem/tenho dificuldade")
            ("Tem/tenho alguma dificuldade","Tem/tenho alguma dificuldade")
            ("Tem/tenho muita dificuldade","Tem/tenho muita dificuldade")
            ("Não consegue/consigo de todo","Não consegue/consigo de todo")
            ("Recusa/Recuso-me a responder","Recusa/Recuso-me a responder")
            ("Não sei/não sabe","Não sei/não sabe")
        ],
    )