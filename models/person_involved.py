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


    @api.model
    def _get_confirm_perpetrador(self):
        return self.env['ir.config_parameter'].sudo().get_param('my_module.confirm_perpetrador')

    @api.model
    def _get_confirm_vitima(self):
        return self.env['ir.config_parameter'].sudo().get_param('my_module.confirm_vitima')

    @api.model
    def create(self, vals):
        person_type = vals.get('person_type')

        if person_type != 'Vítima' and person_type != 'Contactante+Vítima' and not self._get_confirm_vitima() and not self._context.get('vitima_added'):
            raise UserError(_("Desculpe, mas é necessário adicionar uma Vítima para prosseguir."))

        if person_type == 'Vítima':
            vals.update({'person_type': 'Vítima'})
            self = self.with_context(vitima_added=True)

        return super().create(vals)

    def write(self, vals):
        person_type = vals.get('person_type')

        if 'person_type' in vals and person_type != 'Vítima' and person_type != 'Contactante+Vítima' and not self._get_confirm_vitima() and not self._context.get('vitima_added'):
            raise UserError(_("Desculpe, mas é necessário adicionar uma Vítima para prosseguir."))

        if 'person_type' in vals and person_type == 'Vítima':
            vals.update({'person_type': 'Vítima'})
            self = self.with_context(vitima_added=True)

        return super().write(vals)


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
            ("male", "Masculino"),
            ("female", "Feminino"),
            ("other", "Desconhecido"),
        ],
        help="Sexo"
    )
    what_other = fields.Char(string="Qual Outro")
    age = fields.Selection([(str(i), str(i)) for i in range(6, 99)] + [('99+', '99+')],
                           string='Idade')
    on_school = fields.Boolean("Estuda?")
    grade = fields.Selection([(str(i), str(i)) for i in range(0, 12)]
                             + [('Ensino Superior', 'Ensino Superior')],
                             string='Classe')
    case_id = fields.Many2one("linhafala.caso", string="Caso")


