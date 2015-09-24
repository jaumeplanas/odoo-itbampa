# -*- coding: utf-8 -*-
from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError
from openerp import fields
from datetime import timedelta

class TestBoard(TransactionCase):
    
    def setUp(self):
        """Setup for an initial open board"""
        
        super(TestBoard, self).setUp()
        self.board = self.env['itbampa.boards']
        self.open_board = self.board.search([('state', '=', 'open')], limit=1)
        self.last_board = self.board.search([], limit=1)
        # self.board0 will point to a valid open board
        if self.open_board:
            self.board0 = self.open_board
        elif self.last_board:
            self.board0 = self.last_board
            self.board0.signal_workflow('open') 
        else:            
            self.board0 = self.board.create({
                'name': 'Reference Board',
                'date_start': '2015-01-01',
                })
        self.date_start = fields.Date.from_string(self.board0.date_start)

    def test_check_date_start(self):
        """ Test when Date Start is before Date End of last closed board."""
        self.board0.signal_workflow('close')
        dstart = fields.Date.from_string(self.board0.date_end) - timedelta(days=3)
        dend   = dstart + timedelta(days=30)
        with self.assertRaises(ValidationError):
            self.board1 = self.board.create({
                'name': 'Start Date Board',
                'date_start': dstart.strftime('%Y-%m-%d'),
                'date_end': dend.strftime('%Y-%m-%d'),
                })        
        
    def test_check_date_end(self):
        """ Test when Date End is before Start Date."""
        self.board0.signal_workflow('close')
        dstart = fields.Date.from_string(self.board0.date_end) + timedelta(days=1)
        dend   = dstart - timedelta(days=30)
        with self.assertRaises(ValidationError):
            self.board1 = self.board.create({
                'name': 'End Date Board',
                'date_start': dstart.strftime('%Y-%m-%d'),
                'date_end': dend.strftime('%Y-%m-%d'),
                })        
        
    def test_check_board_open(self):
        """ Test when trying to create a board with an existing open board."""
        dstart = fields.Date.from_string(self.board0.date_start) + timedelta(days=1)
        dend   = dstart + timedelta(days=30)
        with self.assertRaises(ValidationError):
            self.board1 = self.board.create({
                'name': 'Board Open',
                'date_start': dstart.strftime('%Y-%m-%d'),
                'date_end': dend.strftime('%Y-%m-%d'),
                })        
        
