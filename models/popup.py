from odoo import models, fields

class Popup(models.Model):
    _name = 'linhafala.popup_notify'
    _description = "Formulário de chamadas linha fala criança"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]

    
    def action_desligar(self):
        self._skip_validation = True

    def action_atender(self):
        self._skip_validation = True