from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import uuid


class Caso(models.Model):
    _name = "linhafala.caso"
    _description = "Formulário de Caso linha fala criança"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]

    case_id = fields.Char(string="Id do caso", readonly=True)

    person_id = fields.One2many('linhafala.person_involved', 'case_id',
                                string="Person_involved")

    @api.constrains('person_id')
    def _check_vitima_contactante(self):
        for caso in self:
            has_vitima = False
            has_contactante_vitima = False

            for person in caso.person_id:
                if person.person_type == 'Vítima':
                    has_vitima = True
                elif person.person_type == 'Contactante+Vítima':
                    has_contactante_vitima = True

            if not has_vitima and not has_contactante_vitima:
                raise ValidationError(
                    "Porfavor adicione uma 'Vitima' ou 'Contactante+Vitima' para prosseguir.")
        

    call_id = fields.Many2one(
        comodel_name='linhafala.chamada', string="Chamada")

    case_status = fields.Selection(
        string='Estado do caso',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido", "Assistido"),
            ("No Arquivo Morto", "No Arquivo Morto"),
            ("Encerrado", "Encerrado")
        ],
        help="Estado do caso"
    )

    @api.constrains('case_status')
    def _check_case_status(self):
        for record in self:
            if record.case_status != 'Aberto/Pendente' and record.case_status != 'Dentro do sistema' and record.case_status != 'Assistido' and record.case_status != 'No Arquivo Morto' and record.case_status != 'Encerrado':
                raise ValidationError(
                    "Por favor, selecione o estado do caso para prosseguir.")

    @api.constrains('case_type', 'secundary_case_type', 'case_type_classification', 'detailed_description', 'place_occurrence', 'case_handling', 'case_priority')
    def _check_all(self):
        for record in self:
            if not record.case_type:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Categoria")
            if not record.secundary_case_type:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Sub-categoria")
            if not record.case_priority:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Período de Resolução")
            if not record.detailed_description:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Detalhes")
            if not record.case_type_classification:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Classificaçäo Provisória")
            if not record.place_occurrence:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Local de Ocorrência ")
            if not record.case_handling:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Tratamento do Caso")

    case_priority = fields.Selection(
        string='Período de Resolução',
        selection=[
            ("Muito Urgente", "Muito Urgente"),
            ("Urgente", "Urgente"),
            ("Moderado", "Moderado"),
            ("Não Aplicável", "Não Aplicável"),
        ],
        default="Moderado",
        help="Período de Resolução"
    )
    resolution_type = fields.Selection(
        string='Tratamento do caso',
        selection=[
            ("Aconselhamento LFC", "Aconselhamento LFC"),
            ("Encaminhado", "Encaminhado"),
            ("Não encaminhado", "Não encaminhado"),
        ],
        default="Aconselhamento LFC",
        help="Tratamento do caso"
    )

    case_handling = fields.Selection(
        string='Tratamento do caso',
        selection=[
            ("Aconselhamento LFC", "Aconselhamento LFC"),
            ("Encaminhado", "Encaminhado"),
            ("Não encaminhado", "Não encaminhado"),
        ],
        default="Aconselhamento LFC",
        help="Tratamento do caso"
    )
    place_occurrence = fields.Selection(
        string='Local de Ocorrência',
        selection=[
            ("Escola", "Escola"),
            ("Casa propria", "Casa propria"),
            ("Casa do vizinho", "Casa do vizinho"),
            ("Cresce/infantário", "Cresce/infantário"),
            ("Casa do parente mais próximo", "Casa do parente mais próximo"),
            ("Outros", "Outros")
        ],
        help="Local de Ocorrência"
    )
    detailed_description = fields.Html(string='Descrição detalhada', attrs={
                                       'style': 'height: 500px;'})
    case_type = fields.Many2one(
        comodel_name='linhafala.caso.categoria', string="Categoria")
    secundary_case_type = fields.Many2one(
        comodel_name='linhafala.caso.subcategoria', string="Subcategoria")
    case_type_classification = fields.Many2one(
        comodel_name='linhafala.caso.case_type_classification', string="Classificaçäo Provisória")

    reporter_by = fields.Many2one(
        'res.users', string='Gestão', default=lambda self: self.env.user, readonly=True)
    data_ocorrencia = fields.Datetime(
        string="Data de Ocorrência", widget="datetime", date_format="%d/%m/%Y %H:%M:%S")

    created_at = fields.Datetime(
        string='Data de criaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    updated_at = fields.Datetime(string='Data de actualizaçäo',
                                 default=lambda self: fields.Datetime.now(), readonly=True)
    created_by = fields.Many2one(
        'res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)
    is_deleted = fields.Boolean(string='Apagado', default=False, readonly=True)
    uuid = fields.Char(string='UUID', readonly=True)
    is_locked = fields.Boolean(string='Is Locked', default=False)
    lock_date = fields.Datetime()

    abuse_time = fields.Char(
        string="Tempo de abuso/Sofrimento:")  # NewField
    forwarding_institution_line_ids = fields.One2many('linhafala.caso.forwarding_institution', 'case_id',
                                                      string="Instituição de encaminhamento")

    deficiency_line_case_ids = fields.One2many('linhafala.deficiente', 'case_id',
                                               string="Linhas do Deficiênte")

    manager_by = fields.Many2one(
        'res.users', string="Gerido por: ", compute='_compute_manager_by', store=True)

    @api.depends('manager_by')
    def _compute_manager_by(self):
        for record in self:
            record.manager_by = record.env.user

    def action_manager(self):
        self._compute_manager_by()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ('Caso Assumido com Sucesso!!'),
                    'type': 'success',
                    'sticky': False,
            },
        }

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}

    _sql_constraints = [
        ('unique_case_id', 'unique(case_id)', 'The case_id must be unique'),
    ]

    def write(self, vals):
        if vals:
            vals['updated_at'] = fields.Datetime.now()
        return super(Caso, self).write(vals)

    def unlink(self):
        for record in self:
            record.write({'is_deleted': True})
        return super(Caso, self).unlink()

    @api.model
    def create(self, vals):
        vals['uuid'] = str(uuid.uuid4())
        return super(Caso, self).create(vals)

    @api.model
    def create(self, vals):
        if vals.get('case_id', '/') == '/':
            vals['case_id'] = self.env['ir.sequence'].next_by_code(
                'linhafala.chamada.case_id.seq') or '/'
        return super(Caso, self).create(vals)

    # Lock the case for single user edit
    # TODO: Check and fix that a record gets created and managed by a single user!
    # @api.model
    # def create(self, vals):
    #     # Set the user_id to the current user
    #     vals['user_id'] = self.env.user.id
    #     return super(Caso, self).create(vals)

    # def write(self, vals):
    #     if 'is_locked' in vals:
    #         # Check if the record is already locked by someone else
    #         if self.is_locked and self.user_id != self.env.user:
    #             raise UserError(
    #                 'This record is locked by {}.'.format(self.user_id.name))

    #         # Set the lock_date and user_id fields when the record is locked
    #         if vals['is_locked']:
    #             vals['lock_date'] = fields.Datetime.now()
    #             vals['user_id'] = self.env.user.id

    #         # Unlock the record when is_locked is set to False
    #         else:
    #             vals['lock_date'] = False
    #             vals['user_id'] = False

    #     return super(Caso, self).write(vals)

    # TODO: Review cascade select or remove this field, replacing with buttons as with the current app workflow
    @api.onchange('case_type')
    def _case_type_onchange(self):
        for rec in self:
            return {'value': {'secundary_case_type': False}, 'domain': {'secundary_case_type': [('categoria_id', '=', rec.case_type.id)]}}

    @api.onchange('secundary_case_type')
    def _secundary_case_type_onchange(self):
        for rec in self:
            return {'value': {'case_type_classification': False}, 'domain': {'case_type_classification': [('categoria_id', '=', rec.secundary_case_type.id)]}}

    @api.model
    def _register_hook(self):
        # Register the new sequence
        seq = self.env['ir.sequence'].create({
            'name': 'Linha Fala Cases ID Sequence',
            'code': 'linhafala.chamada.case_id.seq',
            'prefix': 'LFC-CASO-',
            'padding': 4,
        })
        return super(Caso, self)._register_hook()

    def action_confirm(self):
        self.callcaseassistance_status = 'Aberto/Pendente'

    def action_done(self):
        self.callcaseassistance_status = 'Assistido'

    def action_draft(self):
        self.callcaseassistance_status = 'Dentro do sistema'

    def action_cancel(self):
        self.callcaseassistance_status = 'Encerrado'


class PersonInvolved(models.Model):
    _name = "linhafala.caso.person_involved"
    _description = "Person Involved Lines"

    fullname = fields.Char(string="Nome completo")
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
    nr_identication = fields.Char(string="Numero de Identificação")
    wants_to_be_annonymous = fields.Boolean(
        "Consentimento Informado", default=True)
    person_type = fields.Selection(
        string='Categoria',
        selection=[
            ("Contactante", "Contactante"),
            ("Contactante+Vítima", "Contactante+Vítima"),
            ("Vítima", "Vítima"),
            ("Perpetrador", "Perpetrador"),
        ],
        help="Categoria"
    )
    contact = fields.Char(string="Contacto", widget="phone_raw",
                          size=13, min_length=9, default="+258")
    alternate_contact = fields.Char(string="Contacto Alternativo")
    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Provincia")
    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', string="Districto")  # ,
    #    domain=lambda self: [('provincia', '=', self._compute_allowed_distrito_values())])
    bairro = fields.Char(string="Bairro")
    living_relatives = fields.Selection(
        string='Com quem vive?',
        selection=[
            ("Não aplicavél", "Não aplicavél"),
            ("Outra situação", "Outra situação"),
            ("No Centro", "No Centro"),
            ("Sozinho(a)", "Sozinho(a)"),
            ("Com os tios maternos", "Com os tios maternos"),
            ("Com os tios paternos", "Com os tios paternos"),
            ("Só com a mae", "Só com a mae"),
            ("Só com o pai", "Só com o pai"),
            ("Só com os irmãos", "Só com os irmãos"),
            ("Com a familia adoctiva", "Com a familia adoctiva"),
            ("Familia toda", "Familia toda"),
            ("Avo", "Avo")
        ],
        help="Com quem vive?"
    )
    victim_relationship = fields.Selection(
        string='Relação com a(s) vítima(s):',
        selection=[
            ("Mentora", "Mentora"),
            ("Não aplicavél", "Não aplicavél"),
            ("Denunciante", "Denunciante"),
            ("Vitima", "Vitima"),
            ("Nenhuma", "Nenhuma"),
            ("Outros", "Outros"),
            ("Colega", "Colega"),
            ("Primo(a)", "Primo(a)"),
            ("Esposo", "Esposo"),
            ("Namorado", "Namorado"),
            ("Amigo", "Amigo"),
            ("Educador(a)", "Educador(a)"),
            ("Professor(a)", "Professor(a)"),
            ("Empregador", "Empregador"),
            ("Irmã(o)", "Irmã(o)"),
            ("Avo", "Avo"),
            ("Vizinho (a)", "Vizinho (a)"),
            ("Madrasta", "Madrasta"),
            ("Padrasto", "Padrasto"),
            ("Tio(a)", "Tio(a)"),
            ("Pai", "Pai"),
            ("Mãe", "Mãe"),
        ],
        help="Relação com a(s) vítima(s):"
    )
    gender = fields.Selection(
        string='Sexo',
        selection=[
            ("Masculino", "Masculino"),
            ("Feminino", "Feminino"),
            ("Desconhecido", "Desconhecido"),
        ],
        help="Sexo"
    )
    age = fields.Selection([(str(i), str(i)) for i in range(6, 70)] + [('70+', '70+')],
                           string='Idade')
    on_school = fields.Boolean("Estuda?")
    grade = fields.Selection([(str(i), str(i)) for i in range(0, 12)]
                             + [('Ensino Superior', 'Ensino Superior')],
                             string='Classe')
    case_id = fields.Many2one("linhafala.caso", string="Caso")


class ReferenceArea(models.Model):
    _name = "linhafala.caso.referencearea"
    _description = "Área Institucional ou Näo Institucional"

    name = fields.Char(string="Referencia")
    area_type = fields.Selection(
        string='Tipo de instituição',
        selection=[
            ("Institucional", "Institucional"),
            ("Não Institucional", "Não Institucional"),
        ],
        help="Tipo de instituição"
    )


class ReferenceEntity(models.Model):
    _name = "linhafala.caso.referenceentity"
    _description = "Entidade de referência"

    name = fields.Char(string="Nome de entidade")

    reference_area = fields.Many2one(
        comodel_name='linhafala.caso.referencearea', string="Área de Referência")

    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Provincia")
    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', string="Districto")

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}


class CaseReference(models.Model):
    _name = "linhafala.caso.casereference"
    _description = "Pessoa de Contacto"

    name = fields.Char(string="Pessoa de Contacto")

    reference_area = fields.Many2one(
        comodel_name='linhafala.caso.referencearea', string="Referência")

    area_type = fields.Selection(
        string='Área de Encaminhamento',
        selection=[
            ("Institucional", "Institucional"),
            ("Não Institucional", "Não Institucional"),
        ],
        help="Área de Encaminhamento"
    )

    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Provincia")

    reference_entity = fields.Many2one(
        comodel_name='linhafala.caso.referenceentity', string="Entidade de Referência")

    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', string="Districto")

    contact = fields.Char(string="Contacto", widget="phone_raw",  # add the number of pessoa de contacto
                          size=13, min_length=9, default="+258")

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}


class ForwardingInstitutions(models.Model):
    _name = "linhafala.caso.forwarding_institution"
    _description = "Instituição de encaminhamento"

    case_id = fields.Many2one("linhafala.caso", string="Caso")
    area_type = fields.Selection(
        string='Área de Encaminhamento',
        selection=[
            ("Institucional", "Institucional"),
            ("Não Institucional", "Não Institucional"),
        ],
        help="Área de Encaminhamento"
    )

    reference_area = fields.Many2one(
        comodel_name='linhafala.caso.referencearea',
        string="Área de Referência",
        domain="[('area_type', '=', area_type)]"
    )

    reference_entity = fields.Many2one(
        comodel_name='linhafala.caso.referenceentity', string="Entidade de Referência")

    case_reference = fields.Many2one(
        comodel_name='linhafala.caso.casereference',
        string="Pessoa de Contacto",
        domain="[('reference_entity', '=', reference_entity)]"
    )

    spokes_person_phone = fields.Char(
        string="Telefone do Responsável", related='case_reference.contact')
    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Provincia")
    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', string="Districto")

    case_status = fields.Selection(
        string='Estado do caso',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido", "Assistido"),
            ("No Arquivo Morto", "No Arquivo Morto"),
            ("Encerrado", "Encerrado")
        ], default="Aberto/Pendente",
        help="Estado do caso"
    )

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}

    @api.onchange('reference_area')
    def _reference_area_onchange(self):
        for rec in self:
            return {'value': {'reference_entity': False}, 'domain': {'reference_entity': [('reference_area', '=', rec.reference_area.id)]}}
