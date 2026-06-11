from odoo import fields, models


class AssistanceNivelRisco(models.Model):
    _name = "linhafala.chamada.assistance.nivel_risco"
    _description = "Nível de Risco da Queixa (Automático)"
    _order = "name"

    name = fields.Char(string="Nome do Nível de Risco", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )


class AssistanceSubcategoriaAuto(models.Model):
    _name = "linhafala.chamada.assistance.subcategoria_auto"
    _description = "Subcategoria da Queixa (Automática)"
    _order = "name"

    name = fields.Char(string="Nome da Subcategoria", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )


class AssistancePrograma(models.Model):
    _name = "linhafala.chamada.assistance.programa"
    _description = "Programa da Queixa"
    _order = "name"

    name = fields.Char(string="Nome do Programa", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )


class AssistanceCategoriaQueixa(models.Model):
    _name = "linhafala.chamada.assistance.categoria_queixa"
    _description = "Categoria de Queixa"
    _order = "name"

    name = fields.Char(string="Nome da Categoria de Queixa", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )
    tipo_ids = fields.One2many(
        comodel_name="linhafala.chamada.assistance.tipo_queixa",
        inverse_name="categoria_queixa_id",
        string="Tipos de Queixa",
    )


class AssistanceTipoQueixa(models.Model):
    _name = "linhafala.chamada.assistance.tipo_queixa"
    _description = "Tipo de Queixa"
    _order = "categoria_queixa_id, name"

    name = fields.Char(string="Nome do Tipo de Queixa", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )
    categoria_queixa_id = fields.Many2one(
        comodel_name="linhafala.chamada.assistance.categoria_queixa",
        string="Categoria de Queixa",
        required=True,
        ondelete="cascade",
    )
    # Automatic dimensions derived from the selected Tipo de Queixa. Configured
    # once per Tipo and propagated to the assistance record on selection.
    subcategoria_auto_id = fields.Many2one(
        comodel_name="linhafala.chamada.assistance.subcategoria_auto",
        string="Subcategoria (Automática)",
    )
    nivel_risco_id = fields.Many2one(
        comodel_name="linhafala.chamada.assistance.nivel_risco",
        string="Nível de Risco (Automático)",
    )
