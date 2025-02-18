# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_a_bundle = fields.Boolean(string='Is a bundle', help='Bundle can be add to SO or PO, it allows to add a set of products quickly.')
    bundle_raw_material_ids = fields.One2many('bundle.raw.mat', 'product_tmpl_id', string="Bundle Raw Materials")

    @api.constrains('type')
    def check_bundle_validity(self):
        for product in self:
            if product.is_a_bundle and not product.type == 'consu':
                raise ValidationError(_("Bundle products must be of type consumable."))

    @api.onchange('type')
    def onchange_is_a_bundle(self):
        """
        Only consumable product can be a bundle.
        """
        if not self.type == 'consu' and self.is_a_bundle:
            self.is_a_bundle = False
