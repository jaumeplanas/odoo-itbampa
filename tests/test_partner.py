# -*- coding: utf-8 -*-
from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError

class TestPartner(TransactionCase):
    
    def test_create_default_student(self):
        record = self.env['res.partner'].create({'name': 'Test Partner'})
        self.assertEqual(record.ampa_partner_type, 'student')
        
    def test_no_billing_partner(self):
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        product = self.browse_ref('itbampa.product_product_lunch_1')
        with self.assertRaises(ValidationError):
            partner.lunch_product_id = product

    def test_no_billing_partner_bank(self):
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        product = self.browse_ref('itbampa.product_product_lunch_1')
        partner.billing_partner = partner
        with self.assertRaises(ValidationError):
            partner.lunch_product_id = product
            
        
