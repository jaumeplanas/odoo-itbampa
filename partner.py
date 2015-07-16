# -*- coding: utf-8 -*-
from datetime import date
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

AMPA_PARTNER_TYPES = [
  ("tutor", "Tutor"),
  ("student", "Student")
]

COURSE_AGES = [
    ('0', 'N/D'),
    ('3', 'P3 Infantil'),
    ('4', 'P4 Infantil'),
    ('5', 'P5 Infantil'),
    ('6', '1r Primària'),
    ('7', '2n Primària'),
    ('8', '3r Primària'),
    ('9', '4t Primària'),
    ('10', '5è Primària'),
    ('11', '6è Primària')
]

class Partner(models.Model):
    """AMPA Member"""
    _inherit = "res.partner"

    @api.model
    def get_billing_partner(self):
        if (self.ampa_partner_type in ['tutor']):
            billing_partner = self
        else:
            billing_partner = self.billing_partner_id

    ampa_partner_type = fields.Selection(AMPA_PARTNER_TYPES, "AMPA Partner Type")
    partner_child_ids = fields.Many2many('res.partner', 'res_partner_rel', 'tutor_id', 'child_id')
    partner_tutor_ids = fields.Many2many('res.partner', 'res_partner_rel', 'child_id', 'tutor_id')
    ampa_birthdate = fields.Date("Birthday")
    course_lag = fields.Integer("Lagging courses", default=0)
    billing_partner_id = fields.Many2one("res.partner", "Billing Partner", ondelete="set null")
    current_course = fields.Selection(COURSE_AGES, "Current Course", readonly=True, default='0')
