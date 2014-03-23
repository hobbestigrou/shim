from Tkinter import Tk, Canvas, BOTH
from ttk import Frame
import tkFont
# this is hacky as shit but the math doesn't seem to be working out so far
LINEMAPPING = { 12: 58, 18: 39, 20: 35 }
# Main GUI handler class handles graphics to be displayed to user
class text_canvas(Frame):
    def __init__(self, parent, font_size, input_handler):
        Frame.__init__(self, parent)
        self.parent = parent
        self.text_font = tkFont.Font(family='Monaco', size=font_size, weight='bold')
        self.cheight, self.cwidth, self.line_num_spacing, self.line_height = font_size, self.text_font.measure('c'), 50, LINEMAPPING[font_size]
        self.init_UI(input_handler)

    def init_UI(self, input_handler):
        self.parent.title('')
        self.pack(fill=BOTH, expand=1)
        self.init_canvas(input_handler)

    def init_canvas(self, input_handler):
        self.canvas = Canvas(self, highlightthickness=0, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), bg='#002B36')
        self.canvas.pack()
        self.canvas.focus_set()
        self.bind_events(input_handler)

    def bind_events(self, input_handler):
        # TODO: this should be cleaned up ideally into a separate handler list
        input_handler.set_GUI_reference(self)
        self.canvas.bind('<Key>', input_handler.key)
        self.canvas.bind_all('<Escape>', input_handler.escape)
        self.canvas.bind_all("<MouseWheel>", input_handler.mouse_scroll)
        self.canvas.bind_all('<Control-f>', input_handler.control_f)
        self.canvas.bind_all('<Control-b>', input_handler.control_b)

    # write line of text at given grid co-ordinates
    def write_text_grid(self, x, y, text, color):
        x_val = self.cwidth * x + self.line_num_spacing
        # 2 pixel spacing between each line
        y_val = self.cheight * y + (y * 2)
        #'#839496'
        self.canvas.create_text(x_val, y_val, anchor='nw', text=text, font=self.text_font, fill=color)
    # TODO: REMOVE HARDCODED COLORS
    def draw_highlight_grid(self, y, x1, x2):
        y_val = self.cheight * y + (y * 2)
        x1_val = self.cwidth * x1 + self.line_num_spacing
        x2_val = self.cwidth * x2 + self.line_num_spacing
        self.canvas.create_rectangle(x1_val, y_val, x2_val, y_val + self.cheight + 4, fill='#657b83', outline='#657b83')

    def draw_line_numbers(self, start):
        self.canvas.create_rectangle(0, 0, self.line_num_spacing / 2, self.winfo_screenheight(), fill='#073642', outline='#073642')
        for i in range(self.line_height + 1):
            # 2 pixel spacing between each line
            self.canvas.create_text(0, self.cheight * i + (i * 2), anchor='nw', text=str(start + i), font=self.text_font, fill='#839496')

    def draw_cursor(self, x, y):
        x_val = self.cwidth * x + self.line_num_spacing
        y_val = self.cheight * y + (y * 2)
        self.canvas.create_rectangle(0, y_val, self.winfo_screenwidth(), y_val + self.cheight + 4, fill='#073642', outline='#073642')
        self.canvas.create_rectangle(x_val, 0, x_val + self.cwidth, self.winfo_screenheight(), fill='#073642', outline='#073642')

        self.canvas.create_rectangle(x_val, y_val, x_val + self.cwidth, y_val + self.cheight + 4, fill='#839496', outline='#839496')

        width = tkFont.Font(family='Monaco', size=12, weight='bold').measure('%d, %d' % (x, y))

        self.canvas.create_rectangle(self.winfo_screenwidth() - width, 0, self.winfo_screenwidth(), 12, fill='#073642', outline='#073642')
        self.canvas.create_text(self.winfo_screenwidth() - width, 0, anchor='nw', text='%d, %d' % (x, y), font=tkFont.Font(family='Monaco', size=12, weight='bold'), fill='#839496')

    def clear_all(self):
        self.canvas.delete('all')

    def get_line_height(self):
        return self.line_height
