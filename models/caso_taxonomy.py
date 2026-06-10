from odoo import fields, models


class CasoArea(models.Model):
    _name = "linhafala.caso.area"
    _description = "Área do Caso (Automática)"
    _order = "name"

    name = fields.Char(string="Nome da Área", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )


class CasoCategoriaJuridica(models.Model):
    _name = "linhafala.caso.categoria_juridica"
    _description = "Categoria Jurídica do Caso (Automática)"
    _order = "name"

    name = fields.Char(string="Nome da Categoria Jurídica", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )


class CasoEnquadramento(models.Model):
    _name = "linhafala.caso.enquadramento"
    _description = "Enquadramento do Caso (Automático)"
    _order = "name"

    name = fields.Char(string="Nome do Enquadramento", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )


class CasoSubcategoriaAuto(models.Model):
    _name = "linhafala.caso.subcategoria_auto"
    _description = "Subcategoria do Caso (Automática)"
    _order = "name"

    name = fields.Char(string="Nome da Subcategoria", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )


class CasoPrograma(models.Model):
    _name = "linhafala.caso.programa"
    _description = "Programa do Caso"
    _order = "name"

    name = fields.Char(string="Nome do Programa", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )


class CasoClassificacao(models.Model):
    _name = "linhafala.caso.classificacao"
    _description = "Classificação do Caso"
    _order = "name"

    name = fields.Char(string="Nome da Classificação", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )
    tipo_ids = fields.One2many(
        comodel_name="linhafala.caso.tipo",
        inverse_name="classificacao_id",
        string="Tipos de Caso",
    )


class CasoTipo(models.Model):
    _name = "linhafala.caso.tipo"
    _description = "Tipo do Caso"
    _order = "classificacao_id, name"

    name = fields.Char(string="Nome do Tipo de Caso", required=True)
    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Desmarque para arquivar. Registos existentes continuam a mostrar o nome desta versão.",
    )
    classificacao_id = fields.Many2one(
        comodel_name="linhafala.caso.classificacao",
        string="Classificação",
        required=True,
        ondelete="cascade",
    )
    # Automatic dimensions derived from the selected Tipo do Caso. These are
    # configured once per Tipo and propagated to the case on selection.
    subcategoria_auto_id = fields.Many2one(
        comodel_name="linhafala.caso.subcategoria_auto",
        string="Subcategoria (Automática)",
    )
    area_id = fields.Many2one(
        comodel_name="linhafala.caso.area",
        string="Área do Caso (Automática)",
    )
    categoria_juridica_id = fields.Many2one(
        comodel_name="linhafala.caso.categoria_juridica",
        string="Categoria Jurídica (Automática)",
    )
    enquadramento_id = fields.Many2one(
        comodel_name="linhafala.caso.enquadramento",
        string="Enquadramento (Automático)",
    )
