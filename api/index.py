from http.server import BaseHTTPRequestHandler
import os
import telebot
import json

# Initialize the bot with your token
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse incoming Telegram update
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Send 200 response first
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode())
        
        # Process the update
        try:
            update = telebot.types.Update.de_json(post_data.decode('utf-8'))
            bot.process_new_updates([update])
        except Exception as e:
            print(f"Error processing update: {str(e)}")
    
    def do_GET(self):
        # This is for health checks and webhook setup
        if self.path == '/api/set-webhook':
            try:
                url = f"https://{self.headers.get('Host')}/api"
                webhook_response = bot.set_webhook(url=url)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success", 
                    "webhook_set": webhook_response,
                    "webhook_url": url
                }).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
        else:
            # Default response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Telegram bot webhook is running!'.encode())
