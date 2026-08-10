from odoo import models,fields,api

class TsPurchaseRequest(models.Model):
    _name= "ts.purchase.request"
    _description = "Yeu cau mua hang"

    name = fields.Char(string="Ma yeu cau", required=True)
    request_date = fields.Date(string="Ngay yeu cau", required=True)
    requester_id = fields.Many2one("res.user", string="Nguoi yeu cau", required=True)
    department_name = fields.Char(string="Bo phan yeu cau")
    purpose = fields.Text(string="Muc dich mua")
    needed_date = fields.Date(string="Ngay can hang")
    line_ids = fields.One2many("request_id", "ts.purchase.request", string="Dong vat tu can mua")
    line_count = fields.Integer(string="So dong vat tu", compute="_compute_line_ids")
    amount_total = fields.Float(string="Tong tien du kien", compute="_compute_amount_total")
    state = fields.Selection(string="Trang thai", selection=[
        ("draft", "Nhap"), ("submitted","Da gui duyet"), ("approved","Da duyet"), ("purchasing","Dang mua hang"), ("done","Hoan tat"), ("cancel","Huy"), ("rejected","Tu choi")   
    ], default="draft")
    note = fields.Text(string="Ghi chu")

    @api.depends("line_ids")
    def _compute_line_ids(self):
        for rec in self:
            rec.line_count = len(rec.line_ids)

    @api.depends("line_ids.subtotal")
    def _compute_amount_total(self):
        for rec in self:
            rec.amount_total = sum(rec.line_ids.mapped("subtoatal"))
