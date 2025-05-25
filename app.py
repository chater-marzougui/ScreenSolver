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

api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)            
model = genai.GenerativeModel('gemini-2.0-flash')
countdown = 12
bg_color = "#692782"
text_color = "#FFFFFF"
text_help = None
with open("forwlan.txt", "r") as f:
    text_help = f.read().strip()

prompt = f"""
Analyze the image and answer the multiple choice question (QCM/MCQ) shown.

Instructions:
1. Carefully read the question and all answer options
2. Determine if this is a single-answer or multiple-answer question.
3. Select the most appropriate answer(s)
4. Provide your response in valid JSON format with these exact key:
   - "final_choice": The letter(s) only (e.g., "A" for single answer, "A,C,E" for multiple answers)

Format requirements:
- For single answers: Use one letter (e.g., "A", "B", "C", etc.)
- For multiple answers: Use comma-separated letters with no spaces (e.g., "A,C", "A,B", "B,C,D" etc.)
- If no question is visible in the image, return "X"

IMPORTANT:
- Do not include any additional text or explanations in the response
- Ensure the response is strictly in JSON format

JSON response format:
{{
    "final_choice": the_answer_here
}}

# If you cannot determine the answer, return "X" as the final choice.

These are some examples of questions you might encounter with their answers they are absolutely right:
{text_help}


The image is provided below. Analyze it and provide your answer in the specified JSON format.
            """

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Monitor")
        self.root.geometry("64x64")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 1)
        self.root.overrideredirect(True)  
        self.root.wm_attributes('-transparentcolor', bg_color)
        
        screen_height = root.winfo_screenheight()
        x_position = 16  # 150px from right edge
        y_position = screen_height - 42  # Middle height
        self.root.geometry(f"108x32+{x_position}+{y_position}")
        
        # Two blocks
        self.frame1 = tk.Frame(root, width=32, height=32, bg=bg_color)
        self.frame1.grid(row=0, column=0)
        self.frame1.grid_propagate(False)
        # transparent background
        self.frame2 = tk.Frame(root, width=76, height=32, bg=bg_color)
        self.frame2.grid(row=0, column=1)
        self.frame2.grid_propagate(False)
        
        # Timer in first block
        self.timer_text = tk.StringVar()
        self.timer_text.set(str(countdown))
        self.timer_label = tk.Label(self.frame1, textvariable=self.timer_text,
                            bg=bg_color, fg=text_color, font=("Arial", 12, "bold"))
        self.timer_label.place(x=5, y=8)
        
        # Result in second block
        self.result_text = tk.StringVar()
        self.result_text.set("")
        self.result_label = tk.Label(self.frame2, textvariable=self.result_text,
                    bg=bg_color, fg=text_color, font=("Arial", 12, "bold"))
        self.result_label.place(x=8, y=8)
        
        # Set frame background to match
        self.frame2.config(bg=bg_color)
        
        # Variables
        self.countdown = countdown
        self.running = True
        self.visible = True
        self.paused = False
        
        # Setup hotkeys
        keyboard.add_hotkey('ctrl+alt', self.toggle_visibility)
        # New hotkey for immediate screenshot
        keyboard.add_hotkey('ctrl+shift', self.take_immediate_screenshot)
        # Hotkey to toggle pause state
        keyboard.add_hotkey('ctrl+space', self.toggle_pause)
        
        # Start the screenshot thread
        self.screenshot_thread = threading.Thread(target=self.screenshot_loop)
        self.screenshot_thread.daemon = True
        self.screenshot_thread.start()
        
        # Use Tkinter's after method for UI updates
        self.update_ui_periodic()
    
    def toggle_visibility(self):
        """Toggle the visibility of the app window"""
        self.visible = not self.visible
        if not self.visible:
            self.update_result("")
        else:
            self.update_result("X")
    
    def take_immediate_screenshot(self):
        """Take an immediate screenshot when CTRL+SHIFT is pressed and reset timer"""
        # Reset the countdown to trigger a new screenshot
        self.countdown = 0
                
    def take_screenshot(self) -> Dict[str, Any]:
        """Send the screenshot to Gemini and return the structured response."""
        delete_temp_files = True
        self.update_result("WAIT...")
        try:
            screenshot = ImageGrab.grab()
            
            # Save to temp file to get size
            temp_filename = "screenshots/temp_screenshot" + str(int(time.time())) + ".png"
            screenshot.save(temp_filename)
            
            # Prepare the image for submission
            with open(temp_filename, 'rb') as img_file:
                image_data = img_file.read()
            
            # Create a multipart message with text and image
            if not image_data:
                print("Screenshot is empty, returning error")
                return {"error": "Screenshot is empty", "final_choice": "X"}
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
                    if "final_choice" in parsed_json and parsed_json["final_choice"].strip().upper() != "X":
                        delete_temp_files = False

                    return parsed_json
                else:
                    # If no JSON found, return the raw text
                    return {"final_choice": "X"}
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw text
                return {"final_choice": "X"}
                
        except Exception as e:
            return {"error": str(e), "final_choice": "X"}
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_filename) and delete_temp_files:
                os.remove(temp_filename)

    def screenshot_loop(self):
        """Main loop for taking screenshots"""
        while self.running:
            if self.paused or not self.visible:
                time.sleep(1)
                continue
            self.countdown = countdown
            
            # Take screenshot at the start of each cycle
            response = self.take_screenshot()
            if "final_choice" in response:
                # Use thread-safe method to update GUI
                self.root.after(0, self.update_result, f"{response['final_choice'].upper().strip()}")
            else:
                self.root.after(0, self.update_result, "X")
            
            # Count down
            while self.countdown > 0 and self.running:
                time.sleep(1)
                if self.visible:  # Only refresh topmost when visible
                    self.root.after(0, lambda: self.root.attributes('-topmost', True))
                if not self.paused and self.visible:
                    self.countdown -= 1
    
    def update_ui_periodic(self):
        """Update the UI elements using Tkinter's after method (thread-safe)"""
        if self.running:
            # Update timer
            current_time = ""
            if self.countdown < 10:
                current_time = "0" + str(self.countdown)
            else:
                current_time = str(self.countdown)
            if not self.visible:
                current_time = ""
            
            self.timer_text.set(current_time)
            
            # Schedule the next update
            self.root.after(500, self.update_ui_periodic)

    def update_result(self, result: str):
        """Update the result text"""
        self.result_text.set(result)
        self.root.update_idletasks()
        
    def toggle_pause(self):
        """Toggle the pause state of the screenshot loop"""
        self.paused = not self.paused
        if self.paused:
            self.update_result("Paused")
        else:
            self.update_result("Running")
        
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
        
    def validate_gemini_api_key(self):
        """Validate if the Gemini API key is set"""
        if not api_key or api_key.strip() == "":
            self.update_result("No Key")
            return
        
        try:
            response = model.generate_content(["Hi"])
            if not response.text:
                self.update_result("GE Err")
                return
        except Exception:
            self.update_result("GE Err")
            return
        
        self.update_result("OK")
            
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    app.validate_gemini_api_key()
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