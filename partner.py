# -*- coding: utf-8 -*-
"""AMPA Member"""


from openerp import models, fields, api, _
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
    
    @api.one
    @api.constrains('activity_partner_ids')
    def _check_billing_partner(self):
        # For each activity, get partner
        for act in self.activity_partner_ids:
            if len(act.billing_partner_id.bank_ids) < 1:
                raise ValidationError(
                    _("At least one Bank ID is required for Billing Member %s for Activity %s") % (act.billing_partner_id.name, act.activity_type_id.name))

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
    activity_partner_ids = fields.One2many('itbampa.activity.partner.line', 'partner_id', string="Activity Members")

class ActivityPartnerLine(models.Model):
    _name = 'itbampa.activity.partner.line'
    
    def _get_default_billing(self):
        print self.env.context
        print self
        return False
    
    activity_type_id   = fields.Many2one('itbampa.activity.type', string="Activity Type", required=True)
    partner_id         = fields.Many2one('res.partner', string="Member", required=True)
    billing_partner_id = fields.Many2one('res.partner', string="Billing Partner", required=True)
    product_id         = fields.Many2one('product.product', string="Product", required=True)
    