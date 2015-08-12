# -*- coding: utf-8 -*-

from openerp import models, fields, api
# from openerp.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


class LunchEventEaters(models.Model):
    _name = 'itbampa.lunch.event.partner'

    lunch_id = fields.Many2one('itbampa.lunch.event', string="Lunch Event", required=True, ondelete='cascade')
    partner_id = fields.Many2one(
            'res.partner', string="Lunch Eater", domain="[('ampa_partner_type', 'in', ['tutor', 'student'])]", required=True, ondelete='cascade')
    partner_current_course = fields.Selection("Current Course", related="partner_id.current_course")
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
            record.total_eaters = len(record.eater_ids) # @

    @api.multi
    @api.depends('date_start')
    def _on_change_name(self):
        lang = self._context['lang'] or 'en_US'
        fmt = self.env['res.lang'].search([('code', '=', lang)], limit=1).date_format
        for record in self:
            record.name = fields.Date().from_string(record.date_start).strftime(fmt)

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

    name = fields.Char("Name", compute='_on_change_name', store=True)
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
    
    @api.onchange('school_calendar_id')
    def _get_month_id(self):
        dtstart = self.school_calendar_id.date_start
        dtend = self.school_calendar_id.date_end
        school_id = self.school_calendar_id.id
        month_obj = self.env['itbampa.lunch.report.wizard.month']
        for x in month_obj.search([]):
            x.unlink()
        if (dtstart > '1971-01-01') and (dtend > '1971-01-01'):
            self._cr.execute("""
                SELECT EXTRACT(YEAR from date_start) AS year, EXTRACT(MONTH from date_start) AS month
                FROM itbampa_lunch_event
                WHERE date_start BETWEEN %s AND %s
                GROUP BY EXTRACT(YEAR from date_start), EXTRACT(MONTH from date_start)
            """, (dtstart, dtend))
            for x in self._cr.dictfetchall():
                month_obj.create({
                    'year': int(x['year']),
                    'month': int(x['month']),
                    })
        school_obj = self.env['itbampa.school.calendar'].browse(school_id)
        month = month_obj.search([], limit=1)
        self.school_calendar_id = school_obj
        self.month_id = month
                
    @api.one
    @api.depends('month_id')
    def _get_line_ids(self):
        if self.month_id:
            dtstart_o = date(self.month_id.year, self.month_id.month, 1)
            dtend_o = dtstart_o + relativedelta(day=31)
            dtstart = dtstart_o.isoformat()
            dtend = dtend_o.isoformat()
            for line in self.line_ids:
                line.unlink()
            self._cr.execute("""
                SELECT p.name AS partner, count(*) AS total 
                FROM itbampa_lunch_event_partner e
                JOIN itbampa_lunch_event l ON l.id = e.lunch_id
                JOIN res_partner p ON p.id = e.partner_id
                WHERE l.date_start BETWEEN %s AND %s
                GROUP BY p.name
                """, (dtstart, dtend))
            line_obj = zz = self.env['itbampa.lunch.report.wizard.line']
        
            for x in self._cr.dictfetchall():
                z = line_obj.create({
                    'partner': x['partner'],
                    'total': int(x['total']),
                    })
                zz += z
            self.line_ids = zz
            
            self.lective_days = self.school_calendar_id.count_lective_days(dstart=dtstart_o, dend=dtend_o)
            
    school_calendar_id = fields.Many2one('itbampa.school.calendar', string="School Calendar", required=True, default=_get_default_school_calendar)
    month_id = fields.Many2one('itbampa.lunch.report.wizard.month', required=True, ondelete="cascade")
    line_ids = fields.One2many('itbampa.lunch.report.wizard.line', 'wizard_id', compute='_get_line_ids')
    lective_days = fields.Integer("Total Lective Days", compute='_get_line_ids')
    
    
    @api.multi
    def print_monthly_report(self):
        return {
            'context': self._context,
            'data': {},
            'type': 'ir.actions.report.xml',
            'report_name': 'itbampa.lunch_monthly_report',
            'report_type': 'qweb-html',
            'report_file': 'itbampa.lunch_monthly_report',
            }
            
class LunchReportWizardLines(models.TransientModel):
    _name = 'itbampa.lunch.report.wizard.line'
    
    wizard_id = fields.Many2one('itbampa.lunch.report.wizard', ondelete="cascade")
    partner = fields.Char("Partner")
    total = fields.Integer("Total")

class LunchReportWizardMonths(models.TransientModel):
    _name = 'itbampa.lunch.report.wizard.month'
    _order = 'year, month'
    
    @api.one
    @api.depends('year', 'month')
    def _get_month_name(self):
        if self.year > 0 and self.month > 0:
            self.name = date(self.year, self.month, 1).strftime('%B %Y')
    
    name = fields.Char("Month", compute='_get_month_name', store=True)
    year = fields.Integer()
    month = fields.Integer()   
    
class LunchCustomReport(models.AbstractModel):
    _name = 'report.itbampa.lunch_monthly_report'
    
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('itbampa.lunch_monthly_report')
        active_id = self._context.get('active_id')
        wizard_obj = self.env[report.model].browse(active_id)
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': wizard_obj,
        }
        return report_obj.render('itbampa.lunch_monthly_report', docargs)
