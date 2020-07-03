# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Purchase Barcode Scanning",
  "summary"              :  "The module allows you to scan the product barcode and add the product to the order lines in a Purchase order.",
  "category"             :  "Purchase",
  "version"              :  "1.0.0",
  "sequence"             :  "10",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Sales-Barcode-Scanning.html",
  "description"          :  """Odoo Sales Barcode Scanning
Odoo advanced barcode scanning
Scan products with barcode
Add product to sales order
Scan sales order products
Odoo Scan products to sales order in Odoo
Scan barcode in Odoo
""",
  "depends"              :  [
                             'barcodes',
                             'purchase','stock_barcode'
                            ],
  "data"                 :  ['views/purchase_views.xml'],
  "application"          :  True,
  "price"                :  15,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}