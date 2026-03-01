# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class MailChannel(models.Model):
    _inherit = "mail.channel"

    def _define_command_chamada(self):
        """Register /chamada slash command in Discuss composer."""
        return {"help": _("Open Chamada form (copy info from chat)")}

    def _execute_command_chamada(self, **kwargs):
        """Execute /chamada: open Chamada form. Does not post a message."""
        return self.action_create_chamada()

    def action_create_chamada(self):
        """
        Open the Chamada form pre-filled with contact info from this channel.
        For chat channels: uses the contact (partner) info from the conversation.
        Agent fills remaining required fields and saves.
        """
        self.ensure_one()
        context = {"default_contact_type": "Redes Sociais"}  # Website/Chatwoot default

        if self.channel_type == "chat" and self.channel_partner_ids:
            partner = self.channel_partner_ids[0]
            if partner != self.env.user.partner_id:
                context["default_fullname"] = partner.name or ""
                context["default_contact"] = partner.mobile or partner.phone or ""
                context["default_alternate_contact"] = (
                    partner.phone or partner.mobile or "+258"
                )

        return {
            "type": "ir.actions.act_window",
            "name": "Formulário de chamada LFC",
            "res_model": "linhafala.chamada",
            "view_mode": "form",
            "target": "current",
            "context": context,
        }
