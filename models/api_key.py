# -*- coding: utf-8 -*-
from odoo import api, fields, models
import secrets
import string
from datetime import datetime


class LinhaFalaAPIKey(models.Model):
    _name = 'linhafala.api.key'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'API Keys for Third-Party Access'
    _order = 'create_date desc'

    name = fields.Char(
        string='Key Name',
        required=True,
        help='Descriptive name for this API key (e.g., "Partner XYZ Integration")'
    )

    key = fields.Char(
        string='API Key',
        required=False,
        readonly=True,
        copy=False,
        help='The actual API key - keep this secret!'
    )

    user_id = fields.Many2one(
        'res.users',
        string='Associated User',
        required=True,
        help='User account that will be used for API requests with this key'
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help='Disable to revoke API access without deleting the key'
    )

    expires_at = fields.Datetime(
        string='Expires At',
        help='Optional expiration date for the API key'
    )

    allowed_ips = fields.Text(
        string='Allowed IP Addresses',
        help='Comma-separated list of IP addresses allowed to use this key (leave empty for no restriction)'
    )

    usage_count = fields.Integer(
        string='Usage Count',
        default=0,
        readonly=True,
        help='Number of times this API key has been used'
    )

    last_used = fields.Datetime(
        string='Last Used',
        readonly=True,
        help='Last time this API key was used'
    )

    notes = fields.Text(
        string='Notes',
        help='Additional notes about this API key'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    _sql_constraints = [
        ('key_unique', 'UNIQUE(key)', 'API key must be unique!')
    ]

    @api.model
    def generate_key(self, length=48):
        """Generate a secure random API key"""
        alphabet = string.ascii_letters + string.digits
        return 'lfk_' + ''.join(secrets.choice(alphabet) for _ in range(length))

    @api.model
    def create(self, vals):
        """Generate API key on creation if not provided"""
        if 'key' not in vals or not vals.get('key'):
            vals['key'] = self.generate_key()
        record = super(LinhaFalaAPIKey, self).create(vals)

        # Automatically add the API user group to the associated user
        if record.user_id:
            api_group = self.env.ref('linhafala_odoo.group_linhafala_api_user', raise_if_not_found=False)
            if api_group and api_group.id not in record.user_id.groups_id.ids:
                record.user_id.sudo().write({
                    'groups_id': [(4, api_group.id)]
                })

        # If the action that opened this form requested to show the key
        # immediately after creation, open the transient wizard as a modal.
        # This uses the context flag `show_key_after_create` set on the action
        # that opens the API Keys view.
        if self.env.context.get('show_key_after_create'):
            try:
                wizard = self.env['linhafala.api.key.wizard'].create({
                    'key': record.key,
                    'api_key_id': record.id,
                })
                view = self.env.ref('linhafala_odoo.view_api_key_wizard_form')
                return {
                    'name': 'API Key Generated',
                    'type': 'ir.actions.act_window',
                    'res_model': 'linhafala.api.key.wizard',
                    'res_id': wizard.id,
                    'view_mode': 'form',
                    'view_id': view.id,
                    'views': [(view.id, 'form')],
                    'target': 'new',
                    'context': {'default_key': record.key},
                }
            except Exception:
                # If anything goes wrong creating/opening the wizard, just
                # return the created record so normal flow continues.
                return record

        return record

    def write(self, vals):
        """Add API user group when user_id is updated"""
        result = super(LinhaFalaAPIKey, self).write(vals)
        
        # If user_id is being updated, ensure the new user has API user group
        if 'user_id' in vals and vals['user_id']:
            api_group = self.env.ref('linhafala_odoo.group_linhafala_api_user', raise_if_not_found=False)
            if api_group:
                for record in self:
                    if record.user_id and api_group.id not in record.user_id.groups_id.ids:
                        record.user_id.sudo().write({
                            'groups_id': [(4, api_group.id)]
                        })
        
        return result

    def is_valid(self):
        """Check if the API key is currently valid"""
        self.ensure_one()

        if not self.active:
            return False

        if self.expires_at and self.expires_at < datetime.now():
            return False

        return True

    def action_regenerate_key(self):
        """Regenerate the API key and return a client notification containing the key
        so users can copy it immediately (fallback to modal removed).
        """
        self.ensure_one()
        new_key = self.generate_key()
        self.write({
            'key': new_key,
            'usage_count': 0,
            'last_used': False
        })

        # Return a simple client notification with the key so the user can copy it.
        # We keep the message sticky to make copying easier in some browsers.
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'API Key Regenerated',
                'message': f'New API Key: {new_key}',
                'type': 'success',
                'sticky': True,
            }
        }

    def action_revoke_key(self):
        """Revoke (deactivate) the API key"""
        self.write({'active': False})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'API Key Revoked',
                'message': 'API key has been deactivated.',
                'type': 'warning',
                'sticky': False,
            }
        }

    def action_view_usage(self):
        """Show a simple usage notification for this API key"""
        self.ensure_one()
        msg = f"Usage count: {self.usage_count}. Last used: {self.last_used or 'never'}."
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'API Key Usage',
                'message': msg,
                'type': 'info',
                'sticky': False,
            }
        }


class LinhaFalaAPIKeyWizard(models.TransientModel):
    _name = 'linhafala.api.key.wizard'
    _description = 'Show newly generated API key'

    key = fields.Char(string='API Key')
    api_key_id = fields.Many2one('linhafala.api.key', string='API Key')

    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}

    def action_revoke_key(self):
        """Revoke (deactivate) the API key"""
        self.write({'active': False})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'API Key Revoked',
                'message': 'API key has been deactivated.',
                'type': 'warning',
                'sticky': False,
            }
        }

    def action_view_usage(self):
        """Show a simple usage notification for this API key"""
        self.ensure_one()
        msg = f"Usage count: {self.usage_count}. Last used: {self.last_used or 'never'}."
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'API Key Usage',
                'message': msg,
                'type': 'info',
                'sticky': False,
            }
        }
