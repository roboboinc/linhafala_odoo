from odoo import api, fields, models
import uuid

class Chamada(models.Model):
    _name = "linhafala.chamada"
    _description = "Formulário de Assistências linha fala criança"

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
        help="Type is used to separate Languages"
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
    provincia = fields.Many2one(comodel_name='linhafala.provincia', string="Provincia")
    distrito = fields.Many2one(comodel_name='linhafala.distrito', string="Districto") #,
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
    age = fields.Selection([(str(i), str(i)) for i in range(6, 81)]  + [('81+', '81+')],
                                    string='Idade')
    on_school = fields.Boolean("Estuda?")
    grade = fields.Selection([(str(i), str(i)) for i in range(0, 12)]  
                             + [('Ensino Superior', 'Ensino Superior')],
                                    string='Classe')
    school = fields.Char(string="Escola") 
    call_start = fields.Datetime(string='Hora de início da chamada', default=fields.Datetime.now, readonly=True)
    call_end = fields.Datetime(string='Hora de fim da chamada', readonly=False)
    detailed_description = fields.Html(string='Descrição detalhada', attrs={'style': 'height: 500px;'})
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
    category = fields.Many2one(comodel_name='linhafala.categoria', string="Categoria")
    subcategory = fields.Many2one(comodel_name='linhafala.subcategoria', string="Tipo de Intervençäo/Motivo")
    callcaseassistance_status = fields.Selection(
        string='Estado',
        selection=[
            ("Encerrado", "Encerrado"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Assistido","Assistido")
        ],
        default="Aberto/Pendente",
        help="Estado"
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

    # TODO: Change the domain option to match non deprecated docs
    # def _compute_allowed_distrito_values(self):
    #     for record in self:
    #         # values = self.env['linhafala.distrito'].search([(('provincia', '=', record.provincia.id))])
    #         # record.allowed_distrito_values = values
    #         return record.provincia.id
    

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}

    # TODO: Review cascade select or remove this field, replacing with buttons as with the current app workflow    
    @api.onchange('category')
    def _category_onchange(self):
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