from  odoo import models,  fields,  api,  _

class Company(models.Model):
    _inherit = 'res.company'

    reveni_webhook_ids = fields.One2many('reveni.webhook', 'company_id', string="Company Webhooks")