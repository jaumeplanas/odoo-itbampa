# -*- coding: utf-8 -*-
"""AMPA Member"""


from openerp import models, fields
# from openerp.exceptions import ValidationError

AMPA_PARTNER_TYPES = [
        ("tutor", "Tutor"),
        ("student", "Student")
]

COURSE_AGES = [
        ('03', 'P3 Infantil'),
        ('04', 'P4 Infantil'),
        ('05', 'P5 Infantil'),
        ('06', '1r Primària'),
        ('07', '2n Primària'),
        ('08', '3r Primària'),
        ('09', '4t Primària'),
        ('10', '5è Primària'),
        ('11', '6è Primària'),
        ('99', 'N/D')
]


class Partner(models.Model):
    """Class Partner"""

    _inherit = "res.partner"
    
    def get_default_billing_partner_id(self):
        if self.billing_partner_id:
            res = self.billing_partner_id
        else:
            res = None
            if self.ampa_partner_type == 'student':
                for x in self.partner_tutor_ids:
                    if x.customer_payment_mode:
                        if len(x.bank_ids) > 0:
                            res = x
                            break
                    else:
                        res = x
                        break
            elif self.ampa_partner_type == 'tutor':
                if self.customer_payment_type:
                    if len(self.bank_ids) > 0:
                        res = self
                else:
                    res = self
        return res
    
    ampa_partner_type = fields.Selection(
            AMPA_PARTNER_TYPES, string="AMPA Partner Type")
    partner_child_ids = fields.Many2many(
            'res.partner', 'res_partner_rel', 'tutor_id', 'child_id', string="Partner Childs")
    partner_tutor_ids = fields.Many2many(
            'res.partner', 'res_partner_rel', 'child_id', 'tutor_id', string="Partner Tutors")
    ampa_birthdate = fields.Date(string="Birthday")
    course_lag = fields.Integer(string="Lagging courses", default=0)
    billing_partner_id = fields.Many2one(
            "res.partner", string="Billing Member", ondelete="set null")
    current_course = fields.Selection(
            COURSE_AGES, string="Current Course", readonly=True, default='99')
