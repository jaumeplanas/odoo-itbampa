# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class ActivityQuickSelectWizard(models.TransientModel):
    
    _name = 'itbampa.activity.quick.select.wizard'
        
    def _get_default_partner_ids(self):
        active_model = self.env.context.get('active_model', None)
        active_ids    = self.env.context.get('active_ids', None)
        if (active_model is None) or (active_ids is None):
            raise ValidationError("This error should not occur!")
        omodel = self.env[active_model].browse(active_ids)
        partner_ids = [p.partner_id.id for p in omodel.partner_ids]
        return [[6, 0, partner_ids]]
    
    product_id  = fields.Many2one('product.product', string="Product")    
    partner_ids = fields.Many2many('res.partner', 'itbampa_act_quick_wiz_rel', 'wiz_partner_id', 'act_partner_id', string="Members", default=_get_default_partner_ids)
    
    @api.one
    def save_quick_select(self):
        active_model = self.env.context.get('active_model', None)
        active_ids    = self.env.context.get('active_ids', None)
        if (active_model is None) or (active_ids is None):
            raise ValidationError("This error should not occur!")
        omodel = self.env[active_model].browse(active_ids)
        partner_dict = dict([(p.partner_id.id, p.id) for p in omodel.partner_ids])
        orig_partners_set = set(partner_dict.iterkeys())
        dest_partners_set = set([p.id for p in self.partner_ids])
        pids = []
        # Partners in orig not in dest -> delete
        delete_set = orig_partners_set - dest_partners_set
        for p in delete_set:
            pids.append([2, partner_dict[p], False])
        # Partners in dest not in orig -> add with defaults
        add_set = dest_partners_set - orig_partners_set
        for p in add_set:
            partner_id = self.env['res.partner'].browse([p])
            billing_id = partner_id.get_default_billing_partner_id()
            if billing_id is None:
                err_msg = _("Member {} (AMPA Partner Type = {}) has no valid Billing Partner defined.").format(partner_id.name, partner_id.ampa_partner_type)
                raise ValidationError(err_msg)
            pids.append([0, None, {
                'partner_id': p,
                'billing_partner_id': billing_id.id,
                'product_id': self.product_id.id
                }])
        omodel.sudo().write({'partner_ids': pids})

        