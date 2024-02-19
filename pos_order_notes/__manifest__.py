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
  "name"                 :  "POS Order Notes",
  "summary"              :  "The module allows you the POS user to add notes on each order lines on the POS cart and also on complete POS order. The notes show up on the Odoo POS receipt.",
  "category"             :  "Point of Sale",
  "version"              :  "1.0.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/POS-Order-Notes.html",
  "description"          :  """Odoo POS Order Notes
Add notes on order
Add note on order line
Notes on POS receipt
Short notes on POS order
POS cart product note
POS user note on order
POS note on order
""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_order_notes&custom_url=/pos/web/#action=pos.ui",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'views/pos_config_view.xml',
                             'views/template.xml',
                            ],
  "qweb"                 :  ['static/src/xml/pos_order_note.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}