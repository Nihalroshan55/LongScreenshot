from selenium import webdriver
from PIL import Image, ImageTk
import io
import tkinter as tk
from tkinter import filedialog, messagebox

class LongScreenshotApp:
    def __init__(self, master):
        self.master = master
        master.title("Long Screenshot App")

        self.url_label = tk.Label(master, text="Enter URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_save_path)
        self.browse_button.pack()

        self.save_path_label = tk.Label(master, text="Save Path:")
        self.save_path_label.pack()

        self.save_path_entry = tk.Entry(master, width=50)
        self.save_path_entry.pack()

        self.scroll_pause_label = tk.Label(master, text="Scroll Pause Time (seconds):")
        self.scroll_pause_label.pack()

        self.scroll_pause_entry = tk.Entry(master)
        self.scroll_pause_entry.pack()

        self.image_height_label = tk.Label(master, text="Image Height:")
        self.image_height_label.pack()

        self.image_height_entry = tk.Entry(master)
        self.image_height_entry.pack()

        self.run_button = tk.Button(master, text="Take Long Screenshot", command=self.take_long_screenshot)
        self.run_button.pack()

    def browse_save_path(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        self.save_path_entry.delete(0, tk.END)
        self.save_path_entry.insert(0, save_path)

    def take_long_screenshot(self):
        url = self.url_entry.get()
        save_path = self.save_path_entry.get()
        scroll_pause_time = float(self.scroll_pause_entry.get()) if self.scroll_pause_entry.get() else 1.0
        image_height = int(self.image_height_entry.get()) if self.image_height_entry.get() else 800

        self.run_button.config(state=tk.DISABLED)

        try:
            # Set up the webdriver
            driver = webdriver.Chrome()
            driver.get(url)

            # Get the total height of the webpage
            total_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

            # Set the viewport height
            driver.set_window_size(driver.execute_script("return window.innerWidth;"), image_height)

            # Initialize an image to store the long screenshot
            stitched_image = Image.new("RGB", (driver.execute_script("return window.innerWidth;"), total_height), "white")

            # Scroll and capture screenshot in chunks
            offset = 0
            while offset < total_height:
                # Scroll to the current offset
                driver.execute_script(f"window.scrollTo(0, {offset});")
                # Wait for the page to load
                driver.implicitly_wait(1)
                # Capture the screenshot of the current viewport
                screenshot = driver.get_screenshot_as_png()
                screenshot = Image.open(io.BytesIO(screenshot))
                # Paste the current screenshot onto the stitched image
                stitched_image.paste(screenshot, (0, offset))
                # Increment the offset for the next iteration
                offset += image_height

            # Save the final stitched image
            stitched_image.save(save_path)

            # Show success message
            messagebox.showinfo("Success", "Long screenshot saved successfully!")

        except Exception as e:
            # Show error message
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            # Close the webdriver
            driver.quit()
            self.run_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = LongScreenshotApp(root)
    root.mainloop()
