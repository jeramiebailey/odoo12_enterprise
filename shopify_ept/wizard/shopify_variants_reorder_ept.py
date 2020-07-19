from odoo import models,fields,api
import itertools

class shopify_variant_reorder_ept(models.TransientModel):
    _name="shopify.variant.reorder.ept"
    _description = 'Shopify Variant Reorder Ept'
    shopify_attribute_line_ids=fields.One2many("shopify.attribute.line.ept","shopify_attribute_reorder_id",string="Shopify Attributes")
    
    @api.model
    def default_get(self,fields=None):
        product_tmpl_obj=self.env['shopify.product.template.ept']
        result=[]
        active_id=self._context.get('active_id')
        template=product_tmpl_obj.browse(active_id)
        for line in template.product_tmpl_id.attribute_line_ids:
            sequence=1
            for value in line.value_ids:
                vals={}            
                vals.update({'attribute_id':line.attribute_id.id,
                             'value_id':value.id,
                             'sequence':sequence,
                             })
                result.append((0, 0,vals))
                sequence=sequence+1
        return {'shopify_attribute_line_ids':result}

    @api.multi
    def reorder_variants(self):
        product_tmpl_obj=self.env['shopify.product.template.ept']
        active_id=self._context.get('active_id')
        template=product_tmpl_obj.browse(active_id)
        attributes_ids=[line.attribute_id.id for line in template.product_tmpl_id.attribute_line_ids]
        value_ids=[]
        for attribute_id in attributes_ids:
            tmp_ids=[]
            for line in self.shopify_attribute_line_ids:
                if line.attribute_id.id!=attribute_id:
                    continue
                tmp_ids.append(line.value_id.id)
            value_ids.append(tmp_ids)
        value_ids=list(itertools.product(*value_ids))
        sequence=1
        for value_id in value_ids:
            for variant  in template.shopify_product_ids:
                value_id=list(value_id)
                value_id.sort()
                attribute_val_ids=variant.product_id.attribute_value_ids.ids
                attribute_val_ids.sort()
                if value_id == attribute_val_ids:
                    variant.write({'sequence':sequence})
                    sequence=sequence+1
                    break
        return True
class shopify_attribute_line_ept(models.TransientModel):
    _name="shopify.attribute.line.ept"
    _description = 'Shopify attribute Line Ept'
    _order='attribute_id,sequence'
    
    attribute_id=fields.Many2one("product.attribute",string="Attribute")
    value_id=fields.Many2one("product.attribute.value",string="Attribute Value")
    sequence=fields.Integer("Sequence")
    shopify_attribute_reorder_id=fields.Many2one("shopify.variant.reorder.ept",string="Variant Reorder Id")
    shopify_product_tmpl_id=fields.Many2one('shopify.product.template.ept',string="Template")
    
