from odoo import api, fields, models
from odoo.exceptions import UserError
import uuid

class Caso(models.Model):
    _name = "linhafala.caso"
    _description = "Formulário de Caso linha fala criança"
    _inherit = [
        'mail.thread', 
        'mail.activity.mixin'
        ]
    
    case_id = fields.Char(string="Id do caso", readonly=True)
    call_id = fields.Many2one(comodel_name='linhafala.chamada', string="Chamada")
    case_status = fields.Selection(
        string='Estado do caso',
        selection=[
            ("Encerrado", "Encerrado"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("No Arquivo Morto", "No Arquivo Morto"),
            ("Assistido","Assistido")
        ],
        help="Estado do caso"
    )
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
        string='Período de Resolução',
        selection=[
            ("Aconselhamento LFC", "Aconselhamento LFC"),
            ("Encaminhado", "Encaminhado"),
            ("Não encaminhado", "Não encaminhado"),
        ],
        default="Aconselhamento LFC",
        help="Tratamento do caso"
    )
    place_occurrence = fields.Selection(
        string='Período de Resolução',
        selection=[
            ("Escola", "Escola"),
            ("Casa de parente / vizinho", "Casa de parente / vizinho"),
            ("Casa propria", "Casa propria"),
            ("Instituição", "Instituição"),
            ("Outros", "Outros")
        ],
        default="Escola",
        help="Local de Ocorrencia"
    )
    detailed_description = fields.Html(string='Descrição detalhada', attrs={'style': 'height: 500px;'})
    case_type = fields.Many2one(comodel_name='linhafala.caso.categoria', string="Categoria")
    secundary_case_type = fields.Many2one(comodel_name='linhafala.caso.subcategoria', string="Subcategoria")
    case_type_classification = fields.Many2one(comodel_name='linhafala.caso.case_type_classification', string="Classificaçäo Provisória")


    reporter_by = fields.Many2one('res.users', string='Gestão', default=lambda self: self.env.user, readonly=True)
    created_at = fields.Datetime(string='Data de criaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    updated_at = fields.Datetime(string='Data de actualizaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    created_by = fields.Many2one('res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)
    is_deleted = fields.Boolean(string='Apagado', default=False, readonly=True)
    uuid = fields.Char(string='UUID', readonly=True)
    is_locked = fields.Boolean(string='Is Locked', default=False)
    lock_date = fields.Datetime()


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
            vals['case_id'] = self.env['ir.sequence'].next_by_code('linhafala.chamada.case_id.seq') or '/'
        return super(Caso, self).create(vals)
    
    # Lock the case for single user edit
    # TODO: Check and fix that a record gets created and managed by a single user!
    @api.model
    def create(self, vals):
        # Set the user_id to the current user
        vals['user_id'] = self.env.user.id
        return super(Caso, self).create(vals)
    
    def write(self, vals):
        if 'is_locked' in vals:
            # Check if the record is already locked by someone else
            if self.is_locked and self.user_id != self.env.user:
                raise UserError('This record is locked by {}.'.format(self.user_id.name))
            
            # Set the lock_date and user_id fields when the record is locked
            if vals['is_locked']:
                vals['lock_date'] = fields.Datetime.now()
                vals['user_id'] = self.env.user.id
                
            # Unlock the record when is_locked is set to False
            else:
                vals['lock_date'] = False
                vals['user_id'] = False
                
        return super(Caso, self).write(vals)
    
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
