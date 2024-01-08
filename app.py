# Import the dependencies.

from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_, text
import locale

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Database/shopping_db.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
trends = base.classes.shoppingtrends

# Create our session (link) from Python to the DB
# Session is created within individual routes and closed
# as having common session throws an intermittent error
# "Objects created in a thread can only be used in that same thread"

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)
# Disable default sorting when Jsonify is used
app.config['JSON_SORT_KEYS'] = False
locale.setlocale(locale.LC_ALL, '')
#################################################
# Global variable setup
#################################################
accepted_input_date_format = "%Y-%m-%d"


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"<b><u>Available Routes</u></b><br/>"
        f"<br/>"
        f"<br/>"
        f"1. Shopping Categories and Summary metadata: &ltbase url&gt/api/v1.0/categories<br/>"
        f"<br/>"
        f"2. Categories and Items within categories with total sales - data model compatible for AnyChart Treemap view: &ltbase url&gt/api/v1.0/&ltcategories&gt/treemap<br/>"
        f"<br/>"
        f"3. Shopping trends for each season for each category as series - data model compatible for AnyChart Bubble chart: &ltbase url&gt/api/v1.0/&ltcategories&gt/bubble<br/>"
        f"<br/>"
        f"4. Payment Type distribution for each category  - data model compatible for AnyChart Pie chart: &ltbase url&gt/api/v1.0/&ltcategories&gt/pie<br/>"
        f"<br/>"
        f"5. Shopping trends by age group  - data model compatible for AnyChart Bar chart: &ltbase url&gt/api/v1.0/&ltcategories&gt/bar<br/>"
        f"<br/>"
        f"6. Total Sales by each US State - data model compatible for AnyChart Map view: &ltbase url&gt/api/v1.0/map<br/>"
    )


# Route 1. List all categories along with summary like Total Sale Amount, Top Payment Type, Top Shipping Type
@app.route("/api/v1.0/categories")
def list_categories():
    session = Session(engine)

    # Find list of distinct categories available in trends database

    categories = {'All': {
        'Total Purchased Amount': locale.currency(session.query(func.sum(trends.PurchaseAmount)).all()[0][0],
                                                  grouping=True),
        'Top Shipping Type':
            session.query(trends.ShippingType, func.count(trends.ShippingType).label('counts')).group_by(
                trends.ShippingType).order_by(text('counts DESC')).all()[0][0],
        'Top Payment Method':
            session.query(trends.ShippingType, func.count(trends.PaymentMethod).label('counts')).group_by(
                trends.PaymentMethod).order_by(text('counts DESC')).all()[0][0],
    }}

    results = session.query(trends.Category).distinct().all()

    for row in results:
        category_name = row[0]
        categories[category_name] = {
            'Total Purchased Amount': locale.currency(session.query(func.sum(trends.PurchaseAmount)).filter(
                trends.Category == category_name).all()[0][0], grouping=True),
            'Top Shipping Type':
                session.query(trends.ShippingType, func.count(trends.ShippingType).label('counts')).filter(
                    trends.Category == category_name).group_by(trends.ShippingType).order_by(text('counts DESC')).all()[
                    0][0],
            'Top Payment Method':
                session.query(trends.PaymentMethod, func.count(trends.PaymentMethod).label('counts')).filter(
                    trends.Category == category_name).group_by(trends.PaymentMethod).order_by(
                    text('counts DESC')).all()[0][0]

        }
    session.close()
    return jsonify(categories)


# Route 2. Total Sales Amount for each Shopping Category and Items within each category
@app.route("/api/v1.0/<category_name>/treemap")
def category_treemap(category_name):
    name = 'name'
    value = 'value'
    children = 'children'
    data = {name: 'Categories - All',
            children: [
                {name: 'Clothing', children: [
                    {name: 'Blouse', value: 10410},
                    {name: 'Dress', value: 10320},
                    {name: 'Hoodie', value: 8767},
                    {name: 'Jeans', value: 7548},
                    {name: 'Pants', value: 10090},
                    {name: 'Shirt', value: 10320},
                    {name: 'Shorts', value: 9433},
                    {name: 'Skirt', value: 9402},
                    {name: 'Socks', value: 9252},
                    {name: 'Sweater', value: 9462},
                    {name: 'T-shirt', value: 9248}
                ]},
                {name: 'Accessories', children: [
                    {name: 'Backpack', value: 8636},
                    {name: 'Belt', value: 9635},
                    {name: 'Gloves', value: 8477},
                    {name: 'Handbag', value: 8857},
                    {name: 'Hat', value: 9375},
                    {name: 'Jewelry', value: 10010},
                    {name: 'Scarf', value: 9561},
                    {name: 'Sunglasses', value: 9649}
                ]},
                {name: 'Footwear', children: [
                    {name: 'Boots', value: 9018},
                    {name: 'Sandals', value: 9200},
                    {name: 'Shoes', value: 9240},
                    {name: 'Sneakers', value: 8635}
                ]},
                {name: 'Outerwear', children: [
                    {name: 'Coat', value: 9275},
                    {name: 'Jacket', value: 9249}
                ]}
            ]}

    match category_name:
        case "All":
            return data
        case "Clothing" | "Footwear" | "Outerwear" | "Accessories":
            for element in data[children]:
                if element[name] == category_name:
                    return element


# Route 3. Total Sales Amount for each category per season
@app.route("/api/v1.0/<category_name>/bubble")
def category_bubble(category_name):
    data = {'Clothing': [['Fall', 26220], ['Winter', 27274], ['Spring', 27692], ['Summer', 23078]],
            'Accessories': [['Fall', 19874], ['Winter', 18291], ['Spring', 17007], ['Summer', 19028]],
            'Outerwear': [['Fall', 5259], ['Winter', 4562], ['Spring', 4425], ['Summer', 4278]],
            'Footwear': [['Fall', 8665], ['Winter', 8480], ['Spring', 9555], ['Summer', 9393]]}

    match category_name:
        case "All":
            return data
        case "Clothing" | "Footwear" | "Outerwear" | "Accessories":
            return data[category_name]


# Route 4. Payment type used distribution for each shopping category
@app.route("/api/v1.0/<category_name>/pie")
def category_pie(category_name):
    x_value = 'x'
    value = 'value'

    data = {'All': [
        {x_value: "Bank Transfer", value: 632},
        {x_value: "Cash", value: 648},
        {x_value: "Credit Card", value: 696},
        {x_value: "Debit Card", value: 633},
        {x_value: "PayPal", value: 638},
        {x_value: "Venmo", value: 653}
        ],
        'Clothing': [
        {x_value: "Bank Transfer", value: 291},
        {x_value: "Cash", value: 281},
        {x_value: "Credit Card", value: 319},
        {x_value: "Debit Card", value: 286},
        {x_value: "PayPal", value: 274},
        {x_value: "Venmo", value: 286}
        ],
        'Accessories': [
        {x_value: "Bank Transfer", value: 198},
        {x_value: "Cash", value: 200},
        {x_value: "Credit Card", value: 245},
        {x_value: "Debit Card", value: 195},
        {x_value: "PayPal", value: 199},
        {x_value: "Venmo", value: 203}
        ],
        'Outerwear': [
        {x_value: "Bank Transfer", value: 45},
        {x_value: "Cash", value: 62},
        {x_value: "Credit Card", value: 48},
        {x_value: "Debit Card", value: 61},
        {x_value: "PayPal", value: 52},
        {x_value: "Venmo", value: 56}
        ],
        'Footwear': [
         {x_value: "Bank Transfer", value: 98},
        {x_value: "Cash", value: 105},
        {x_value: "Credit Card", value: 84},
        {x_value: "Debit Card", value: 91},
        {x_value: "PayPal", value: 113},
        {x_value: "Venmo", value: 108}
        ]}

    return data[category_name]


# Route 5. Total Sales Amount by age group for each category
@app.route("/api/v1.0/<category_name>/bar")
def category_bar(category_name):
    x_value = 'x'
    value = 'value'

    data = {'Clothing': [['below 20', 6188], ['21-30', 20014], ['31-40', 18883], ['41-50', 19462], ['51-60', 20296], ['above 60', 19421]],
            'Accessories': [['below 20', 3332], ['21-30', 14732], ['31-40', 14447], ['41-50', 13723], ['51-60', 13456], ['above 60', 14510]],
            'Outerwear': [['below 20', 1279], ['21-30', 3200], ['31-40', 3353], ['41-50', 3986], ['51-60', 3425], ['above 60', 3281]],
            'Footwear': [['below 20', 1705], ['21-30', 6829], ['31-40', 6510], ['41-50', 6958], ['51-60', 8139], ['above 60', 5952]]}

    match category_name:
        case "All":
            return data
        case "Clothing" | "Footwear" | "Outerwear" | "Accessories":
            return data[category_name]

    return data[category_name]


# Route 6. Total Sales amount for each USA states
@app.route("/api/v1.0/map")
def shopping_map():
    data = [
        {'id': 'US.AL', 'value': 5261},
        {'id': 'US.AK', 'value': 4867},
        {'id': 'US.AZ', 'value': 4326},
        {'id': 'US.AR', 'value': 4828},
        {'id': 'US.CA', 'value': 5605},
        {'id': 'US.CO', 'value': 4222},
        {'id': 'US.CT', 'value': 4226},
        {'id': 'US.DE', 'value': 4758},
        {'id': 'US.FL', 'value': 3798},
        {'id': 'US.GA', 'value': 4645},
        {'id': 'US.HI', 'value': 3752},
        {'id': 'US.ID', 'value': 5587},
        {'id': 'US.IL', 'value': 5617},
        {'id': 'US.IN', 'value': 4655},
        {'id': 'US.IA', 'value': 4201},
        {'id': 'US.KS', 'value': 3437},
        {'id': 'US.KY', 'value': 4402},
        {'id': 'US.LA', 'value': 4848},
        {'id': 'US.ME', 'value': 4388},
        {'id': 'US.MD', 'value': 4795},
        {'id': 'US.MA', 'value': 4384},
        {'id': 'US.MI', 'value': 4533},
        {'id': 'US.MN', 'value': 4977},
        {'id': 'US.MS', 'value': 4883},
        {'id': 'US.MO', 'value': 4691},
        {'id': 'US.MT', 'value': 5784},
        {'id': 'US.NE', 'value': 5172},
        {'id': 'US.NV', 'value': 5514},
        {'id': 'US.NH', 'value': 4219},
        {'id': 'US.NJ', 'value': 3802},
        {'id': 'US.NM', 'value': 5014},
        {'id': 'US.NY', 'value': 5257},
        {'id': 'US.NC', 'value': 4742},
        {'id': 'US.ND', 'value': 5220},
        {'id': 'US.OH', 'value': 4649},
        {'id': 'US.OK', 'value': 4376},
        {'id': 'US.OR', 'value': 4243},
        {'id': 'US.PA', 'value': 4926},
        {'id': 'US.RI', 'value': 3871},
        {'id': 'US.SC', 'value': 4439},
        {'id': 'US.SD', 'value': 4236},
        {'id': 'US.TN', 'value': 4772},
        {'id': 'US.TX', 'value': 4712},
        {'id': 'US.UT', 'value': 4443},
        {'id': 'US.VT', 'value': 4860},
        {'id': 'US.VA', 'value': 4842},
        {'id': 'US.WA', 'value': 4623},
        {'id': 'US.WV', 'value': 5174},
        {'id': 'US.WI', 'value': 4196},
        {'id': 'US.WY', 'value': 4309}
    ]
    return data


if __name__ == "__main__":
    app.run(debug=True)
