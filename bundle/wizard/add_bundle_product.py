# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools import float_is_zero


class BundleRawMat(models.TransientModel):
    _name = 'add.bundle.product'
    _description = 'Allow to add components of a bundle product to a sale order'

    product_tmpl_id = fields.Many2one('product.template', string='Bundle', required=True, domain=[('is_a_bundle', '=', True)], ondelete='cascade')
    quantity = fields.Float(string="Quantity", default=1.0)
    bundle_raw_mat_ids = fields.One2many('bundle.raw.mat.wiz', 'bundle_wizard_id', string='Components')
    bundle_model = fields.Selection([('purchase', 'Purchase'), ('sale', 'Sale')], string='Model', required=True)
    max_sequence = fields.Integer(string='Max Sequence')

    def _prepare_bundle_raw_mat(self):
        """
        Prepare a list of values for creating the component lines of the bundle.
        """
        self.ensure_one()
        values_list = []
        if not self.product_tmpl_id:
            return values_list
        for raw_mat in self.product_tmpl_id.bundle_raw_material_ids:
            values = raw_mat.prepare_raw_mat_wiz(quantity=self.quantity)
            values_list.append(values)
        return values_list

    @api.onchange('product_tmpl_id')
    def generate_components_lines(self):
        """
        Depending on the product chosen, fulfill the component lines of the bundle's wizard.
        """
        self.update({'bundle_raw_mat_ids': [(5, 0, 0)]})
        if not self.product_tmpl_id:
            return
        rounding = self.product_tmpl_id.uom_id.rounding
        if float_is_zero(self.quantity, precision_rounding=rounding):
            return
        values_list = self._prepare_bundle_raw_mat()
        create_values = [(0, 0, values) for values in values_list]
        self.update({'bundle_raw_mat_ids': create_values})

    @api.onchange('quantity')
    def update_components_qty(self):
        """
        Depending on the quantity of bundle, adapt the quantity of bundle's components.
        """
        if not self.product_tmpl_id:
            return
        rounding = self.product_tmpl_id.uom_id.rounding
        if float_is_zero(self.quantity, precision_rounding=rounding):
            return
        for raw_mat in self.bundle_raw_mat_ids:
            raw_mat.quantity = raw_mat.unit_quantity * self.quantity
