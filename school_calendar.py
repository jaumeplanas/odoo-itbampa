# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, Warning
from datetime import date
from dateutil.rrule import *

def _session_name_get():
    year = date.today().year
    return [(str(x), '%d-%d' % (x, x+1)) for x in reversed(range(year-10,year+10))]

class SchoolCalendarHoliday(models.Model):
    '''Holiday ranges'''

    _name = 'itbampa.school.calendar.holiday'

    name = fields.Char(required=True)
    date_start = fields.Date(string="Date Start", required=True)
    date_end = fields.Date(string="Date End", required=True)
    school_calendar_id = fields.Many2one('itbampa.school.calendar', "School Calendar")

class SchoolCalendar(models.Model):
    '''School Calendar
    It holds holidays, courses, sessions and so on'''

    _name = 'itbampa.school.calendar'
    _order = 'name desc'

    @api.one
    @api.constrains('date_start', 'date_end', 'name', 'holiday_ids')
    def _check_dates(self):
        lang = self._context['lang'] or 'en_US'
        fmt = self.env['res.lang'].search([('code', '=', lang)], limit=1).date_format
        date_start = fields.Date.from_string(self.date_start)
        date_end = fields.Date.from_string(self.date_end)
        allowed_start = date(int(self.name), 7, 1)
        allowed_end = date(int(self.name) + 1, 6, 30)
        if date_start < allowed_start:
            raise ValidationError(_("Start date (%s) must be after allowed start date (%s)" % (date_start.strftime(fmt), allowed_start.strftime(fmt))))
        if date_start >= allowed_end:
            raise ValidationError(_("Start date (%s) must be before allowed end date (%s)" % (date_start.strftime(fmt), allowed_end.strftime(fmt))))
        if date_end > allowed_end:
            raise ValidationError(_("End date (%s) must be before allowed end date (%s)" % (date_end.strftime(fmt), allowed_end.strftime(fmt))))
        if date_end < date_start:
            raise ValidationError(_("End date (%s) must be after start date (%s)" % (date_end.strftime(fmt), date_start.strftime(fmt))))

    @api.model
    def count_lective_days(self, dstart=None, dend=None):
        """
        Count lective days between two dates using a Calendar.

        @param dstart: Start date for counting.
        @param dend: End date for counting.
        @return Integer. Lective days between the two dates.

        The most usual purpose of this method is to count lective days, i.e. days with open lunch service.
        """
        date_start = fields.Date.from_string(self.date_start)
        date_end = fields.Date.from_string(self.date_end)
        if dstart and (dstart > date_start) and (dstart < date_end):
            date_start = dstart
        if dend and (dend < date_end) and (dend > date_start):
            date_end = dend
        rr = rruleset()
        rr0 = rrule(WEEKLY, wkst=MO, byweekday=(MO, TU, WE, TH, FR), dtstart=date_start, until=date_end)
        rr.rrule(rr0)
        for holiday in self.holiday_ids:
            holiday_date_start = fields.Date.from_string(holiday.date_start)
            holiday_date_end   = fields.Date.from_string(holiday.date_end)
            rrz = rrule(DAILY, dtstart=holiday_date_start, until=holiday_date_end)
            rr.exrule(rrz)
        return len(list(rr))

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
        rr = rruleset()
        rr0 = rrule(WEEKLY, wkst=MO, byweekday=(MO, TU, WE, TH, FR), dtstart=date_start, until=date_end)
        rr.rrule(rr0)
        for holiday in self.holiday_ids:
            holiday_date_start = fields.Date.from_string(holiday.date_start)
            holiday_date_end   = fields.Date.from_string(holiday.date_end)
            rrz = rrule(DAILY, dtstart=holiday_date_start, until=holiday_date_end)
            rr.exrule(rrz)
        rr_o = map(lambda x: x.toordinal(), rr)
        date_o = date.toordinal()
        return date_o in rr_o

    @api.multi
    def _is_lective_date(self):
        for rec in self:
            rec.is_lective = rec.is_lective_day(date(2015, 6, 23))

    name = fields.Selection(_session_name_get(), string="Session", required=True)
    date_start = fields.Date("Start Date", required=True)
    date_end = fields.Date("End Date", required=True)
    holiday_ids = fields.One2many('itbampa.school.calendar.holiday', 'school_calendar_id')
    lective_dates = fields.Integer("Lective Days", compute='_get_lective_dates')
    is_lective = fields.Boolean("Is 2015-06-23 Lective Day", compute='_is_lective_date')
