"""Banking Management System local web server. Run: python web_app.py"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from banking import accounts, transactions

ROOT=Path(__file__).parent; HOST="127.0.0.1"; PORT=8001
class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        raw=json.dumps(payload).encode(); self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(raw))); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers(); self.wfile.write(raw)
    def do_OPTIONS(self):
        self.send_response(204); self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Access-Control-Allow-Headers","Content-Type"); self.send_header("Access-Control-Allow-Methods","GET,POST,OPTIONS"); self.end_headers()
    def do_GET(self):
        path=urlparse(self.path).path
        try:
            if path=="/api/accounts": return self.send_json(200,{"accounts":accounts.list_accounts()})
            if path.startswith("/api/history/"): return self.send_json(200,{"transactions":transactions.history(path.rsplit("/",1)[-1])})
            file=ROOT/"static"/("index.html" if path=="/" else path.lstrip("/"))
            if not file.resolve().is_relative_to((ROOT/"static").resolve()) or not file.is_file(): return self.send_json(404,{"error":"Page not found."})
            raw=file.read_bytes(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8" if file.suffix==".html" else "text/css; charset=utf-8" if file.suffix==".css" else "application/javascript; charset=utf-8"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
        except ValueError as e: self.send_json(400,{"error":str(e)})
    def do_POST(self):
        try:
            body=json.loads(self.rfile.read(int(self.headers.get("Content-Length",0))) or b"{}")
            path=urlparse(self.path).path
            if path=="/api/accounts": result=accounts.create_account(body.get("name",""),body.get("type"),body.get("opening_balance",0),body.get("pin","")); return self.send_json(201,{"account":result})
            if path=="/api/deposit": result=transactions.deposit(body.get("account"),body.get("amount")); return self.send_json(200,{"balance":result})
            if path=="/api/withdraw": result=transactions.withdraw(body.get("account"),body.get("amount"),body.get("pin")); return self.send_json(200,{"balance":result})
            if path=="/api/transfer": result=transactions.transfer(body.get("account"),body.get("destination"),body.get("amount"),body.get("pin")); return self.send_json(200,{"balance":result})
            if path.startswith("/api/close/"): return self.send_json(200,{"account":accounts.close_account(path.rsplit("/",1)[-1])})
            return self.send_json(404,{"error":"Action not found."})
        except (ValueError, json.JSONDecodeError) as e: self.send_json(400,{"error":str(e)})
    def log_message(self, fmt, *args): print("%s - %s"%(self.address_string(),fmt%args))
if __name__=="__main__":
    print(f"Banking Management System running at http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST,PORT),Handler).serve_forever()
