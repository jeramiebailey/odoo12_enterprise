# Copyright 2019 Tecnativa - Pedro M. Baeza

from openupgradelib import openupgrade

column_renames = {
    'product_brand': [
        ('logo', None),
    ],
}


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, 'product_brand', 'logo'):
        openupgrade.rename_columns(env.cr, column_renames)
