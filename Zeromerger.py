import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import *
from PIL import Image, ImageTk

class MapMergerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("2b2t Map Merger by RobinZero")
        self.master.configure(bg="#3f3f3f")

        self.cell_size = 64  # Half the size of each grid cell
        self.grid_size = (2, 2)  # Default grid size
        self.images = {}
        self.file_name = tk.StringVar(value="merged_map.png")  # Default file name
        self.create_widgets()
        self.create_grid()

    def create_widgets(self):
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack(expand=True, fill=tk.BOTH)
        self.grid_frame.configure(bg="#3f3f3f")

        control_frame = tk.Frame(self.master)
        control_frame.pack()
        control_frame.configure(bg="#3f3f3f")

        self.rows_var = tk.IntVar(value=self.grid_size[0])
        self.cols_var = tk.IntVar(value=self.grid_size[1])

        tk.Label(control_frame, text="Rows:", bg="#3f3f3f", fg="white").grid(row=0, column=0, pady=5)
        tk.Entry(control_frame, textvariable=self.rows_var, width=5).grid(row=0, column=1, pady=5)
        tk.Label(control_frame, text="Columns:", bg="#3f3f3f", fg="white").grid(row=0, column=2, pady=5)
        tk.Entry(control_frame, textvariable=self.cols_var, width=5).grid(row=0, column=3, pady=5)

        tk.Label(control_frame, text="File Name:", bg="#3f3f3f", fg="white").grid(row=1, column=0, pady=5)
        tk.Entry(control_frame, textvariable=self.file_name, width=40).grid(row=1, column=1, columnspan=3, pady=5)

        tk.Button(control_frame, text="Choose Save Location", command=self.choose_save_location, bg="#3f3f3f", fg="white").grid(row=2, column=3, pady=5)
        tk.Button(control_frame, text="Update Grid", command=self.update_grid, bg="#3f3f3f", fg="white").grid(row=2, column=0, pady=5)
        tk.Button(control_frame, text="Merge", command=self.merge_images, bg="#3f3f3f", fg="white").grid(row=2, column=1, pady=5)

    def create_grid(self):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                frame = tk.Frame(self.grid_frame, width=self.cell_size, height=self.cell_size, bg="white", borderwidth=1, relief="solid")
                frame.grid(row=row, column=col, padx=1, pady=1)
                frame.drop_target_register(DND_FILES)
                frame.dnd_bind('<<Drop>>', self.drop)

                self.images[(row, col)] = None

    def update_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.grid_size = (self.rows_var.get(), self.cols_var.get())
        self.create_grid()

    def drop(self, event):
        file_path = event.data
        if file_path:
            grid_info = event.widget.grid_info()
            row, col = grid_info['row'], grid_info['column']
            self.add_image(row, col, file_path)

    def add_image(self, row, col, file_path):
        image = Image.open(file_path)
        original_image = image.copy()  # Make a copy of the original image
        image.thumbnail((self.cell_size, self.cell_size))
        image_tk = ImageTk.PhotoImage(image)

        frame = tk.Label(self.grid_frame, bg="white", borderwidth=0)
        frame.grid(row=row, column=col, padx=1, pady=1)

        label = tk.Label(frame, image=image_tk)
        label.image = image_tk
        label.pack(expand=True)  # Center the image in the cell

        self.images[(row, col)] = (original_image, image)

    def merge_images(self):
        merged_width = 0
        merged_height = 0

        # Calculate dimensions of the merged image based on the original image sizes
        for (row, col), image_data in self.images.items():
            if image_data:
                original_image, _ = image_data
                image_width, image_height = original_image.size
                merged_width = max(merged_width, (col + 1) * image_width)
                merged_height = max(merged_height, (row + 1) * image_height)

        # Create a transparent background for the merged image
        merged_image = Image.new("RGBA", (merged_width, merged_height), (0, 0, 0, 0))

        # Paste original images onto the merged image
        for (row, col), image_data in self.images.items():
            if image_data:
                original_image, _ = image_data
                image_width, image_height = original_image.size
                x = col * image_width
                y = row * image_height
                merged_image.paste(original_image, (x, y))

        # Save the merged image
        save_path = filedialog.asksaveasfilename(initialfile=self.file_name.get(), defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            merged_image.save(save_path)

    def choose_save_location(self):
        save_path = filedialog.askdirectory()
        if save_path:
            self.file_name.set(save_path + "/merged_map.png")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = MapMergerApp(root)
    root.mainloop()
