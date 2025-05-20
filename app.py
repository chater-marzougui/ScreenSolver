import tkinter as tk
import time
import threading
import os
from PIL import ImageGrab
import google.generativeai as genai
import json
from typing import Dict, Any
import keyboard
import dotenv
import os
dotenv.load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))            
model = genai.GenerativeModel('gemini-2.0-flash')
countdown = 12

prompt = """See the the image and respond to the QCM question in it, choose the best answer.
            The answer should be a single word, and the response should be in a valid JSON structure
            with keys 'response' and 'final_choice' which is a single letter (comma seperated if multi answer),
            if there's no question return the letter X in both response and final_choice."""

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Monitor")
        self.root.geometry("64x64")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', '')# Always on top
        # self.root.attributes('-alpha', 0.6)     # Transparency (0.5/1.0)
        self.root.overrideredirect(True)        # Remove title bar/window decorations
        
        # Position in middle-right of screen
        # screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = 16  # 150px from right edge
        y_position = screen_height - 42  # Middle height
        self.root.geometry(f"64x32+{x_position}+{y_position}")
        
        # Two blocks
        self.frame1 = tk.Frame(root, width=32, height=32, bg="")
        self.frame1.grid(row=0, column=0)
        self.frame1.grid_propagate(False)
        # transparent background
        self.frame2 = tk.Frame(root, width=32, height=32, bg="")
        self.frame2.grid(row=0, column=1)
        self.frame2.grid_propagate(False)
        
        # Timer in first block
        self.timer_text = tk.StringVar()
        self.timer_text.set(str(countdown))
        self.timer_label = tk.Label(self.frame1, textvariable=self.timer_text,
                            bg="#692782", fg="#FFFFFF", font=("Arial", 12, "bold"))
        self.timer_label.place(x=5, y=8)
        
        # Result in second block
        self.result_text = tk.StringVar()
        self.result_text.set("X")
        self.result_label = tk.Label(self.frame2, textvariable=self.result_text,
                            bg="#692782", fg="#FFFFFF", font=("Arial", 12, "bold"))
        self.result_label.place(x=5, y=8)
        
        # Variables
        self.countdown = countdown
        self.running = True
        self.visible = True  # Track visibility state
        
        # Setup hotkeys
        keyboard.add_hotkey('ctrl+alt', self.toggle_visibility)
        # New hotkey for immediate screenshot
        keyboard.add_hotkey('ctrl+shift', self.take_immediate_screenshot)
        
        # Start the screenshot thread
        self.screenshot_thread = threading.Thread(target=self.screenshot_loop)
        self.screenshot_thread.daemon = True
        self.screenshot_thread.start()
        
        # Start the UI update thread
        self.ui_thread = threading.Thread(target=self.update_ui)
        self.ui_thread.daemon = True
        self.ui_thread.start()
    
    def toggle_visibility(self):
        """Toggle the visibility of the app window"""
        if self.visible:
            self.root.withdraw()  # Hide the window
            self.visible = False
        else:
            self.root.deiconify()  # Show the window
            self.root.attributes('-topmost', True)  # Make sure it's on top
            self.visible = True
    
    def take_immediate_screenshot(self):
        """Take an immediate screenshot when CTRL+SHIFT is pressed and reset timer"""
        # Reset the countdown to trigger a new screenshot
        self.countdown = 0
                
    def take_screenshot(self) -> Dict[str, Any]:
        """Send the screenshot to Gemini and return the structured response."""
        try:
            screenshot = ImageGrab.grab()
            
            # Save to temp file to get size
            temp_filename = "temp_screenshot.png"
            screenshot.save(temp_filename)
            
            # Prepare the image for submission
            with open(temp_filename, 'rb') as img_file:
                image_data = img_file.read()
            
            # Create a multipart message with text and image
            response = model.generate_content([prompt, {"mime_type": "image/png", "data": image_data}])
            
            # Extract the text response
            text_response = response.text
            
            # Try to parse JSON from the response text
            try:
                # Find JSON in the response (in case it's embedded in text)
                json_start = text_response.find('{')
                json_end = text_response.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = text_response[json_start:json_end]
                    parsed_json = json.loads(json_str)
                    return parsed_json
                else:
                    # If no JSON found, return the raw text
                    return {"raw_response": text_response, "final_choice": "X"}
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw text
                return {"raw_response": text_response, "final_choice": "X"}
                
        except Exception as e:
            return {"error": str(e), "final_choice": "X"}
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    def screenshot_loop(self):
        """Main loop for taking screenshots"""
        while self.running:
            self.countdown = countdown
            
            # Take screenshot at the start of each cycle
            response = self.take_screenshot()
            if "final_choice" in response:
                self.result_text.set(f"{response['final_choice'].upper()}")
            else:
                self.result_text.set("X")
            
            # Count down
            while self.countdown > 0 and self.running:
                time.sleep(1)
                if self.visible:  # Only refresh topmost when visible
                    self.root.attributes('-topmost', True)
                self.countdown -= 1
    
    def update_ui(self):
        """Update the UI elements"""
        while self.running:
            # Update timer
            current_time = ""
            if self.countdown < 10:
                current_time = "0" + str(self.countdown)
            else:
                current_time = str(self.countdown)
            self.timer_text.set(current_time)
            time.sleep(0.5)
    
    def start_move(self, event):
        """Start window drag operation"""
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        """Stop window drag operation"""
        self.x = None
        self.y = None

    def do_move(self, event):
        """Move the window during drag operation"""
        dx = event.x - self.x
        dy = event.y - self.y
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        self.root.geometry(f"+{x}+{y}")
    
    def on_closing(self):
        """Handle window closing"""
        self.running = False
        keyboard.unhook_all()  # Remove hotkey listeners
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    # Add right-click menu to close the app
    root.bind("<Button-3>", lambda event: show_popup(event, app))
    
    # Create popup menu
    def show_popup(event, app):
        popup_menu = tk.Menu(root, tearoff=0)
        popup_menu.add_command(label="Close", command=app.on_closing)
        popup_menu.add_command(label="Toggle Visibility", command=app.toggle_visibility)
        popup_menu.add_command(label="Take Screenshot Now", command=app.take_immediate_screenshot)
        popup_menu.tk_popup(event.x_root, event.y_root)
        
    root.mainloop()