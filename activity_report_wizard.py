# -*- coding: utf-8 -*-

from datetime import date
from dateutil.relativedelta import relativedelta

from openerp import models, fields, api

class ActivityReportWizard(models.TransientModel):
    """Wizard to select School Calendar for Monthly Activity Attendance"""
    _name = 'itbampa.activity.report.wizard'
    
    def _get_default_school_calendar(self):
        return self.env['itbampa.school.calendar'].search([], limit=1)
    
    @api.onchange('school_calendar_id')
    def _get_month_id(self):
        dtstart = self.school_calendar_id.date_start
        dtend = self.school_calendar_id.date_end
        school_id = self.school_calendar_id.id
        month_obj = self.env['itbampa.activity.report.wizard.month']
        for x in month_obj.search([]):
            x.unlink()
        if (dtstart > '1971-01-01') and (dtend > '1971-01-01'):
            self._cr.execute("""
                SELECT EXTRACT(YEAR from date_start) AS year, EXTRACT(MONTH from date_start) AS month
                FROM itbampa_activity_event
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
                SELECT p.name AS partner, t.name_template AS product, count(*) AS total 
                FROM itbampa_activity_event_partner e
                JOIN itbampa_activity_event l ON l.id = e.activity_event_id
                JOIN res_partner p ON p.id = e.partner_id
                JOIN product_product t ON t.id = e.product_id
                WHERE l.date_start BETWEEN %s AND %s
                GROUP BY p.name, t.name_template
                """, (dtstart, dtend))
            line_obj = zz = self.env['itbampa.activity.report.wizard.line']
        
            for x in self._cr.dictfetchall():
                z = line_obj.create({
                    'partner': x['partner'],
                    'product': x['product'],
                    'total': int(x['total']),
                    })
                zz += z
            self.line_ids = zz
            
            self.lective_days = self.school_calendar_id.count_lective_days(dstart=dtstart_o, dend=dtend_o)
            
    school_calendar_id = fields.Many2one('itbampa.school.calendar', string="School Calendar", required=True, default=_get_default_school_calendar)
    month_id = fields.Many2one('itbampa.activity.report.wizard.month', required=True, ondelete="cascade", string="Mes")
    line_ids = fields.One2many('itbampa.activity.report.wizard.line', 'wizard_id', compute='_get_line_ids')
    lective_days = fields.Integer(string="Total Lective Days", compute='_get_line_ids', store=True)
    
    @api.multi
    def create_invoices(self):
        y = self.month_id.year
        m = self.month_id.month
        adate = date(y, m, 1)
        self.env['itbampa.activity.event'].create_invoices(xdate = adate, lective_days = self.lective_days)        
        return {'type':'ir.actions.act_window_close'}
    
    @api.multi
    def print_monthly_report(self):
        return {
            'context': self._context,
            'data': {},
            'type': 'ir.actions.report.xml',
            'report_name': 'itbampa.activity_monthly_report',
            'report_type': 'qweb-html',
            'report_file': 'itbampa.activity_monthly_report',
            }
            
class ActivityReportWizardLines(models.TransientModel):
    _name = 'itbampa.activity.report.wizard.line'
    _order = 'partner, product'
    
    wizard_id = fields.Many2one('itbampa.activity.report.wizard', ondelete="cascade")
    partner = fields.Char(string="Member")
    product = fields.Char(string="Product")
    total = fields.Integer(string="Total")

class ActivityReportWizardMonths(models.TransientModel):
    _name = 'itbampa.activity.report.wizard.month'
    _order = 'year, month'
    
    @api.one
    @api.depends('year', 'month')
    def _get_month_name(self):
        if self.year > 0 and self.month > 0:
            self.name = date(self.year, self.month, 1).strftime('%B %Y')
    
    name = fields.Char(string="Month", compute='_get_month_name', store=True)
    year = fields.Integer(string="Year")
    month = fields.Integer(string="Month")   
    
class ActivityCustomReport(models.AbstractModel):
    _name = 'report.itbampa.activity_monthly_report'
    
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('itbampa.activity_monthly_report')
        active_id = self._context.get('active_id')
        wizard_obj = self.env[report.model].browse(active_id)
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': wizard_obj,
        }
        return report_obj.render('itbampa.activity_monthly_report', docargs)
