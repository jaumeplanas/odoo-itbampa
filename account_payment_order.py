# -*- coding: utf-8 -*-
from openerp import models, api


class PaymentOrderCreate(models.TransientModel):
    _inherit = 'payment.order.create'

    @api.multi   
    def create_payment(self):
        order_obj = self.env['payment.order']
        payment_obj = self.env['payment.line']
        context = self._context
        if len(self.entries) == 0:
            return {'type': 'ir.actions.act_window_close'}

        payment = order_obj.browse(context['active_id'])

        ## Finally populate the current payment with new lines:
        for line in self.entries:
            if payment.date_prefered == "now":
                #no payment date => immediate payment
                date_to_pay = False
            elif payment.date_prefered == 'due':
                date_to_pay = line.date_maturity
            elif payment.date_prefered == 'fixed':
                date_to_pay = payment.date_scheduled
            payment_obj.create({
                    'move_line_id': line.id,
                    'amount_currency': line.amount_residual_currency,
                    'bank_id': line.partner_id.bank_ids[0].id,
                    'order_id': payment.id,
                    'partner_id': line.partner_id and line.partner_id.id or False,
                    'communication': line.invoice and line.invoice.origin,
                    'state': line.invoice and line.invoice.reference_type != 'none' and 'structured' or 'normal',
                    'date': date_to_pay,
                    'currency': (line.invoice and line.invoice.currency_id.id) or line.journal_id.currency.id or line.journal_id.company_id.currency_id.id,
                })
        return {'type': 'ir.actions.act_window_close'}
    