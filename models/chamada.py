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

    are_you_disabled = fields.Selection(
        string="E deficiente?",
        selection=[
            ("Sim", "Sim"),
            ("Não", "Não"),
        ],
        help="E deficiente?",
    )

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
            ("Pai", "Pai"),
            ("Mãe", "Mãe"),
            ("Avo", "Avo"),
            ("Amigo", "Amigo"),
            ("Esposo", "Esposo"),
            ("Outros", "Outros"),
            ("Tio(a)", "Tio(a)"),
            ("Colega", "Colega"),
            ("Mentora", "Mentora"),
            ("Nenhuma", "Nenhuma"),
            ("Irmã(o)", "Irmã(o)"),
            ("Madrasta", "Madrasta"),
            ("Padrasto", "Padrasto"),
            ("Primo(a)", "Primo(a)"),
            ("Namorado", "Namorado"),
            ("Sobrinho", "Sobrinho"),
            ("Ativista", "Ativista"),
            ("Cunhado/a", "Cunhado/a"),
            ("Paralegal", "Paralegal"),
            ("Empregador", "Empregador"),
            ("Ponto Focal", "Ponto Focal"),
            ("Vizinho (a)", "Vizinho (a)"),
            ("Educador(a)", "Educador(a)"),
            ("Professor(a)", "Professor(a)"),
            ("Membro da PRM", "Membro da PRM"),
            ("Lider relegioso", "Lider relegioso"),
            ("líder cumunitario", "líder cumunitario"),
        ],
        help="Relação com a(s) vítima(s):"
    )

    category_status = fields.Many2one(
        comodel_name='linhafala.categoria', string="Categoria", default=lambda self: self.env['linhafala.categoria'].browse(2))

    #def action_shutdown(self):
        #self.category_status = "Sem Interveção"
        #self.env['linhafala.chamada'].browse(self.id).write(
            #{'category_status': 'Sem Interveção'})

    #def action_silent(self):
        #self.category_status = "Sem Interveção"
        #self.env['linhafala.chamada'].browse(self.id).write(
            #{'category_status': 'Sem Interveção'})

    #category_status = fields.Selection(
       #string='Estado da chamada',
        #selection=[
            #("Sem Interveção Silencio", "Silencio"),
            #("Sem Interveção Desligado", "Desligado"),
            #("Com Interveção", "Com Interveção"),
        #],
        #default="Com Interveção",
        #help="Categoria",
    #)

    _skip_validation = fields.Boolean(string="Skip Validation")


    def action_shutdown(self):
        self._skip_validation = True
        self.category_status = 1

    def action_silent(self):
        self._skip_validation = True
        self.category_status = 1

    category_calls = fields.Selection(
        string='Categoria',
        selection=[
            ("Contactante", "Contactante"),
            ("Contactante+Vítima", "Contactante+Vítima"),
        ],
        help="Categoria",
    )

    # TODO: Create new contact for each callee on contacts app?
    fullname = fields.Char(string="Nome Completo")
    contact = fields.Char(string="Contacto", widget="phone_raw",
                          size=13, min_length=9, default="+258")
    alternate_contact = fields.Char(
        string="Contacto Alternativo", widget="phone_raw", size=13, min_length=9, default="+258")
    wants_to_be_annonymous = fields.Selection(
        string='Consentimento Informado',
        selection=[
            ("Sim", "Sim"),
            ("Não", "Não"),
        ],
        default = "Sim",
        help="Consentimento Informado",
    )

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
            ("Masculino", "Masculino"),
            ("Feminino", "Feminino"),
            ("Desconhecido", "Desconhecido"),
        ],
        help="Sexo"
    )
    age = fields.Selection([(str(i), str(i)) for i in range(6, 70)] + [('70+', '70+')],
                           string='Idade')
    on_school = fields.Selection(
        string='Estuda?',
        selection=[
            ("Sim", "Sim"),
            ("Não", "Não"),
        ],
        help="Estuda?"
    )
    grade = fields.Selection([('Pre Escolar', 'Pre Escolar')] + [(str(i), str(i)) for i in range(1, 13)] + [('Ensino Superior', 'Ensino Superior')],
                             string='Qual a Classe ?:')
    school = fields.Char(string="Escola", default=False)
    call_start = fields.Datetime(string='Hora de início da chamada',
                                 default=fields.Datetime.now, readonly=True)
    call_end = fields.Datetime(
        string='Hora de fim da chamada', readonly=False)
    detailed_description = fields.Html(string='Descrição detalhada', attrs={
                                       'style': 'height: 500px;'})
    how_knows_lfc = fields.Selection(
        string='Como conhece a LFC',
        selection=[
            ("Redes Sociais", "Redes Sociais"),
            ("Rádio", "Rádio"),
            ("Internet", "Internet"),
            ("Palestras", "Palestras"),
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
    
    def _onchange_type_of_intervention(self):
        if self.type_of_intervention == 'Caso' or 'Chamada de Assistência':
            self.case_line_ids = [(0, 0, {})]  # Create an empty record
            self.assistance_line_ids = [(0, 0, {})]
        else:
            self.case_line_ids = [(5, 0, 0)]  # Remove all records
            self.assistance_line_ids = [(5, 0, 0)]

    @api.constrains('type_of_intervention')
    def _check_type_of_intervention(self):
        for record in self:
            if record.type_of_intervention == 'Caso' and not record.case_line_ids:
                raise ValidationError("Para guardar um caso é necessário que tenha pelo menos uma vítima, por favor preencha todos os campos do formulário de Caso(s) Relacionados.")
            if record.type_of_intervention == 'Chamada de Assistência' and not record.assistance_line_ids:
                raise ValidationError("Para gravar uma chamada de Assistência é necessário preencher o formulário de Assistências Relacionados.")


    assistance_line_ids = fields.One2many('linhafala.chamada.assistance', 'call_id',
                                          string="Linhas de Assistências")

    moz_learning_line_ids = fields.One2many('linhafala.moz_learning', 'call_id',
                                            string="Linhas do Moz Learning")

    deficiency_line_calls_ids = fields.One2many('linhafala.deficiente', 'call_id',
                                                string="Linhas do Deficiênte")

    _sql_constraints = [
        ('unique_call_id', 'unique(call_id)', 'The call_id must be unique'),
    ]

    def unlink(self):
        for record in self:
            record.write({'is_deleted': True})
        return super(Chamada, self).unlink()

    @api.model
    def create(self, vals):
        vals['uuid'] = str(uuid.uuid4())
        self.action_notification()
        return super(Chamada, self).create(vals)

    def action_notification(self):
        self.save({})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Informação gravada com sucesso!!',
                'type': 'success',
                'sticky': False,
            },
        }

    @api.model
    def create(self, vals):
        if vals.get('call_id', '/') == '/':
            next_call_id = self.env['ir.sequence'].next_by_code('linhafala.chamada.call_id.seq') or '/'
            vals['call_id'] = next_call_id.split('-')[-1]
        return super(Chamada, self).create(vals)

    @api.constrains('caller_language', 'how_knows_lfc', 'distrito', 'provincia', 'call_end', 'detailed_description','are_you_disabled','category_status','type_of_intervention','category_calls','on_school','gender','age')
    def _check_all(self):
        for record in self:
            if self.category_status.id == 2:
                if not record._skip_validation:  # Check the flag
                    if not record.caller_language:
                        raise ValidationError("Dialeto/Lingua é um campo obrigatório.")
                    if not record.how_knows_lfc:
                        raise ValidationError("Como conhece a LFC é um campo obrigatório.")
                    if not record.distrito:
                        raise ValidationError("Distrito é um campo obrigatório.")
                    if not record.provincia:
                        raise ValidationError("Província é um campo obrigatório.")
                    if not record.call_end:
                        raise ValidationError("Fim da chamada é um campo obrigatório.")
                    if not record.detailed_description:
                        raise ValidationError("Detalhes é um campo obrigatório.")
                    if not record.are_you_disabled:
                        raise ValidationError("Tem algum tipo de dificiência ? é um campo obrigatório.")
                    if not record.type_of_intervention:
                        raise ValidationError("Tipo de Intervenção / Motivo é um campo obrigatório.")
                    if not record.category_calls:
                        raise ValidationError("Categoria é um campo obrigatório.")
                    if not record.on_school:
                        raise ValidationError("Frequenta a Escola? é um campo obrigatório.")
                    if not record.gender:
                        raise ValidationError("Género é um campo obrigatório.")
                    if not record.age:
                        raise ValidationError("Género é um campo obrigatório.")

    def action_confirm(self):
        self.callcaseassistance_status = 'Aberto/Pendente'

    def action_done(self):
        self.callcaseassistance_status = 'Assistido'

    def action_draft(self):
        self.callcaseassistance_status = 'Dentro do sistema'

    def action_cancel(self):
        self.callcaseassistance_status = 'Encerrado'

    @api.model
    def save(self, vals):
        return super(Chamada, self).write(vals)
    
    @api.model
    def edit(self, vals):
        return super(Chamada, self).write(vals)
        

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
    assistanceReferall_id = fields.One2many('linhafala.chamada.assistance.referral', 'assistance_id',
                                            string="Referall")
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
            ("Masculino", "Masculino"),
            ("Feminino", "Feminino"),
            ("Desconhecido", "Desconhecido"),
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
        ],default="Aberto/Pendente",
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
    data_ocorrencia = fields.Datetime(
        string="Data de Ocorrência", widget="datetime", date_format="%d/%m/%Y %H:%M:%S")
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
            next_assistance_id = self.env['ir.sequence'].next_by_code('linhafala.chamada.assistance_id.seq') or '/'
            vals['assistance_id'] = next_assistance_id.split('-')[-1]
        return super(CallCaseAssistance, self).create(vals)

    @api.constrains('distrito', 'provincia', 'category', 'subcategory', 'callcaseassistance_priority', 'detailed_description','age','gender')
    def _check_all(self):
        for record in self:
            if not record.distrito:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio: Distrito")
            if not record.provincia:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio: Provincia")
            if not record.category:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio: Categoria")
            if not record.subcategory:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio: Sub-categoria")
            if not record.callcaseassistance_priority:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio: Período de Resolução")
            if not record.detailed_description:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio: Detalhes")
            if not record.age:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio: Idade")
            if not record.gender:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio: Género")

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}

    @api.onchange('category')
    def _category_onchange(self):
        for rec in self:
            return {'value': {'subcategory': False}, 'domain': {'subcategory': [('parent_category', '=', rec.category.id)]}}

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
            'padding': 4,
        })
        return super(CallCaseAssistance, self)._register_hook()

    manager_by = fields.Many2one(
        'res.users', string="Gerido por: ", compute='_compute_manager_by', store=True)

    @api.depends('manager_by')
    def _compute_manager_by(self):
        for record in self:
            record.manager_by = record.env.user

    def action_manager(self):
        self._compute_manager_by()

    @api.model
    def save(self, vals):
        return super(CallCaseAssistance, self).write(vals)
    
    @api.model
    def edit(self, vals):
        return super(CallCaseAssistance, self).write(vals)


class AssistanceReferall(models.Model):
    _name = "linhafala.chamada.assistance.referral"
    _description = "Instituição de encaminhamento de assistência"

    assistanceReferall_id = fields.Char(
        string="Assistência No.", readonly=True)

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
        comodel_name='linhafala.caso.referencearea',
        string="Área de Referência",
        domain="[('area_type', '=', area_type)]"
    )
    reference_entity = fields.Many2one(
        comodel_name='linhafala.caso.referenceentity', 
        string="Entidade de Referência",
        domain="[('reference_area', '=', reference_area)]"
    )

    @api.onchange('distrito')
    def _distrito_onchange(self):
        for rec in self:
            return {'value': {'reference_entity': False}, 'domain': {'reference_entity': [('distrito', '=', rec.distrito.id)]}}


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
    assistance_status = fields.Selection(
        string='Estado do caso',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido", "Assistido"),
            ("Encerrado", "Encerrado"),
        ],default="Aberto/Pendente",
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

    @api.constrains('assistance_status')
    def _check_assistance_status(self):
        for record in self:
            if record.assistance_status != 'Aberto/Pendente' and record.assistance_status != 'Dentro do sistema' and record.assistance_status != 'Assistido' and record.assistance_status != 'Encerrado':
                raise ValidationError(
                    "Por favor, selecione o estado do caso para prosseguir.")
