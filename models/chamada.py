from odoo import api, fields, models
import uuid

class Chamada(models.Model):
    _name = "linhafala.chamada"
    _description = "Formulário de chamadas linha fala criança"
    _inherit = [
        'mail.thread', 
        'mail.activity.mixin'
        ]

    call_id = fields.Char(string="Id da chamada", readonly=True)
    contact_type = fields.Selection(
        string='Tipo de contacto',
        selection=[
            ("SMS BIZ", "SMS BIZ"),
            ("LInha Verde 1458", "LInha Verde 1458"),
            ("Não definido", "Não definido"),
            ("Presencial", "Presencial"),
            ("Telefónica", "Telefónica"),
            ("Email", "Email"),
            ("Redes Sociais", "Redes Sociais"),
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
        help="Type is used to separate Languages", required=True
    )
    fullname = fields.Char(string="Nome completo") # TODO: Create new contact for each callee on contacts app?
    contact = fields.Char(string="Contacto") 
    alternate_contact  = fields.Char(string="Contacto Alternativo") 
    wants_to_be_annonymous = fields.Boolean("Deja permanecer Anónimo")
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
    provincia = fields.Many2one(comodel_name='linhafala.provincia', string="Provincia", required=True)
    distrito = fields.Many2one(comodel_name='linhafala.distrito', string="Districto", required=True) #,
                            #    domain=lambda self: [('provincia', '=', self._compute_allowed_distrito_values())])
    bairro = fields.Char(string="Bairro")
    gender = fields.Selection(
        string='Sexo',
        selection=[
            ("male", "Masculino"),
            ("female", "Feminino"),
            ("other", "Desconhecido"),
        ],
        help="Sexo", required=True
    )
    age = fields.Selection([(str(i), str(i)) for i in range(6, 81)]  + [('81+', '81+')],
                                    string='Idade')
    on_school = fields.Boolean("Estuda?")
    grade = fields.Selection([(str(i), str(i)) for i in range(0, 12)]  
                             + [('Ensino Superior', 'Ensino Superior')],
                                    string='Classe')
    school = fields.Char(string="Escola", required=True) 
    call_start = fields.Datetime(string='Hora de início da chamada', default=fields.Datetime.now, readonly=True, required=True)
    call_end = fields.Datetime(string='Hora de fim da chamada', readonly=False, required=True)
    detailed_description = fields.Html(string='Descrição detalhada', attrs={'style': 'height: 500px;'}, required=True)
    how_knows_lfc = fields.Selection(
        string='Como conhece a LFC',
        selection=[
            ("Redes Sociais", "Redes Sociais"),
            ("Rádio", "Rádio"),
            ("Internet", "Internet"),
            ("Televisão", "Televisão"),
            ("Brochuras","Brochuras"),
            ("Panfletos", "Panfletos"),
            ("Cartazes","Cartazes"),
            ("Outros","Outros")
        ],
        help="Como conhece a LFC"
    )
    category = fields.Many2one(comodel_name='linhafala.categoria', string="Categoria", required=True)
    subcategory = fields.Many2one(comodel_name='linhafala.subcategoria', string="Tipo de Intervençäo/Motivo", required=True)
    callcaseassistance_status = fields.Selection(
        string='Estado',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido","Assistido"),
            ("Encerrado", "Encerrado")
        ],
        default="Aberto/Pendente",
        help="Estado", required=True
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
    reporter = fields.Many2one('res.users', string='Gestor', default=lambda self: self.env.user, readonly=True)
    created_at = fields.Datetime(string='Data de criaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    updated_at = fields.Datetime(string='Data de actualizaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    created_by = fields.Many2one('res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)
    is_deleted = fields.Boolean(string='Apagado', default=False, readonly=True)
    uuid = fields.Char(string='UUID', readonly=True)
    case_line_ids = fields.One2many('linhafala.caso', 'call_id',
                                                string="Linhas de Casos")
    assistance_line_ids = fields.One2many('linhafala.chamada.assistance', 'call_id',
                                                string="Linhas de Assistências")

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
            vals['call_id'] = self.env['ir.sequence'].next_by_code('linhafala.chamada.call_id.seq') or '/'
        return super(Chamada, self).create(vals)
    
    def action_confirm(self):
        self.callcaseassistance_status = 'Aberto/Pendente'

    def action_done(self):
        self.callcaseassistance_status = 'Assistido'

    def action_draft(self):
        self.callcaseassistance_status = 'Dentro do sistema'

    def action_cancel(self):
        self.callcaseassistance_status = 'Encerrado'

    # TODO: Change the domain option to match non deprecated docs
    # def _compute_allowed_distrito_values(self):
    #     for record in self:
    #         # values = self.env['linhafala.distrito'].search([(('provincia', '=', record.provincia.id))])
    #         # record.allowed_distrito_values = values
    #         return record.provincia.id
    

    def create_a_new_case(self):
        new_related_model = self.env['linhafala.caso'].create({'call_id': self.id})
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

    name = fields.Char(string="Categoria", required=True)

class CasoSubcategoria(models.Model):
    _name = "linhafala.chamada.assistance.subcategoria"
    _description = "Subcategoria de Assistências"

    name = fields.Char(string="Nome da Subcategoria", required=True)
    parent_category = fields.Many2one("linhafala.chamada.assistance.categoria", string="Categoria do caso", required=True)

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
    contact = fields.Char(string="Contacto") 
    provincia = fields.Many2one(comodel_name='linhafala.provincia', string="Provincia", required=True)
    distrito = fields.Many2one(comodel_name='linhafala.distrito', string="Districto", required=True) #,
                            #    domain=lambda self: [('provincia', '=', self._compute_allowed_distrito_values())])
    bairro = fields.Char(string="Bairro")
    gender = fields.Selection(
        string='Sexo',
        selection=[
            ("male", "Masculino"),
            ("female", "Feminino"),
            ("other", "Desconhecido"),
        ],
        help="Sexo", required=True
    )
    age = fields.Selection([(str(i), str(i)) for i in range(6, 81)]  + [('81+', '81+')],
                                    string='Idade')
    detailed_description = fields.Html(string='Descrição detalhada', attrs={'style': 'height: 500px;'}, required=True)
    category = fields.Many2one(comodel_name='linhafala.chamada.assistance.categoria', string="Categoria", required=True)
    subcategory = fields.Many2one(comodel_name='linhafala.chamada.assistance.subcategoria', string="Subcategoria", required=True)
    callcaseassistance_status = fields.Selection(
        string='Estado',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido","Assistido"),
            ("Encerrado", "Encerrado")
        ],
        default="Aberto/Pendente",
        help="Estado", required=True
    )
    callcaseassistance_priority = fields.Selection(
        string='Período de Resolução',
        selection=[
            ("Muito Urgente", "Muito Urgente"),
            ("Urgente", "Urgente"),
            ("Moderado", "Moderado"),
            ("Não Aplicável", "Não Aplicável"),
        ],
        default="Moderado",
        help="Período de Resolução", required=True
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
    reporter = fields.Many2one('res.users', string='Gestor', default=lambda self: self.env.user, readonly=True)
    created_at = fields.Datetime(string='Data de criaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    updated_at = fields.Datetime(string='Data de actualizaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    created_by = fields.Many2one('res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)
    is_deleted = fields.Boolean(string='Apagado', default=False, readonly=True)
    uuid = fields.Char(string='UUID', readonly=True)
    assistance_referral_line_ids = fields.One2many('linhafala.chamada.assistance.referral', 'assistance_id',
                                                string="Linhas de Referências de Assistências")

    _sql_constraints = [
        ('unique_assistance_id', 'unique(assistance_id)', 'The assistance id must be unique'),
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
            vals['assistance_id'] = self.env['ir.sequence'].next_by_code('linhafala.chamada.assistance_id.seq') or '/'
        return super(CallCaseAssistance, self).create(vals)
    
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

    assistance_id = fields.Many2one("linhafala.chamada.assistance", string="Assistência")
    area_type = fields.Selection(
        string='Tipo de Área',
        selection=[
            ("Institucional", "Institucional"),
            ("Não Institucional", "Não Institucional"),
        ],
        help="Tipo de Área"
    )
    reference_area = fields.Many2one(
        comodel_name='linhafala.caso.referencearea', string="Área de Referência")
    reference_entity = fields.Many2one(
        comodel_name='linhafala.caso.referenceentity', string="Entidade de Referência")
    case_reference = fields.Many2one(
        comodel_name='linhafala.caso.casereference', string="Pessoa de Contacto")
    spokes_person = fields.Char(string="Pessoa de Responsável", required=True)
    spokes_person_phone = fields.Char(string="Telefone do Responsável")
    assistance_status = fields.Selection(
        string='Estado do caso',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido", "Assistido"),
            ("Encerrado", "Encerrado")
        ],
        help="Estado do caso", required=True
    )
