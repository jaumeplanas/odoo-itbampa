# -*- coding: utf-8 -*-
from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError
#from openerp import fields
from datetime import date

class TestSchoolCalendar(TransactionCase):
    
    def test_check_date_after_start_allowed(self):
        """ Test when Start Date is before allowed Start Date (before Jun 1st)"""
        with self.assertRaises(ValidationError):
            self.env['itbampa.school.calendar'].create({
                'name': 'School Calendar Test',
                'year': 2015,
                'date_start': '2015-01-01',
                'date_end': '2016-05-01',
                })        
            
    def test_check_date_start_before_end_allowed(self):
        """ Test when Start Date is after End Date. """
        with self.assertRaises(ValidationError):
            self.env['itbampa.school.calendar'].create({
                'name': 'School Calendar Test',
                'year': 2015,
                'date_end': '2016-05-01',
                'date_start': '2016-08-01',
                })        

    def test_check_date_end_before_end_allowed(self):
        """ Test when End Date is after allowed End Date."""
        with self.assertRaises(ValidationError):
            self.env['itbampa.school.calendar'].create({
                'name': 'School Calendar Test',
                'year': 2015,
                'date_start': '2015-09-01',
                'date_end': '2016-08-01',
                })
            
    def test_check_date_end_after_start(self):
        """ Test when End Date is before Start Date. """
        with self.assertRaises(ValidationError):
            self.env['itbampa.school.calendar'].create({
                'name': 'School Calendar Test',
                'year': 2015,
                'date_start': '2015-09-01',
                'date_end': '2015-08-15',
                })
            
    def test_count_lective_days(self):
        """ Test calculation of lective days between two dates. """
        dstart = date(2015, 10, 2)
        dend = date(2015, 10, 8)
        rec = self.env['itbampa.school.calendar'].with_context(lang='ca_ES').create({
            'date_end': '2016-06-22', 
            'date_start': '2015-09-14', 
            'year': 2015})
        total = rec.count_lective_days(dstart, dend)
        self.assertEqual(total, 5)

    def test_is_lective_day_yes(self):
        """ Test if a date is a lective day. """
        dstart = date(2015, 10, 2)
        sch = self.env['itbampa.school.calendar'].with_context(lang='ca_ES').create({
            'year': 2015,
            'date_start': '2015-09-14',
            'date_end': '2016-05-22'
            })
        self.assertTrue(sch.is_lective_day(dstart))
        
    def test_is_lective_day_no(self):
        """ Test if a date is not a lective day. """
        dstart = date(2015, 10, 17)
        sch = self.env['itbampa.school.calendar'].with_context(lang='ca_ES').create({
            'year': 2015,
            'date_start': '2015-09-14',
            'date_end': '2016-05-22'
            })
        self.assertFalse(sch.is_lective_day(dstart))
        