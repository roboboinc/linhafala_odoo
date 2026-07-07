from xml.dom import ValidationErr
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import uuid


class PersonInvolved(models.Model):
    _name = "linhafala.person_involved"
    _description = "Person Involved Lines"

    PERPETRADOR_RELATIONSHIP_SELECTION = [
        ("Pai", "Pai"),
        ("Mãe", "Mãe"),
        ("Padrasto", "Padrasto"),
        ("Madrasta", "Madrasta"),
        ("Irmão(ã)", "Irmão(ã)"),
        ("Meio-irmão(ã)", "Meio-irmão(ã)"),
        ("Avô(ó)", "Avô(ó)"),
        ("Tio(a)", "Tio(a)"),
        ("Primo(a)", "Primo(a)"),
        ("Enteado(a)", "Enteado(a)"),
        ("Cunhado(a)", "Cunhado(a)"),
        ("Sogro(a)", "Sogro(a)"),
        ("Professor(a)", "Professor(a)"),
        ("Director(a) escolar", "Director(a) escolar"),
        ("Funcionário(a) da escola", "Funcionário(a) da escola"),
        ("Colega/aluno(a)", "Colega/aluno(a)"),
        ("Ex-colega", "Ex-colega"),
        ("Namorado(a)", "Namorado(a)"),
        ("Ex-namorado(a)", "Ex-namorado(a)"),
        ("Companheiro(a)", "Companheiro(a)"),
        ("Vizinho(a)", "Vizinho(a)"),
        ("Líder comunitário", "Líder comunitário"),
        ("Líder religioso", "Líder religioso"),
        ("Empregador(a)", "Empregador(a)"),
        ("Agente da Polícia", "Agente da Polícia"),
        ("Profissional de saúde", "Profissional de saúde"),
        ("Assistente social", "Assistente social"),
        ("Outro profissional institucional", "Outro profissional institucional"),
        ("Funcionario de Projecto", "Funcionario de Projecto"),
        ("Pessoa da comunidade (não familiar nem vizinho)", "Pessoa da comunidade (não familiar nem vizinho)"),
        ("Comerciante local", "Comerciante local"),
        ("Outro", "Outro (especificar)"),
    ]

    CONTACTANTE_RELATIONSHIP_SELECTION = [
        ("própria vítima", "própria vítima"),
        ("Pai", "Pai"),
        ("Mãe", "Mãe"),
        ("Padrasto", "Padrasto"),
        ("Madrasta", "Madrasta"),
        ("Irmão(ã)", "Irmão(ã)"),
        ("Outro familiar", "Outro familiar"),
        ("Professor(a)", "Professor(a)"),
        ("Diretor(a) escolar", "Diretor(a) escolar"),
        ("Funcionário(a) da escola", "Funcionário(a) da escola"),
        ("Colega/aluno(a)", "Colega/aluno(a)"),
        ("Namorado(a)", "Namorado(a)"),
        ("Vizinho(a)", "Vizinho(a)"),
        ("Líder comunitário", "Líder comunitário"),
        ("Líder religioso", "Líder religioso"),
        ("Profissional de saúde", "Profissional de saúde"),
        ("Assistente social", "Assistente social"),
        ("Agente da Polícia", "Agente da Polícia"),
        ("Colaborador(a) de OCS", "Colaborador(a) de OCS"),
        ("Colaborador(a) de Instituição de acolhimento", "Colaborador(a) de Instituição de acolhimento"),
        ("Anónimo(a)", "Anónimo(a)"),
        ("Outro", "Outro (especificar)"),
    ]

    PERPETRADOR_RELATIONSHIP_VALUES = {
        "Pai",
        "Mãe",
        "Padrasto",
        "Madrasta",
        "Irmão(ã)",
        "Meio-irmão(ã)",
        "Avô(ó)",
        "Tio(a)",
        "Primo(a)",
        "Enteado(a)",
        "Cunhado(a)",
        "Sogro(a)",
        "Professor(a)",
        "Director(a) escolar",
        "Funcionário(a) da escola",
        "Colega/aluno(a)",
        "Ex-colega",
        "Namorado(a)",
        "Ex-namorado(a)",
        "Companheiro(a)",
        "Vizinho(a)",
        "Líder comunitário",
        "Líder religioso",
        "Empregador(a)",
        "Agente da polícia",
        "Profissional de saúde",
        "Assistente social",
        "Outro profissional institucional",
        "Funcionario de Projecto",
        "Pessoa da comunidade (não familiar nem vizinho)",
        "Comerciante local",
        "Outro",
    }

    CONTACTANTE_RELATIONSHIP_VALUES = {
        "própria vítima",
        "Pai",
        "Mãe",
        "Padrasto",
        "Madrasta",
        "Irmão(ã)",
        "Outro familiar",
        "Professor(a)",
        "Diretor(a) escolar",
        "Funcionário(a) da escola",
        "Colega/aluno(a)",
        "Namorado(a)",
        "Vizinho(a)",
        "Líder comunitário",
        "Líder religioso",
        "Profissional de saúde",
        "Assistente social",
        "Agente da Polícia",
        "Colaborador(a) de OCS",
        "Colaborador(a) de Instituição de acolhimento",
        "Anónimo(a)",
        "Outro",
    }

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
        required=True
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
        valid_types = ('Perpetrador', 'Contactante')
        if self.person_type == 'Perpetrador':
            self.age = False  # Hide the "Idade" field
        else:
            self.age = False  # Show the "Idade" field

        if self.person_type not in valid_types:
            self.victim_relationship = False
            self.what_other = False
            self.victim_relationship_perpetrador = False
            self.victim_relationship_contactante = False
        elif self.person_type == 'Perpetrador' and self.victim_relationship and self.victim_relationship not in self.PERPETRADOR_RELATIONSHIP_VALUES:
            self.victim_relationship = False
            self.what_other = False
            self.victim_relationship_perpetrador = False
        elif self.person_type == 'Contactante' and self.victim_relationship and self.victim_relationship not in self.CONTACTANTE_RELATIONSHIP_VALUES:
            self.victim_relationship = False
            self.what_other = False
            self.victim_relationship_contactante = False

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
        domain="[('distrito', '=', distrito)]",
        required=True
        )

    localidade = fields.Many2one(
        comodel_name='linhafala.localidade', string="Localidade",
        domain="[('posto', '=', posto)]",
        required=True,
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
        string='Com quem vive? (legado)',
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
            ("Avo", "Avo"),
        ],
        help="Campo legado preservado para histórico e compatibilidade."
    )
    family_situation_id = fields.Many2one(
        comodel_name='linhafala.family_situation',
        string='Situação familiar',
        domain="['|', ('active', '=', True), ('id', '=', family_situation_id)]",
        help="Situação familiar configurável no menu de configurações."
    )
    family_situation_snapshot = fields.Char(
        string='Situação familiar (histórico)',
        readonly=True,
        copy=False,
        help="Valor textual preservado para histórico mesmo após alterações nas opções."
    )
    family_situation_is_other = fields.Boolean(
        string='Situação familiar é outro',
        compute='_compute_family_situation_is_other'
    )
    family_situation_other = fields.Char(
        string='Outra situação familiar (especificar)'
    )
    socioeconomic_condition = fields.Selection(
        string='Condição socioeconómica',
        selection=[
            ('Muito baixa', 'Muito baixa'),
            ('Baixa', 'Baixa'),
            ('Média', 'Média'),
            ('Alta', 'Alta'),
            ('Beneficiário(a) de apoio social', 'Beneficiário(a) de apoio social'),
            ('Sem informação', 'Sem informação'),
        ],
        default='Sem informação',
        help='Condição socioeconómica da pessoa envolvida.'
    )
    legal_guardian = fields.Selection(
        string='Responsável legal',
        selection=[
            ('Pai', 'Pai'),
            ('Mãe', 'Mãe'),
            ('Familiar', 'Familiar'),
            ('Tutor formal', 'Tutor formal'),
            ('Instituição de acolhimento', 'Instituição de acolhimento'),
            ('Outro', 'Outro (especificar)'),
        ],
        help='Responsável legal da pessoa envolvida.'
    )
    legal_guardian_other = fields.Char(
        string='Outro responsável legal (especificar)'
    )
    support_type_needed = fields.Selection(
        string='Tipo de apoio necessário',
        selection=[
            ('Apoio psicossocial', 'Apoio psicossocial'),
            ('Apoio jurídico', 'Apoio jurídico'),
            ('Apoio médico', 'Apoio médico'),
            ('Reintegração escolar', 'Reintegração escolar'),
            ('Material escolar', 'Material escolar'),
            ('Proteção imediata', 'Proteção imediata'),
            ('Encaminhamento institucional', 'Encaminhamento institucional'),
            ('Aconselhamento', 'Aconselhamento'),
            ('Outra', 'Outra (especificar)'),
        ],
        help='Tipo de apoio necessário para a pessoa envolvida.'
    )
    support_type_needed_other = fields.Char(
        string='Outro tipo de apoio (especificar)'
    )
    victim_relationship = fields.Selection(
        string='Relação com a(s) vítima(s):',
        selection=[
            ("própria vítima", "própria vítima"),
            ("Pai", "Pai"),
            ("Mãe", "Mãe"),
            ("Padrasto", "Padrasto"),
            ("Madrasta", "Madrasta"),
            ("Irmão(ã)", "Irmão(ã)"),
            ("Meio-irmão(ã)", "Meio-irmão(ã)"),
            ("Avô(ó)", "Avô(ó)"),
            ("Tio(a)", "Tio(a)"),
            ("Primo(a)", "Primo(a)"),
            ("Outro familiar", "Outro familiar"),
            ("Enteado(a)", "Enteado(a)"),
            ("Cunhado(a)", "Cunhado(a)"),
            ("Sogro(a)", "Sogro(a)"),
            ("Professor(a)", "Professor(a)"),
            ("Director(a) escolar", "Director(a) escolar"),
            ("Diretor(a) escolar", "Diretor(a) escolar"),
            ("Funcionário(a) da escola", "Funcionário(a) da escola"),
            ("Colega/aluno(a)", "Colega/aluno(a)"),
            ("Ex-colega", "Ex-colega"),
            ("Namorado(a)", "Namorado(a)"),
            ("Ex-namorado(a)", "Ex-namorado(a)"),
            ("Companheiro(a)", "Companheiro(a)"),
            ("Vizinho(a)", "Vizinho(a)"),
            ("Líder comunitário", "Líder comunitário"),
            ("Líder religioso", "Líder religioso"),
            ("Empregador(a)", "Empregador(a)"),
            ("Agente da Polícia", "Agente da Polícia"),
            ("Profissional de saúde", "Profissional de saúde"),
            ("Assistente social", "Assistente social"),
            ("Outro profissional institucional", "Outro profissional institucional"),
            ("Funcionario de Projecto", "Funcionario de Projecto"),
            ("Pessoa da comunidade (não familiar nem vizinho)", "Pessoa da comunidade (não familiar nem vizinho)"),
            ("Comerciante local", "Comerciante local"),
            ("Colaborador(a) de OCS", "Colaborador(a) de OCS"),
            ("Colaborador(a) de Instituição de acolhimento", "Colaborador(a) de Instituição de acolhimento"),
            ("Anónimo(a)", "Anónimo(a)"),
            ("Outro", "Outro (especificar)"),
        ],
        help="Relação com a(s) vítima(s):",
        required=False
    )
    victim_relationship_perpetrador = fields.Selection(
        string='Relação com a(s) vítima(s) (Perpetrador)',
        selection=PERPETRADOR_RELATIONSHIP_SELECTION,
        compute='_compute_split_victim_relationship',
        inverse='_inverse_victim_relationship_perpetrador'
    )
    victim_relationship_contactante = fields.Selection(
        string='Relação com a(s) vítima(s) (Contactante)',
        selection=CONTACTANTE_RELATIONSHIP_SELECTION,
        compute='_compute_split_victim_relationship',
        inverse='_inverse_victim_relationship_contactante'
    )
    what_other = fields.Char(string="Qual Outro")
    gender = fields.Selection(
        string='Sexo',
        selection=[
            ("Masculino", "Masculino"),
            ("Feminino", "Feminino"),
        ],
        help="Sexo",
        # required=True
    )
    age = fields.Selection([('0-6 meses', '0-6 meses')] + [('7-11 meses', '7-11 meses')] + [(str(i), str(i)) for i in range(1, 25)] + [('25+', '25+')],
                           string='Idade',
                        #    required=True
                           )                        
    on_school = fields.Boolean("Estuda?")
    grade = fields.Selection([(str(i), str(i)) for i in range(0, 12)]
                             + [('Ensino Superior', 'Ensino Superior')],
                             string='Classe')
    case_id = fields.Many2one("linhafala.caso", string="Caso")

    are_you_disabled = fields.Selection(
        string="Tem alguma deficiência??",
        selection=[
            ("Sim", "Sim"),
            ("Não", "Não"),
        ],
        help="Tem alguma deficiência??",
        required=False
    )

    deficiency_line_calls_ids = fields.One2many('linhafala.deficiente', 'person_id',
                                                string="Linhas do Deficiênte")

    @api.onchange('family_situation_id')
    def _onchange_family_situation_id(self):
        if self.family_situation_id:
            self.family_situation_snapshot = self.family_situation_id.name
        if not self.family_situation_is_other:
            self.family_situation_other = False

    @api.depends('family_situation_id', 'family_situation_id.name')
    def _compute_family_situation_is_other(self):
        for record in self:
            name = (record.family_situation_id.name or '').strip().lower() if record.family_situation_id else ''
            record.family_situation_is_other = name.startswith('outr')

    @api.onchange('victim_relationship')
    def _onchange_victim_relationship(self):
        if self.victim_relationship != 'Outro':
            self.what_other = False

    @api.depends('person_type', 'victim_relationship')
    def _compute_split_victim_relationship(self):
        for record in self:
            record.victim_relationship_perpetrador = False
            record.victim_relationship_contactante = False

            if record.person_type == 'Perpetrador' and record.victim_relationship in record.PERPETRADOR_RELATIONSHIP_VALUES:
                record.victim_relationship_perpetrador = record.victim_relationship
            elif record.person_type == 'Contactante' and record.victim_relationship in record.CONTACTANTE_RELATIONSHIP_VALUES:
                record.victim_relationship_contactante = record.victim_relationship

    def _inverse_victim_relationship_perpetrador(self):
        for record in self:
            if record.person_type == 'Perpetrador':
                record.victim_relationship = record.victim_relationship_perpetrador or False
                record.victim_relationship_contactante = False

    def _inverse_victim_relationship_contactante(self):
        for record in self:
            if record.person_type == 'Contactante':
                record.victim_relationship = record.victim_relationship_contactante or False
                record.victim_relationship_perpetrador = False

    @api.onchange('legal_guardian')
    def _onchange_legal_guardian(self):
        if self.legal_guardian != 'Outro':
            self.legal_guardian_other = False

    @api.onchange('support_type_needed')
    def _onchange_support_type_needed(self):
        if self.support_type_needed != 'Outra':
            self.support_type_needed_other = False

    def _find_or_create_family_situation(self, name):
        clean_name = (name or '').strip()
        if not clean_name:
            return self.env['linhafala.family_situation']

        option = self.env['linhafala.family_situation'].search([
            ('name', '=', clean_name),
            ('active', '=', True),
        ], limit=1)
        if option:
            return option
        return self.env['linhafala.family_situation'].create({'name': clean_name})

    def _prepare_family_situation_values(self, vals):
        prepared = dict(vals)
        family_situation = self.env['linhafala.family_situation']

        if 'family_situation_id' in prepared and not prepared['family_situation_id']:
            prepared['family_situation_snapshot'] = False
            prepared['living_relatives'] = False
            return prepared

        if prepared.get('family_situation_id'):
            family_situation = self.env['linhafala.family_situation'].browse(prepared['family_situation_id'])
        elif prepared.get('living_relatives'):
            family_situation = self._find_or_create_family_situation(prepared.get('living_relatives'))
            if family_situation:
                prepared['family_situation_id'] = family_situation.id

        if family_situation:
            prepared['family_situation_snapshot'] = family_situation.name

        return prepared

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [self._prepare_family_situation_values(vals) for vals in vals_list]
        return super().create(vals_list)

    def write(self, vals):
        vals = self._prepare_family_situation_values(vals)
        return super().write(vals)

    
    @api.constrains('provincia', 'distrito', 'person_type', 'victim_relationship', 'what_other', 'are_you_disabled', 'family_situation_id', 'family_situation_other')
    def _check_all(self):
        for record in self:
            if not record.provincia:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Provincia")
            if not record.distrito:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Distrito")
            if record.person_type in ('Perpetrador', 'Contactante'):
                if not record.victim_relationship:
                    raise ValidationError(
                        "Por favor, preencha os campos de caracter obrigatorio Relação com a(s) vítima(s)")

                allowed_values = self.PERPETRADOR_RELATIONSHIP_VALUES
                if record.person_type == 'Contactante':
                    allowed_values = self.CONTACTANTE_RELATIONSHIP_VALUES

                if record.victim_relationship not in allowed_values:
                    raise ValidationError(
                        "A opção de Relação com a(s) vítima(s) não é válida para a categoria selecionada.")

                if record.victim_relationship == 'Outro' and not record.what_other:
                    raise ValidationError(
                        "Por favor, especifique o campo Outro em Relação com a(s) vítima(s)")

            if record.person_type != 'Perpetrador' and not record.are_you_disabled:
                raise ValidationError(
                    "Por favor, preencha os campos de caracter obrigatorio Tem alguma deficiência??")

            if record.family_situation_is_other and not record.family_situation_other:
                raise ValidationError(
                    "Por favor, especifique o campo Outro em Situação familiar")