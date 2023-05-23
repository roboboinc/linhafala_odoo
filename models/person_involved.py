from xml.dom import ValidationErr
from odoo import api, fields, models
import uuid

class PersonInvolved(models.Model):
    _name = "linhafala.person_involved"
    _description = "Person Involved Lines"

    person_id = fields.Char(string="ID person_involved", readonly=True)
    fullname = fields.Char(string="Nome completo", required=True)

    address = fields.Char(string="Endereço da Vitima")

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
        help="Categoria", required=True
    )
    contact = fields.Char(string="Contacto")
    alternate_contact = fields.Char(string="Contacto Alternativo")
    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Provincia", required=True)
    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', string="Districto", required=True)  # ,
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
            ("male", "Masculino"),
            ("female", "Feminino"),
            ("other", "Desconhecido"),
        ],
        help="Sexo", required=True
    )
    age = fields.Selection([(str(i), str(i)) for i in range(6, 99)] + [('99+', '99+')],
                           string='Idade')
    on_school = fields.Boolean("Estuda?")
    grade = fields.Selection([(str(i), str(i)) for i in range(0, 12)]
                             + [('Ensino Superior', 'Ensino Superior')],
                             string='Classe')
    case_id = fields.Many2one("linhafala.caso", string="Caso")
