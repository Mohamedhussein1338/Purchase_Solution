from odoo import models, fields, api,_

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = "Purchase Request Cycle Solutio"

    state=fields.Selection([('draft','Draft'),('confirmed','Confirmed')],string='State')
    analytic_account_id= fields.Many2one('account.analytic.account', string='Analytical Account')
    date=fields.Date(default=fields.Datetime.now,string='Date',readonly=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user, )
    requested_by = fields.Many2one('res.partner', string='Requested By', default=lambda self: self.env.user)
    requested_on = fields.Date(string='Requested On', default=fields.Date.context_today)
    purchase_request_lines = fields.One2many('purchase.request.line', 'purchase_request_id', string='Purchase Request Lines')
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')
    purchase_order_count = fields.Integer(string='Purchase Order Count', compute='_compute_purchase_order_count', store=True)
    purchase_order_tab = fields.Many2many('purchase.order', 'purchase_request_order_rel', 'request_id', 'order_id', string='Purchase Orders')
    purchase_order_ids = fields.One2many('purchase.order', 'purchase_requests_id', string='Purchase Orders')



    @api.depends('purchase_request_lines')
    def _compute_purchase_order_count(self):
        for request in self:
            request.purchase_order_count = len(request.purchase_request_lines)

    def action_draft(self):
        self.state = "draft"


    def action_view_purchase_order(self):
        for rec in self:
            purchase_requests_id = []
            return  {
                    'name': 'Purchase Order',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'purchase.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    # 'domain': [('purchase_requests_id', '=', 'active_id')],

                }

    def action_view_purchase_orders(self):
        purchase_orders = self.env['purchase.order'].search([('purchase_requests_id', '=', self.id)])

        action = {
            'name': 'Related Purchase Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.purchase_order_ids.ids)],
            # ('id', 'in', self.payments_id.ids)
        }
        return action

    def smartbuttun(self):
        return {
            'name': 'Related Purchase Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.purchase_order_ids.ids)]

        }

    def action_purchase_order(self):
        return {
            'name': _('Requested Orders'),
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('purchase_requests_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window'
        }




    def purchase_order(self):
        return

    def action_pur_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

            # Group lines by vendor
            grouped_lines = {}
            for product in rec.purchase_request_lines:
                vendor_id = product.vendor_id.id
                if vendor_id not in grouped_lines:
                    grouped_lines[vendor_id] = []
                grouped_lines[vendor_id].append({
                    'product_id': product.product_id.id,
                    'product_qty': product.quantity,
                    'price_unit': product.price_id,
                    # Add other line fields as needed
                })

            for vendor_id, lines in grouped_lines.items():
                purchase_request_lines = {
                    'partner_id': vendor_id,
                    'order_line': [(0, 0, line) for line in lines],
                }
                purchase_order = self.env['purchase.order'].create(purchase_request_lines)

                rec.purchase_order_tab |= purchase_order







    class PurchaseRequestLine(models.Model):
        _name = 'purchase.request.line'
        _description = 'Purchase Request Line'

        product_id = fields.Many2one('product.product', string='Product')
        vendor_id = fields.Many2one('res.partner', string='Vendor')
        quantity = fields.Float(string='Quantity')
        price_id = fields.Integer(string="Price")
        uom_id = fields.Many2one('uom.uom', string='UOM')
        purchase_request_id = fields.Many2one('purchase.request', string='Purchase Request')



    class PurchaseOrder(models.Model):
        _inherit = 'purchase.order'

        purchase_requests_id = fields.Many2one('purchase.request', string='Purchase Requests')

        def action_view_purchase_request(self):
            return {
                'name': 'Related Purchase Request',
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.request',
                # Replace with the actual name of your purchase request model
                'view_mode': 'tree,form',
                'res_id': self.purchase_requests_id.id,
            }




