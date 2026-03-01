/** @odoo-module */

import { _lt } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

/**
 * Add "/" slash command to open Chamada form from Discuss.
 * Press Ctrl+K (Cmd+K on Mac), type "/" then "chamada", select "Criar Chamada".
 * Form opens with contact pre-filled from current chat when available.
 */

async function openChamadaForm(env) {
    const actionService = env.services.action;
    const orm = env.services.orm;
    let channelId = null;
    try {
        const messaging = await env.services.messaging?.get?.();
        if (messaging?.discuss?.thread) {
            const thread = messaging.discuss.thread;
            if (thread?.id) {
                channelId = thread.id;
            }
        }
    } catch (_e) {
        // Messaging not available (e.g. not in Discuss)
    }
    let action;
    if (channelId && orm) {
        try {
            action = await orm.call(
                "mail.channel",
                "action_create_chamada",
                [[channelId]],
                {}
            );
        } catch (_e) {
            // Fallback to default action
        }
    }
    if (!action) {
        action = {
            type: "ir.actions.act_window",
            name: "Formulário de chamada LFC",
            res_model: "linhafala.chamada",
            view_mode: "form",
            target: "current",
            context: { default_contact_type: "Redes Sociais" },
        };
    }
    // Odoo 16 doAction expects action.views to be an array; backend may omit it
    if (action && !Array.isArray(action.views) && action.view_mode) {
        action = { ...action };
        action.views = (action.view_mode || "form").split(",").map((mode) => [false, mode.trim()]);
    }
    if (action && actionService) {
        await actionService.doAction(action);
    }
}

const commandSetupRegistry = registry.category("command_setup");
commandSetupRegistry.add("/", {
    debounceDelay: 200,
    emptyMessage: _lt("No command found"),
    name: _lt("commands"),
    placeholder: _lt("Type to search... e.g. chamada"),
});

const commandProviderRegistry = registry.category("command_provider");
commandProviderRegistry.add("chamada", {
    namespace: "/",
    async provide(env, options) {
        const searchValue = (options.searchValue || "").toLowerCase();
        if (searchValue && !"chamada".includes(searchValue)) {
            return [];
        }
        return [
            {
                name: _lt("Criar Chamada"),
                async action() {
                    await openChamadaForm(env);
                },
            },
        ];
    },
});
