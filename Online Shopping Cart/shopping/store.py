"""Product tuples, cart tuple operations, and simple local persistence."""
import json
from pathlib import Path
DATA_FILE=Path(__file__).resolve().parent.parent/'cart_data.json'
# Each immutable product tuple: (id, name, category, price, stock)
PRODUCTS=[(1,'Canvas Weekender','Bags',54.00,12),(2,'Everyday Bottle','Home',22.50,18),(3,'Linen Notebook Set','Stationery',16.00,25),(4,'Classic Desk Lamp','Home',68.00,7),(5,'Soft Knit Throw','Living',47.00,9),(6,'Travel Pouch','Bags',19.50,15)]

def load_cart():
    """Load a list of cart item tuples from JSON."""
    if not DATA_FILE.exists(): return []
    try: return [tuple(item) for item in json.loads(DATA_FILE.read_text(encoding='utf-8'))]
    except (OSError,json.JSONDecodeError,TypeError): return []

def save_cart(cart):
    """JSON stores arrays; convert tuples for saving and restore them on load."""
    DATA_FILE.write_text(json.dumps(cart,indent=2),encoding='utf-8')

def product_list():
    """Return the product catalog as a list of tuples."""
    return [{'id':p[0],'name':p[1],'category':p[2],'price':p[3],'stock':p[4]} for p in PRODUCTS]

def add_to_cart(product_id,quantity=1):
    """Add to cart by rebuilding tuples because tuple values cannot be changed."""
    try: quantity=int(quantity)
    except (TypeError,ValueError): raise ValueError('Quantity must be a whole number.')
    if quantity<1: raise ValueError('Choose at least one item.')
    product=next((p for p in PRODUCTS if str(p[0])==str(product_id)),None)
    if product is None: raise ValueError('Product not found.')
    cart=load_cart(); existing=next((i for i,x in enumerate(cart) if x[0]==product[0]),None)
    new_quantity=quantity+(cart[existing][3] if existing is not None else 0)
    if new_quantity>product[4]: raise ValueError('Only '+str(product[4])+' are available.')
    item=(product[0],product[1],product[3],new_quantity)
    if existing is None: cart.append(item)
    else: cart[existing]=item
    save_cart(cart); return cart_view()

def set_quantity(product_id,quantity):
    """Replace one cart tuple with an updated tuple, or remove it at zero."""
    try: quantity=int(quantity)
    except (TypeError,ValueError): raise ValueError('Quantity must be a whole number.')
    cart=load_cart(); found=False; updated=[]
    for item in cart:
        if str(item[0])==str(product_id):
            found=True
            if quantity>0:
                product=next(p for p in PRODUCTS if p[0]==item[0])
                if quantity>product[4]: raise ValueError('Only '+str(product[4])+' are available.')
                updated.append((item[0],item[1],item[2],quantity))
        else: updated.append(item)
    if not found: raise ValueError('Cart item not found.')
    save_cart(updated); return cart_view()

def cart_view():
    """Convert tuples to display dictionaries and calculate the total."""
    items=load_cart(); view=[{'id':x[0],'name':x[1],'price':x[2],'quantity':x[3],'subtotal':round(x[2]*x[3],2)} for x in items]
    return {'items':view,'count':sum(x[3] for x in items),'total':round(sum(x[2]*x[3] for x in items),2)}

def clear_cart():
    """Empty the list of cart item tuples."""
    save_cart([]); return cart_view()
