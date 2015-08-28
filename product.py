# -*- coding: utf-8 -*-
from openerp import models, fields

class ProductTemplate(models.Model):
    """Product Template including AMPA Product type"""
    
    _inherit = 'product.template'
    
    is_ampa_product = fields.Boolean(string="Is AMPA product")
    
    