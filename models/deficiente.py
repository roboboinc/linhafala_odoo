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
        string="ID deficiente", readonly=True)

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

    vision_type = fields.Boolean("Deficiência visual")
    hearing_type = fields.Boolean("Deficiência auditiva")
    mobility_type = fields.Boolean("Deficiência física")
    cognition_type = fields.Boolean("Deficiência intelectual")
    comunication_type = fields.Boolean("Deficiência de comunicação")
    autonomous_care_type = fields.Boolean("Cuidados Autónomos:")
    psicossocial_type = fields.Boolean("Deficiência psicossocial")
    multideficiencia_type = fields.Boolean("Multideficiência")
    autismo_type = fields.Boolean("Autismo")
    albinismo_type = fields.Boolean("Albinismo")

    necessidades_especiais_ok = fields.Char(
        string='Necessidades Especiais OK',
        compute='_compute_necessidades_especiais_ok',
        store=True,
    )

    parent_are_you_disabled = fields.Selection(
        selection=[('Sim','Sim'),('Não','Não')],
        string='Parent tem deficiência?',
        compute='_compute_parent_are_you_disabled',
        store=True,
    )

    @api.depends('vision_type', 'hearing_type', 'mobility_type', 'cognition_type', 'comunication_type', 'autonomous_care_type', 'what_disability_does_he_suffer', 'psicossocial_type', 'multideficiencia_type', 'autismo_type', 'albinismo_type')
    def _compute_necessidades_especiais_ok(self):
        for rec in self:
            if rec.vision_type or rec.hearing_type or rec.mobility_type or rec.cognition_type or rec.comunication_type or rec.autonomous_care_type or rec.what_disability_does_he_suffer or rec.psicossocial_type or rec.multideficiencia_type or rec.autismo_type or rec.albinismo_type:
                rec.necessidades_especiais_ok = 'ok'
            else:
                rec.necessidades_especiais_ok = False

    @api.depends('person_id', 'person_id.are_you_disabled')
    def _compute_parent_are_you_disabled(self):
        for rec in self:
            rec.parent_are_you_disabled = rec.person_id.are_you_disabled if rec.person_id else False

    @api.constrains('vision_type', 'hearing_type', 'mobility_type', 'cognition_type', 'comunication_type', 'autonomous_care_type', 'what_disability_does_he_suffer', 'psicossocial_type', 'multideficiencia_type', 'autismo_type', 'albinismo_type')
    def _check_necessidades_especiais(self):
        for rec in self:
            if rec.person_id and rec.person_id.are_you_disabled == 'Sim':
                if not (rec.vision_type or rec.hearing_type or rec.mobility_type or rec.cognition_type or rec.comunication_type or rec.autonomous_care_type or rec.what_disability_does_he_suffer or rec.psicossocial_type or rec.multideficiencia_type or rec.autismo_type or rec.albinismo_type):
                    raise ValidationError('Selecione pelo menos uma opção em "Necessidades Especiais".')

    @api.model
    def create(self, vals):
        fields = ['vision_type', 'hearing_type', 'mobility_type', 'cognition_type', 'comunication_type', 'autonomous_care_type', 'what_disability_does_he_suffer', 'psicossocial_type', 'multideficiencia_type', 'autismo_type', 'albinismo_type']
        # Only enforce when linked person indicates they have a disability
        person_id = vals.get('person_id') or vals.get('person_id')
        if person_id:
            person = self.env['linhafala.person_involved'].browse(person_id)
            if person and person.are_you_disabled == 'Sim' and not any([vals.get(f) for f in fields]):
                raise ValidationError('Selecione pelo menos uma opção em "Necessidades Especiais".')
        return super(Deficiente, self).create(vals)

    def write(self, vals):
        fields = ['vision_type', 'hearing_type', 'mobility_type', 'cognition_type', 'comunication_type', 'autonomous_care_type', 'what_disability_does_he_suffer', 'psicossocial_type', 'multideficiencia_type', 'autismo_type', 'albinismo_type']
        for rec in self:
            # Determine final values after write
            final = {}
            for f in fields:
                final[f] = vals.get(f, getattr(rec, f))
            # Only enforce when linked person indicates they have a disability
            person = rec.person_id
            if person and person.are_you_disabled == 'Sim' and not any([final.get(f) for f in fields]):
                raise ValidationError('Selecione pelo menos uma opção em "Necessidades Especiais".')
        return super(Deficiente, self).write(vals)
