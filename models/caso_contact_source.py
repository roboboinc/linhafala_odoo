from odoo import fields, models


class CasoContactSource(models.Model):
    """Ensure Fonte de Informação / Como conhece a LFC exist on linhafala.caso.

    These fields are also declared on caso.py. This inherit is a second
    registration so the case form can upgrade even if an older caso.py is
    still what the worker imported first.
    """

    _inherit = "linhafala.caso"

    contact_type = fields.Selection(
        string="Fonte de Informação",
        selection=[
            ("SMS BIZ", "SMS BIZ"),
            ("LInha Verde 1458", "LInha Verde 1458"),
            ("Não definido", "Não definido"),
            ("Presencial", "Presencial"),
            ("Telefónica", "Telefónica"),
            ("Palestras", "Palestras"),
            ("Email", "Email"),
            ("WhatsApp", "WhatsApp"),
            ("Website", "Website"),
            ("SMS", "SMS"),
            ("Facebook", "Facebook"),
            ("Messenger", "Messenger"),
        ],
        help="Fonte/canal de contacto (igual ao formulário Chamadas)",
    )
    how_knows_lfc = fields.Selection(
        string="Como conhece a LFC",
        selection=[
            ("WhatsApp", "WhatsApp"),
            ("Website", "Website"),
            ("Email", "Email"),
            ("SMS", "SMS"),
            ("Facebook", "Facebook"),
            ("Messenger", "Messenger"),
            ("Rádio", "Rádio"),
            ("Internet", "Internet"),
            ("Palestras", "Palestras"),
            ("Televisão", "Televisão"),
            ("Brochuras", "Brochuras"),
            ("Panfletos", "Panfletos"),
            ("Cartazes", "Cartazes"),
            ("SMS em Massa", "SMS em Massa"),
            ("Outros", "Outros"),
        ],
        help="Canal pelo qual conheceu a LFC (igual ao formulário Chamadas)",
    )
