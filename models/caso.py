from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import uuid


LEGACY_CASE_PRIORITY_NAME_MAP = {
    'Muito Urgente': 'Muito urgente',
    'Urgente': 'Urgente',
    'Moderado': 'Moderado',
    'Baixo': 'Baixo',
    'Não Aplicável': 'Sem urgência',
    'Sem urgência': 'Sem urgência',
}

DISPLAY_TO_LEGACY_CASE_PRIORITY_NAME_MAP = {
    'Muito urgente': 'Muito Urgente',
    'Urgente': 'Urgente',
    'Moderado': 'Moderado',
    'Baixo': 'Baixo',
    'Sem urgência': 'Não Aplicável',
}


class Caso(models.Model):
    _name = "linhafala.caso"
    _description = "Formulário de Caso linha fala criança"
    _rec_name ='case_id'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]

    case_id = fields.Char(string="Id do caso", readonly=True)

    inqueritos_id = fields.One2many(
        'linhafala.caso.inqueritos', 'case_id', string="Iqueritos")

    person_id = fields.One2many('linhafala.person_involved', 'case_id',
                                string="Pessoa Envolvida")

    @api.constrains('person_id')
    def _check_vitima_contactante(self):
        for caso in self:
            has_vitima = False
            has_contactante_vitima = False

            for person in caso.person_id:
                if person.person_type == 'Vítima':
                    has_vitima = True
                elif person.person_type == 'Contactante+Vítima':
                    has_contactante_vitima = True

            if not has_vitima and not has_contactante_vitima:
                raise ValidationError(
                    "Porfavor adicione uma 'Vitima' ou 'Contactante+Vitima' para prosseguir.")     

    @api.constrains('person_id')
    def _check_contactante(self):
        for caso in self:
            has_contactante = False
            has_contactante_vitima = False


            for person in caso.person_id:
                if person.person_type == 'Contactante':
                    has_contactante = True
                elif person.person_type == 'Contactante+Vítima':
                    has_contactante_vitima = True
                
            if not has_contactante and not has_contactante_vitima:
                raise ValidationError(
                    "Porfavor adicione um 'Contactante' ou 'Contactante+Vitima' para prosseguir.")    

    call_id = fields.Many2one(
        comodel_name='linhafala.chamada', string="Chamada")

    case_status = fields.Selection(
        string='Estado do caso',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido", "Assistido"),
            ("No Arquivo Morto", "No Arquivo Morto"),
            ("Encerrado", "Encerrado")
        ],default="Aberto/Pendente",
        help="Estado do caso"
    )

    def save(self):
        return True

    def edit(self):
        return self.save()

    def init(self):
        """Backfill the taxonomy version for historical records.

        New records default to version 2 (new taxonomy). Any pre-existing
        record that does not use the new Classificação field is, by
        definition, a legacy record and must keep version 1 so that its
        original Categoria/Sub-categoria/Classificação Provisória configuration
        and validation are preserved. This is idempotent: version-2 records
        always have ``classificacao_id`` set and are never affected.
        """
        if not self._column_exists(self._table, 'classificacao_id'):
            return
        self.env.cr.execute(
            """
            UPDATE %s
               SET taxonomy_version = 1
             WHERE classificacao_id IS NULL
               AND (taxonomy_version IS NULL OR taxonomy_version <> 1)
            """
            % self._table
        )

    def _column_exists(self, table_name, column_name):
        self.env.cr.execute(
            """
            SELECT 1
              FROM information_schema.columns
             WHERE table_name = %s
               AND column_name = %s
            """,
            (table_name, column_name),
        )
        return bool(self.env.cr.fetchone())


    @api.constrains('case_status')
    def _check_case_status(self):
        for record in self:
            if record.case_status != 'Aberto/Pendente' and record.case_status != 'Dentro do sistema' and record.case_status != 'Assistido' and record.case_status != 'No Arquivo Morto' and record.case_status != 'Encerrado':
                raise ValidationError(
                    "Por favor, selecione o estado do caso para prosseguir.")
            
    @api.constrains('case_type','secundary_case_type','case_type_classification','classificacao_id','tipo_case_id','place_occurrence','case_handling','case_priority','case_priority_id','case_priority_snapshot','detailed_description','taxonomy_version')
    def _check_all(self):
        if self.env.context.get('skip_case_priority_backfill_validation'):
            return
        for record in self:
            if record.taxonomy_version and record.taxonomy_version >= 3:
                if not record.case_type:
                    raise ValidationError(
                        "Por favor, preencha os campos de carácter obrigatorio Categoria")
                if not record.classificacao_id:
                    raise ValidationError(
                        "Por favor, preencha os campos de carácter obrigatorio Classificação")
                if not record.tipo_case_id:
                    raise ValidationError(
                        "Por favor, preencha os campos de carácter obrigatorio Tipo do Caso")
            elif record.taxonomy_version and record.taxonomy_version >= 2:
                # New taxonomy: data-entry user only fills Classificação and
                # Tipo do Caso (Programa is optional for now). The remaining
                # dimensions are derived automatically from the Tipo do Caso.
                if not record.classificacao_id:
                    raise ValidationError(
                        "Por favor, preencha os campos de carácter obrigatorio Classificação")
                if not record.tipo_case_id:
                    raise ValidationError(
                        "Por favor, preencha os campos de carácter obrigatorio Tipo do Caso")
            else:
                # Legacy taxonomy (registos antigos): manter validação original.
                if not record.case_type:
                    raise ValidationError(
                        "Por favor, preencha os campos de carácter obrigatorio Categoria")
                if not record.secundary_case_type:
                    raise ValidationError(
                        "Por favor, preencha os campos de carácter obrigatorio Sub-categoria")
                if not record.case_type_classification:
                    raise ValidationError(
                        "Por favor, preencha os campos de carácter obrigatorio Classificaçäo Provisória")
            if not (record.case_priority_id or record.case_priority_snapshot or record.case_priority):
                raise ValidationError(
                    "Por favor, preencha os campos de carácter obrigatorio Nível de urgência")
            if not record.detailed_description:
                raise ValidationError(
                    "Por favor, preencha os campos de carácter obrigatorio Detalhes")
            if not record.place_occurrence:
                raise ValidationError(
                    "Por favor, preencha os campos de carácter obrigatorio Local de Ocorrência ")
            if not record.case_handling:
                raise ValidationError(
                    "Por favor, preencha os campos de carácter obrigatorio Tratamento do Caso")
            if not record.detailed_description:
                raise ValidationError(
                    "Por favor, preencha os campos de carácter obrigatorio Detalhes")

    case_priority = fields.Selection(
        string='Nível de urgência (legado)',
        selection=[
            ("Muito Urgente", "Muito Urgente"),
            ("Urgente", "Urgente"),
            ("Moderado", "Moderado"),
            ("Baixo", "Baixo"),
            ("Não Aplicável", "Não Aplicável"),
        ],
        help='Campo legado preservado para histórico e compatibilidade.'
    )
    case_priority_id = fields.Many2one(
        comodel_name='linhafala.case_priority',
        string='Nível de urgência',
        domain="['|', ('active', '=', True), ('id', '=', case_priority_id)]",
        help='Nível de urgência configurável no menu de configurações.'
    )
    case_priority_snapshot = fields.Char(
        string='Nível de urgência (histórico)',
        readonly=True,
        copy=False,
        help='Valor textual preservado para histórico mesmo após alterações nas opções.'
    )
    resolution_type = fields.Selection(
        string='Tratamento do caso',
        selection=[
            ("Aconselhamento LFC", "Aconselhamento LFC"),
            ("Encaminhado", "Encaminhado"),
            ("Não encaminhado", "Não encaminhado"),
        ],
        default="Aconselhamento LFC",
        help="Tratamento do caso"
    )

    case_handling = fields.Selection(
        string='Tratamento do caso',
        selection=[
            ("Aconselhamento LFC", "Aconselhamento LFC"),
            ("Encaminhado", "Encaminhado"),
            ("Não encaminhado", "Não encaminhado"),
        ],
        default="Aconselhamento LFC",
        help="Tratamento do caso"
    )
    place_occurrence = fields.Selection(
        string='Local de Ocorrência',
        selection=[
            ("Escola", "Escola"),
            ("Casa propria", "Casa propria"),
            ("Casa do vizinho", "Casa do vizinho"),
            ("Cresce/infantário", "Cresce/infantário"),
            ("Casa do parente mais próximo", "Casa do parente mais próximo"),
            ("Outros", "Outros")
        ],
        help="Local de Ocorrência",
        required=True
    )
    detailed_description = fields.One2many(
        'linhafala.caso.description',
        'case_id',
        string='Detalhes'
    )
    case_type = fields.Many2one(
        comodel_name='linhafala.caso.categoria',
        string="Categoria",
        domain="['|', ('active', '=', True), ('id', '=', case_type)]",
    )
    case_type_snapshot = fields.Char(
        string='Categoria (histórico)',
        readonly=True,
        copy=False,
        help='Valor textual preservado para histórico mesmo após alterações nas opções.',
    )
    
    is_criminal_case = fields.Boolean(
        compute="_compute_is_criminal_case", 
        store=True
    )

    @api.depends('case_type')
    def _compute_is_criminal_case(self):
        """Determine if the case is criminal"""
        for record in self:
            record.is_criminal_case = record.case_type.name == "caso de natureza criminal"

    online_offline = fields.Selection(
        string='Selecione se o crime foi:',
        selection=[
            ("Online", "Online"),
            ("Offline", "Offline"),
        ],
        help="Selecione se o crime foi:"
    )

    # Computed fields for visibility
    show_online_offline = fields.Boolean(
        compute="_compute_show_online_offline", store=False
    )

    show_secundary_case_type = fields.Boolean(
        compute="_compute_show_secundary_case_type", store=False
    )

    @api.onchange('case_priority_id')
    def _onchange_case_priority_id(self):
        if self.case_priority_id:
            self.case_priority_snapshot = self.case_priority_id.name
            self.case_priority = DISPLAY_TO_LEGACY_CASE_PRIORITY_NAME_MAP.get(
                self.case_priority_id.name,
                self.case_priority_id.name,
            )

    def _find_or_create_case_priority(self, name):
        clean_name = (name or '').strip()
        normalized_name = LEGACY_CASE_PRIORITY_NAME_MAP.get(clean_name, clean_name)
        if not normalized_name:
            return self.env['linhafala.case_priority']

        option = self.env['linhafala.case_priority'].search([
            ('name', '=', normalized_name),
            ('active', '=', True),
        ], limit=1)
        if option:
            return option
        return self.env['linhafala.case_priority'].create({'name': normalized_name})

    def _prepare_case_priority_values(self, vals):
        prepared = dict(vals)
        case_priority = self.env['linhafala.case_priority']

        if 'case_priority_id' in prepared and not prepared['case_priority_id']:
            prepared['case_priority_snapshot'] = False
            prepared['case_priority'] = False
            return prepared

        raw_priority = prepared.get('case_priority')
        if prepared.get('case_priority_id'):
            case_priority = self.env['linhafala.case_priority'].browse(prepared['case_priority_id'])
        elif raw_priority:
            case_priority = self._find_or_create_case_priority(raw_priority)
            if case_priority:
                prepared['case_priority_id'] = case_priority.id

        if case_priority:
            prepared['case_priority_snapshot'] = case_priority.name
            should_fill_legacy_value = (
                'case_priority' in prepared
                or not self
                or not any(record.case_priority for record in self)
            )
            if should_fill_legacy_value and not raw_priority:
                prepared['case_priority'] = DISPLAY_TO_LEGACY_CASE_PRIORITY_NAME_MAP.get(
                    case_priority.name,
                    case_priority.name,
                )

        return prepared

    def _prepare_category_snapshot_values(self, vals):
        prepared = dict(vals)

        if prepared.get('case_type'):
            cat = self.env['linhafala.caso.categoria'].browse(prepared['case_type'])
            if cat.exists():
                prepared['case_type_snapshot'] = cat.name

        if prepared.get('secundary_case_type'):
            subcat = self.env['linhafala.caso.subcategoria'].browse(prepared['secundary_case_type'])
            if subcat.exists():
                prepared['secundary_case_type_snapshot'] = subcat.name

        if prepared.get('case_type_classification'):
            classif = self.env['linhafala.caso.case_type_classification'].browse(prepared['case_type_classification'])
            if classif.exists():
                prepared['case_type_classification_snapshot'] = classif.name

        return prepared

    def _prepare_new_taxonomy_values(self, vals):
        """Populate snapshots and derive the automatic dimensions for the new
        taxonomy (Classificação/Tipo do Caso).

        The four automatic fields (Subcategoria, Área, Categoria Jurídica e
        Enquadramento) are taken from the selected Tipo do Caso so that the
        data-entry user never has to fill them in manually.
        """
        prepared = dict(vals)

        if prepared.get('tipo_case_id'):
            tipo = self.env['linhafala.caso.tipo'].browse(prepared['tipo_case_id'])
            if tipo.exists():
                prepared['tipo_case_snapshot'] = tipo.name
                prepared['subcategoria_auto_id'] = tipo.subcategoria_auto_id.id
                prepared['area_id'] = tipo.area_id.id
                prepared['categoria_juridica_id'] = tipo.categoria_juridica_id.id
                prepared['enquadramento_id'] = tipo.enquadramento_id.id
                prepared['subcategoria_auto_snapshot'] = tipo.subcategoria_auto_id.name
                prepared['area_snapshot'] = tipo.area_id.name
                prepared['categoria_juridica_snapshot'] = tipo.categoria_juridica_id.name
                prepared['enquadramento_snapshot'] = tipo.enquadramento_id.name
                # Keep Classificação consistent with the Tipo's parent.
                if tipo.classificacao_id and not prepared.get('classificacao_id'):
                    prepared['classificacao_id'] = tipo.classificacao_id.id

        if prepared.get('classificacao_id'):
            classif = self.env['linhafala.caso.classificacao'].browse(prepared['classificacao_id'])
            if classif.exists():
                prepared['classificacao_snapshot'] = classif.name

        return prepared

    @api.depends('is_criminal_case')
    def _compute_show_online_offline(self):
        """Show online_offline only if the case is criminal"""
        for record in self:
            record.show_online_offline = record.is_criminal_case

    @api.depends('is_criminal_case', 'online_offline')
    def _compute_show_secundary_case_type(self):
        """Show secundary_case_type for all cases, but delay it for criminal cases until online_offline is selected"""
        for record in self:
            if record.is_criminal_case:
                record.show_secundary_case_type = bool(record.online_offline)
            else:
                record.show_secundary_case_type = True

    secundary_case_type = fields.Many2one(
        comodel_name='linhafala.caso.subcategoria',
        string="Subcategoria",
        domain="['|', ('active', '=', True), ('id', '=', secundary_case_type)]",
    )
    secundary_case_type_snapshot = fields.Char(
        string='Subcategoria (histórico)',
        readonly=True,
        copy=False,
        help='Valor textual preservado para histórico mesmo após alterações nas opções.',
    )
    case_type_classification = fields.Many2one(
        comodel_name='linhafala.caso.case_type_classification',
        string="Classificaçäo Provisória",
        domain="['|', ('active', '=', True), ('id', '=', case_type_classification)]",
    )
    case_type_classification_snapshot = fields.Char(
        string='Classificação Provisória (histórico)',
        readonly=True,
        copy=False,
        help='Valor textual preservado para histórico mesmo após alterações nas opções.',
    )

    # ------------------------------------------------------------------
    # New case taxonomy.
    # V2: the data-entry user only selects Classificação and Tipo do Caso.
    # V3: the user also selects Categoria as an independent dimension.
    # The remaining dimensions (Subcategoria, Área, Categoria Jurídica,
    # Enquadramento) are derived automatically from the selected Tipo do Caso
    # and are visible (read-only) to administrators only.
    # ------------------------------------------------------------------
    taxonomy_version = fields.Integer(
        string="Versão da Classificação",
        default=3,
        readonly=True,
        copy=False,
        help="1 = classificação antiga (Categoria/Sub-categoria/Classificação Provisória); "
               "2 = nova classificação (Classificação/Tipo do Caso); "
             "3 = nova classificação + Categoria independente. "
             "Registos antigos mantêm a sua versão e configuração original.",
    )

    classificacao_id = fields.Many2one(
        comodel_name='linhafala.caso.classificacao',
        string="Classificação",
        domain="['|', ('active', '=', True), ('id', '=', classificacao_id)]",
    )
    classificacao_snapshot = fields.Char(
        string='Classificação (histórico)',
        readonly=True,
        copy=False,
        help='Valor textual preservado para histórico mesmo após alterações nas opções.',
    )
    tipo_case_id = fields.Many2one(
        comodel_name='linhafala.caso.tipo',
        string="Tipo do Caso",
        domain="['&', ('classificacao_id', '=', classificacao_id), "
               "'|', ('active', '=', True), ('id', '=', tipo_case_id)]",
    )
    tipo_case_snapshot = fields.Char(
        string='Tipo do Caso (histórico)',
        readonly=True,
        copy=False,
        help='Valor textual preservado para histórico mesmo após alterações nas opções.',
    )
    # Automatic (derived) dimensions - read-only, admin-only in the UI.
    subcategoria_auto_id = fields.Many2one(
        comodel_name='linhafala.caso.subcategoria_auto',
        string="Subcategoria (Automática)",
        readonly=True,
    )
    subcategoria_auto_snapshot = fields.Char(
        string='Subcategoria automática (histórico)',
        readonly=True,
        copy=False,
    )
    area_id = fields.Many2one(
        comodel_name='linhafala.caso.area',
        string="Área do Caso (Automática)",
        readonly=True,
    )
    area_snapshot = fields.Char(
        string='Área do Caso (histórico)',
        readonly=True,
        copy=False,
    )
    categoria_juridica_id = fields.Many2one(
        comodel_name='linhafala.caso.categoria_juridica',
        string="Categoria Jurídica (Automática)",
        readonly=True,
    )
    categoria_juridica_snapshot = fields.Char(
        string='Categoria Jurídica (histórico)',
        readonly=True,
        copy=False,
    )
    enquadramento_id = fields.Many2one(
        comodel_name='linhafala.caso.enquadramento',
        string="Enquadramento (Automático)",
        readonly=True,
    )
    enquadramento_snapshot = fields.Char(
        string='Enquadramento (histórico)',
        readonly=True,
        copy=False,
    )

    reporter_by = fields.Many2one(
        'res.users', string='Gestão', default=lambda self: self.env.user, readonly=True)
    data_ocorrencia = fields.Datetime(
        string="Data de Ocorrência", widget="datetime", date_format="%d/%m/%Y %H:%M:%S")

    created_at = fields.Datetime(
        string='Data de criaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    updated_at = fields.Datetime(string='Data de actualizaçäo',
                                 default=lambda self: fields.Datetime.now(), readonly=True)
    created_by = fields.Many2one(
        'res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)
    is_deleted = fields.Boolean(string='Apagado', default=False, readonly=True)
    uuid = fields.Char(string='UUID', readonly=True)
    is_locked = fields.Boolean(string='Is Locked', default=False)
    lock_date = fields.Datetime()

    abuse_time = fields.Char(
        string="Tempo de abuso/Sofrimento:")  # NewField
    forwarding_institution_line_ids = fields.One2many('linhafala.caso.forwarding_institution', 'case_id',
                                                      string="Instituição de encaminhamento")
    
    # TODO: Review the naming convention of the field, such that the classification of disability should be auxiliary - REMOVE from here and becomes part of the person_involved
    deficiency_line_case_ids = fields.One2many('linhafala.deficiente', 'case_id',
                                               string="Linhas do Deficiênte")

    manager_by = fields.Many2one(
        'res.users', string="Gerido por: ", compute='_compute_manager_by', store=True)

    @api.depends('manager_by')
    def _compute_manager_by(self):
        for record in self:
            record.manager_by = record.env.user

    def action_manager(self):
        self._compute_manager_by()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ('Caso Assumido com Sucesso!!'),
                    'type': 'success',
                    'sticky': False,
            },
        }


    def action_redirect(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        form_view_id = self.env.ref('linhafala_odoo.linhafala_cases_form_view')
        form_url = f"{base_url}/web?#id={self.id}&view_type=form&model=linhafala.caso&menu_id={form_view_id.id}"
        #form_url += '&no_redirect=1'
        #whatsapp_number = input('Enter the WhatsApp contact number: ')
        #form_url += f'&whatsapp={whatsapp_number}'

        return {
            'type': 'ir.actions.act_url',
            'url': form_url,
            'target': 'new',
        }

    _sql_constraints = [
        ('unique_case_id', 'unique(case_id)', 'The case_id must be unique'),
    ]

    def write(self, vals):
        vals = self._prepare_case_priority_values(vals)
        vals = self._prepare_category_snapshot_values(vals)
        vals = self._prepare_new_taxonomy_values(vals)
        if vals:
            vals['updated_at'] = fields.Datetime.now()
        res = super(Caso, self).write(vals)
        if self.env.context.get('skip_case_priority_backfill_validation') or self.env.context.get('skip_case_person_role_validation'):
            return res
        # Enforce after any edit: must keep at least one 'Vítima' or 'Contactante+Vítima'
        for record in self:
            has_required_role = any(
                p.person_type in ('Vítima', 'Contactante+Vítima') for p in record.person_id
            )
            if not has_required_role:
                raise ValidationError(
                    "Por favor, adicione uma 'Vítima' ou 'Contactante+Vítima' para prosseguir.")
        return res

    def unlink(self):
        for record in self:
            record.write({'is_deleted': True})
        return super(Caso, self).unlink()

    @api.model
    def create(self, vals):
        vals = self._prepare_case_priority_values(vals)
        vals = self._prepare_category_snapshot_values(vals)
        vals = self._prepare_new_taxonomy_values(vals)
        # New records use taxonomy v3 by default. Historical records keep the
        # taxonomy_version explicitly assigned to them.
        vals.setdefault('taxonomy_version', 3)
        # Ensure UUID is always set
        vals.setdefault('uuid', str(uuid.uuid4()))

        # Generate sequential case_id if not provided
        if vals.get('case_id', '/') == '/':
            # Use sudo() to ensure sequence generation works for API users
            next_case_id = self.env['ir.sequence'].sudo().next_by_code('linhafala.chamada.case_id.seq') or '/'
            # Extract the numeric part after the last hyphen
            vals['case_id'] = next_case_id.split('-')[-1]

        # Create the record first so we can reliably inspect one2many values
        record = super(Caso, self).create(vals)

        # Enforce: at least one person must be a 'Vítima' or 'Contactante+Vítima'
        has_required_role = any(
            p.person_type in ('Vítima', 'Contactante+Vítima') for p in record.person_id
        )
        if not has_required_role:
            # Rollback by raising a ValidationError to prevent saving invalid cases
            raise ValidationError(
                "Por favor, adicione uma 'Vítima' ou 'Contactante+Vítima' para prosseguir.")

        return record

    # Lock the case for single user edit
    # TODO: Check and fix that a record gets created and managed by a single user!
    # @api.model
    # def create(self, vals):
    #     # Set the user_id to the current user
    #     vals['user_id'] = self.env.user.id
    #     return super(Caso, self).create(vals)

    # def write(self, vals):
    #     if 'is_locked' in vals:
    #         # Check if the record is already locked by someone else
    #         if self.is_locked and self.user_id != self.env.user:
    #             raise UserError(
    #                 'This record is locked by {}.'.format(self.user_id.name))

    #         # Set the lock_date and user_id fields when the record is locked
    #         if vals['is_locked']:
    #             vals['lock_date'] = fields.Datetime.now()
    #             vals['user_id'] = self.env.user.id

    #         # Unlock the record when is_locked is set to False
    #         else:
    #             vals['lock_date'] = False
    #             vals['user_id'] = False

    #     return super(Caso, self).write(vals)

    # TODO: Review cascade select or remove this field, replacing with buttons as with the current app workflow
    @api.onchange('case_type')
    def _case_type_onchange(self):
        for rec in self:
            rec.case_type_snapshot = rec.case_type.name if rec.case_type else False
            if rec.taxonomy_version and rec.taxonomy_version >= 3:
                # V3 keeps Categoria independente da cadeia de
                # Classificação -> Tipo do Caso.
                return {}
            elif rec.taxonomy_version and rec.taxonomy_version >= 2:
                # V2 does not use Categoria in the active selection flow.
                return {}
            else:
                return {'value': {'secundary_case_type': False}, 'domain': {'secundary_case_type': [('categoria_id', '=', rec.case_type.id)]}}

    @api.onchange('secundary_case_type')
    def _secundary_case_type_onchange(self):
        for rec in self:
            rec.secundary_case_type_snapshot = rec.secundary_case_type.name if rec.secundary_case_type else False
            return {'value': {'case_type_classification': False}, 'domain': {'case_type_classification': [('categoria_id', '=', rec.secundary_case_type.id)]}}

    @api.onchange('case_type_classification')
    def _case_type_classification_onchange(self):
        for rec in self:
            rec.case_type_classification_snapshot = rec.case_type_classification.name if rec.case_type_classification else False

    @api.onchange('classificacao_id')
    def _classificacao_id_onchange(self):
        for rec in self:
            rec.classificacao_snapshot = rec.classificacao_id.name if rec.classificacao_id else False
            # Reset Tipo do Caso if it no longer matches the chosen Classificação.
            if rec.tipo_case_id and rec.tipo_case_id.classificacao_id != rec.classificacao_id:
                rec.tipo_case_id = False
            return {'domain': {'tipo_case_id': [('classificacao_id', '=', rec.classificacao_id.id)]}}

    @api.onchange('tipo_case_id')
    def _tipo_case_id_onchange(self):
        for rec in self:
            tipo = rec.tipo_case_id
            rec.tipo_case_snapshot = tipo.name if tipo else False
            # Derive the automatic dimensions from the selected Tipo do Caso.
            rec.subcategoria_auto_id = tipo.subcategoria_auto_id if tipo else False
            rec.area_id = tipo.area_id if tipo else False
            rec.categoria_juridica_id = tipo.categoria_juridica_id if tipo else False
            rec.enquadramento_id = tipo.enquadramento_id if tipo else False
            rec.subcategoria_auto_snapshot = tipo.subcategoria_auto_id.name if tipo and tipo.subcategoria_auto_id else False
            rec.area_snapshot = tipo.area_id.name if tipo and tipo.area_id else False
            rec.categoria_juridica_snapshot = tipo.categoria_juridica_id.name if tipo and tipo.categoria_juridica_id else False
            rec.enquadramento_snapshot = tipo.enquadramento_id.name if tipo and tipo.enquadramento_id else False
            if tipo and tipo.classificacao_id and rec.classificacao_id != tipo.classificacao_id:
                rec.classificacao_id = tipo.classificacao_id

    def action_confirm(self):
        self.callcaseassistance_status = 'Aberto/Pendente'

    def action_done(self):
        self.callcaseassistance_status = 'Assistido'

    def action_draft(self):
        self.callcaseassistance_status = 'Dentro do sistema'

    def action_cancel(self):
        self.callcaseassistance_status = 'Encerrado'


class PersonInvolved(models.Model):
    _name = "linhafala.caso.person_involved"
    _description = "Person Involved"

    fullname = fields.Char(string="Nome completo")
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
            ("Contactante+Vítima", "Contactante+Vítima"),
            ("Vítima", "Vítima"),
            ("Perpetrador", "Perpetrador"),
        ],
        help="Categoria"
    )
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
            ("Masculino", "Masculino"),
            ("Feminino", "Feminino"),
        ],
        help="Sexo"
    )
    age = fields.Selection([(str(i), str(i)) for i in range(6, 70)] + [('70+', '70+')],
                           string='Idade')

    on_school = fields.Boolean("Estuda?")
    grade = fields.Selection([(str(i), str(i)) for i in range(0, 12)]
                             + [('Ensino Superior', 'Ensino Superior')],
                             string='Classe')
    case_id = fields.Many2one("linhafala.caso", string="Caso")


class ReferenceArea(models.Model):
    _name = "linhafala.caso.referencearea"
    _description = "Área Institucional ou Näo Institucional"

    name = fields.Char(string="Referencia")
    area_type = fields.Selection(
        string='Tipo de instituição',
        selection=[
            ("Institucional", "Institucional"),
            ("Não Institucional", "Não Institucional"),
        ],
        help="Tipo de instituição"
    )


class ReferenceEntity(models.Model):
    _name = "linhafala.caso.referenceentity"
    _description = "Entidade de referência"

    name = fields.Char(string="Nome de entidade")

    reference_area = fields.Many2one(
        comodel_name='linhafala.caso.referencearea', string="Área de Referência")

    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Provincia")
    distrito = fields.Many2one(
        comodel_name='linhafala.distrito', string="Districto")

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}


class CaseReference(models.Model):
    _name = "linhafala.caso.casereference"
    _description = "Pessoa de Contacto"

    name = fields.Char(string="Pessoa de Contacto")

    reference_area = fields.Many2one(
        comodel_name='linhafala.caso.referencearea', string="Referência")

    area_type = fields.Selection(
        string='Área de Encaminhamento',
        selection=[
            ("Institucional", "Institucional"),
            ("Não Institucional", "Não Institucional"),
        ],
        help="Área de Encaminhamento"
    )

    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Provincia")

    reference_entity = fields.Many2one(
        comodel_name='linhafala.caso.referenceentity', string="Entidade de Referência")

    distrito = fields.Many2one(
        comodel_name='linhafala.distrito',
        domain="[('provincia', '=', provincia)]", 
        string="Districto")

    contact = fields.Char(string="Contacto", widget="phone_raw",  # add the number of pessoa de contacto
                          min_length=9, default="+258")

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}


class ForwardingInstitutions(models.Model):
    _name = "linhafala.caso.forwarding_institution"
    _rec_name ='case_id'
    _description = "Instituição de encaminhamento"

    case_id = fields.Many2one("linhafala.caso", string="Caso")
    created_by = fields.Many2one(
        'res.users',
        string='Encaminhado por',
        related='create_uid',
        store=True,
        readonly=True,
        index=True,
    )
    forwarding_institution_id = fields.Char(string="Id do encaminhamento", readonly=True)
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
        comodel_name='linhafala.caso.referenceentity', string="Entidade de Referência",
        domain="[('reference_area', '=', reference_area),('provincia', '=', provincia), ('distrito', '=', distrito)]"
    )

    case_reference = fields.Many2one(
        comodel_name='linhafala.caso.casereference',
        string="Pessoa de Contacto",
        domain="[('reference_entity', '=', reference_entity),('provincia', '=', provincia), ('distrito', '=', distrito)]"
    )

    @api.onchange('reference_entity', 'provincia', 'distrito')
    def _onchange_reference_filters(self):
        if self.reference_entity:
            domain = [
                ('reference_entity', '=', self.reference_entity.id)
            ]
            if self.provincia:
                domain.append(('provincia', '=', self.provincia.id))
            if self.distrito:
                domain.append(('distrito', '=', self.distrito.id))
            return {'domain': {'case_reference': domain}}


    spokes_person_phone = fields.Char(
        string="Telefone do Responsável", related='case_reference.contact')
    provincia = fields.Many2one(
        comodel_name='linhafala.provincia', string="Provincia")
    distrito = fields.Many2one(
        comodel_name='linhafala.distrito',         
        domain="[('provincia', '=', provincia)]",
        string="Distrito")

    case_status = fields.Selection(
        string='Estado do caso',
        selection=[
            ("Aberto/Pendente", "Aberto/Pendente"),
            ("Dentro do sistema", "Dentro do sistema"),
            ("Assistido", "Assistido"),
            ("No Arquivo Morto", "No Arquivo Morto"),
            ("Encerrado", "Encerrado")
        ], default="Aberto/Pendente",
        help="Estado do caso"
    )

    created_at = fields.Datetime(
        string='', default=lambda self: fields.Datetime.now(), readonly=True)

    @api.onchange('provincia')
    def _provincia_onchange(self):
        for rec in self:
            return {'value': {'distrito': False}, 'domain': {'distrito': [('provincia', '=', rec.provincia.id)]}}

   
        
class Description(models.Model):
    _name = 'linhafala.caso.description'
    _description = 'Descrição Detalhada'

    created_by = fields.Many2one(
        'res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)
    content = fields.Html(string='Conteudo Dos Detalhes', attrs={'style': 'height: 500px;'})
    case_id = fields.Many2one('linhafala.caso', string='ID do caso')

class Inqueritos(models.Model):
    _name='linhafala.caso.inqueritos'
    _description='Inqueritos'

    case_id = fields.Many2one(
        comodel_name='linhafala.caso', string="Caso")

    sexo = fields.Selection(
        string='Sexo:',
        selection=[
            ("Masculino", "Masculino"),
            ("Feminino", "Feminino"),
        ]
    )

    idade = fields.Char(
        string='Idade',
    )

    sector_de_trabalho = fields.Selection(
        string='Sector de trabalho:',
        selection=[
            ("Funcionario Publico", "Funcionario Publico"),
            ("Privado", "Privado"),
            ("Conta Propria", "Conta Propria"),
        ]
    )

    nivel_academico = fields.Selection(
        string='Nível académico:',
        selection=[
            ("Nenhum", "Nenhum"),
            ("Elementar", "Elementar"),
            ("Medio", "Medio"),
            ("Superior", "Superior"),
            ("Outro/s", "Outro/s"),
        ]
    )

    primeira_vez = fields.Selection(
        string='Será a primeira vez a entrar em contacto com a LFC:',
        selection=[
            ("Sim", "Sim"),
            ("Não", "Não"),
        ]
    )

    lingua_atendimento = fields.Selection(
        string='Em que língua gostaria de ser atendido(a)',
        selection=
        [
            ("Português ", "Português "),
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
        ]
    )

    escala_likert = fields.Selection(
        string='O questionário que se segue baseia-se na Escala de Likert  de  ( 1 - 5)',
        selection=[
            ("Muito Satisfeito", "Muito Satisfeito"),
            ("Satisfeito", "Satisfeito"),
            ("Indiferente", "Indiferente"),
            ("Insatisfeito", "Insatisfeito"),
            ("Muito Insatisfeito", "Muito Insatisfeito"),
        ]
    )

    o_que_sentiu = fields.Selection(
        string='De 1 a 5 , diga como é que se sentiu em relação ao atendimento dado no dia em que contactou a Linha Fala Criança ?',
        selection=[
            ("Muito Satisfeito", "Muito Satisfeito"),
            ("Satisfeito", "Satisfeito"),
            ("Indiferente", "Indiferente"),
            ("Insatisfeito", "Insatisfeito"),
            ("Muito Insatisfeito", "Muito Insatisfeito"),
        ]
    )

    o_que_sentiu_entidade_referencia = fields.Selection(
        string='De 1 a 5, diga como e que se sentiu no atendimento dado pela (entidade de referencia) ?',
        selection=[
            ("Muito Satisfeito", "Muito Satisfeito"),
            ("Satisfeito", "Satisfeito"),
            ("Indiferente", "Indiferente"),
            ("Insatisfeito", "Insatisfeito"),
            ("Muito Insatisfeito", "Muito Insatisfeito"),
        ]
    )

    o_que_sentiu_entidade_referencia_segmento = fields.Selection(
        string='De 1 a 5, diga como é que se sentiu em relação ao segmento dado na entidade de referência?',
        selection=[
            ("Muito Satisfeito", "Muito Satisfeito"),
            ("Satisfeito", "Satisfeito"),
            ("Indiferente", "Indiferente"),
            ("Insatisfeito", "Insatisfeito"),
            ("Muito Insatisfeito", "Muito Insatisfeito"),
        ]
    )

    desfecho = fields.Selection(
        string='De 1 a 5, diga como é que se sentiu em relação a resolução / desfecho do caso?',
        selection=[
            ("Muito Satisfeito", "Muito Satisfeito"),
            ("Satisfeito", "Satisfeito"),
            ("Indiferente", "Indiferente"),
            ("Insatisfeito", "Insatisfeito"),
            ("Muito Insatisfeito", "Muito Insatisfeito"),
        ]
    )

    nivel_tempo = fields.Selection(
        string='Tendo em conta o período de resolução do caso que denunciou, diga de 1 a 5 qual é a sua satisfação em relação ao tempo que levou para a resolução do caso?',
        selection=[
            ("Muito Satisfeito", "Muito Satisfeito"),
            ("Satisfeito", "Satisfeito"),
            ("Indiferente", "Indiferente"),
            ("Insatisfeito", "Insatisfeito"),
            ("Muito Insatisfeito", "Muito Insatisfeito"),
        ]
    )

    recomendations = fields.Html(
        string='Tem algum comentário, recomendação, acréscimo, por favor deixe ficar',
     )

    created_by = fields.Many2one(
        'res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)

    demograficos = fields.Boolean("Dados demográficos:")
    medicao_nivel = fields.Boolean("Questões de medição de satisfação:")
    comments = fields.Boolean("Comentários e Recomendaçòes:")
