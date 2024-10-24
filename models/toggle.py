from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    enable_ami = fields.Boolean(string="Activar AMI", default=False)
