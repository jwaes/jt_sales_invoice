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


    delivery_status = fields.Selection(selection_add=[
        ('na', 'Not applicable')
    ], string='Delivery Status', compute='_compute_delivery_status')

    @api.depends('picking_ids', 'picking_ids.state')
    def _compute_delivery_status(self):
        for so in self:
            delivered_count = 0
            not_delivered_count = 0
            for picking in so.picking_ids:
                if picking.state == 'done':
                    delivered_count += 1
                elif picking.state not in ('draft', 'cancel'):
                    not_delivered_count += 1
            if delivered_count > 0:
                if not_delivered_count == 0:
                    so.delivery_status = 'delivered'
                elif not_delivered_count > 0:
                    so.delivery_status = 'partial'
            elif not_delivered_count > 0:
                so.delivery_status = 'pending'
            else :
                so.delivery_status = 'na'

