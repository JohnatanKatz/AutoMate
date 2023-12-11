from PIL import Image
from source.automations.macro import Macro
from source.utility import miscfunctions
from source.automations import macro, imageclick
from source.automations.imageclick import ImageClick
from source.utility.toast import *
from filehandler import *
import os

def trace_callback(*args):
    print("Variable changed:", args)
class FileDataError(Exception):
    pass

class ButtonRowApp:
    def __init__(self, root):
        self.root = root
        #program data intilization
        self.image_count = 1
        self.loop_repetitions = 0
        self.widget_rows = []  # List of rows containing widgets
        self.data_rows = []  # List of rows containing Macro objects or ImageClick objects

        self.root.title("Button Row Example")
        self.root.geometry(f"{1100}x{580}")

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=0)
        self.root.grid_rowconfigure(0, weight=1)

        #sidebar initialization
        sidebar_frame = ctk.CTkFrame(self.root, width=140, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        sidebar_frame.grid_rowconfigure(4, weight=1)
        logo_label = ctk.CTkLabel(sidebar_frame, text="AutoMate", font=ctk.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        sidebar_load = ctk.CTkButton(sidebar_frame, text="Load", command=lambda: self.load_ui())
        sidebar_load.grid(row=1, column=0, padx=20, pady=10)
        sidebar_save = ctk.CTkButton(sidebar_frame, text="Save", command=lambda: save(self.data_rows, self.loop_repetitions, self.root))
        sidebar_save.grid(row=2, column=0, padx=20, pady=10)
        sidebar_button_3 = ctk.CTkButton(sidebar_frame)
        sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
        appearance_mode_label = ctk.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        appearance_mode_optionemenu = ctk.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        scaling_label = ctk.CTkLabel(sidebar_frame, text="UI Scaling:", anchor="w")
        scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        scaling_optionemenu = ctk.CTkOptionMenu(sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.scrollable_frame = ctk.CTkScrollableFrame(self.root, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)


        self.add_ImageClick_row("Normal", 1, 0)  # Initial button row

        #title_label = ctk.CTkLabel(self.scrollable_frame, text="Full Repetitions")
        #title_label.grid(row=0, column=3, padx=4, pady=4)
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Runtime")
        title_label.grid(row=0, column=2, padx=4, pady=4)
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Repetitions")
        title_label.grid(row=0, column=3, padx=4, pady=4)
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Pause S")
        title_label.grid(row=0, column=4, padx=4, pady=4)

        grid_button = ctk.CTkFrame(self.root)
        grid_button.grid(row=1, column=1)#padx=8, pady=8)
        add_row_button = ctk.CTkButton(grid_button, text="Add Image Recognition", command=lambda: self.add_ImageClick_row("Normal",1,0))
        add_row_button.grid(row=0, column=0, padx=10, pady=10)
        add_row_button = ctk.CTkButton(grid_button, text="Add Macro", command=lambda: self.add_Macro_row("Normal",1, 0))
        add_row_button.grid(row=0, column=1, padx=10, pady=10)
        add_row_button = ctk.CTkButton(grid_button, text="Play all", command=lambda: self.play_all())
        add_row_button.grid(row=0, column=2, padx=10, pady=10)


        file_menu = tk.Menu(self.root, tearoff=0)
        #self.root.add_cascade(label="File", menu=file_menu)
        #file_menu.add_command(label="Open", command=self.load)
        #file_menu.add_command(label="Save", command=self.save)


    def add_ImageClick_row(self, option, repeat, pause):
        """
        Sets up the row of widgets for the ImageClick object
        """
        row_number = len(self.widget_rows) + 1

        row_number_var = tk.StringVar(value=str(row_number))

        # Numerical input field for changing row position
        new_row_number_entry = ctk.CTkEntry(self.scrollable_frame, textvariable=row_number_var)
        new_row_number_entry.configure(width=40)
        new_row_number_entry.grid(row=row_number, column=0, padx=4, pady=4)
        new_row_number_entry.bind("<FocusOut>", lambda event, widget=new_row_number_entry: self.update_row_position(event, widget))
        #row_number_var.trace("w", trace_callback)  # "w" stands for "write"

        image_input = ctk.CTkFrame(self.scrollable_frame)
        image_input.grid(row=row_number, column=1, padx=0, pady=0)

        # Screen cut icon button (Replace with your icon)
        screen_cut_button = ctk.CTkButton(image_input, text="Screen Cut")
        screen_cut_button.configure(command=lambda widget=image_input: self.screen_shot(widget))
        #screen_cut_button.grid(row=row_number, column=1, padx=4, pady=4)
        screen_cut_button.pack(side= ctk.LEFT, padx=4, pady=4)

        # Open file icon button (Replace with your icon)
        open_file_button = ctk.CTkButton(image_input, text="Open File")
        open_file_button.configure(command=lambda widget=image_input: self.open_image(widget))
        #open_file_button.grid(row=row_number, column=2, padx=4, pady=4)
        open_file_button.pack(side= ctk.RIGHT, padx=4, pady=4)

        widgets = self.common_row_ui(option, repeat, pause, row_number)

        self.widget_rows.append([new_row_number_entry, image_input, widgets[0], widgets[1], widgets[2], widgets[3]])
        data = {'object': ImageClick(), 'option': "normal", 'repeat': repeat, 'pause': pause}
        self.data_rows.append(data)

    def add_Macro_row(self, option, repeat, pause):
        row_number = len(self.widget_rows) + 1

        row_number_var = tk.StringVar(value=str(row_number))

        # Numerical input field for changing row position
        new_row_number_entry = ctk.CTkEntry(self.scrollable_frame, textvariable=row_number_var)
        new_row_number_entry.grid(row=row_number, column=0, padx=4, pady=4)
        new_row_number_entry.bind("<FocusOut>", lambda event, widget=new_row_number_entry: self.update_row_position(event, widget))
        #row_number_var.trace("w", trace_callback)  # "w" stands for "write"

        # Screen cut icon button (Replace with your icon)
        record_button = ctk.CTkButton(self.scrollable_frame, text="Record")
        record_button.configure(command=lambda widget=record_button: self.screen_shot(widget))
        #screen_cut_button.grid(row=row_number, column=1, padx=4, pady=4)
        record_button.grid(row=row_number, column=1, padx=4, pady=4)

        widgets = self.common_row_ui(option, repeat, pause, row_number)

        self.widget_rows.append([new_row_number_entry, record_button, widgets[0], widgets[1], widgets[2], widgets[3]])
        data = {'object': ImageClick(), 'option': "normal", 'repeat': repeat, 'pause': pause}
        self.data_rows.append(Macro())

    def add_WindowAction_row(self, option, repeat, pause):
        row_number = len(self.widget_rows) + 1

        row_number_var = tk.StringVar(value=str(row_number))

        # Numerical input field for changing row position
        new_row_number_entry = ctk.CTkEntry(self.scrollable_frame, textvariable=row_number_var)
        new_row_number_entry.grid(row=row_number, column=0, padx=4, pady=4)
        new_row_number_entry.bind("<FocusOut>",
                                  lambda event, widget=new_row_number_entry: self.update_row_position(event, widget))
        # row_number_var.trace("w", trace_callback)  # "w" stands for "write"

        self.data_rows.append(Macro())

    def common_row_ui(self, option, repeat, pause, row_number):
        # Dropdown
        """
        And gives the user the ability to account for two or more different buttons being used for the same proccess. It
        loops around between the current line and the next one, till they're out of repeats.

        Skip gives the user the ability to skip a line without deleting it.
        """
        options = ["Normal", "And", "Skip"]
        dropdown_var = tk.StringVar(self.scrollable_frame)
        dropdown_var.set(option)  # default Normal
        dropdown = ctk.CTkOptionMenu(self.scrollable_frame, values=options)
        dropdown.grid(row=row_number, column=2, padx=4, pady=4)

        # Repeat Input
        repeat_variable = tk.StringVar(value=str(repeat))  # default 1

        repeat_entry = ctk.CTkEntry(self.scrollable_frame, textvariable=repeat_variable)
        repeat_entry.configure(width=50)
        repeat_entry.grid(row=row_number, column=3, padx=4, pady=4)
        repeat_entry.bind("<FocusOut>", lambda event, widget=repeat_entry: self.set_repeat(event, widget))

        # Pause Input
        pause_variable = tk.StringVar(value=str(pause))  # default 0

        pause_entry = ctk.CTkEntry(self.scrollable_frame, textvariable=pause_variable)
        pause_entry.configure(width=60)
        pause_entry.grid(row=row_number, column=4, padx=4, pady=4)
        pause_entry.bind("<FocusOut>", lambda event, widget=pause_entry: self.set_pause(event, widget))

        # Delete button
        del_icon = get_asset('delete_icon.png')  # Image.open('AutoMate/assets/delete_icon.svg')
        del_icon = ctk.CTkImage(del_icon)
        delete_button = ctk.CTkButton(self.scrollable_frame, text="Delete", image=del_icon)
        delete_button.configure(command=lambda widget=delete_button: self.delete_row(widget))
        delete_button.grid(row=row_number, column=5, padx=4, pady=4)

        return [dropdown, repeat_entry, pause_entry, delete_button]

    def play_button_func(self, widget):
        info = widget.grid_info()
        index = int(info["row"]) - 1
        self.root.state('iconic')
        self.data_rows[index]['object'].play()
        self.root.state('normal')

    def play_all(self):
        """
        This function handles running the entire loop.
        It prepares every object that needs to run togather, checked via And argument, in lists within the main list to loop over.
        It stores the repeats for each object into a separate array keep count of repeats without changing the program data.

        Once the data is prepared it loops over the entire list of lists until the total repeats is 0. While running every object.
        """
        repeat_counter = []
        and_repeat_array = []
        and_array = []
        play_all_array = []
        for row in self.data_rows: #prepares
            print(row)
            if row['option']=="And":
                and_array.append(row['object'])
                repeat_counter.append(row['repeat'])
            elif row['option']!="Skip":
                and_array.append(row['object'])
                play_all_array.append(and_array)
                and_array = []
                repeat_counter.append(row['repeat'])
                and_repeat_array.append(repeat_counter)
                repeat_counter = []
        print("lel")
        for object_array, repeat_array in zip(play_all_array, and_repeat_array):
            print("test")
            i = 0
            while sum(repeat_array)>0:
                print("repeat", repeat_array)
                if i==len(object_array):
                    i=0
                if repeat_array[i]>0:
                    repeat_array[i]=-1
                    print("play")
                    object_array[i].play()



    def screen_shot(self, widget):
        """
        Calls a function that gets a specific screenshot of the screen and passes it to the UI changing function.
        :param widget: used to get the widgets' index on the grid
        """
        info = widget.grid_info()
        index = int(info["row"]) - 1
        image = miscfunctions.get_cut_image()
        name="image"+str(self.image_count)
        self.image_count += 1
        self.set_image(index, image, name)

    def record_macro(self, widget):



    def open_image(self, widget):
        """
        Opens up the file viewer to select an image and passes it to the UI changing function.
        :param widget: used to get the widgets' index on the grid
        """
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.jpg *.jpeg *.png *apng *.webp *.bmp *.ppm *.pgm")])
            image = Image.open(file_path)
            info = widget.grid_info()
            index = int(info["row"]) - 1
            name = os.path.basename(file_path)
            self.set_image(index, image, name)
            self.image_count += 1
        except Exception as e:
            toast_thread = threading.Thread(target=toast.show_toast(root, "Error opening the image"))
            toast_thread.start()
            return
            #log error here later {str(e)}

    def set_image(self, index, image, name):
        """

        :param index:
        :param image:
        :param name: the name of the image file
        """
        self.data_rows[index]['object'].set_img(image)
        self.data_rows[index]['object'].set_img_name(name)
        self.set_image_ui(index, name)

    def set_image_ui(self, index, name):
        display_name = name[:10]

        image_input = ctk.CTkFrame(self.scrollable_frame)
        image_input.grid(row=index + 1, column=1, padx=0, pady=0)

        # Screen cut icon button (Replace with your icon)
        cancel_icon = get_asset('cancel_icon.png')  # Image.open('AutoMate/assets/delete_icon.svg')
        cancel_icon = ctk.CTkImage(cancel_icon)
        image_widget_name = ctk.CTkButton(image_input, text=display_name, image=cancel_icon, compound="right")
        image_widget_name.configure(command=lambda widget=image_input: self.unset_image(widget))
        image_widget_name.pack(side=ctk.LEFT, padx=4, pady=4)

        # Open file icon button (Replace with your icon)
        play_button = ctk.CTkButton(image_input, text="Play")
        play_button.configure(command=lambda widget=image_input: self.play_button_func(widget))
        play_button.pack(side=ctk.RIGHT, padx=4, pady=4)

        self.widget_rows[index][1].destroy()
        self.widget_rows[index].pop(1)
        self.widget_rows[index].insert(1, image_input)

    def unset_image(self, widget):
        """
        Removes the image from the UI and the ImageClick object
        :param widget: used to get the widgets' index on the grid
        """
        info = widget.grid_info()
        index = int(info["row"]) - 1
        self.data_rows[index]['object'].unset_img()
        self.data_rows[index]['object'].unset_img_name()

        image_input = ctk.CTkFrame(self.scrollable_frame)
        image_input.grid(row=index+1, column=1, padx=0, pady=0)

        # Screen cut icon button (Replace with your icon)
        screen_cut_button = ctk.CTkButton(image_input, text="Screen Cut")
        screen_cut_button.configure(command=lambda widget=image_input: self.screen_shot(widget))
        # screen_cut_button.grid(row=row_number, column=1, padx=4, pady=4)
        screen_cut_button.pack(side=ctk.LEFT, padx=4, pady=4)

        # Open file icon button (Replace with your icon)
        open_file_button = ctk.CTkButton(image_input, text="Open File")
        open_file_button.configure(command=lambda widget=image_input: self.open_image(widget))
        # open_file_button.grid(row=row_number, column=2, padx=4, pady=4)
        open_file_button.pack(side=ctk.RIGHT, padx=4, pady=4)

        self.widget_rows[index][1].destroy()
        self.widget_rows[index].insert(1, image_input)

    def load_ui(self):
        data=load(self.root)
        if data is None:
            return
        self.clear_all_rows()
        self.loop_repetitions=data['loop_repetitions']
        i=0
        for row in data['data_rows']:
            if row['object']['type'] == 'imageClick':
                self.add_ImageClick_row(row['option'], row['repeat'], row['pause'])
                self.data_rows[i]['object']= imageclick.create_via_dictionary(row['object'])
                if row['object']['imgName']!="":
                    self.set_image_ui(i, row['object']['imgName'])
            elif row['object']['type'] == 'macro':
                self.add_Macro_row(row['option'], row['repeat'], row['pause'])
                self.data_rows.append(macro.create_via_dictionary(row['object']))
            i=+1
        self.loop_repetitions = data['loop_repetitions']

    def clear_all_rows(self):
        self.data_rows = []
        for row in self.widget_rows:
            for widget in row:
                widget.destroy()
        self.widget_rows = []


    def set_repeat(self, event, widget):
        info = widget.grid_info()
        index = int(info["row"]) - 1
        if event.type != tk.EventType.FocusOut:  # If the event was not triggered by the entry widget losing focus, oddly happened a few times during testing.
            raise Exception("Event type is not <FocusOut>")  # change to external library error.
        if not (widget.get().isdigit()):
            widget.delete(0, ctk.END)
            widget.insert(0, index)
        self.data_rows[index]['repeat'] = int(widget.get())

    def set_pause(self, event, widget):
        info = widget.grid_info()
        index = int(info["row"]) - 1
        if event.type != tk.EventType.FocusOut:  # If the event was not triggered by the entry widget losing focus, oddly happened a few times during testing.
            raise Exception("Event type is not <FocusOut>")  # change to external library error.
        if not (widget.get().isdigit()):
            widget.delete(0, ctk.END)
            widget.insert(0, index)
        self.data_rows[index]['pause'] = int(widget.get())
    def update_row_position(self, event, widget):
        info = widget.grid_info()
        index = int(info["row"]) - 1
        print(len(self.widget_rows))
        print(index, widget.get())
        if event.type != tk.EventType.FocusOut:  # If the event was not triggered by the entry widget losing focus, oddly happened a few times during testing.
            raise Exception("Event type is not <FocusOut>") #change to external library error.
        if not(widget.get().isdigit()):
            widget.delete(0, ctk.END)
            widget.insert(0, index)

        new_position = int(widget.get()) - 1
        if index == new_position or new_position < 0:  #Same position or negative, do nothing.
            return
        if new_position > len(self.widget_rows) - 1:
            widget.delete(0, ctk.END)
            widget.insert(0, str(len(self.widget_rows)))
            new_position = len(self.widget_rows) - 1
        print("inserting", widget.get())
        print("Moving row", index, "to position", new_position)
        print(self.widget_rows)
        self.widget_rows.insert(new_position, self.widget_rows.pop(index))
        print(self.widget_rows)
        self.rearrange_rows(min(index, new_position))
        #self.rearrange_rows(0)


    def delete_row(self, widget):
        info = widget.grid_info()
        index = int(info["row"]) - 1
        print("Deleting row", index,"length", len(self.widget_rows))
        for widget in self.widget_rows[index]:
            widget.destroy()
        del self.widget_rows[index]
        if index != len(self.widget_rows):  # If the deleted row was not the last row
            self.rearrange_rows(index-1)

    def rearrange_rows(self, index):
        print("Rearranging rows", index)
        while index < len(self.widget_rows):
            print("redoing",index)
            for col, widget in enumerate(self.widget_rows[index]):
                print("col", col, "widget", widget, "length", len(self.widget_rows[index]))
                if col == 0:
                    widget.delete(0, ctk.END)
                    widget.insert(0, index+1)
                widget.grid(row=index+1, column=col)
            index = index + 1
            print(self.widget_rows)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    root = ctk.CTk()
    app = ButtonRowApp(root)

    root.mainloop()
