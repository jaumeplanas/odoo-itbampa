# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY


class LunchEventEaters(models.Model):
    _name = 'itbampa.lunch.event.partner'

    lunch_id = fields.Many2one('itbampa.lunch.event', string="Lunch Event", required=True, ondelete='cascade')
    partner_id = fields.Many2one(
            'res.partner', string="Lunch Eater", domain="[('ampa_partner_type', 'in', ['tutor', 'student'])]", required=True, ondelete='cascade')
    comment = fields.Char("Comment")
    lunch_product_id = fields.Many2one('product.product', "Lunch Product", required=True, ondelete='cascade')


class LunchEvent(models.Model):

    '''Lunch Event.'''

    _name = 'itbampa.lunch.event'
    _order = 'date_start desc'

    @api.multi
    @api.depends('eater_ids')
    def _compute_total_eaters(self):
        for record in self:
            record.total_eaters = len(record.eater_ids)

    @api.onchange('date_start')
    def _on_change_name(self):
        if self.date_start:
            lang = self._context['lang'] or 'en_US'
            fmt = self.env['res.lang'].search(
                    [('code', '=', lang)], limit=1).date_format
            self.name = fields.Date().from_string(self.date_start).strftime(fmt)

    def _get_lunch_registered(self):
        pids = []
        for x in self.env['res.partner'].search([('is_lunch_subscribed', '=', True)]):
            pids.append([0, 0, {'partner_id': x.id, 'lunch_product_id': x.lunch_product_id}])
        return pids

    @api.one
    def update_with_registered(self):
        pids = []
        registered_set = set([x.id for x in self.env['res.partner'].search([('is_lunch_subscribed', '=', True)])])
        current_set = set([y.partner_id.id for y in self.eater_ids])
        intersect_list = list(registered_set - current_set)
        intersect_objs = self.env['res.partner'].browse(intersect_list)
        for z in intersect_objs:
            pids.append([0, 0, {'partner_id': z.id, 'lunch_product_id': z.lunch_product_id.id}])
        self.write({'eater_ids': pids})

    name = fields.Char("Name")
    date_start = fields.Date(
            "Start Date", required=True, default=fields.Date.today())
    date_stop = fields.Date("End Date", default=fields.Date.today())
    all_day = fields.Boolean("All Day", default=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    eater_ids = fields.One2many(
            'itbampa.lunch.event.partner', 'lunch_id', default=_get_lunch_registered)
    state = fields.Selection(
            [('open', 'Open'), ('closed', 'Closed'), ('billed', 'Billed')], string="State", default='open')
    total_eaters = fields.Integer(
            "Total Registered", compute='_compute_total_eaters', store=True)

    @api.one
    def action_closed(self):
        self.state = 'closed'

    @api.one
    def action_open(self):
        self.state = 'open'

    @api.one
    def action_billed(self):
        pass

    # When called from code
    # self.signal_workflow('bill_lunch_event')
    
class LunchReportWizard(models.TransientModel):
    """Wizard to select School Calendar for Monthly Lunch Attendants"""
    _name = 'itbampa.lunch.report.wizard'
    
    def _get_default_school_calendar(self):
        return self.env['itbampa.school.calendar'].search([], limit=1)
    
    school_calendar_id = fields.Many2one('itbampa.school.calendar', string="School Calendar", required=True, default=_get_default_school_calendar)
    
    
    @api.multi
    def print_monthly_report(self):
        
        
#        return self.env['report'].get_action(self._ids, 'itbampa.lunch_monthly_report_action', data=data)

        return {
            'context': self._context,
            'data': {},
            'type': 'ir.actions.report.xml',
            'report_name': 'itbampa.lunch_monthly_report',
            'report_type': 'qweb-html',
            'report_file': 'itbampa.lunch_monthly_report',
            }


class LunchCustomReport(models.AbstractModel):
    _name = 'report.itbampa.lunch_monthly_report'
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('itbampa.lunch_monthly_report')
        wizo = self.env[report.model].browse(self._context.get('active_id'))
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self._context,
            'data': ['Tres', 'Dos'],
            'calendar': wizo.school_calendar_id,
        }
        return report_obj.render('itbampa.lunch_monthly_report', docargs)
