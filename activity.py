# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
#from datetime import date
#from dateutil.relativedelta import relativedelta

class ActivityType(models.Model):
    _name = 'itbampa.activity.type'
    
    name = fields.Char(string="Activity Type", required=True)
    default_product_id = fields.Many2one('product.product', domain="[('is_ampa_product', '=', True)]", string="Default Product")
    partner_ids = fields.One2many('itbampa.activity.type.partner', 'activity_type_id', string="Members Subscribed")
    
class ActivityTypePartner(models.Model):
    _name = 'itbampa.activity.type.partner'
    
    @api.one
    @api.constrains('billing_partner_id')
    def _check_billing_partner(self):
        if self.billing_partner_id.customer_payment_mode and len(self.billing_partner_id.bank_ids) < 1:
            raise ValidationError(
                _("At least one Bank ID is required for Billing Member {0}").format(self.billing_partner_id.name))

    @api.onchange('partner_id')
    def _onchangepartnerid(self):
        p = self.partner_id
        if p:
            b = p.get_default_billing_partner_id()
            if b:
                self.billing_partner_id = b

    activity_type_id = fields.Many2one('itbampa.activity.type', string="Activity Type", required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string="Member", domain="[('ampa_partner_type', 'in', ['tutor', 'student'])]", required=True, ondelete='cascade')
    billing_partner_id = fields.Many2one(
            'res.partner', string="Billing Member", domain="[('ampa_partner_type', 'in', ['tutor'])]", required=True, ondelete='cascade')
    partner_current_course = fields.Selection(related="partner_id.current_course", string="Current Course")
    product_id = fields.Many2one('product.product', domain="[('is_ampa_product', '=', True)]", string="Product", required=True, ondelete='cascade')
    
    
class ActivityEventPartner(models.Model):
    _name = 'itbampa.activity.event.partner'
    _order = 'partner_current_course, partner_id'
        
    @api.one
    @api.constrains('billing_partner_id')
    def _check_billing_partner(self):
        if self.billing_partner_id.customer_payment_mode and len(self.billing_partner_id.bank_ids) < 1:
            raise ValidationError(
                _("At least one Bank ID is required for Billing Member {0}").format(self.billing_partner_id.name))

    @api.onchange('partner_id')
    def _onchangepartnerid(self):
        p = self.partner_id
        if p:
            b = p.get_default_billing_partner_id()
            if b:
                self.billing_partner_id = b

    activity_event_id = fields.Many2one('itbampa.activity.event', string="Activity Event", required=True, ondelete='cascade')
    partner_id = fields.Many2one(
            'res.partner', string="Member", domain="[('ampa_partner_type', 'in', ['tutor', 'student'])]", required=True, ondelete='restrict')
    billing_partner_id = fields.Many2one(
            'res.partner', string="Billing Member", required=True, ondelete='restrict')
    partner_current_course = fields.Selection(related="partner_id.current_course", string="Current Course", store=True)
    comment = fields.Char(string="Comment")
    product_id = fields.Many2one('product.product', string="Product", required=True, ondelete='restrict')
    # For graph view
    date_start = fields.Date(string="Date Start", related='activity_event_id.date_start', store=True)
    school_calendar_id = fields.Many2one('itbampa.school.calendar', related='activity_event_id.school_calendar_id', string="School Calendar", store="True")
    invoice_id = fields.Many2one('account.invoice', 'Invoice', readonly=True)


class ActivityEvent(models.Model):

    '''Activity Event.'''

    _name = 'itbampa.activity.event'
    _order = 'date_start desc'

    @api.multi
    @api.depends('partner_ids')
    def _compute_total_partners(self):
        for record in self:
            record.total_partners = len(record.partner_ids)  # 

    @api.one
    @api.depends('date_start')
    def _get_name_and_school_calendar(self):
        lang = self._context.get('lang', 'ca_ES')
        fmt = self.env['res.lang'].search([('code', '=', lang)], limit=1).date_format
        odate = fields.Date().from_string(self.date_start)
        self.name = odate.strftime(fmt)
        ocalendar = self.env['itbampa.school.calendar'].get_school_calendar_from_date(odate)
        self.school_calendar_id = ocalendar

    @api.onchange('date_start')
    def _check_school_calendar_id(self):
        if not self.school_calendar_id:
            return {
                'warning': {
                    'title': _('No School Calendar associated'),
                    'message': _('No School Calendar associated to this date. Please consider to create a new School Calendar that includes this date or to change the date.')
                    }
                }
            
    @api.onchange('activity_type_id')
    def _on_change_activity_type(self):
        self.update_with_subscribed()
    
    @api.one
    def update_with_subscribed(self):
        pids = []
        set_event = set(x.partner_id for x in self.partner_ids)
        set_activ = set(x.partner_id for x in self.activity_type_id.partner_ids)
        set_new   = set_activ - set_event
        list_new  = [x.id for x in set_new]
        objs = self.env['itbampa.activity.type.partner'].search([
            ('activity_type_id', '=', self.activity_type_id.id),
            ('partner_id', 'in', list_new)
            ])
        for obj in objs:
            pids.append([0, 0, {
                'partner_id': obj.partner_id.id,
                'billing_partner_id': obj.billing_partner_id.id,
                'product_id': obj.product_id.id
                }])
        if len(pids) > 0:
            self.partner_ids = pids
            
    name = fields.Char("Name", compute='_get_name_and_school_calendar', store=True)
    activity_type_id = fields.Many2one('itbampa.activity.type', string="Activity Type", required=True)
    date_start = fields.Date(
            "Start Date", required=True, default=fields.Date.today())
    date_stop = fields.Date("End Date", default=fields.Date.today())
    all_day = fields.Boolean("All Day", default=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    partner_ids = fields.One2many(
            'itbampa.activity.event.partner', 'activity_event_id', string="Members")
    state = fields.Selection(
            [('open', 'Open'), ('closed', 'Closed'), ('billed', 'Billed')], string="State", default='open')
    total_partners = fields.Integer(
            "Total Registered", compute='_compute_total_partners', store=True)
    school_calendar_id = fields.Many2one('itbampa.school.calendar', string="School Calendar", compute='_get_name_and_school_calendar', store=True)
    activity_product_id = fields.Many2one('product.product', string="Default Product", related='activity_type_id.default_product_id')
    
    @api.one
    def action_closed(self):
        self.state = 'closed'

    @api.one
    def action_open(self):
        self.state = 'open'

    @api.one
    def action_billed(self):
        self.state = 'billed'

    # When called from code
    # self.signal_workflow('bill_activity_event')
    