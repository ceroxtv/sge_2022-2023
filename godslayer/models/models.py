# -*- coding: utf-8 -*-
from odoo import models, fields, api


class mundo(models.Model):
    _name = 'godslayer.mundo'
    _description = 'Mundo'

    name = fields.Char(String = "Nombre",required = True)
    image = fields.Image(max_width=200, max_height=200)
    size = fields.Float()

    aldea = fields.One2many('godslayer.aldea','mundo')

    @api.constrains('size')
    def check_mundo_size(self):
        for mundo in self:
            if mundo.size > 1000 or mundo.size <1:
                raise ValidationError("Mundo demasiado grande: %s" %mundo.size)

class aldea(models.Model):
    _name = 'godslayer.aldea'
    _description = 'aldea'

    name = fields.Char(String="Nombre", required = True)
    avatar = fields.Image(max_width=200, max_height=200)

    mundo = fields.Many2one('godslayer.mundo')
    religion = fields.Many2one('godslayer.religion')

    templos = fields.One2many('godslayer.templo','aldea')
    edificio = fields.One2many('godslayer.edificio', 'aldea')

    creation_date = fields.Datetime(default = fields.Datetime.now)

class religion(models.Model):
    _name = 'godslayer.religion'
    _description = 'religion'

    name = fields.Char(String="Nombre", required=True)

    aldea = fields.One2many('godslayer.aldea','religion')
    #templo = fields.One2many('godslayer.templo','religion')
    dioses = fields.One2many('godslayer.dioses','religion')

class templo(models.Model):
    _name = 'godslayer.templo'
    _description = 'templo'

    name = fields.Char(String="Nombre", required = True)

    aldea = fields.Many2one('godslayer.aldea')
    dioses = fields.Many2one('godslayer.dioses')
    #religion = fields.Many2one('godslayer.religion')

class edificio(models.Model):
    _name = 'godslayer.edificio'
    _description = 'edificios'

    name = fields.Char(String="Nombre", required=True)

    aldea = fields.Many2one('godslayer.aldea')
    soldados = fields.One2many('godslayer.soldado','edificio')

class dioses(models.Model):
    _name = 'godslayer.dioses'
    _description = 'dioses'

    name = fields.Char(String="Nombre", required=True)
    health = fields.Integer()
    atack = fields.Integer()
    defense = fields.Integer()
    speed = fields.Integer()
    power = fields.Integer()

    templo = fields.One2many('godslayer.templo','dioses')
    religion  =fields.Many2one('godslayer.religion')

class soldado(models.Model):
    _name = 'godslayer.soldado'
    _description = 'soldados'

    name = fields.Char(String="Nombre", required=True)
    health = fields.Integer()
    atack = fields.Integer()
    defense = fields.Integer()
    speed = fields.Integer()
    edificio = fields.Many2one('godslayer.edificio')



