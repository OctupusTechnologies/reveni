from odoo import fields, models
from .reveni_api.api import ReveniApi
import json


class ReveniEvent(models.Model):
    _name = 'reveni.event'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Reveni Event'
    _rec_name = 'event_name'
    event_name = fields.Char(string="Event Name", required=True)
    event_data = fields.Char(string="Event Data", required=True)
    event_date = fields.Datetime(string="Event Date", required=True)
    event_type = fields.Selection([('return.created', 'Return Created'), ('return.updated', 'Return Updated')])
    state = fields.Selection([
        ('draft', 'Draft'),
        ('error', 'Error'),
        ('done', 'Done'),
        ('cancel', 'Cancel')],
        default='draft')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.event_name))
        return result

    def action_process_event(self):
        for record in self:
            if record.event_type == 'return.updated':
                try:
                    record.process_return_created()
                    record.state = 'done'
                except Exception as e:
                    record.state = 'error'
                    record.message_post(body=str(e))

    def process_return_created(self: object) -> object:
        """
        Process return created event
        :return: RMA object
        """
        # TODO need object of RMA claim
        rma_clain_obj = self.env['RMA.OBJECT']

        IrConfigParams = self.env['ir.config_parameter'].sudo()
        reveni_api = ReveniApi(IrConfigParams)

        for record in self:
            return_uuid = json.loads(record.event_data.replace("\'", "\"")).get('resource_id')
            result = reveni_api.request_reveni('returns/{}'.format(return_uuid), 'GET')

            if not result:
                record.state = 'error'
                continue
            # TODO search sale order using external_id
            # order = self.env['sale.order'].search([('shopify_order_id', '=', result.get('order',{}).get('external_id',False))], limit=1)
            order = self.env['sale.order'].search([], limit=1)
            if not order:
                record.state = 'error'
                continue
            picking = order.picking_ids.filtered(lambda l: l.state == 'done' and l.picking_type_code == 'outgoing')
            if not result.get('return_items'):
                record.state = 'error'
                continue

            # TODO need check if rma claim is already created
            vals = {
                'name': 'RMA Claim {}'.format(order.name),
                'picking_id': picking.id,
                'sale_id': order.id,
                'reveni_event_id': record.id,

            }

            items = result.get('return_items')
            type = result.get('type')
            lines = self.generate_line_vals(items, type)
            vals.update({'claim_line_ids': lines})

            rma_claim = rma_clain_obj.create(vals)
            record.state = 'done'

        return rma_claim

    # TODO need check chnage of product
    def generate_line_vals(self, items: list(dict), type: 'refund' or 'exchange') -> \
            [(0, 0, dict)]:

        products = []
        for item in items:
            product = self.env['product.product'].search([('default_code', '=', item.get('sku'))], limit=1)
            if not product:
                continue
            products.append(
                (0, 0, {
                    'product_id': product.id,
                    'product_qty': item.get('quantity'),
                    'claim_type': type,
                    'partner_note': 'Customer say return_reason: {} exchange:{}'.format(item.get('return_reason'),
                                                                                        item.get('exchange')),
                })
            )

        return products

    def send_partial_validate(self, rma: object) -> None:
        """
        Send partial validate to reveni
        :param rma: RMA object
        :return: None
        """
        IrConfigParams = self.env['ir.config_parameter'].sudo()
        reveni_api = ReveniApi(IrConfigParams)
        return_uuid = rma.reveni_event_id.event_data.get('resource_id')
        payload = {"items": [
            {
                "item_id": "string",
                "quantity": 0,
                "status": "accepted",
                "reject_reason": "defect",
                "reject_reason_text": "string"
            }
        ]}
        reveni_api.request_reveni('returns/{}/partial_validate'.format(return_uuid), 'POST', payload)
