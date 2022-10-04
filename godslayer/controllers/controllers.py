# -*- coding: utf-8 -*-
# from odoo import http


# class Godslayer(http.Controller):
#     @http.route('/godslayer/godslayer', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/godslayer/godslayer/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('godslayer.listing', {
#             'root': '/godslayer/godslayer',
#             'objects': http.request.env['godslayer.godslayer'].search([]),
#         })

#     @http.route('/godslayer/godslayer/objects/<model("godslayer.godslayer"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('godslayer.object', {
#             'object': obj
#         })
