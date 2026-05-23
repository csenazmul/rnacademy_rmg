# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RmgOrder(models.Model):
    _name        = 'rmg.order'
    _description = 'RMG Buyer Order'
    _order       = 'order_date desc, order_ref'
    _inherit     = ['mail.thread', 'mail.activity.mixin']

        # ── Identification ──
    order_ref = fields.Char(
        string='অর্ডার রেফারেন্স',
        required=True,
        copy=False,
        default=lambda self: 'New',
    )

        # ── Many2one: বায়ারের সাথে সংযোগ ──
    buyer_id = fields.Many2one(
        comodel_name='rmg.buyer',
        string='বায়ার',
        required=True,
        ondelete='restrict',
                # restrict: বায়ারের অর্ডার থাকলে বায়ার মুছা যাবে না
        tracking=True,
        domain=[('active', '=', True)],
    )

        # ── Related fields থেকে buyer-এর তথ্য ──
    buyer_country = fields.Char(
        related='buyer_id.country',
        string='বায়ারের দেশ',
        readonly=True,
        store=True,
    )

        # ── Date fields ──
    order_date    = fields.Date(string='অর্ডারের তারিখ',
                                default=fields.Date.today, required=True)
    delivery_date = fields.Date(string='ডেলিভারির তারিখ', required=True,
                                tracking=True)

        # ── State ──
    state = fields.Selection(
        selection=[
            ('draft',         'খসড়া'),
            ('confirmed',     'নিশ্চিত'),
            ('in_production', 'উৎপাদনে'),
            ('shipped',       'শিপ হয়েছে'),
            ('cancelled',    'বাতিল'),
        ],
        default='draft',
        string='অবস্থা',
        tracking=True,
    )

        # ── One2many: অর্ডার লাইন ──
    line_ids = fields.One2many(
        comodel_name='rmg.order.line',
        inverse_name='order_id',
                # inverse_name MUST match Many2one field name in rmg.order.line
        string='অর্ডার লাইনসমূহ',
    )

        # ── Many2many: সম্পর্কিত পণ্য ──
    product_ids = fields.Many2many(
        comodel_name='product.template',
        relation='rmg_order_product_rel',
        column1='order_id',
        column2='product_id',
        string='সম্পর্কিত পণ্য',
        domain=[('active', '=', True)],
    )

        # ── Computed: মোট পরিমাণ ও মোট মূল্য ──
    total_qty = fields.Integer(
        string='মোট পিস',
        compute='_compute_totals',
        store=True,
    )
    total_value = fields.Float(
        string='মোট মূল্য (USD)',
        compute='_compute_totals',
        store=True,
        digits=(12, 2),
    )

    @api.depends('line_ids.qty_pcs', 'line_ids.subtotal')
    def _compute_totals(self):
        for order in self:
            order.total_qty   = sum(order.line_ids.mapped('qty_pcs'))
            order.total_value = sum(order.line_ids.mapped('subtotal'))

        # ── SQL Constraints ──
    _sql_constraints = [
        ('order_ref_unique', 'UNIQUE(order_ref)',
         'অর্ডার রেফারেন্স অনন্য হতে হবে!'),
    ]


class RmgOrderLine(models.Model):
    _name        = 'rmg.order.line'
    _description = 'RMG Order Line'

        # ── Many2one: parent order-এর সাথে সংযোগ ──
    order_id = fields.Many2one(
        comodel_name='rmg.order',
        string='অর্ডার',
        required=True,
        ondelete='cascade',
                # cascade: অর্ডার মুছলে এই line-ও মুছে যাবে
    )

        # ── Line details ──
    style_ref = fields.Char(string='স্টাইল রেফারেন্স', required=True)
    color     = fields.Char(string='রঙ')
    size      = fields.Selection([
        ('XS','XS'),('S','S'),('M','M'),
        ('L','L'),('XL','XL'),('XXL','XXL')
    ], string='সাইজ')
    qty_pcs   = fields.Integer(string='পরিমাণ (পিস)', default=0)
    price_usd = fields.Float(string='দাম (USD/pcs)', digits=(10, 2))

    subtotal = fields.Float(
        string='সাব-টোটাল',
        compute='_compute_subtotal',
        store=True,
        digits=(12, 2),
    )

    @api.depends('qty_pcs', 'price_usd')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty_pcs * line.price_usd