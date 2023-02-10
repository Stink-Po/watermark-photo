import customtkinter
from PIL import Image, ImageTk, ImageFont, ImageDraw

formats = [('Jpg Files', ('*.jpg', '*.jpeg', '*.jpe')), ('Png Files', '*.png'),
           ]

my_font1 = ('times', 18, 'bold')
canvas_img = None


class PhotoWaterMark:

    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.window = customtkinter.CTk()
        self.window.title("Water mark Photo")
        self.window.config(padx=50, pady=50)
        self.window.geometry("600x600")

        self.canvas = customtkinter.CTkCanvas(master=self.window,
                                              width=400,
                                              height=400,
                                              highlightthickness=0,
                                              bg="black")

        self.input_pic_label = customtkinter.CTkLabel(master=self.window,
                                                      text="Choose Your Photo",
                                                      font=my_font1)

        self.choose_pic_button = customtkinter.CTkButton(master=self.window,
                                                         text="Upload Photo",
                                                         command=lambda: self.upload_file())

        self.change_photo_but = customtkinter.CTkButton(master=self.window,
                                                        text="Change Photo",
                                                        command=lambda: self.change_photo())

        self.next_button = customtkinter.CTkButton(master=self.window,
                                                   text="Next",
                                                   command=lambda: self.set_mod())

        self.add_text_watermark_but = customtkinter.CTkButton(master=self.window,
                                                              text="Next",
                                                              width=200,
                                                              command=lambda: self.adding_text_watermark())

        self.text_watermark_entry = customtkinter.CTkEntry(master=self.window,
                                                           width=150)

        self.text_label = customtkinter.CTkLabel(master=self.window,
                                                 text="Type Your WaterMark",
                                                 font=my_font1)

        self.upload_watermark_btn = customtkinter.CTkButton(master=self.window,
                                                            text="Upload WaterMark",
                                                            command=lambda: self.upload_water_mark())
        self.watermark_file = None
        self.img = None
        self.original_image_size = None
        self.resized_image = None
        self.new_image = None
        self.canvas_img = None
        self.temp_image_save = None
        self.temp_original = None
        self.temp_resized = None
        self.image = None

        self.save_image = customtkinter.CTkButton(master=self.window,
                                                  text="Save Photo",
                                                  command=self.save_photo)

        self.change_text = customtkinter.CTkButton(master=self.window,
                                                   text="Cancel",
                                                   command=lambda: self.change_watermark_text())

        self.temp_image = None
        self.choose_pic()
        self.window.mainloop()

    # let user choose a photo from locaL DRIVE
    def choose_pic(self):
        self.input_pic_label.grid(row=0, column=0, padx=(180, 0), pady=(200, 0))
        self.choose_pic_button.grid(row=1, column=0, padx=(180, 0))

    # this function upload photo to app and resize it for canvas also
    #  ask user if user want to change photo
    def upload_file(self):
        self.choose_pic_button.grid_forget()
        self.input_pic_label.grid_forget()
        f_types = [('Jpg Files', '*.jpg'), ('Png Files', '*.png')]
        filename = customtkinter.filedialog.askopenfilename(filetypes=f_types)
        self.image = Image.open(filename)
        self.temp_original = self.image
        self.original_image_size = self.image.size
        self.resized_image = self.image.resize((400, 400))
        self.temp_resized = self.resized_image
        self.new_image = ImageTk.PhotoImage(self.temp_resized)
        self.temp_image = self.new_image
        self.canvas.grid(row=2, column=1, columnspan=2, padx=(50, 0))
        self.img = self.canvas.create_image(200, 200, image=self.temp_image)
        self.change_photo_but.grid(row=3, column=1, pady=(20, 0), padx=(20, 0))
        self.next_button.grid(row=3, column=2, pady=(20, 0), padx=(10, 0))

    # if choose change photo in past function this function will do it
    def change_photo(self):
        self.next_button.grid_forget()
        self.change_photo_but.grid_forget()
        self.canvas.grid_forget()
        self.choose_pic()

    # ask user if user want to add a text watermark to photo or use photo watermark
    def set_mod(self):
        self.next_button.configure(text="Text", command=lambda: self.text_water_mark())
        self.change_photo_but.configure(text="Photo", command=lambda: self.photo_water_mark())

    # if user choose photo watermark this function grid button to screen that can upload a watermark
    def photo_water_mark(self):
        self.next_button.grid_forget()
        self.change_photo_but.grid_forget()
        self.upload_watermark_btn.grid(row=3, column=1)

    # if user choose a text  watermark this function grid an entry and button to screen for user text watermark
    def text_water_mark(self):
        self.next_button.grid_forget()
        self.change_photo_but.grid_forget()
        self.text_label.grid(row=3, column=1, pady=(20, 0))
        self.text_watermark_entry.grid(row=3, column=2, pady=(20, 0))
        self.add_text_watermark_but.grid(row=4, column=1, columnspan=2, pady=(20, 0), padx=(50, 0))

    # this function add the user text watermark to photo
    def adding_text_watermark(self):
        text = self.text_watermark_entry.get()
        if text != "":
            draw = ImageDraw.Draw(self.image)
            font = ImageFont.truetype('arial.ttf', 36)
            text_width, text_height = draw.textsize(text, font)
            margin = 10
            x = self.original_image_size[0] - text_width - margin
            y = self.original_image_size[1] - text_height - margin
            draw.text((x, y), text, font=font)
            draw_resized = ImageDraw.Draw(self.resized_image)
            canvas_text_width, canvas_text_height = draw_resized.textsize(text, font)
            width, height = self.resized_image.size
            x = width - canvas_text_width - margin
            y = height - canvas_text_height - margin
            draw_resized.text((x, y), text, font=font)
            self.add_text_watermark_but.grid_forget()
            self.text_watermark_entry.grid_forget()
            self.text_label.grid_forget()
            self.new_image = ImageTk.PhotoImage(self.resized_image)
            self.canvas.itemconfig(self.img, image=self.new_image)
            self.save_image.grid(row=3, column=1)
            self.change_text.grid(row=3, column=2)

    # this function save watermarked photo to local DRIVE
    def save_photo(self):
        self.save_image.grid_forget()
        self.change_text.grid_forget()

        result = customtkinter.filedialog.asksaveasfile(filetypes=formats, defaultextension=formats)
        if result:
            self.image.save(fp=result, format=None)
            self.canvas.grid_forget()
            self.choose_pic()

    # if user cancel and the progress of text watermark this function will make a fresh upload window
    def change_watermark_text(self):
        self.save_image.grid_forget()
        self.change_text.grid_forget()
        self.canvas.grid_forget()
        self.choose_pic()

    def upload_water_mark(self):
        global canvas_img
        self.upload_watermark_btn.grid_forget()
        temp_image = self.image.copy()
        temp_canvas_image = self.resized_image.copy()
        f_types = [('Jpg Files', '*.jpg'), ('Png Files', '*.png')]
        filename = customtkinter.filedialog.askopenfilename(filetypes=f_types)
        self.watermark_file = Image.open(filename)
        resize_watermark = self.watermark_file.resize((int(self.original_image_size[0] / 5),
                                                       int(self.original_image_size[1] / 5)))
        resize_for_canvas = self.watermark_file.resize((80, 80))
        x = self.original_image_size[0] - temp_image.size[0] - 10
        y = self.original_image_size[1] - temp_image.size[1] - 10
        temp_image.paste(resize_watermark, (x, y))
        temp_canvas_image.paste(resize_for_canvas, (400 - 80 - 10, 400 - 80 - 10))
        canvas_img = ImageTk.PhotoImage(temp_canvas_image)
        self.canvas.itemconfig(self.img, image=canvas_img)
        self.save_image.grid(row=3, column=1)
        self.change_text.grid(row=3, column=2)


main = PhotoWaterMark()
