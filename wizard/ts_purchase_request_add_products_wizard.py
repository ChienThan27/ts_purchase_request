from odoo import models,fields,api
from odoo.exceptions import UserError

class TsPurchaseRequestAddProductsWizard(models.TransientModel):
    _name = "ts.purchase.request.add.products.wizard"
    _description = "Thêm sản phẩm"

    request_id = fields.Many2one("ts.purchase.request", string="Phiếu yêu cầu", required=True)
    product_ids = fields.Many2many("product.product", string="Sản Phẩm", required=True)
    default_quantity = fields.Integer(string="Số lượng", defaulf=1)
    skip_existing = fields.Boolean(string="Bỏ qua sản phẩm trùng", default=False)

    def action_add_products(self):
        self.ensure_one()
        existing_product_ids = self.request_id.line_ids.mapped("product_id").ids
        for product in self.product_ids:
            if product.id in existing_product_ids:
                if self.skip_existing == True:
                    continue
                else:
                    raise UserError("Da co san pham nay o dong yeu cau {product.name}")
            self.env["ts.purchase.request.line"].create({
                "request_id": self.request_id.id,
                "product_id": product.id,
                "quantity": self.default_quantity,
            })
        return {
            "type": "ir.actions.act_window_close",
        }
