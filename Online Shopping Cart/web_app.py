"""Online Shopping Cart web server. Run: python web_app.py"""
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from shopping import store
ROOT=Path(__file__).parent; HOST='127.0.0.1'; PORT=8003
class Handler(BaseHTTPRequestHandler):
    def json(self,status,payload):
        raw=json.dumps(payload).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/api/products': return self.json(200,{'products':store.product_list()})
        if path=='/api/cart': return self.json(200,store.cart_view())
        file=ROOT/'static'/('index.html' if path=='/' else path.lstrip('/'))
        if not file.resolve().is_relative_to((ROOT/'static').resolve()) or not file.is_file(): return self.json(404,{'error':'Page not found.'})
        raw=file.read_bytes(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8' if file.suffix=='.html' else 'text/css; charset=utf-8' if file.suffix=='.css' else 'application/javascript; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_POST(self):
        try:
            body=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))) or b'{}'); path=urlparse(self.path).path
            if path=='/api/cart/add': return self.json(200,store.add_to_cart(body.get('id'),body.get('quantity',1)))
            if path=='/api/cart/quantity': return self.json(200,store.set_quantity(body.get('id'),body.get('quantity',1)))
            if path=='/api/cart/clear': return self.json(200,store.clear_cart())
            return self.json(404,{'error':'Action not found.'})
        except (ValueError,json.JSONDecodeError) as e: return self.json(400,{'error':str(e)})
    def log_message(self,fmt,*args): print('%s - %s'%(self.address_string(),fmt%args))
if __name__=='__main__':
    print(f'Online Shopping Cart running at http://{HOST}:{PORT}')
    ThreadingHTTPServer((HOST,PORT),Handler).serve_forever()
