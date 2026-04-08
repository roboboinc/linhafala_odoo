import uuid

from odoo import api, fields, models
from odoo.exceptions import UserError


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


class FamilySituation(models.Model):
    _name = "linhafala.family_situation"
    _description = "Family Situation"
    _order = "active desc, name asc, version desc"

    name = fields.Char(string="Situação familiar", required=True)
    code = fields.Char(
        string="Código",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: str(uuid.uuid4()),
    )
    version = fields.Integer(string="Versão", default=1, readonly=True)
    previous_id = fields.Many2one(
        "linhafala.family_situation",
        string="Versão anterior",
        readonly=True,
        copy=False,
        ondelete="set null",
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("linhafala_family_situation_code_version_uniq", "unique(code, version)", "A versão da situação familiar deve ser única por código."),
    ]

    def init(self):
        """Keep options and legacy data synchronized on module updates."""
        self._seed_default_options()
        self._backfill_person_involved_records()

    def _seed_default_options(self):
        for name in DEFAULT_FAMILY_SITUATIONS:
            if not self.search([("name", "=", name), ("active", "=", True)], limit=1):
                self.create({"name": name})

    def _backfill_person_involved_records(self):
        person_model = self.env["linhafala.person_involved"]
        records = person_model.search([
            ("family_situation_id", "=", False),
            "|",
            ("family_situation_snapshot", "!=", False),
            ("living_relatives", "!=", False),
        ])

        for record in records:
            fallback_name = (record.family_situation_snapshot or record.living_relatives or "").strip()
            if not fallback_name:
                continue

            option = self.search([("name", "=", fallback_name), ("active", "=", True)], limit=1)
            if not option:
                option = self.create({"name": fallback_name})

            updates = {"family_situation_id": option.id}
            if not record.family_situation_snapshot:
                updates["family_situation_snapshot"] = option.name
            record.write(updates)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("code"):
                vals["code"] = str(uuid.uuid4())
        return super().create(vals_list)

    def write(self, vals):
        if "name" not in vals:
            return super().write(vals)

        if len(self) > 1:
            raise UserError("Edite uma situação familiar de cada vez para preservar o histórico de versões.")

        record = self[0]
        new_name = (vals.get("name") or "").strip()
        if not new_name or new_name == record.name:
            return super().write(vals)

        passthrough_vals = {k: v for k, v in vals.items() if k != "name"}
        new_record = record.copy(
            default={
                "name": new_name,
                "version": record.version + 1,
                "previous_id": record.id,
                "active": True,
            }
        )
        if passthrough_vals:
            super(FamilySituation, new_record).write(passthrough_vals)

        super(FamilySituation, record).write({"active": False})
        return True
