# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

AMPA_BOARD_STATES = [
    ("open", "Open"),
    ("closed", "Closed")
]

BOARD_STATE_CLOSED = {
    "closed": [
        ("readonly", True)
    ]
}


class ItbampaBoardRoles(models.Model):

  """Roles for Board Members"""

  _name = "itbampa.board.roles"

  name = fields.Char(
      string="Role Name", required=True, help="Board Role Name")


class ItbampaBoardMembers(models.Model):

  """Board Members"""

  _name = "itbampa.board.members"

  partner = fields.Many2one("res.partner", "Board Member", ondelete="set null", domain=[
                            ("ampa_partner_type", "=", "tutor")], required=True)
  role = fields.Many2one(
      "itbampa.board.roles", "Board Role", ondelete="set null", required=True)
  board = fields.Many2one(
      "itbampa.boards", "Board", ondelete="cascade", required=True)
  mobile = fields.Char(
      string=_("Mobile"), related="partner.mobile", readonly=True)
  email = fields.Char(
      string=_("Email"), related="partner.email", readonly=True)


class ItbampaBoards(models.Model):

  """Boards composition and dates"""

  _name = "itbampa.boards"
  _inherit = ["mail.thread"]
  _order = "date_start desc"

  @api.one
  @api.depends("date_end")
  def action_closed(self):
    if (self.date_end == False):
      self.date_end = fields.Date.today()
    self.state = "closed"

  @api.one
  def action_open(self):
    self.state = "open"

  @api.one
  @api.constrains("date_start")
  def _check_date_start(self):
    boards = self.env["itbampa.boards"].search([("state", "=", "closed")])
    for board in boards:
      if (self.date_start < board.date_end):
        raise ValidationError(_("Date start is before than date end for: %s (%s)") % (
            board.name, board.date_end))

  @api.one
  @api.constrains("date_end")
  def _check_date_end(self):
    if (self.date_end != False and self.date_end < self.date_start):
      raise ValidationError(_("Date end is before than date start"))

  @api.one
  @api.constrains("state")
  def _check_state(self):
    opened = self.env["itbampa.boards"].search_count(
        [("state", "=", "open")])
    if (opened > 1):
      raise ValidationError(_("Too many opened boards."))

  name = fields.Char(string="Board Name", required=True)
  date_start = fields.Date(
      string="Start Date", default=fields.Date.today, required=True, states=BOARD_STATE_CLOSED)
  date_end = fields.Date(string="End Date", states=BOARD_STATE_CLOSED)
  members = fields.One2many(
      "itbampa.board.members", "board", states=BOARD_STATE_CLOSED)
  state = fields.Selection(AMPA_BOARD_STATES, default="open")
