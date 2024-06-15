from xml.dom import ValidationErr
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import uuid


class PersonInvolved(models.Model):
    _name = "linhafala.person_involved"
    _description = "Person Involved Lines"

    person_id = fields.Char(string="ID person_involved", readonly=True)

    moz_learning_id = fields.Many2one(
        comodel_name='linhafala.moz_learning', string="Moz Learning")

    fullname = fields.Char(string="Nome completo")

    address = fields.Char(string="Endereço da Vítima", email=True)

    email = fields.Char(string="Endereço Eletronico")

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
    
    person_type = fields.Selection(
        string='Categoria',
        selection=[
            ("Contactante", "Contactante"),
            ("Contactante+Vítima", "Contactante+Vítima"),
            ("Vítima", "Vítima"),
            ("Perpetrador", "Perpetrador"),
        ],
        help="Categoria",
    )

    perpetrator_age = fields.Selection([(str(i), str(i)) for i in range(16, 65)] + [('65+', '65+')],
                           string='Idade do perpetrador')
    
    perpetrator_gender = fields.Selection(

        string='Sexo do Perpetrator',
        selection=[
            ("Masculino", "Masculino"),
            ("Feminino", "Feminino"),
        ],
        help="Sexo"
    )
    
    @api.onchange('person_type')
    def _onchange_person_type(self):
        if self.person_type == 'Perpetrador':
            self.age = False  # Hide the "Idade" field
        else:
            self.age = False  # Show the "Idade" field

    created_at = fields.Datetime(
        string='Data de criaçäo', default=lambda self: fields.Datetime.now(), readonly=True)

    contact = fields.Char(string="Contacto", widget="phone_raw",
                          size=13, min_length=9, default="+258")

    alternate_contact = fields.Char(string="Contacto Alternativo")
    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Provincia", help="Provincia", required=True)

    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', 
        string="Distrito", 
        help="Distrito",
        required=True,
        domain="[('provincia', '=', provincia)]")

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}
        
    posto = fields.Many2one(
        comodel_name="linhafala.posto", string="Posto",
        domain="[('distrito', '=', distrito)]"
        )

    localidade = fields.Many2one(
        comodel_name='linhafala.localidade', string="Localidade",
        domain="[('posto', '=', posto)]"
        )
    
    @api.onchange('distrito')
    def _distrito_onchange(self):
        for rec in self:
            return {'value': {'posto': False}, 'domain': {'posto': [('distrito', '=', rec.distrito.id)]}}

    @api.onchange('posto')
    def _posto_onchange(self):
        for rec in self:
            return {'value': {'localidade': False}, 'domain': {'localidade': [('posto', '=', rec.posto.id)]}}
        
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
            ("Pai", "Pai"),
            ("Mãe", "Mãe"),
            ("Avo", "Avo"),
            ("Amigo", "Amigo"),
            ("Outros", "Outros"),
            ("Colega", "Colega"),
            ("Esposo", "Esposo"),
            ("Tio(a)", "Tio(a)"),
            ("Nenhuma", "Nenhuma"),
            ("Mentora", "Mentora"),
            ("Irmã(o)", "Irmã(o)"),
            ("Primo(a)", "Primo(a)"),
            ("Namorado", "Namorado"),
            ("Madrasta", "Madrasta"),
            ("Padrasto", "Padrasto"),
            ("Empregador", "Empregador"),
            ("Vizinho (a)", "Vizinho (a)"),
            ("Denunciante", "Denunciante"),
            ("Educador(a)", "Educador(a)"),
            ("Professor(a)", "Professor(a)"),
            ("Não aplicavél", "Não aplicavél"),
        ],
        help="Relação com a(s) vítima(s):"
    )
    gender = fields.Selection(
        string='Sexo',
        selection=[
            ("Masculino", "Masculino"),
            ("Feminino", "Feminino"),
        ],
        help="Sexo"
    )
    what_other = fields.Char(string="Qual Outro")
    age = fields.Selection([('0-6 meses', '0-6 meses')] + [('7-11 meses', '7-11 meses')] + [(str(i), str(i)) for i in range(1, 25)] + [('25+', '25+')],
                           string='Idade')                        
    on_school = fields.Boolean("Estuda?")
    grade = fields.Selection([(str(i), str(i)) for i in range(0, 12)]
                             + [('Ensino Superior', 'Ensino Superior')],
                             string='Classe')
    case_id = fields.Many2one("linhafala.caso", string="Caso")

    are_you_disabled = fields.Selection(
        string="E deficiente?",
        selection=[
            ("Sim", "Sim"),
            ("Não", "Não"),
        ],
        help="E deficiente?",
    )

    deficiency_line_calls_ids = fields.One2many('linhafala.deficiente', 'person_id',
                                                string="Linhas do Deficiênte")

    
    @api.constrains('provincia','distrito','victim_relationship')
    def _check_all(self):
        for record in self:
            if not record.provincia:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Provincia")
            if not record.distrito:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Distrito")
            if not record.victim_relationship:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio  Relação com a(s) vítima(s)")