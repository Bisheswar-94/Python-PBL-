"""Library Management System web server. Run: python web_app.py"""
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from library import books
ROOT=Path(__file__).parent; HOST='127.0.0.1'; PORT=8002
class Handler(BaseHTTPRequestHandler):
    def json(self,status,payload):
        raw=json.dumps(payload).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/api/books': return self.json(200,{'books':books.all_books()})
        file=ROOT/'static'/('index.html' if path=='/' else path.lstrip('/'))
        if not file.resolve().is_relative_to((ROOT/'static').resolve()) or not file.is_file(): return self.json(404,{'error':'Page not found.'})
        raw=file.read_bytes(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8' if file.suffix=='.html' else 'text/css; charset=utf-8' if file.suffix=='.css' else 'application/javascript; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_POST(self):
        try:
            body=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))) or b'{}'); path=urlparse(self.path).path
            if path=='/api/books': return self.json(201,{'book':books.add_book(body.get('title',''),body.get('author',''),body.get('category',''),body.get('copies',1))})
            if path.startswith('/api/borrow/'): return self.json(200,{'book':books.borrow_book(path.rsplit('/',1)[-1],body.get('borrower',''))})
            if path.startswith('/api/return/'): return self.json(200,{'book':books.return_book(path.rsplit('/',1)[-1],body.get('borrower',''))})
            if path.startswith('/api/remove/'): books.remove_book(path.rsplit('/',1)[-1]); return self.json(200,{'ok':True})
            return self.json(404,{'error':'Action not found.'})
        except (ValueError,json.JSONDecodeError) as e: return self.json(400,{'error':str(e)})
    def log_message(self,fmt,*args): print('%s - %s'%(self.address_string(),fmt%args))
if __name__=='__main__':
    print(f'Library Management System running at http://{HOST}:{PORT}')
    ThreadingHTTPServer((HOST,PORT),Handler).serve_forever()
