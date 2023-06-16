from xml.dom import ValidationErr
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import uuid


class Chamada(models.Model):
    _name = "linhafala.chamada"
    _description = "Formulário de chamadas linha fala criança"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]

    call_id = fields.Char(string="ID da chamada", readonly=True)

    case_id = fields.One2many('linhafala.caso', 'call_id',
                              string="Caso")
    person_id = fields.One2many('linhafala.person_involved', 'case_id',
                                string="Person_involved")

    category = fields.Many2one(
        comodel_name='linhafala.categoria', string="Categoria", default=lambda self: self.env['linhafala.categoria'].browse(2))
    contact_type = fields.Selection(
        string='Fonte de Informação',
        selection=[
            ("SMS BIZ", "SMS BIZ"),
            ("LInha Verde 1458", "LInha Verde 1458"),
            ("Não definido", "Não definido"),
            ("Presencial", "Presencial"),
            ("Telefónica", "Telefónica"),
            ("Palestras", "Palestras"),
            ("Email", "Email"),
            ("Redes Sociais", "Redes Sociais"),
        ], default="Telefónica",
        help="Type is used to separate Contact types"
    )
    type_of_intervention = fields.Selection(
        string='Tipo de Intervenção / Motivo',
        selection=[
            ("Caso", "Caso"),
            ("Engano", "Engano"),
            ("Perdida", "Perdida"),
            ("Moz Learning", "Moz Learning"),
            ("Agradecimento", "Agradecimento"),
            ("Comportamento", "Comportamento"),
            ("Chamada de Assistência", "Chamada de Assistência"),
            ("Informação Geral sobre a LFC", "Informação Geral sobre a LFC"),
        ],
        help="Type is used to separate Contact types"
    )
    caller_language = fields.Selection(
        string='Lingua/Dialetos',
        selection=[("Português ", "Português "),
                   ("Inglês ", "Inglês"),
                   ("Kimwani", "Kimwani - (Kimwani)"),
                   ("Shimakonde", "Shimakonde - (makonde)"),
                   ("Ciyaawo", "Ciyaawo - (Yaawo)"),
                   ("Emakhuwa", "Emakhuwa - (macua)"),
                   ("Ekoti", "Ekoti - (koti)"),
                   ("Elomowe", "Elomowe - (lomowe)"),
                   ("Echuwabo", "Echuwabo -(Chuwabo)"),
                   ("Cinyaja", "Cinyaja - (nyanja)"),
                   ("Cinyungwe", "Cinyungwe - ( Nyugue)"),
                   ("Cisena", "Cisena - (sena)"),
                   ("Cibalke", "Cibalke - (Balke)"),
                   ("Cimanyika", "Cimanyika - Chimanyika)"),
                   ("Cindau", "Cindau - (Ndau)"),
                   ("Ciwute", "Ciwute - (chiute)"),
                   ("Guitonga", "Guitonga"),
                   ("Citshwa", "Citshwa - (xitwa)"),
                   ("Cicope", "Cicope -(shope)"),
                   ("Xichangana", "Xichangana - (changana)"),
                   ("Xirhonga", "Xirhonga -(ronga)"),
                   ("Kiswahili", "Kiswahili - (swahili)"),
                   ("Isizulo", "Isizulo - (zulo)"),
                   ("Siswati", "Siswati - (swati)"),
                   ("Chewa", "Chewa - (Chichewa)")
                   ],
        help="Type is used to separate Languages"
    )
    victim_relationship = fields.Selection(
        string='Relação com a(s) Vítima(s):',
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
    # TODO: Create new contact for each callee on contacts app?
    fullname = fields.Char(string="Nome Completo")
    contact = fields.Char(string="Contacto", widget="phone_raw",
                          size=13, min_length=9, default="+258")
    alternate_contact = fields.Char(
        string="Contacto Alternativo", widget="phone_raw", size=13, min_length=9, default="+258")
    wants_to_be_annonymous = fields.Boolean(
        "Consetimento Informado", default=True)
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
    nr_identication = fields.Char(string="Número de Identificação")
    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Província")
    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', string="Districto")  # ,
    #    domain=lambda self: [('provincia', '=', self._compute_allowed_distrito_values())])
    bairro = fields.Char(string="Bairro")
    gender = fields.Selection(
        string='Sexo',
        selection=[
            ("male", "Masculino"),
            ("female", "Feminino"),
            ("other", "Desconhecido"),
        ],
        help="Sexo"
    )
    age = fields.Selection([(str(i), str(i)) for i in range(6, 70)] + [('70+', '70+')],
                           string='Idade')
    on_school = fields.Boolean("Estuda?")
    grade = fields.Selection([(str(i), str(i)) for i in range(0, 12)]
                             + [('Ensino Superior', 'Ensino Superior')],
                             string='Classe')
    school = fields.Char(string="Escola")
    call_start = fields.Datetime(string='Hora de início da chamada',
                                 default=fields.Datetime.now, readonly=True)
    call_end = fields.Datetime(
        string='Hora de fim da chamada', readonly=False)
    detailed_description = fields.Html(string='Descrição detalhada', attrs={
                                       'style': 'height: 500px;'}, required=False)
    how_knows_lfc = fields.Selection(
        string='Como conhece a LFC',
        selection=[
            ("Redes Sociais", "Redes Sociais"),
            ("Rádio", "Rádio"),
            ("Internet", "Internet"),
            ("Televisão", "Televisão"),
            ("Brochuras", "Brochuras"),
            ("Panfletos", "Panfletos"),
            ("Cartazes", "Cartazes"),
            ("Outros", "Outros")
        ],
        help="Como conhece a LFC"
    )

    subcategory = fields.Many2one(
        comodel_name='linhafala.subcategoria', string="Tipo de Intervençäo/Motivo")
    callcaseassistance_status = fields.Selection(
        string='Estado',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido", "Assistido"),
            ("Encerrado", "Encerrado")
        ],
        help="Estado"
    )

    @api.constrains('callcaseassistance_status')
    def _check_callcaseassistance_status(self):
        for record in self:
            if record.callcaseassistance_status != 'Aberto/Pendente' and record.callcaseassistance_status != 'Dentro do sistema' and record.callcaseassistance_status != 'Assistido' and record.callcaseassistance_status != 'Encerrado':
                raise ValidationError(
                    "Por favor, selecione o estado da chamada para prosseguir.")

    reporter = fields.Many2one(
        'res.users', string='Gestor', default=lambda self: self.env.user, readonly=True)
    created_at = fields.Datetime(
        string='Data de criaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    updated_at = fields.Datetime(string='Data de actualizaçäo',
                                 default=lambda self: fields.Datetime.now(), readonly=True)
    created_by = fields.Many2one(
        'res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)
    is_deleted = fields.Boolean(string='Apagado', default=False, readonly=True)
    uuid = fields.Char(string='UUID', readonly=True)
    case_line_ids = fields.One2many('linhafala.caso', 'call_id',
                                    string="Linhas de Casos")
    assistance_line_ids = fields.One2many('linhafala.chamada.assistance', 'call_id',
                                          string="Linhas de Assistências")

    moz_learning_line_ids = fields.One2many('linhafala.moz_learning', 'call_id',
                                            string="Linhas do Moz Learning")
    
    deficiency_line_calls_ids = fields.One2many('linhafala.deficiente', 'call_id',
                                            string="Linhas do Deficiênte")

    _sql_constraints = [
        ('unique_call_id', 'unique(call_id)', 'The call_id must be unique'),
    ]

    def write(self, vals):
        if vals:
            vals['updated_at'] = fields.Datetime.now()
        return super(Chamada, self).write(vals)

    def unlink(self):
        for record in self:
            record.write({'is_deleted': True})
        return super(Chamada, self).unlink()

    @api.model
    def create(self, vals):
        vals['uuid'] = str(uuid.uuid4())
        return super(Chamada, self).create(vals)

    @api.model
    def create(self, vals):
        if vals.get('call_id', '/') == '/':
            vals['call_id'] = self.env['ir.sequence'].next_by_code(
                'linhafala.chamada.call_id.seq') or '/'
        return super(Chamada, self).create(vals)
    
    @api.constrains('caller_language', 'distrito', 'provincia', 'call_start','call_end', 'on_school', 'gender', 'detailed_description')
    def _check_all(self):
        for record in self:
            if not record.caller_language or not record.distrito or not record.provincia or not record.call_start or not record.call_end or not record.on_school or not record.gender or not record.detailed_description:
                raise ValidationError("Por favor, preencha os campos de caracter obrigatorio.")

    def action_confirm(self):
        self.callcaseassistance_status = 'Aberto/Pendente'

    def action_done(self):
        self.callcaseassistance_status = 'Assistido'

    def action_draft(self):
        self.callcaseassistance_status = 'Dentro do sistema'

    def action_cancel(self):
        self.callcaseassistance_status = 'Encerrado'

    def action_shutdown(self):
        self.category = 1

    def action_silent(self):
        self.category = 1

    # TODO: Change the domain option to match non deprecated docs
    # def _compute_allowed_distrito_values(self):
    #     for record in self:
    #         # values = self.env['linhafala.distrito'].search([(('provincia', '=', record.provincia.id))])
    #         # record.allowed_distrito_values = values
    #         return record.provincia.id

    def create_a_new_case(self):
        new_related_model = self.env['linhafala.caso'].create(
            {'call_id': self.id})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'linhafala.caso',
            'view_mode': 'form',
            'res_id': new_related_model.id,
            'target': 'current',
        }

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}

    # TODO: Review cascade select or remove this field, replacing with buttons as with the current app workflow
    @api.onchange('category')
    def _category_onchange(self):
        # Restrict the Subcategories to the current category.
        for rec in self:
            return {'value': {'subcategory': False}, 'domain': {'subcategory': [('categoria_id', '=', rec.category.id)]}}

    @api.model
    def _register_hook(self):
        # Register the new sequence
        seq = self.env['ir.sequence'].create({
            'name': 'Linha Fala Chamadas Call ID Sequence',
            'code': 'linhafala.chamada.call_id.seq',
            'prefix': 'LFC-',
            'padding': 4,
        })
        return super(Chamada, self)._register_hook()

# Override the Delete button action
# TODO: Validate whether the function works


class ActWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    @api.model
    def unlink(self, ids):
        model = self.env[self.res_model]
        for record in model.browse(ids):
            record.write({'is_deleted': True})
        return {'type': 'ir.actions.act_window_close'}

# @api.model
# def get_action_views(self):
#     res = super(Chamada, self).get_action_views()
#     form_view_id = self.env.ref('linhafala.chamada.call_form_view').id
#     # kanban_view_id = self.env.ref('my_module.my_model_kanban_view').id
#     res.update({
#         'form': {'view_id': form_view_id, 'view_mode': 'form'},
#         # 'kanban': {'view_id': kanban_view_id, 'view_mode': 'kanban'},
#     })
#     return res


class CallCaseAssistenceCategory(models.Model):
    _name = "linhafala.chamada.assistance.categoria"
    _description = "Categoria de Assistências"

    name = fields.Char(string="Categoria")


class CasoSubcategoria(models.Model):
    _name = "linhafala.chamada.assistance.subcategoria"
    _description = "Subcategoria de Assistências"

    name = fields.Char(string="Nome da Subcategoria")
    parent_category = fields.Many2one(
        "linhafala.chamada.assistance.categoria", string="Categoria do caso")


class CallCaseAssistance(models.Model):
    _name = "linhafala.chamada.assistance"
    _description = "Formulário de Assistências linha fala criança"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]

    assistance_id = fields.Char(string="Assistência No.", readonly=True)
    call_id = fields.Many2one(
        comodel_name='linhafala.chamada', string="Chamada")
    fullname = fields.Char(string="Benificiário")
    contact = fields.Char(string="Contacto", widget="phone_raw",
                          size=13, min_length=9, default="+258")
    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Provincia")
    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', string="Districto")  # ,
    #    domain=lambda self: [('provincia', '=', self._compute_allowed_distrito_values())])
    bairro = fields.Char(string="Bairro")
    gender = fields.Selection(
        string='Sexo',
        selection=[
            ("male", "Masculino"),
            ("female", "Feminino"),
            ("other", "Desconhecido"),
        ],
        help="Sexo"
    )

    age = fields.Selection([(str(i), str(i)) for i in range(6, 70)] + [('70+', '70+')],
                           string='Idade')
    detailed_description = fields.Html(string='Descrição detalhada', attrs={
                                       'style': 'height: 500px;'}, required=False)
    category = fields.Many2one(
        comodel_name='linhafala.chamada.assistance.categoria', string="Categoria")
    subcategory = fields.Many2one(
        comodel_name='linhafala.chamada.assistance.subcategoria', string="Subcategoria")
    callcaseassistance_status = fields.Selection(
        string='Estado',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido", "Assistido"),
            ("Encerrado", "Encerrado")
        ],
        help="Estado"
    )

    @api.constrains('callcaseassistance_status')
    def _check_callcaseassistance_status(self):
        for record in self:
            if record.callcaseassistance_status != 'Aberto/Pendente' and record.callcaseassistance_status != 'Dentro do sistema' and record.callcaseassistance_status != 'Assistido' and record.callcaseassistance_status != 'Encerrado':
                raise ValidationError(
                    "Por favor, selecione o estado da Assistência para prosseguir.")

    callcaseassistance_priority = fields.Selection(
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
        string='Tratamento',
        selection=[
            ("Aconselhamento LFC", "Aconselhamento LFC"),
            ("Encaminhado", "Encaminhado"),
            ("Não encaminhado", "Não encaminhado"),
        ],
        default="Aconselhamento LFC",
        help="Tratamento"
    )
    reporter = fields.Many2one(
        'res.users', string='Gestor', default=lambda self: self.env.user, readonly=True)
    created_at = fields.Datetime(
        string='Data de criaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    updated_at = fields.Datetime(string='Data de actualizaçäo',
                                 default=lambda self: fields.Datetime.now(), readonly=True)
    created_by = fields.Many2one(
        'res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)
    is_deleted = fields.Boolean(string='Apagado', default=False, readonly=True)
    uuid = fields.Char(string='UUID', readonly=True)
    assistance_referral_line_ids = fields.One2many('linhafala.chamada.assistance.referral', 'assistance_id',
                                                   string="Linhas de Referências de Assistências")

    _sql_constraints = [
        ('unique_assistance_id', 'unique(assistance_id)',
         'The assistance id must be unique'),
    ]

    def write(self, vals):
        if vals:
            vals['updated_at'] = fields.Datetime.now()
        return super(CallCaseAssistance, self).write(vals)

    @api.model
    def create(self, vals):
        vals['uuid'] = str(uuid.uuid4())
        return super(CallCaseAssistance, self).create(vals)

    @api.model
    def create(self, vals):
        if vals.get('assistance_id', '/') == '/':
            vals['assistance_id'] = self.env['ir.sequence'].next_by_code(
                'linhafala.chamada.assistance_id.seq') or '/'
        return super(CallCaseAssistance, self).create(vals)

    @api.constrains('distrito', 'provincia', 'category','subcategory', 'callcaseassistance_priority', 'detailed_description')
    def _check_all(self):
        for record in self:
            if not record.distrito or not record.provincia or not record.category or not record.subcategory or not record.callcaseassistance_priority or not record.detailed_description:
                raise ValidationError("Por favor, preencha os campos de caracter obrigatorio.")


    def action_confirm(self):
        self.callcaseassistance_status = 'Aberto/Pendente'

    def action_done(self):
        self.callcaseassistance_status = 'Assistido'

    def action_draft(self):
        self.callcaseassistance_status = 'Dentro do sistema'

    def action_cancel(self):
        self.callcaseassistance_status = 'Encerrado'

    @api.model
    def _register_hook(self):
        # Register the new sequence
        seq = self.env['ir.sequence'].create({
            'name': 'Linha Fala Chamadas Assistance ID Sequence',
            'code': 'linhafala.chamada.assistance_id.seq',
            'prefix': 'LFC-Assist-',
            'padding': 4,
        })
        return super(CallCaseAssistance, self)._register_hook()


class AssistanceReferall(models.Model):
    _name = "linhafala.chamada.assistance.referral"
    _description = "Instituição de encaminhamento de assistência"

    # add the possibility to add more than one victim , perpetrator and reference age
    # person_id = fields.Many2one('linhafala.person_involved')

    # case_id = models.ManyToManyField('linhafala.caso')
    # refEnt_id = models.ManyToManyField('linhafala.caso.referenceentity')

    assistance_id = fields.Many2one(
        "linhafala.chamada.assistance", string="Assistência")
    area_type = fields.Selection(
        string='Área de Encaminhamento',
        selection=[
            ("Institucional", "Institucional"),
            ("Não Institucional", "Não Institucional"),
        ],
        help="Área de Encaminhamento"
    )
    reference_area = fields.Many2one(
        comodel_name='linhafala.caso.referencearea', string="Área de Referência")
    reference_entity = fields.Many2one(
        comodel_name='linhafala.caso.referenceentity', string="Entidade de Referência")

    case_reference = fields.Many2one(
        comodel_name='linhafala.caso.casereference', string="Pessoa de Contacto")

    spokes_person_phone = fields.Char(
        string="Telefone do Responsável", related='case_reference.contact')
    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Provincia")
    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', string="Districto")
    assistance_status = fields.Selection(
        string='Estado do caso',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido", "Assistido"),
            ("Encerrado", "Encerrado"),
        ],
        help="Estado do caso"
    )

    @api.constrains('assistance_status')
    def _check_assistance_status(self):
        for record in self:
            if record.assistance_status != 'Aberto/Pendente' and record.assistance_status != 'Dentro do sistema' and record.assistance_status != 'Assistido' and record.assistance_status != 'Encerrado':
                raise ValidationError(
                    "Por favor, selecione o estado do caso para prosseguir.")
