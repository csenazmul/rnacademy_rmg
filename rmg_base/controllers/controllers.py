# from odoo import http


# class RmgBase(http.Controller):
#     @http.route('/rmg_base/rmg_base', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rmg_base/rmg_base/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rmg_base.listing', {
#             'root': '/rmg_base/rmg_base',
#             'objects': http.request.env['rmg_base.rmg_base'].search([]),
#         })

#     @http.route('/rmg_base/rmg_base/objects/<model("rmg_base.rmg_base"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rmg_base.object', {
#             'object': obj
#         })

