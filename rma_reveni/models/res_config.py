import logging

from odoo import models, fields
from .reveni_api.api import ReveniApi

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    reveni_api_key = fields.Char(string='Api Key', config_parameter='reveni.api_key')
    reveni_sandbox_api_key = fields.Char(string='SandBox Api Key', config_parameter='reveni.sandbox_api_key')
    reveni_store_id = fields.Char(string='Store id', config_parameter='reveni.store_id')
    reveni_sandbox_store_id = fields.Char(string='SandBox Store id', config_parameter='reveni.sandbox_store_id')
    reveni_webhook_ids = fields.One2many(related="company_id.reveni_webhook_ids", string="Company Webhooks")
    reveni_debug = fields.Boolean(string='Debug', config_parameter='reveni.debug')

    def action_reveni_webhook_subscribe(self):
        IrConfigParams = self.env['ir.config_parameter'].sudo()
        api_instance = ReveniApi(IrConfigParams)
        for webhooks in self.env['reveni.webhook'].search([('company_id', '=', self.company_id.id)]):
            api_instance.request_reveni('webhooks/{}'.format(webhooks.webhook_name),'DELETE')
            webhooks.unlink()
        result = api_instance.request_reveni('webhooks', 'POST', {
            'event_types': ['return.updated'],
            'url': IrConfigParams.get_param('web.base.url') + '/reveni/webhook',
        })
        if result.get('id'):
            self.env['reveni.webhook'].create({
                'webhook_name': result['id'],
                'webhook_url': result['url'],
                'webhook_event_ids': [(6, 0, self.env['reveni.webhook.event'].search([('webhook_event_code', 'in', result['event_types'])]).ids)],
                'company_id': self.company_id.id,
            })
        # return self.env['reveni.webhook'].action_reveni_webhook_suscribe()
