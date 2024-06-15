from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Localidade(models.Model):
    _name = "linhafala.posto"
    _description = "Posto"

    name = fields.Char(string="Nome do posto")
    distrito = fields.Many2one("linhafala.distrito", string="Distrito")

    #_sql_constraints = [
     #   ('unique_fields', 'unique(LOWER(name))', 'Combination of fields must be unique!'),
    #]

    #@api.constrains('name')
    #def _check_unique_name(self):
       # for record in self:
            # Convert the name to lowercase for comparison
        #    name_lower = record.name.lower()
         #   if self.search([('id', '!=', record.id), ('name', '=ilike', name_lower)]):
          #      raise ValidationError("Name must be unique!")
    
    @api.constrains('name')
    def _check_all(self):
        for record in self:
            if not record.name:
                raise ValidationError(
                    "Please fill in the mandatory fields Location Name")