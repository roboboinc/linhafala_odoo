from odoo import api, fields, models
from odoo.exceptions import UserError


class KnowledgeBase(models.Model):
    _name = "linhafala.knowledgebase"
    _description = "Formulário de Base de conhecimentos fala criança"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]

    title = fields.Char(string="Título", required=True)
    text = fields.Html(string='Descrição', attrs={
                                       'style': 'height: 500px;'})
    file = fields.Binary(string='File Upload') # TODO: , store=True, attachment=True) # add parameters and configure for external store to be used
    photo = fields.Image(string='Image')
    created_at = fields.Datetime(string='Data de criaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    updated_at = fields.Datetime(string='Data de actualizaçäo', default=lambda self: fields.Datetime.now(), readonly=True)
    created_by = fields.Many2one('res.users', string='Criado por', default=lambda self: self.env.user, readonly=True)

    def write(self, vals):
        if vals:
            vals['updated_at'] = fields.Datetime.now()
        return super(KnowledgeBase, self).write(vals)