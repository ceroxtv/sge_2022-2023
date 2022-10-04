# -*- coding: utf-8 -*-
from odoo import models, fields, api


class player(models.Model):
    _name = 'godslayer.player'
    _description = 'Players of the game'

    avatar = fields.Image(max_width = 200, max_height = 200)
    name = fields.Char(String = "Nombre", required = True)
    password = fields.Char()

    aldea = fields.One2many('godslayer.aldea','player')

class mundo(models.Model):
    _name = 'godslayer.mundo'
    _description = 'Mundo'

    name = fields.Char(String = "Nombre",required = True)
    name = fields.Char(String = "Nombre",required = True)
    image = fields.Image(max_width=200, max_height=200)
    image = fields.Image(max_width=200, max_height=200)
    size = fields.Float()

    mundo = fields.One2many('godslayer.mundo', 'mundo')

class aldea(models.Model):
    _name = 'godslayer.aldea'
    _description = 'aldea'

    name = fields.Char(String="Nombre", required = True)
    mundo = fields.Many2one('godslayer.mundo')
    player = fields.Many2one('godslayer.player')



