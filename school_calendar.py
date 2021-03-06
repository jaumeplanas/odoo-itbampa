# -*- coding: utf-8 -*-

from datetime import date
from dateutil.rrule import rrule, rruleset, WEEKLY, DAILY, MO, TU, WE, TH, FR

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, Warning

class SchoolCalendarHoliday(models.Model):
    '''Holiday ranges'''

    _name = 'itbampa.school.calendar.holiday'

    name = fields.Char(required=True)
    date_start = fields.Date(string="Date Start", required=True)
    date_end = fields.Date(string="Date End", required=True)
    school_calendar_id = fields.Many2one('itbampa.school.calendar', string="School Calendar")

class SchoolCalendar(models.Model):
    '''School Calendar
    It holds holidays, courses, sessions and so on'''

    _name = 'itbampa.school.calendar'
    _order = 'name desc'

    @api.one
    @api.depends('year')
    def _get_name(self):
        y = self.year
        self.name = "%d - %d" % (y, y+1)
    
    @api.one
    @api.constrains('date_start', 'date_end', 'name', 'holiday_ids')
    def _check_dates(self):
        lang = self._context['lang'] or 'en_US'
        fmtx = self.env['res.lang'].search([('code', '=', lang)], limit=1)
        fmt  = fmtx or fmtx.date_format or '%Y-%m-%d'
        date_start = fields.Date.from_string(self.date_start)
        date_end = fields.Date.from_string(self.date_end)
        allowed_start = date(self.year, 7, 1)
        allowed_end = date(self.year + 1, 6, 30)
        if date_start < allowed_start:
            raise ValidationError(_("Start date (%s) must be after allowed start date (%s)" % (date_start.strftime(fmt), allowed_start.strftime(fmt))))
        if date_start >= allowed_end:
            raise ValidationError(_("Start date (%s) must be before allowed end date (%s)" % (date_start.strftime(fmt), allowed_end.strftime(fmt))))
        if date_end > allowed_end:
            raise ValidationError(_("End date (%s) must be before allowed end date (%s)" % (date_end.strftime(fmt), allowed_end.strftime(fmt))))
        if date_end < date_start:
            raise ValidationError(_("End date (%s) must be after start date (%s)" % (date_end.strftime(fmt), date_start.strftime(fmt))))

    @api.model
    def get_rrules(self, dstart=None, dend=None):
        rr = rruleset()
        rr0 = rrule(WEEKLY, wkst=MO, byweekday=(MO, TU, WE, TH, FR), dtstart=dstart, until=dend)
        rr.rrule(rr0)
        for holiday in self.holiday_ids:
            holiday_date_start = fields.Date.from_string(holiday.date_start)
            holiday_date_end = fields.Date.from_string(holiday.date_end)
            rrz = rrule(DAILY, dtstart=holiday_date_start, until=holiday_date_end)
            rr.exrule(rrz)
        return rr
        
    @api.model
    def count_lective_days(self, dstart=None, dend=None):
        """
        Count lective days between two dates using a Calendar.

        :param dstart: Start date for counting.
        :param dend: End date for counting.
        :return Integer. Lective days between the two dates.

        The most usual purpose of this method is to count lective days, i.e. days with open activity service.
        """
        date_start = fields.Date.from_string(self.date_start)
        date_end = fields.Date.from_string(self.date_end)
        if dstart and (dstart > date_start) and (dstart < date_end):
            date_start = dstart
        if dend and (dend < date_end) and (dend > date_start):
            date_end = dend
        rr = self.get_rrules(date_start, date_end)
        return len(list(rr))
    
    @api.model
    def get_school_calendar_from_date(self, xdate):
        sdate = xdate.isoformat()
        calendar_obj = self.search([
            ('date_start', '<=', sdate),
            ('date_end', '>=', sdate)
            ], limit=1)
        return calendar_obj

    @api.multi
    def _get_lective_dates(self):
        for rec in self:
            rec.lective_dates = rec.count_lective_days()

    @api.model
    def is_lective_day(self, date=None):
        """
        Check if a given date in a given calendar is a lective date.

        @param date: Required. Date to be checked whether it is lective.
        @return: Boolean. True is lective, False it is not.
        """
        if date is None:
            raise Warning(_("Date parameter is required!"))
        date_start = fields.Date.from_string(self.date_start)
        date_end = fields.Date.from_string(self.date_end)
        rr = self.get_rrules(date_start, date_end)
        rr_o = map(lambda x: x.toordinal(), rr)
        date_o = date.toordinal()
        return date_o in rr_o

    name = fields.Char(string="Session", compute='_get_name', store=True)
    year = fields.Integer(string="Year", required=True)
    date_start = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="End Date", required=True)
    holiday_ids = fields.One2many('itbampa.school.calendar.holiday', 'school_calendar_id', string="Holiday Ranges")
    lective_dates = fields.Integer(string="Lective Days", compute='_get_lective_dates')

class ComputeCourseWizard(models.TransientModel):
    _name = 'school.course.compute.wizard'

    def _get_default_school_calendar(self):
        return self.env['itbampa.school.calendar'].browse(self._context.get('active_id'))

    school_calendar_id = fields.Many2one('itbampa.school.calendar', default=_get_default_school_calendar, string="School Calendar")
    state = fields.Selection([('inici', 'inici'), ('final', 'final')], default='inici')
    total_computed = fields.Integer("Total Computed", readonly=True)

    @api.multi
    def action_compute_current_course(self):
        total_computed = 0
        current_year = self.school_calendar_id.year
        partners = self.env['res.partner'].search([('ampa_partner_type', '=', 'student')])
        for partner in partners:
            partner_year = fields.Date.from_string(partner.ampa_birthdate).year
            age = current_year - partner_year - partner.course_lag
            if age in range(3, 12):
                partner.current_course = "%02d" % (age)
            else:
                partner.current_course = '99'
            total_computed += 1
        self.write({'state': 'final', 'total_computed': total_computed})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'school.course.compute.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
            }
