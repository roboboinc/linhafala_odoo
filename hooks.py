from odoo import SUPERUSER_ID, api


DEFAULT_FAMILY_SITUATIONS = [
    "Não aplicavél",
    "Outra situação",
    "No Centro",
    "Sozinho(a)",
    "Com os tios maternos",
    "Com os tios paternos",
    "Só com a mae",
    "Só com o pai",
    "Só com os irmãos",
    "Com a familia adoctiva",
    "Familia toda",
    "Avo",
]


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    family_model = env["linhafala.family_situation"]

    for name in DEFAULT_FAMILY_SITUATIONS:
        if not family_model.search([("name", "=", name), ("active", "=", True)], limit=1):
            family_model.create({"name": name})

    records = env["linhafala.person_involved"].search([])
    for record in records:
        fallback_name = (record.family_situation_snapshot or record.living_relatives or "").strip()
        if not fallback_name:
            continue

        option = family_model.search([("name", "=", fallback_name), ("active", "=", True)], limit=1)
        if not option:
            option = family_model.create({"name": fallback_name})

        updates = {}
        if not record.family_situation_id:
            updates["family_situation_id"] = option.id
        if not record.family_situation_snapshot:
            updates["family_situation_snapshot"] = option.name

        if updates:
            record.write(updates)
