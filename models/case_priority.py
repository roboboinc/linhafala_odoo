import uuid

from odoo import api, fields, models
from odoo.exceptions import UserError


DEFAULT_CASE_PRIORITIES = [
    "Muito urgente",
    "Urgente",
    "Moderado",
    "Baixo",
    "Sem urgência",
]

LEGACY_CASE_PRIORITY_NAME_MAP = {
    "Muito Urgente": "Muito urgente",
    "Urgente": "Urgente",
    "Moderado": "Moderado",
    "Baixo": "Baixo",
    "Não Aplicável": "Sem urgência",
    "Sem urgência": "Sem urgência",
}


class CasePriority(models.Model):
    _name = "linhafala.case_priority"
    _description = "Case Priority"
    _order = "active desc, name asc, version desc"

    name = fields.Char(string="Nível de urgência", required=True)
    code = fields.Char(
        string="Código",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: str(uuid.uuid4()),
    )
    version = fields.Integer(string="Versão", default=1, readonly=True)
    previous_id = fields.Many2one(
        "linhafala.case_priority",
        string="Versão anterior",
        readonly=True,
        copy=False,
        ondelete="set null",
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "linhafala_case_priority_code_version_uniq",
            "unique(code, version)",
            "A versão do nível de urgência deve ser única por código.",
        ),
    ]

    def init(self):
        """Keep options and legacy data synchronized on module updates."""
        self._seed_default_options()
        self._backfill_case_records()

    def _seed_default_options(self):
        for name in DEFAULT_CASE_PRIORITIES:
            if not self.search([("name", "=", name), ("active", "=", True)], limit=1):
                self.create({"name": name})

    def _backfill_case_records(self):
        case_model = self.env["linhafala.caso"]
        records = case_model.search([
            ("case_priority_id", "=", False),
            "|",
            ("case_priority_snapshot", "!=", False),
            ("case_priority", "!=", False),
        ])

        for record in records:
            raw_name = (record.case_priority_snapshot or record.case_priority or "").strip()
            normalized_name = LEGACY_CASE_PRIORITY_NAME_MAP.get(raw_name, raw_name)
            if not normalized_name:
                continue

            option = self.search([("name", "=", normalized_name), ("active", "=", True)], limit=1)
            if not option:
                option = self.create({"name": normalized_name})

            updates = {"case_priority_id": option.id}
            if not record.case_priority_snapshot:
                updates["case_priority_snapshot"] = option.name
            record.with_context(
                skip_case_person_role_validation=True,
                skip_case_priority_backfill_validation=True,
            ).write(updates)

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
            raise UserError("Edite um nível de urgência de cada vez para preservar o histórico de versões.")

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
            super(CasePriority, new_record).write(passthrough_vals)

        super(CasePriority, record).write({"active": False})
        return True