# -*- coding: utf-8 -*-
from odoo import models, fields, api


class mundo(models.Model):
    _name = 'godslayer.mundo'
    _description = 'Mundo'

    name = fields.Char(String = "Nombre",required = True)
    image = fields.Image(max_width=200, max_height=200)
    size = fields.Float()

    aldea = fields.One2many('godslayer.aldea','mundo')
    aldea_qty = fields.Integer(compute="get_aldeas_qty")

    @api.constrains('size')
    def check_mundo_size(self):
        for mundo in self:
            if mundo.size > 1000 or mundo.size <1:
                raise ValidationError("Mundo demasiado grande: %s" %mundo.size)

    @api.depends('aldea')
    def get_aldeas_qty(self):
        for p in self:
            p.aldea_qty = len(p.aldea)

class aldea(models.Model):
    _name = 'godslayer.aldea'
    _description = 'aldea'

    name = fields.Char(String="Nombre", required = True)
    avatar = fields.Image(max_width=200, max_height=200)
    password = fields.Char(String="Contrsenya")

    oro = fields.Integer();
    fe = fields.Integer();
    materiales= fields.Integer(String="Materiales");

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
    coste_oro = fields.Integer(String = "Precio")
    coste_fe = fields.Integer(String =  "Cantidad Fe")
    imagen = fields.Image(max_width=150, max_height=150)

    aldea = fields.Many2one('godslayer.aldea')
    dioses = fields.Many2one('godslayer.dioses')
    #religion = fields.Many2one('godslayer.religion')
    dioses_qty = fields.Integer(compute="get_dioses_qty")

    @api.depends('dioses')
    def get_dioses_qty(self):
        for p in self:
            p.dioses_qty = len(p.dioses)

class edificio(models.Model):
    _name = 'godslayer.edificio'
    _description = 'edificios'

    edificio_type = fields.Many2one('godslayer.edificio_type')
    name = fields.Char(String="Nombre")
    coste_oro = fields.Float(String="Precio", related='edificio_type.coste_oro')
    coste_material = fields.Float(String="Cantidad Material", related='edificio_type.coste_material')
    imagen = fields.Image(max_width=150, max_height=150, related='edificio_type.imagen')
    production_oro = fields.Float(related='edificio_type.production_oro')
    production_fe=fields.Float(related='edificio_type.production_fe')
    production_material = fields.Float(related='edificio_type.production_material')

    aldea = fields.Many2one('godslayer.aldea')

class edificio_type(models.Model):
    _name = 'godslayer.edificio_type'
    _desciption = 'Tipo de edificio'

    name = fields.Char(String="Nombre", required=True)
    coste_oro = fields.Float()
    coste_material = fields.Float()
    imagen = fields.Image()
    production_oro = fields.Float()
    production_fe = fields.Float()
    production_material = fields.Float()


class dioses(models.Model):
    _name = 'godslayer.dioses'
    _description = 'dioses'

    name = fields.Char(String="Nombre", required=True)
    imagen = fields.Image(max_width=200, max_height=200)
    health = fields.Integer()
    atack = fields.Integer()
    defense = fields.Integer()
    speed = fields.Integer()
    power = fields.Integer()
    total = fields.Integer(compute = "get_dioses_stats")

    templo = fields.One2many('godslayer.templo','dioses')
    religion  =fields.Many2one('godslayer.religion')

    @api.depends('health','atack','defense','speed','power')
    def get_dioses_stats(self):
        for p in self:
            p.total = p.atack+p.health+p.defense+p.speed+p.power




