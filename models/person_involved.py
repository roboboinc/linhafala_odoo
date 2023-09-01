from xml.dom import ValidationErr
from odoo import api, fields, models, _
from odoo.exceptions import UserError
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
    wants_to_be_annonymous= fields.Selection(
        string='Consentimento Informado',
        selection=[
            ("Sim", "Sim"),
            ("Não", "Não"),
        ],
        help="Consentimento Informado",
    )
    person_type = fields.Selection(
        string='Categoria',
        selection=[
            ("Contactante+Vítima", "Contactante+Vítima"),
            ("Vítima", "Vítima"),
            ("Perpetrador", "Perpetrador"),
        ],
        required=True,
        help="Categoria",
    )

    perpetrator_age = fields.Selection([(str(i), str(i)) for i in range(16, 65)] + [('65+', '65+')],
                           string='Idade do perpetrador')

    created_at = fields.Datetime(
        string='Data de criaçäo', default=lambda self: fields.Datetime.now(), readonly=True)

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
            ("Desconhecido", "Desconhecido"),
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

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}