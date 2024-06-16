from xml.dom import ValidationErr
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import uuid


class Deficiente(models.Model):
    _name = "linhafala.deficiente"
    _description = "Formulário Deficiente"
    _rec_name ='call_id'
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
    
    person_id = fields.Many2one(
        comodel_name='linhafala.person_involved', string="Person involved")


    what_disability_does_he_suffer = fields.Selection(
        string='De que necessidade especial padece?',
        selection=[
            ("Visão", "Visão"),
            ("Audição", "Audição"),
            ("Mobilidade", "Mobilidade"),
            ("Cognição", "Cognição"),
            ("Cuidados Autónomo", "Cuidados Autónomo"),
            ("Comunicação", "Comunicação"),
        ]
    )

    vision = fields.Selection(
        string='[O(a) inquirido(a)/ele/ela] tem dificuldade em ver, [mesmo quando usa os seus óculos]? Diria que',
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
        string='[O(a) inquirido(a)/ele/ela] tem dificuldade em ouvir, [mesmo quando usa aparelho(s) auditivo(s)]? Diria que',
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
        string='[O(a) inquirido(a)/ele/ela] tem dificuldade em caminhar ou subir escadas? Diria que',
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
        string='[O(a) inquirido(a)/ele/ela] tem dificuldade em lembrar-se ou concentrar-se? Diria que',
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
        string='[O(a) inquirido(a)/ele/ela] tem dificuldades em cuidar de si próprio(a), como lavar o corpo inteiro ou vestir-se? Diria que',
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

    vision_type = fields.Boolean("Visão:")
    hearing_type = fields.Boolean("Audição:")
    mobility_type = fields.Boolean("Mobilidade:")
    cognition_type = fields.Boolean("Cognição:")
    comunication_type = fields.Boolean("Comunicação:")
    autonomous_care_type = fields.Boolean("Cuidados Autónomos:")
