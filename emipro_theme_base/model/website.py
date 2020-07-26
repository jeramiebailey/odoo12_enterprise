from odoo import api, fields, models
from odoo.tools.translate import _
from datetime import date, datetime, timedelta
from odoo.http import request


class website(models.Model):
    _inherit = "website"

    def _get_default_header_content(self):
        return """
            <p></p>
            <div class="s_rating row te_s_header_offer_text">
            <ul>
                <li>Special Offer on First Purchase</li>
                <li>
                    <section>|</section>
                </li>
                <li>Code : #ASDA44</li>
                <li>
                    <section>|</section>
                </li>
                <li>Get 50% Off</li>
            </ul>
            </div>
            """

    def _get_default_footer_extra_links(self):
        return """
        <section>
        <div class="te_footer_inline_menu">
            <ul class="te_footer_inline_menu_t">
                <section>
                    <li>
                        <a href="#">About Us</a>
                    </li>
                </section>
                <section>
                    <li>
                        <a href="#">Contact Us</a>
                    </li>
                </section>
                <section>
                    <li>
                        <a href="#">Customer Service</a>
                    </li>
                </section>
                <section>
                    <li>
                        <a href="#">Privacy Policy</a>
                    </li>
                </section>
                <section>
                    <li>
                        <a href="#">Accessibility</a>
                    </li>
                </section>
                <section>
                    <li>
                        <a href="#">Store Directory</a>
                    </li>
                </section>
            </ul>
        </section>
        </div>
        """

    def _get_default_footer_content(self):
        return """
            <p></p>
            <div class="row">
                <div class="col-lg-4 col-md-4 col-6">
                    <ul class="te_footer_info_ept">
                        <section>
                            <li>
                                <a href="#">Help</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Gift Cards</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Order Status</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Free Shipping</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Returns Exchanges</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">International</a>
                            </li>
                        </section>
                    </ul>
                </div>
                <div class="col-lg-4 col-md-4 col-6">
                    <ul class="te_footer_info_ept">
                        <section>
                            <li>
                                <a href="#">About Us</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Jobs</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Affiliates</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Meet The Maker</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Contact</a>
                            </li>
                        </section>
                    </ul>
                </div>
                <div class="col-lg-4 col-md-4 col-6">
                    <ul class="te_footer_info_ept">
                        <section>
                            <li>
                                <a href="#">Security</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Privacy</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Text Messaging</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Legal</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Supply Chain</a>
                            </li>
                        </section>
                    </ul>
                </div>
            </div>
        """
    def _get_footer_style_3_content(self):
        return """
        <p></p>
        <section>
            <div>
                <h4 class="te_footer_menu_info">Informations</h4>
            </div>
        </section>
        <div class="row">
            <div class="col-lg-6 col-md-6 col-6">
                <ul class="te_footer_info_ept">
                    <section>
                        <li>
                            <a href="#">Help</a>
                        </li>
                    </section>
    
    
                    <section>
                        <li>
                            <a href="#">Gift Cards</a>
                        </li>
                    </section>
    
                    <section>
                        <li>
                            <a href="#">Order Status</a>
                        </li>
                    </section>
                    <section>
                        <li>
                            <a href="#">Free Shipping</a>
                        </li>
                    </section>
                    <section>
                        <li>
                            <a href="#">Returns Exchanges</a>
                        </li>
                    </section>
                    <section>
                        <li>
                            <a href="#">International</a>
                        </li>
                    </section>
                </ul>
            </div>
            <div class="col-lg-6 col-md-6 col-6">
                <ul class="te_footer_info_ept">
    
                    <section>
                        <li>
                            <a href="#">Security</a>
                        </li>
                    </section>
                    <section>
                        <li>
                            <a href="#">Privacy</a>
                        </li>
                    </section>
                    <section>
                        <li>
                            <a href="#">Text Messaging</a>
                        </li>
                    </section>
                    <section>
                        <li>
                            <a href="#">Legal</a>
                        </li>
                    </section>
                    <section>
                        <li>
                            <a href="#">Supply Chain</a>
                        </li>
                    </section>
                    <section>
                        <li>
                            <a href="#">Contact</a>
                        </li>
                    </section>
                </ul>
            </div>
        </div>
        """
    def _get_default_header_extra_links(self):
        return """
            <p></p>
            <div class="te_header_static_menu">
                <ul>
                    <li>
                        <a href="#">Custom menu</a>
                    </li>
                    <li>
                        <a href="#">Information</a>
                    </li>
                    <li>
                        <a href="#">About us</a>
                    </li>
                    <li>
                        <a href="#">Our story</a>
                    </li>
                </ul>
            </div>
        """

    def _get_default_header_extra_content(self):
        return """
            <p></p>
            <div class="s_rating row te_s_header_offer_text">
                <ul>
                    <li><span>Email:</span>support@emiprotechnologies.com</li>
                    <li>
                        <section>|</section>
                    </li>
                    <li>Free Shipping for all Order of $99</li>
                </ul>
            </div>
        """
    def _get_default_equino_header_content(self):
        return """
            <p></p>
            <section class="py-3">
                <span class="header-text">Welcome to Equino Mutipurpose eCommerce Theme</span>
            </section>   
        """

    def _get_default_equino_footer_content(self):
        return """
            <p></p>
            <section class="row">
                <div class="col-sm-4 te_extra">
                    <section class="te_extra_title">
                        <div class="te_footer_title">company</div>
                        <span>
                            <span class="fa fa-angle-down"></span>
                        </span>
                    </section>
                    <ul class="te_footer_list">
                        <section>
                            <li>
                                <a href="#">About Us</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Our Services</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Affiliate Program</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Our Work</a>
                            </li>
                        </section>
                    </ul>
                </div>
                <div class="col-sm-4 te_extra">
                    <section class="te_extra_title">
                        <div class="te_footer_title">usefull links</div>
                        <span>
                            <span class="fa fa-angle-down"></span>
                        </span>
                    </section>
                    <ul class="te_footer_list">
                        <section>
                            <li>
                                <a href="#">The Collections</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Size Guide</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Return Policy</a>
                            </li>
                        </section>
                    </ul>
                </div>
                <div class="col-sm-4 te_extra">
                    <section class="te_extra_title">
                        <div class="te_footer_title">shopping</div>
                        <span>
                            <span class="fa fa-angle-down"></span>
                        </span>
                    </section>
                    <ul class="te_footer_list">
                        <section>
                            <li>
                                <a href="#">Look Book</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Shop Sidebar</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Shop Fullwidth</a>
                            </li>
                        </section>
                        <section>
                            <li>
                                <a href="#">Man &amp; Woman</a>
                            </li>
                        </section>
                    </ul>
                </div>
            </section>
        """

    is_ajax_sorting_products = fields.Boolean(string="Load Products through Ajax")
    show_more_msg = fields.Char(string='Show More Message', translate=True, default="Show More")
    show_less_msg = fields.Char(string='Show Less Message', translate=True, default="Show Less")
    view_all_msg = fields.Char(string='View All Message', translate=True, default="View All")
    is_price_filter_enable = fields.Boolean(string="Allow Price Filter")
    facebook_sharing = fields.Boolean(string='Facebook')
    twitter_sharing = fields.Boolean(string='Twitter')
    linkedin_sharing = fields.Boolean(string='Linkedin')
    mail_sharing = fields.Boolean(string='Mail')
    number_of_product_line = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    ], string="Number of lines for product name", required=True, default='1', readonly=False,
        help="Number of lines to show in product name for shop.")
    website_footer_extra_links = fields.Html(string="Footer Content", translate=True, sanitize=False,
                                             default=_get_default_footer_extra_links)
    website_header_offer_ept = fields.Html(string="Header Offer Content", translate=True, sanitize=False,
                                           default=_get_default_header_content)
    footer_style_1_content_ept = fields.Html(string="Footer Style 1 Content", translate=True, sanitize=False,
                                             default=_get_default_footer_content)
    footer_style_3_content_ept = fields.Html(string="Footer Style 3 Content", translate=True, sanitize=False,
                                             default=_get_footer_style_3_content)
    website_header_extra_links = fields.Html(string="Header Extra Content", translate=True, sanitize=False,
                                             default=_get_default_header_extra_links)
    website_header_extra_offer = fields.Html(string="Header Offer Extra Content", translate=True, sanitize=False,
                                           default=_get_default_header_extra_content)
    equino_header_offer = fields.Html(string="Equino Header Offer Content", translate=True, sanitize=False,
                                     default=_get_default_equino_header_content)
    equino_footer_content_ept = fields.Html(string="Equino Footer Content", translate=True, sanitize=False,
                                      default=_get_default_equino_footer_content)
    website_company_info = fields.Text(string="Company Information", translate=True,
                                       default="We are a team of passionate people whose goal is to improve "
                                               "everyone's life through disruptive products. We build great products to solve your business problems.")

    # to render main parent product.public.category website specific
    def category_check(self):
        return self.env['product.public.category'].sudo().search(
            [('website_published', '=', True), ('parent_id', '=', False), ('website_id', 'in', (False, self.id))])

    # to render full path for breadcrumbs based on argument
    # args : product.public.category
    # return : list of category path and website url
    def get_product_categs_path(self, id):
        categ_set = []
        if id:
            while id:
                categ = self.env['product.public.category'].sudo().search([('id', '=', id)])
                categ_set.append(categ.id)
                if categ and categ.parent_id:
                    id = categ.parent_id.id
                else:
                    break

        # For Reverse order
        categ_set = categ_set[::-1]

        values = {
            'categ_set': categ_set,
            'web_url': self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        }
        return values

    # Return The Current Pricelist Item For diplay a Offer In Slider
    def get_pricelist_item_id(self, product):
        item_ids = self.get_current_pricelist().item_ids
        for item in item_ids:
            if item.date_end and item.date_end >= datetime.today().date():
                if item.applied_on == '0_product_variant':
                    if product.product_variant_id[0].id == item.product_id.id:
                        return item
                elif item.applied_on == '1_product':
                    if product.id == item.product_tmpl_id.id:
                        return item
                elif item.applied_on == '2_product_category':
                    if product.categ_id.id == item.categ_id.id:
                        return item
                elif item.applied_on == '3_global':
                    return item
        return False

    def get_recently_viewed_items(self, product_id=False):
        recently_viewed_product_ids = request.session.get('recently_viewed_product_ids', False)
        if not recently_viewed_product_ids and not product_id:
            return False

        # set product id into session if it not into session if session is not than create a session
        if product_id:
            if recently_viewed_product_ids:
                if product_id not in request.session['recently_viewed_product_ids']:
                    if len(recently_viewed_product_ids) >= 10:
                        recently_viewed_product_ids.pop()
                    tmp = recently_viewed_product_ids
                    tmp.insert(0, product_id)
                    request.session['recently_viewed_product_ids'] = tmp
                else:
                    recently_viewed_product_ids.remove(product_id)
                    tmp = recently_viewed_product_ids
                    tmp.insert(0, product_id)
                    request.session['recently_viewed_product_ids'] = tmp

            else:
                request.session['recently_viewed_product_ids'] = [product_id]

        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency._convert(price, to_currency, request.env.user.company_id,
                                                                fields.Date.today())
        values = {
            'recent_products': request.session.get('recently_viewed_product_ids', False),
            'compute_currency': compute_currency
        }
        return values

    # return brand list
    def get_brand(self):
        brand_list = self.env['product.brand.ept'].sudo().search(
                [('website_published', '=', True), ('website_id', 'in', (False, self.id))])
        return brand_list

    # Get minimum price and maximum price according to Price list as well as discount for Shop page
    def get_min_max_prices(self):
        range_list = []
        cust_min_val = request.httprequest.values.get('min_val', False)
        cust_max_val = request.httprequest.values.get('max_val', False)

        products = self.env['product.template'].search(self.website_domain())
        prices_list = []
        if products:
            pricelist = self.get_current_pricelist()
            for prod in products:
                context = dict(self.env.context, quantity=1, pricelist=pricelist.id if pricelist else False)
                product_template = prod.with_context(context)

                list_price = product_template.price_compute('list_price')[product_template.id]
                price = product_template.price if pricelist else list_price
                if price:
                    prices_list.append(price)

        if not prices_list: return False

        if not cust_min_val and not cust_max_val:
            range_list.append(round(min(prices_list)))
            range_list.append(round(max(prices_list)))
            range_list.append(round(min(prices_list)))
            range_list.append(round(max(prices_list)))
        else:
            range_list.append(cust_min_val)
            range_list.append(cust_max_val)
            range_list.append(round(min(prices_list)))
            range_list.append(round(max(prices_list)))
        return range_list
