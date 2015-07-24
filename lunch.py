# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class LunchEventEaters(models.Model):
  _name = 'itbampa.lunch.event.partner'

  lunch_id = fields.Many2one('itbampa.lunch.event', string="Lunch Event", required=True)
  partner_id = fields.Many2one(
      'res.partner', string="Lunch Eater", domain="[('ampa_partner_type', 'in', ['tutor', 'student'])]", required=True)
  comment = fields.Char("Comment")
  lunch_product_id = fields.Many2one('product.product', "Lunch Product", required=True)


class LunchEvent(models.Model):

  '''Lunch Event.'''

  _name = 'itbampa.lunch.event'
  _order = 'date_start desc'

  @api.multi
  @api.depends('eater_ids')
  def _compute_total_eaters(self):
    for record in self:
      record.total_eaters = len(record.eater_ids)

  @api.onchange('date_start')
  def _on_change_name(self):
    d = 'undef'
    if self.date_start:
      lang = self._context['lang'] or 'en_US'
      fmt = self.env['res.lang'].search(
          [('code', '=', lang)], limit=1).date_format
      self.name = fields.Date().from_string(self.date_start).strftime(fmt)

  def _get_lunch_registered(self):
    pids = []
    for x in self.env['res.partner'].search([('is_lunch_subscribed', '=', True)]):
      pids.append([0, 0, {'partner_id': x.id, 'lunch_product_id': x.lunch_product_id}])
    return pids

  name = fields.Char("Name")
  date_start = fields.Date(
      "Start Date", required=True, default=fields.Date.today())
  date_stop = fields.Date("End Date", default=fields.Date.today())
  all_day = fields.Boolean("All Day", default=True)
  user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
  eater_ids = fields.One2many(
      'itbampa.lunch.event.partner', 'lunch_id', default=_get_lunch_registered)
  state = fields.Selection(
      [('open', 'Open'), ('closed', 'Closed'), ('billed', 'Billed')], string="State", default='open')
  total_eaters = fields.Integer(
      "Total Registered", compute='_compute_total_eaters')

  @api.one
  def action_closed(self):
    self.state = 'closed'

  @api.one
  def action_open(self):
    self.state = 'open'

  @api.one
  def action_billed(self):
    pass

  # When called from code
  # self.signal_workflow('bill_lunch_event')
