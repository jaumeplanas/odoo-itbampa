# -*- coding: utf-8 -*-
"""AMPA Member"""


from openerp import models, fields, api
from openerp.exceptions import ValidationError

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

    @api.constrains('lunch_product_id', 'billing_partner_id')
    def _check_billing(self):
        for record in self:
            for activity in record.activity_partner_ids:
                if activity.partner_id.billing_partner_id is False:
                    raise ValidationError(
                            "A Billing Member is required when selecting an Activity")
                if len(activity.partner_id.billing_partner_id.bank_ids) < 1:
                    raise ValidationError(
                            "At least one Bank ID is required for Billing Member")

    ampa_partner_type = fields.Selection(
            AMPA_PARTNER_TYPES, "AMPA Partner Type")
    partner_child_ids = fields.Many2many(
            'res.partner', 'res_partner_rel', 'tutor_id', 'child_id', string="Partner Childs")
    partner_tutor_ids = fields.Many2many(
            'res.partner', 'res_partner_rel', 'child_id', 'tutor_id', string="Partner Tutors")
    ampa_birthdate = fields.Date("Birthday")
    course_lag = fields.Integer("Lagging courses", default=0)
    billing_partner_id = fields.Many2one(
            "res.partner", "Billing Member", ondelete="set null")
    current_course = fields.Selection(
            COURSE_AGES, "Current Course", readonly=True, default='99')
    activity_partner_ids = fields.One2many('itbampa.activity.partner.line', 'partner_id', string="Activity Members")

class ActivityPartnerLine(models.Model):
    _name = 'itbampa.activity.partner.line'
    
    activity_type_id = fields.Many2one('itbampa.activity.type', string="Activity Type")
    partner_id       = fields.Many2one('res.partner', string="Member", required=True)
    product_id       = fields.Many2one('product.product', string="Product", required=True)
    