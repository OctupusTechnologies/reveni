from odoo import api, fields, models

class ClaimProcessWizard(models.TransientModel):
    _inherit = 'claim.process.wizard'

    def reject_claim(self):
        res = super(ClaimProcessWizard, self).reject_claim()
        self.claim_line_id.claim_reject_message_id = self.reject_message_id.id
        self.claim_line_id.mapped('claim_id').partial_validation_claim()
        return res