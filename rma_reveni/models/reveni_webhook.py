from odoo import models, fields, api, _


class ReveniWebhook(models.Model):
    _name = 'reveni.webhook'
    _description = 'Reveni Webhook'
    _rec_name = 'webhook_name'

    webhook_name = fields.Char(string="Webhook Name", required=True)
    webhook_url = fields.Char(string="Webhook URL", required=True)
    company_id = fields.Many2one('res.company', string="Company", required=True)
    webhook_event_ids = fields.Many2many('reveni.webhook.event', string="Webhook Events")
    webhook_active = fields.Boolean(string="Active", default=True)


    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.webhook_name))
        return result


class ReveniWebhookEvent(models.Model):
    _name = 'reveni.webhook.event'
    _description = 'Reveni Webhook Event'
    _rec_name = 'webhook_event_name'

    webhook_event_name = fields.Char(string="Webhook Event Name", required=True)
    webhook_event_code = fields.Selection([('return.created', 'Return Created'), ('return.updated', 'Return Updated')],
                                          string="Webhook Event Code", required=True)

    _sql_constraints = [
        ('webhook_event_code_unique', 'unique(webhook_event_code)', 'Webhook Event Code must be unique'),
    ]
