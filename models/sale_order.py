import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_status_overruled = fields.Selection([
        ('not overruled', 'Not overruled'),
        ('invoiced', 'Fully invoiced'),
        ('to invoice', 'To invoice'),
        ('no', 'Nothing to invoice'),

    ], default='not overruled', tracking=True, string='Invoice status overruled')

    @api.depends('invoice_status_overruled', 'state', 'order_line.invoice_status')
    def _get_invoice_status(self):
        super()._get_invoice_status()

        for order in self:
            if order.invoice_status_overruled != 'not overruled':
                _logger.info("Sale order invoice status overruling from [%s] -> [%s]", order.invoice_status, order.invoice_status_overruled)
                order.invoice_status = order.invoice_status_overruled

