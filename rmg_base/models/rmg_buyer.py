from odoo import models, fields, api
# from odoo.orm import Constraint

class RmgBuyer(models.Model):
    _name = "rmg.buyer"
    _description = "RMG Buyer"
    _order = "name asc"

    _inherit = ['mail.thread', 'mail.activity.mixin']

    # @api.model
    def action_confirm(self):
        self.write({'state': 'confirmed'})
        return True

    # name = fields.Char(
    #     string="Buyer Name", 
    #     required=True,
    #     size=128,
    #     tracking=True,
    #     index=True,)
    
    name = fields.Char(
        string="Buyer Name", 
        required=True,
        tracking=True,
        index=True,)

    # country_id = fields.Many2one(
    #     'res.country',
    #     string = 'Country',
    #     help="Enter the name of the buyer's country (eg: Germany, Sweden)",
    # )

    country = fields.Char(
        string='দেশ',
        help='বায়ারের দেশের নাম লিখুন (যেমন: Germany, Sweden)',
                # help: ? আইকনে hover করলে দেখাবে
    )

    email = fields.Char(string='Email Address')
    phone = fields.Char(string="Phone Number")

    website = fields.Char(string="Website")

    buyer_code = fields.Char(
        string='বায়ার কোড',
        copy=False,
                # Duplicate করলে কোড কপি হবে না
        readonly=True,
                # UI থেকে পরিবর্তন করা যাবে না (sequence দিয়ে auto-set হবে)
    )

    @api.model_create_multi   # ✅ MUST USE
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('buyer_code', 'New') == 'New':
                vals['buyer_code'] = self.env['ir.sequence'].next_by_code('rmg.buyer') or 'New'
        return super().create(vals_list)

    currency_id = fields.Many2one(
        'res.currency',
        string = 'Currency',
        # default = lambda self: self.env.ref('base.USD')
        default=lambda self: self.env.company.currency_id,
    )

    payment_terms = fields.Integer(
        string = 'Payment Term (Days)',
        default = 30,
        help= "শিপমেন্টের পর কত দিনের মধ্যে পেমেন্ট পাবেন",
    )

    notes = fields.Text(string='Special Notes ')

    active = fields.Boolean(
        string = 'active',
        default = True,
    )


    # ══════════════════════════════════════════════
    # SQL Constraints — ডেটাবেজ স্তরে নিয়ম
    # ══════════════════════════════════════════════

    _sql_constraints = [
    (
        'buyer_code_unique',
        'UNIQUE(buyer_code)',
        'বায়ার কোড অবশ্যই অনন্য হতে হবে!',
    ),
    (
        'payment_terms_positive',
        'CHECK(payment_terms > 0)',
        'পেমেন্টের সময়সীমা শূন্যের বেশি হতে হবে!',
    ),
    ]

    # _sql_constraints = [
    #     (
    #         'buyer_code_unique',       # constraint-এর অনন্য নাম
    #         'UNIQUE(buyer_code)',      # SQL: এই column-এ duplicate নয়
    #         'বায়ার কোড অবশ্যই অনন্য হতে হবে!',  # Error message
    #     ),
    #     (
    #         'payment_terms_positive',
    #         'CHECK(payment_terms > 0)',
    #         'পেমেন্টের সময়সীমা শূন্যের বেশি হতে হবে!',
    #     ),
    # ]

    # # ✅ NEW CONSTRAINT STYLE
    # _constraints = [
    #     Constraint(
    #         'buyer_code_unique',
    #         'unique(buyer_code)',
    #         'বায়ার কোড অবশ্যই অনন্য হতে হবে!'
    #     ),
    #     Constraint(
    #         'payment_terms_positive',
    #         'CHECK(payment_terms > 0)',
    #         'পেমেন্টের সময়সীমা শূন্যের বেশি হতে হবে!'
    #     ),
    # ]