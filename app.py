from bottle import route, run, template, SimpleTemplate, static_file
import sqlite3
import logging

# Define the batch filter function
def batch(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

# Register the batch filter with SimpleTemplate
SimpleTemplate.defaults['batch'] = batch

# Sqlite dict factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Establish sqlite connection
conn = sqlite3.connect("db.sqlite")

# Set row factory to get result as dict instead of list
# Make sure this is executed before cursor init
conn.row_factory = dict_factory

# Sqlite cursor
cur = conn.cursor()

@route('/')
def index():
    """Index page"""
    stmt = "SELECT * FROM products ORDER BY id DESC"
    cur.execute(stmt)
    products = list(cur.fetchall())
    return template('index.html', products=products)

@route('/product/<product_id>')
def product(product_id: int):
    """Product details page"""
    stmt = "SELECT * FROM products where id = ?"
    cur.execute(stmt, [str(product_id)])
    product = cur.fetchone()
    return template('product.html', product=product)

@route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./static')


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)


# <div class="columns is-multiline is-mobile">
#     % for product in products:
#         <div class="column is-half-mobile is-one-third-tablet">
#             <div id="product_component_6854648660149" class="product-component"><a
#                 href="/product/{{product['id']}}"
#                 title="{{ product['product_name'] }}"><img
#                 src="{{ product['product_image'] }}"></a>
#             <h2 class="product-component__title">{{ product['product_name'] }}</h2>
#             <div class="product-component__prices"><span
#                 class="product-component__prices__product-price">${{ product['product_price']}} </span>
#                 <!---->
#             </div>
#             </div>
#         </div>
#     % end
# </div>