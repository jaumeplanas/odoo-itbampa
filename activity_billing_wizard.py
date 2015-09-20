# -*- coding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta

from collections import namedtuple

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

BMPTuple = namedtuple('BMPTuple', ['billing', 'member', 'product'])

class ActivityBillingWizard(models.TransientModel):
    """Activity Billing Wizard"""
    
    _name = 'itbampa.activity.billing.wizard'
               
    due_date = fields.Date(string="Due date month", default=date.today().isoformat())

    @api.onchange('due_date')
    def _onchange_due_date(self):
        due = fields.Date.from_string(self.due_date)
        due += relativedelta(day=31)
        if due > date.today():
            due -= relativedelta(months=1, day=31)
        self.due_date = due
    
    @api.one
    def create_invoices(self):
        # Check if exist open activities
        open_activities = self.env['itbampa.activity.event'].search_count([
                                                                ('state', '=', 'open'),
                                                                ('date_start', '<=', self.due_date)
                                                                ])
        if open_activities > 0:
            raise ValidationError(_('There are {0} activities open before specified date. Please close them before attempting to bill them.').format(open_activities))
                
        activities = self.env['itbampa.activity.event'].search([
            ('date_start', '<=', self.due_date),
            ('state', '=', 'closed')
            ])
        
        res = dict()
        short_date_old = ''
        for activity in activities:
            short_date_obj = fields.Date.from_string(activity.date_start)
            short_date = short_date_obj.strftime('%b %Y')
            if short_date != short_date_old:
                short_date_old = short_date
                dstart = date(short_date_obj.year, short_date_obj.month, 1)
                dend = dstart + relativedelta(day=31)
                lective_days = activity.school_calendar_id.count_lective_days(dstart=dstart, dend=dend)
            for p in activity.partner_ids:
                xtuple = BMPTuple(p.billing_partner_id.id, p.partner_id.id, p.product_id.id)
                xentry = res.setdefault(xtuple, {'quantity': 0, 'short_date': short_date, 'lective_days': lective_days, 'ids': set()})
                xentry['quantity'] += 1
                xentry['ids'].add(p.id)

        invs = set()
        for k, v in res.items():
            xinv = self.create_single_invoice(k, v)
            invs.add(xinv.id)
            self.env['itbampa.activity.event.partner'].browse(list(v['ids'])).write({'invoice_id': xinv.id})
                
        activities.signal_workflow('bill_activity_event')

    def create_single_invoice(self, k, v):
        objinvoice = self.env['account.invoice']
        objinvoice_line = self.env['account.invoice.line']
        objinvoice_tax = self.env['account.invoice.tax']
        objpartner = self.env['res.partner']
        objproduct = self.env['product.product']

        product = objproduct.browse(k.product)
        member = objpartner.browse(k.member)
        billing = objpartner.browse(k.billing)
        
        tagline = u"{} | {} | {} ({}/{}) ".format(member.name, product.name, v['short_date'], v['quantity'], v['lective_days'])

        account_id = billing.property_account_receivable and billing.property_account_receivable.id or False
        fpos_id = billing.property_account_position and billing.property_account_position.id or False
        
        line_value = {
            'product_id': k.product,
            'name': tagline
            }
        
        line_dict = objinvoice_line.product_id_change(k.product, False, v['quantity'], '', 'out_invoice', k.billing, fpos_id, price_unit=product.list_price)
        line_value.update(line_dict['value'])
        line_value['price_unit'] = product.list_price
        line_value['quantity'] = v['quantity']
        if line_value.get('invoice_line_tax_id', False):
            tax_tab = [(6, 0, line_value['invoice_line_tax_id'])]
            line_value['invoice_line_tax_id'] = tax_tab
            
        invoice_id = objinvoice.create({
            'partner_id': k.billing,
            'account_id': account_id,
            'fiscal_position': fpos_id or False,
            'origin': tagline,
            'name': tagline
            })
        line_value['invoice_id'] = invoice_id.id
        objinvoice_line.create(line_value)
        if line_value['invoice_line_tax_id']:
            tax_value = objinvoice_tax.compute(invoice_id).values()
            for tax in tax_value:
                objinvoice_tax.create(tax)
        return invoice_id        
