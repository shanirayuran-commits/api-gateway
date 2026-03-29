import asyncio
import threading
import uvicorn
import customtkinter as ctk
from main import app, logger
import logging
from datetime import datetime

class LogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg + "\n")
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")
        self.text_widget.after(0, append)

class GatewayDesktopApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("High-Concurrency API Gateway")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # UI Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkLabel(self, text="API Gateway Status: Running", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Log Display
        self.log_display = ctk.CTkTextbox(self, state="disabled", font=("Consolas", 12))
        self.log_display.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

        # Stats/Info Panel
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.status_label = ctk.CTkLabel(self.info_frame, text="Port: 8000 | Burst: 20 | Rate: 2/s")
        self.status_label.pack(side="left", padx=20, pady=10)

        # Test Button
        self.test_button = ctk.CTkButton(self.info_frame, text="Send Test Request", command=self.send_test_request)
        self.test_button.pack(side="right", padx=20, pady=10)

        # Initial Log Message
        self.log_message("System initialized. Server starting on http://127.0.0.1:8000")
        self.log_message("Waiting for incoming requests...")

    def log_message(self, message: str):
        self.log_display.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_display.insert("end", f"{timestamp} [INFO] {message}\n")
        self.log_display.see("end")
        self.log_display.configure(state="disabled")

    def send_test_request(self):
        def run_test():
            self.log_message("Sending internal test request...")
            try:
                import httpx
                with httpx.Client() as client:
                    response = client.get("http://127.0.0.1:8000/test", headers={"X-API-Key": "secret-token-123"})
                    self.log_message(f"Test Response: {response.status_code}")
            except Exception as e:
                self.log_message(f"Test Error: {str(e)}")
        
        threading.Thread(target=run_test, daemon=True).start()

    def start_server(self):
        # Setup Logging to UI - moved here to ensure it's initialized before server starts
        handler = LogHandler(self.log_display)
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S"))
        
        # Add to the specific gateway logger only to avoid duplicates from root/uvicorn
        logger.propagate = False
        logger.handlers = [handler]
        
        logging.getLogger("uvicorn.access").disabled = True
        logging.getLogger("uvicorn.error").disabled = True

        def run():
            config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
            server = uvicorn.Server(config)
            server.run()
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()

if __name__ == "__main__":
    app_gui = GatewayDesktopApp()
    app_gui.start_server()
    app_gui.mainloop()
