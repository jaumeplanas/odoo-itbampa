# -*- coding: utf-8 -*-
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

    """AMPA Member"""
    _inherit = "res.partner"

    @api.constrains('lunch_product_id', 'billing_partner_id')
    def _check_billing(self):
        for record in self:
            if record.lunch_product_id.id is not False:
                if record.billing_partner_id.id is False:
                    raise ValidationError(
                            "A Billing Partner is required when selecting a Lunch Product")
                if len(record.billing_partner_id.bank_ids) < 1:
                    raise ValidationError(
                            "At least one Bank ID is required for Billing Partner")

    ampa_partner_type = fields.Selection(
            AMPA_PARTNER_TYPES, "AMPA Partner Type", default='student')
    partner_child_ids = fields.Many2many(
            'res.partner', 'res_partner_rel', 'tutor_id', 'child_id')
    partner_tutor_ids = fields.Many2many(
            'res.partner', 'res_partner_rel', 'child_id', 'tutor_id')
    ampa_birthdate = fields.Date("Birthday")
    course_lag = fields.Integer("Lagging courses", default=0)
    billing_partner_id = fields.Many2one(
            "res.partner", "Billing Partner", ondelete="set null")
    current_course = fields.Selection(
            COURSE_AGES, "Current Course", readonly=True, default='99')
    is_lunch_subscribed = fields.Boolean("Is subscribed to lunchs?")
    lunch_product_id = fields.Many2one(
            'product.product', "Lunch Product", ondelete='set null')
    lunch_ids = fields.One2many('itbampa.lunch.event.partner', 'partner_id')
