# -*- coding: utf-8 -*-
from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError

class TestPartner(TransactionCase):
    
    def test_create_default_student(self):
        record = self.env['res.partner'].with_context(default_ampa_partner_type='student').create({'name': 'Test Partner'})
        self.assertEqual(record.ampa_partner_type, 'student')
                
