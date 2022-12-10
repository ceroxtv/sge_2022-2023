# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
from datetime import datetime, timedelta


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
            if mundo.size > 10000 or mundo.size <1:
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
    avatar_tumb = fields.Image(related="avatar", max_width=50, max_height=50)
    password = fields.Char(String="Contrsenya")
    location = fields.Integer(default=random.randint(1,9999))

    oro = fields.Float(default=50)
    fe = fields.Float(default=50)
    materiales= fields.Float(default=50)
    production_oro = fields.Float(compute="_get_total_productions")
    production_fe = fields.Float(compute="_get_total_productions")
    production_material = fields.Float(compute="_get_total_productions")
    
    mundo = fields.Many2one('godslayer.mundo')
    religion = fields.Many2one('godslayer.religion', required=True)

    templos = fields.One2many('godslayer.templo','aldea')
    templos_disponible = fields.Many2many('godslayer.templo_type',compute="get_avaliable_temples")
    dioses_disponibles = fields.Many2many('godslayer.dioses',compute="get_avaliable_dioses")
    edificio = fields.One2many('godslayer.edificio', 'aldea')

    creation_date = fields.Datetime(default = fields.Datetime.now)

    @api.depends('religion')
    def get_avaliable_temples(self):  # ORM
        for c in self:
            c.templos_disponible = self.env['godslayer.templo_type'].search([('religion', '=', c.religion.id)])
            
    @api.depends('templos')
    def get_avaliable_dioses(self):
        for c in self:
            c.dioses_disponibles = self.env['godslayer.dioses'].search([('templo.aldea','=',c.id)])
    
    @api.depends('edificio')
    def _get_total_productions(self):
        for h in self:
            h.production_oro = sum(h.edificio.mapped('production_oro'))
            h.production_fe = sum(h.edificio.mapped('production_fe'))
            h.production_material = sum(h.edificio.mapped('production_material'))
            
    @api.model
    def produce(self):  # ORM CRON
        self.search([]).produce_aldea()    
        
    def produce_aldea(self):
        for e in self:
            oro = e.oro + e.production_oro
            fe = e.fe + e.production_fe
            materiales = e.materiales + e.production_material

            e.write({
                "oro":oro,
                "fe":fe,
                "materiales":materiales
            })
    def distance(self,other_aldea):
        distance = 0
        if(len(self) > 0 and len(other_aldea) > 0):
            distance = abs(self.location - other_aldea.location)
            return distance


class religion(models.Model):
    _name = 'godslayer.religion'
    _description = 'religion'

    name = fields.Char(String="Nombre", required=True)

    aldea = fields.One2many('godslayer.aldea','religion')
    templo_type = fields.Many2one('godslayer.templo_type')
    dioses = fields.One2many('godslayer.dioses','religion')
    dioses_qty = fields.Integer(String="Cantidad Dioses",compute="get_dioses_qty")

    @api.depends('dioses')
    def get_dioses_qty(self):
        for p in self:
            p.dioses_qty = len(p.dioses)


class templo(models.Model):
    _name = 'godslayer.templo'
    _description = 'templo'

    templo_type = fields.Many2one('godslayer.templo_type', ondelete="restrict")
    name = fields.Char(String="Nombre Templo", related='templo_type.name')
    coste_oro = fields.Float(String="Precio", related='templo_type.coste_oro')
    coste_material = fields.Float(String="Cantidad Material", related='templo_type.coste_material')
    coste_fe = fields.Float(String="Cantidad Fe", related='templo_type.coste_fe')
    imagen = fields.Image(max_width=150, max_height=150, related='templo_type.imagen')

    aldea = fields.Many2one('godslayer.aldea')
    dioses = fields.Many2one('godslayer.dioses')
    religion = fields.Many2one('godslayer.religion', related='templo_type.religion')
    dioses_qty = fields.Integer(compute="get_dioses_qty")

    @api.depends('dioses')
    def get_dioses_qty(self):
        for p in self:
            p.dioses_qty = len(p.dioses)



class templo_type(models.Model):
    _name = 'godslayer.templo_type'
    _description = 'templo_type'

    name = fields.Char(String="Nombre", required=True)
    coste_oro = fields.Float()
    coste_material = fields.Float()
    coste_fe = fields.Float()
    imagen = fields.Image()
    religion = fields.Many2one('godslayer.religion')

    def create_temple(self):
        for c in self:
            aldea = self.env['godslayer.aldea'].browse(self.env.context['ctx_aldea'])[0]
            dios = self.env['godslayer.dioses'].search([('religion', '=', c.religion.id)])
            d = random.choice(dios)
            if aldea.oro >= c.coste_oro and aldea.fe >= c.coste_fe and aldea.materiales >= c.coste_material:
                self.env['godslayer.templo'].create({
                    "aldea": aldea.id,
                    "templo_type": c.id,
                    "dioses":d.id
                })
                aldea.oro -= c.coste_oro
                aldea.fe -= c.coste_fe
                aldea.materiales -= c.coste_material


class edificio(models.Model):
    _name = 'godslayer.edificio'
    _description = 'edificios'

    edificio_type = fields.Many2one('godslayer.edificio_type', ondelete = "restrict")
    name = fields.Char(related='edificio_type.name')
    coste_oro = fields.Float(String="Precio", related='edificio_type.coste_oro')
    coste_material = fields.Float(String="Cantidad Material", related='edificio_type.coste_material')
    imagen = fields.Image(max_width=150, max_height=150, related='edificio_type.imagen')

    production_oro = fields.Float(compute='_get_productions')
    production_fe=fields.Float(compute='_get_productions')
    production_material = fields.Float(compute='_get_productions')

    aldea = fields.Many2one('godslayer.aldea')
    
    def _get_productions(self):
     for b in self:
            production_oro = b.edificio_type.production_oro
            production_fe = b.edificio_type.production_fe
            production_material = b.edificio_type.production_material
           

            if production_oro + b.aldea.oro >= 0 and production_fe + b.aldea.fe >= 0 and production_material + b.aldea.materiales >= 0:
                b.production_oro = production_oro
                b.production_fe = production_fe
                b.production_material = production_material             
            else:
                b.production_oro =0
                b.production_fe =0
                b.production_material =0     

class edificio_type(models.Model):
    _name = 'godslayer.edificio_type'
    _desciption = 'Tipo de edificio'

    name = fields.Char(String="Nombre", required=True)
    coste_oro = fields.Float()
    coste_material = fields.Float()
    imagen = fields.Image()
    imagen_icon = fields.Image(related="imagen", max_width=50, max_height=50)
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



class battle(models.Model): #falta terminar
    _name = 'godslayer.battle'
    _description = 'Battles'

    name = fields.Char()
    date_start = fields.Datetime(readonly=True, default=fields.Datetime.now)
    date_end = fields.Datetime(compute='_get_time')
    time = fields.Float(compute='_get_time')
    distance = fields.Float(compute='_get_time')
    progress = fields.Float()
    state = fields.Selection([('1', 'Preparation'), ('2', 'Send'), ('3', 'Finished')], default='1')
    aldea1 = fields.Many2one('godslayer.aldea')
    aldea2 = fields.Many2one('godslayer.aldea')
    dioses_list = fields.One2many('godslayer.battle_dioses_rel', 'battle_id')
    
    @api.depends('dioses_list', 'aldea1', 'aldea2')
    def _get_time(self):
        for b in self:
            b.time = 0
            b.distance = 0
            b.date_end = fields.Datetime.now()
            if len(b.aldea1) > 0 and len(b.aldea2) > 0 and len(b.dioses_list) > 0 and len(
                    b.dioses_list.dioses_id) > 0:
                b.distance = b.aldea1.distance(b.aldea2)
                min_speed = b.dioses_list.dioses_id.sorted(lambda s: s.speed).mapped('speed')[0]
                b.time = b.distance / min_speed
                b.date_end = fields.Datetime.to_string(
                    fields.Datetime.from_string(b.date_start) + timedelta(minutes=b.time))


    @api.onchange('aldea1')
    def onchange_aldea1(self):
        print(self)
        if len(self.aldea1) > 0:
            self.name = self.aldea1.name
            return {
                'domain': {
                    'aldea2': [('id', '!=', self.aldea1.id)],
                }
            } 

    @api.onchange('aldea2')
    def onchange_aldea2(self):
        print(self)
        if len(self.aldea2) > 0:
            self.name = self.aldea2.name
            return {
                'domain': {
                    'aldea1': [('id', '!=', self.aldea2.id)],
                }
            }
    def launch_battle(self):
        print("launch")

    def execute_battle(self):
        print("execute")

    def back(self):
        print("back")
                
    def simulate_battle(self):
        print("simulate")        

class battle_dioses_rel(models.Model):
    _name = 'godslayer.battle_dioses_rel'
    _description = 'battle_dioses_rel'

    name = fields.Char(related="dioses_id.name")
    dioses_id = fields.Many2one('godslayer.dioses')
    battle_id = fields.Many2one('godslayer.battle')
    qty = fields.Integer()

