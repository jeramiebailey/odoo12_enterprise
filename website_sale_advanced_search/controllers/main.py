# -*- coding: utf-8 -*-

import json
from odoo.addons.website.controllers.main import QueryURL
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.http_routing.models.ir_http import slug
from odoo import fields, http, tools, _
from odoo.http import request

PPG = 20  # Products Per Page
PPR = 4  # Products Per Row


class TableCompute(object):

    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= PPR:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(PPR):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, products, ppg=PPG):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        x = 0
        for p in products:
            x = min(max(p.website_size_x, 1), PPR)
            y = min(max(p.website_size_y, 1), PPR)
            if index >= ppg:
                x = y = 1

            pos = minpos
            while not self._check_place(pos % PPR, pos // PPR, x, y):
                pos += 1
            # if 21st products (index 20) and the last line is full (PPR products in it), break
            # (pos + 1.0) / PPR is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= ppg and ((pos + 1.0) // PPR) > maxy:
                break

            if x == 1 and y == 1:  # simple heuristic for CPU optimization
                minpos = pos // PPR

            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos // PPR) + y2][(pos % PPR) + x2] = False
            self.table[pos // PPR][pos % PPR] = {
                'product': p, 'x': x, 'y': y,
                'class': " ".join(x.html_class for x in p.website_style_ids if x.html_class)
            }
            if index <= ppg:
                maxy = max(maxy, y + (pos // PPR))
            index += 1

        # Format table according to HTML needs
        rows = sorted(self.table.items())
        rows = [r[1] for r in rows]
        for col in range(len(rows)):
            cols = sorted(rows[col].items())
            x += len(cols)
            rows[col] = [r[1] for r in cols if r[1]]

        return rows


class WebsiteSearch(http.Controller):

    def _get_search_domain(self, search, category, search_attrib_ids, attrib_values):
        domain = request.website.sale_product_domain()
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', ('name', 'ilike', search), ('name', 'ilike', srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch)]
        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]
        attrib_values_list = []
        attrib_ids_list = []
        if attrib_values:
            attrib_values_list = []
            for value in attrib_values:
                attrib_values_list.append(value.id)
            domain += [('attribute_line_ids.value_ids', 'in', attrib_values_list)]
        if search_attrib_ids:
            attrib_ids_list = []
            for attrib_id in search_attrib_ids:
                attrib_ids_list.append(attrib_id.id)
            domain += [('attribute_line_ids.attribute_id', 'in', attrib_ids_list)]
        return domain

    def _get_compute_currency_and_context(self, product=None):
        pricelist_context, pricelist = self._get_pricelist_context()
        compute_currency = self._get_compute_currency(pricelist, product)
        return compute_currency, pricelist_context, pricelist

    def _get_pricelist_context(self):
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        return pricelist_context, pricelist

    def _get_compute_currency(self, pricelist, product=None):
        company = product and product._get_current_company(pricelist=pricelist,
                                                           website=request.website) or pricelist.company_id or request.website.company_id
        from_currency = (product or request.env['res.company']._get_main_company()).currency_id
        to_currency = pricelist.currency_id
        return lambda price: from_currency._convert(price, to_currency, company, fields.Date.today())

    def _get_search_order(self, post):
        # OrderBy will be parsed in orm and so no direct sql injection
        # id is added to be sure that order is a unique sort key
        return 'is_published desc,%s , id desc' % post.get('order', 'website_sequence desc')

    @http.route('/shop/search_advance', csrf=False, type="json",
                auth="public", website=True)
    def search_advance(self, page=0, category=None, search='', ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        if category:
            category = request.env['product.public.category'].search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}
        search_attrib_values = []
        search_attrib_ids = []
        for srch in search.split(" "):
            att_values = request.env['product.attribute.value'].search([('name', 'ilike', srch)])
            att_ids = request.env['product.attribute'].search([('name', 'ilike', srch)])
            for att_value in att_values:
                search_attrib_values.append(att_value)
            for att_id in att_ids:
                search_attrib_ids.append(att_id)

        print("search_attrib_values========", search_attrib_values)

        domain = self._get_search_domain(search, category, search_attrib_ids, search_attrib_values)
        print("domain=---------------------", domain)
        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list,
                        order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()
        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template'].with_context(bin_size=True)

        Category = request.env['product.public.category']
        search_categories = False
        search_product = Product.search(domain)
        if search:
            categories = search_product.mapped('public_categ_ids')
            search_categories = Category.search(
                [('id', 'parent_of', categories.ids)] + request.website.website_domain())
            categs = search_categories.filtered(lambda c: not c.parent_id)
        else:
            categs = Category.search([('parent_id', '=', False)] + request.website.website_domain())

        parent_category_ids = []
        if category:
            url = "/shop/category/%s" % slug(category)
            parent_category_ids = [category.id]
            current_category = category
            while current_category.parent_id:
                parent_category_ids.append(current_category.parent_id.id)
                current_category = current_category.parent_id

        product_count = len(search_product)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        offset = pager['offset']
        products = search_product[offset: offset + ppg]

        ProductAttribute = request.env['product.attribute']
        if products:
            attributes = ProductAttribute.search([
                ('attribute_line_ids.value_ids', '!=', False),
                ('attribute_line_ids.product_tmpl_id', 'in', search_product.ids)
            ])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        compute_currency = self._get_compute_currency(pricelist, products[:1])

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'rows': PPR,
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'parent_category_ids': parent_category_ids,
            'search_categories_ids': search_categories and search_categories.ids,
        }
        if category:
            values['main_object'] = category
        return_url = request.env['ir.ui.view'].render_template(
            "website_sale_advanced_search.new_products_list_template",
            values
        )
        return {'return_url': return_url}

    @http.route('/shop/search', csrf=False, type="http",
                methods=['POST', 'GET'], auth="public", website=True)
    def search_contents(self, **kw):

        """
        Searches products according to the category selected on front,
        :param kw: dict contains the category and search key
        :return: Dict with params as name, res_id, value
        """
        strings = '%' + kw.get('name') + '%'
        category = int(kw.get('category')) if not kw.get(
            'category') == 'all' else ''
        try:
            domain = [('public_categ_ids', 'child_of',
                       [category])] if category else []
            domain.append(('website_published', '=', True))
            product_as_category = request.env['product.template'].search(
                domain)
            sql = """select id as res_id, name as name, name as value from product_template where name ILIKE '{}'"""
            extra_query = ''
            if product_as_category:
                extra_query = " and id in {}"
            limit = " limit 15"
            qry = sql + extra_query + limit
            product_list = []
            if len(product_as_category.ids) == 1:
                product_list = product_as_category.ids
                product_list.append(0)
            request.cr.execute(qry.format(strings, tuple(
                product_as_category and product_list if len(
                    product_as_category.ids) == 1 else product_as_category.ids)))
            name = request.cr.dictfetchall()
        except:
            name = {'name': 'None', 'value': 'None'}
        return json.dumps(name)
