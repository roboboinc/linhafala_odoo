from odoo import models, fields, api


class ExportChamadasWizard(models.TransientModel):
    _name = 'linhafala.export.chamadas.wizard'
    _description = 'Exportar Chamadas Wizard'

    start_date = fields.Date(string='Data Início', required=True)
    end_date = fields.Date(string='Data Fim', required=True)

    def action_export(self):
        self.ensure_one()
        url = '/api/export/chamadas?start_date=%s&end_date=%s' % (self.start_date, self.end_date)
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }
