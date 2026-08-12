{
    "name": "TS Purchase Request",
    "version": "19.0.0.0.0",
    "author": "Chien",
    "summary": "Yeu cau mua hang",
    "category": "Purchase",
    "depends": ["base","purchase"],
    "data": [
        "security/ir.model.access.csv",
        "views/ts_purchase_request_views.xml",
        "views/ts_purchase_request_add_products_wizard_views.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}