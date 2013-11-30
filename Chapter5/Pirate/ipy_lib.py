'''
Created on 30 Jan. 2012
Finished on 6 Feb. 2012

Improvements:
 - 1 Mar. 2012 to 2 Mar. 2012: fixed a rare threading related crash
 - 3 Mar. 2012 to 5 Mar. 2012: fixed a bug in showing names of the barchart
 - 17 Mar. 2012 to 18 Mar. 2012: fixed not running on Linux
 - 31 Jul. 2012 to 31 Jul. 2012: added UserInput and 'privatised' most classes and imports
 - 1 Aug. 2012 to 2 Aug. 2012: fixed another bug with showing names of the barchart and a bug with displaying text in othello
 - 4 Aug. 2012 to 4 Aug. 2012: fixed bug with opening a file and fixed functionality of closing the window
 - 6 Aug. 2012 to 7 Aug. 2012: fixed multiple windows crashing the UI, reverted change to UserInput with this change
 - 21 Aug. 2012 to 21 Aug. 2012: adjusted naming from JAVA to Python convention, changed UserInput to a function that returns all input, added Life interface
 - 22 Aug. 2012 to 22 Aug. 2012: added scrollbar to othello, snake and life interfaces, added type checking and exceptions for all input
 - 2 Sep. 2012 to 2 Sep. 2012: fixed another bug with names of the barchart, allowed ints to be given to floats, fixed spelling
 - 13 Sep. 2012 to 13 Sep. 2012: fixed more spelling, added functionality for multiple answers per question
 - 27 Sep. 2012 to 27 Sep. 2012: changed multiple answers from array to arbitrary arguments list, added exception if argument list is empty
 - 6 Dec. 2012 to 6. Dec. 2012: fixed resets of auto alarm speed by adding a timer
 - 2 Oct. 2013 to 3. Oct. 2013: fixed ranged errors, fixed closing bug in Windows and Linux when only calling ask_user or file_input,
                                fixed typos, added Escape as window closer, fixed window not getting focus when started, added Mac support (!)
 - 9 Oct. 2013 to 9. Oct. 2013: fixed get_event (Mac version) to properly give refresh events
 
@author: Gerben Rozie
'''
import Tkinter as _tk
import Dialog as _Dialog
import tkFileDialog as _tkFileDialog
import tkMessageBox as _tkMessageBox
import Queue as _Queue
import threading as _threading
import time as _time
import os as _os
import random as _random
import sys as _sys
have_pil = False
try:
    from PIL import Image as _Image, ImageTk as _ImageTk
    have_pil = True
except ImportError:
    print "Could not import the Python Imaging Library (PIL)."
    print "Usage of OthelloReplay-, Snake- and LifeUserInterface are disabled." 

class _IPyException(Exception):
    def __init__(self, value):
        self.parameter = value
    
    def __str__(self):
        return repr(self.parameter)

def _verify_int(value_var, string_var, minimum=None, maximum=None):
    if not isinstance(value_var, int):
        value = "%s not an int for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
        raise _IPyException(value)
    _verify_input(value_var, string_var, minimum, maximum)

def _verify_float(value_var, string_var, minimum=None, maximum=None):
    if not isinstance(value_var, float):
        if not isinstance(value_var, int):
            value = "%s is not a float or int for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
            raise _IPyException(value)
    _verify_input(value_var, string_var, minimum, maximum)

def _verify_str(value_var, string_var):
    if not isinstance(value_var, basestring):
        value = "%s is not a string for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
        raise _IPyException(value)

def _verify_bool(value_var, string_var):
    if not isinstance(value_var, bool):
        value = "%s is not a boolean for %s, got %s" % (value_var, string_var, str(type(value_var))[1:-1])
        raise _IPyException(value)

def _verify_input(value_var, string_var, minimum=None, maximum=None):
    if minimum is None:
        minimum = float('-inf')
    if maximum is None:
        maximum = float('inf')
    if value_var >= minimum:
        if value_var <= maximum:
            return
    value = "%s is out of bounds, expected range: %s to %s, got: %s" % (string_var, minimum, maximum, value_var)
    raise _IPyException(value)

class _OthelloReplayHolder(object):
    #used in the queue to hold values of the changes to be made
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class _BarChartHolder(object):
    #used in the queue to hold values of the changes to be made
    def __init__(self, bar_index):
        self.bar_index = bar_index

class _BarChartNameHolder(object):
    #used in the queue to hold values of the changes to be made
    def __init__(self, bar_index, bar_name):
        self.bar_index = bar_index
        self.bar_name = bar_name

class _SnakeHolder(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class _LifeHolder(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

if _sys.platform == 'darwin':
    _ui_factory = None
    
    def file_input():
        """This function lets the user select a file to use for input.
        Returns the file contents in a string.
        """
        
        global _ui_factory
        f = _AskInput(_ui_factory.mainroot).f
        if f == '':
            return None
        return str(_sys.stdin.read())
    
    def ask_user(question, *options):
        """Ask the user a question.
        Parameters:
        - question: the string to ask the user
        - options: arbitrary list of arguments (at least 1)
        Returns the chosen option by the user or None if nothing was chosen (e.g. hit Escape).
        """
        
        if len(options) == 0:
            value = "User needs to be able to select at least 1 answer"
            raise _IPyException(value)
        global _ui_factory
        return _AskUser(_ui_factory.mainroot, question, options).answer
    

    class _Factory():
        def __init__(self):
            self.mainroot = _tk.Tk()
            self.mainroot.withdraw()
            self.mainroot.update()
    
    class _AskInput(object):
        def __init__(self, mainroot):
            root = _tk.Toplevel(mainroot)
            root.withdraw()
            self.f = _tkFileDialog.askopenfilename(parent=root)
            if self.f is not '':
                _sys.stdin = file(self.f)
            root.destroy()
    
    class _AskUser(object):
        def __init__(self, mainroot, question, options):
            root = _tk.Toplevel(mainroot)
            root.withdraw()
            dg = _Dialog.Dialog(None,
            title="",
            text=question,
            default=0,
            bitmap=_tkMessageBox.QUESTION,
            strings=options)
            self.answer = options[dg.num]
            root.destroy()
    
    class OthelloReplayUserInterface(object):
        def __init__(self, scale=1.0):
            """This class starts the OthelloReplayUserInterface.
            Constants:
            - NUMBER_OF_ROWS
            - NUMBER_OF_COLUMNS
            - EMPTY
            - WHITE
            - BLACK
            
            Parameters for the class: (none)
            
            Optional parameters:
            - scale: 0.25 to 1.0
            """
            
            if not have_pil:
                value = "OthelloReplay: PIL wasn't found, can't use this interface right now."
                raise _IPyException(value)
            _verify_float(scale, 'Scale', 0.25, 1.0)
            global _ui_factory
            self.othello_replay = _Othello(_ui_factory.mainroot, scale)
            self.NUMBER_OF_ROWS = _Othello.NUMBER_OF_ROWS
            self.NUMBER_OF_COLUMNS = _Othello.NUMBER_OF_COLUMNS
            self.EMPTY = _Othello.EMPTY
            self.WHITE = _Othello.WHITE
            self.BLACK = _Othello.BLACK
        
        def place(self, x, y, color):
            """Place an Othello piece (defined by 'color') on the given X and Y coordinates.
            """
            
            _verify_int(x, 'X', 0, self.NUMBER_OF_COLUMNS - 1)
            _verify_int(y, 'Y', 0, self.NUMBER_OF_ROWS - 1)
            # 0 = empty, 1 = white, 2 = black, 3 = white_t, 4 = black_t
            _verify_int(color, 'Color', 0, 4)
            self.othello_replay.place(x, y, color)
        
        def place_transparent(self, x, y, color):
            """Place a semi-transparent Othello piece (defined by 'color') on the given X and Y coordinates.
            """
            
            _verify_int(x, 'X', 0, self.NUMBER_OF_COLUMNS - 1)
            _verify_int(y, 'Y', 0, self.NUMBER_OF_ROWS - 1)
            # 0 = empty, 1 = white_t, 2 = black_t (before next step in code)
            _verify_int(color, 'Color', 0, 2)
            if color == self.EMPTY:
                self.place(x, y, self.EMPTY)
            else:
                self.place(x, y, color+2)
        
        def clear(self):
            """Clears the display.
            Note: this does not clear the text area!
            """
            
            self.othello_replay.clear()
        
        def show(self):
            """Show the changes made to the display (i.e. after calling place or clear).
            """
            
            self.othello_replay.show()
        
        def print_(self, text):
            """Print text to the text area on the display.
            This function does not add a trailing newline by itself.
            """
            
            
            _verify_str(text, "Text")
            self.othello_replay.print_(text)
        
        def clear_text(self):
            """Clears the text area on the display.
            """
            
            self.othello_replay.clear_text()
        
        def wait(self, ms):
            """Let your program wait for an amount of milliseconds.
            
            This function only guarantees that it will wait at least this amount of time.
            If the system, i.e., is too busy, then this time might increase.
            - Python time module.
            """
            
            _verify_int(ms, "Waiting time", 0)
            self.othello_replay.wait(ms)
        
        def close(self):
            """Closes the display and stops your program.
            """
            
            self.othello_replay.close()
        
        def stay_open(self):
            """Force the window to remain open.
            Only has effect on Mac OS to prevent the window from closing after the execution finishes.
            
            Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
            """
            
            global _ui_factory
            _ui_factory.mainroot.mainloop()
    
    class _Othello(object):
        #one cannot prevent users from editing 'constants', as constants simply do not exist in Python
        NUMBER_OF_ROWS = 8
        NUMBER_OF_COLUMNS = 8
        EMPTY = 0
        WHITE = 1
        BLACK = 2
        
        BACKGROUND = "#147800"
        
        def __init__(self, mainroot, scale=1.0):
            #create queue to store changes to placings
            self.to_show_queue = _Queue.Queue(maxsize=0)
            
            #start the main window
            self.root = _tk.Toplevel(mainroot)
            self.root.title("OthelloReplayUserInterface")
            self.root.protocol("WM_DELETE_WINDOW", self.callback)
            self.root.bind("<Escape>", self.callback)
            self.root.resizable(False, False)
            
            #calculate sizes
            self.text_height = int(200 * scale)
            self.othello_size = int(800 * scale)
            
            #create main frame
            self.frame = _tk.Frame(self.root, width=self.othello_size, height=self.othello_size+self.text_height)
            self.frame.pack_propagate(0)
            self.frame.pack()
            
            #create board to hold references to othello-pieces
            self.white_board = [] # for storing references to create_image
            self.black_board = []
            self.white_ghost_board = []
            self.black_ghost_board = []
            self.img_refs = [] # for storing references to images - order: white, black
            
            #create and fill the canvas --> paintable area
            self.c = _tk.Canvas(self.frame, width=self.othello_size, height=self.othello_size, bg=self.BACKGROUND, bd=0, highlightthickness=0)
            self.c.pack()
            self.c.focus_set()
            self.fill_canvas()
            
            #create the textholder
            self.scrollbar = _tk.Scrollbar(self.frame)
            self.scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
            self.textarea = _tk.Text(self.frame, yscrollcommand=self.scrollbar.set)
            self.textarea.pack(side=_tk.LEFT, fill=_tk.BOTH)
            self.scrollbar.config(command=self.textarea.yview)
            self.textarea.config(state=_tk.DISABLED)
            
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def callback(self, event=None):
            self.root.destroy()
            _os._exit(0)
        
        def place(self, x, y, color):
            element = _OthelloReplayHolder(x, y, color)
            self.to_show_queue.put(element)
        
        def clear(self):
            for x in range(self.NUMBER_OF_COLUMNS):
                for y in range(self.NUMBER_OF_ROWS):
                    self.place(x, y, self.EMPTY)
        
        def show(self):
            try:
                while True:
                    element = self.to_show_queue.get_nowait()
                    position = []
                    position.append(self.white_board[element.x][element.y])
                    position.append(self.black_board[element.x][element.y])
                    position.append(self.white_ghost_board[element.x][element.y])
                    position.append(self.black_ghost_board[element.x][element.y])
                    for i in range(len(position)):
                        if element.color == i+1:
                            self.c.itemconfig(position[i], state=_tk.NORMAL)
                        else:
                            self.c.itemconfig(position[i], state=_tk.HIDDEN)
            except _Queue.Empty:
                pass
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def print_(self, text):
            self.textarea.config(state=_tk.NORMAL)
            self.textarea.insert(_tk.END, text)
            self.textarea.see(_tk.END)
            self.textarea.config(state=_tk.DISABLED)
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def clear_text(self):
            self.textarea.config(state=_tk.NORMAL)
            self.textarea.delete(1.0, _tk.END)
            self.textarea.see(_tk.END)
            self.textarea.config(state=_tk.DISABLED)
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def wait(self, ms):
            try:
              _time.sleep(ms * 0.001)
            except:
              self.close()
        
        def close(self):
            self.root.destroy()
            _os._exit(0)
        
        def create_othello_grid(self):
            for i in range(self.NUMBER_OF_COLUMNS+1):
                x0 = self.xpad + self.xstep * i
                y0 = self.ypad
                x1 = x0
                y1 = self.ypad + self.ystep * self.NUMBER_OF_ROWS + 1
                coords = x0, y0, x1, y1
                self.c.create_line(coords, fill='black')
            for j in range(self.NUMBER_OF_ROWS+1):
                x0 = self.xpad
                y0 = self.ypad + self.ystep * j
                x1 = self.xpad + self.xstep * self.NUMBER_OF_COLUMNS + 1
                y1 = y0
                coords = x0, y0, x1, y1
                self.c.create_line(coords, fill='black')
            for i in range(self.NUMBER_OF_COLUMNS):
                x0 = self.xpad + self.xstep / 2 + self.xstep * i
                y0 = self.ypad / 2
                x1 = x0
                y1 = self.othello_size - self.ystep / 2
                coords0 = x0, y0
                coords1 = x1, y1
                self.c.create_text(coords0, text=chr(ord('a')+i))
                self.c.create_text(coords1, text=chr(ord('a')+i))
            for j in range(self.NUMBER_OF_ROWS):
                x0 = self.xpad / 2
                y0 = self.ypad + self.ystep / 2 + self.ystep * j
                x1 = self.othello_size - self.xstep / 2
                y1 = y0
                coords0 = x0, y0
                coords1 = x1, y1
                self.c.create_text(coords0, text='%s'%(j+1))
                self.c.create_text(coords1, text='%s'%(j+1))
        
        def create_images(self):
            relative_locations = "images/white.png", "images/black.png", "images/white_t.png", "images/black_t.png"
            locations = []
            for i in range(len(relative_locations)):
                locations.append(_os.path.join(_os.path.dirname(__file__), _os.path.normpath(relative_locations[i])))
            for i in locations:
                size = int(self.xstep * 0.8), int(self.ystep * 0.8)
                img = _Image.open(i).resize(size, _Image.ANTIALIAS)
                ref = _ImageTk.PhotoImage(img)
                self.img_refs.append(ref)
        
        def create_othello_pieces(self):
            boards = self.white_board, self.black_board, self.white_ghost_board, self.black_ghost_board
            for n in range(len(boards)):
                for i in range(self.NUMBER_OF_COLUMNS):
                    boards[n].append([])
                    for j in range(self.NUMBER_OF_ROWS):
                        x0 = self.xpad + self.xstep * i + self.xstep/2
                        y0 = self.ypad + self.ystep * j + self.ystep/2
                        img = self.c.create_image(x0, y0, anchor=_tk.CENTER, image=self.img_refs[n], state=_tk.HIDDEN)
                        boards[n][i].append(img)
        
        def fill_canvas(self):
            self.xstep = self.othello_size / (self.NUMBER_OF_COLUMNS + 2)
            self.ystep = self.othello_size / (self.NUMBER_OF_ROWS + 2)
            self.xpad = (self.othello_size - self.NUMBER_OF_COLUMNS * self.xstep) / 2
            self.ypad = (self.othello_size - self.NUMBER_OF_ROWS * self.ystep) / 2
            self.create_images()
            self.create_othello_grid()
            self.create_othello_pieces()
    
    class BarChartUserInterface(object):
        def __init__(self, bar_count):
            """This class starts the BarChartUserInterface.
            Constants: (none)
            
            Parameters for the class:
            - bar_count: at least 1
            
            Optional parameters: (none)
            """
            _verify_int(bar_count, "Bar count", 1)
            global _ui_factory
            self.bar_chart = _BarChart(bar_count, _ui_factory.mainroot)
        
        def set_bar_name(self, bar_index, text):
            """Set a name, provided by 'text', to a given bar_index.
            Note: this function's effects are visible without calling show.
            """
            
            _verify_int(bar_index, "Bar index", 0, self.bar_chart.bar_count - 1)
            _verify_str(text, "Text")
            self.bar_chart.set_bar_name(bar_index, text)
        
        def raise_bar(self, bar_index):
            """Increment the given bar_index by 1.
            """
            
            _verify_int(bar_index, "Bar index", 0, self.bar_chart.bar_count - 1)
            self.bar_chart.raise_bar(bar_index)
        
        def show(self):
            """Show the changes made to the display (i.e. after calling raise_bar).
            """
            
            self.bar_chart.show()
        
        def show_names(self, value):
            """Whether or not to show the names of the bars.
            Value given must be a boolean.
            Default at start is False.
            """
            
            _verify_bool(value, "Show names")
            self.bar_chart.show_names(value)
        
        def show_values(self, value):
            """Whether or not to show the values of the bars.
            Value given must be a boolean.
            Default at start is True.
            """
            
            _verify_bool(value, "Show values")
            self.bar_chart.show_values(value)
        
        def wait(self, ms):
            """Let your program wait for an amount of milliseconds.
            
            This function only guarantees that it will wait at least this amount of time.
            If the system, i.e., is too busy, then this time might increase.
            - Python time module.
            """
            
            _verify_int(ms, "Waiting time", 0)
            self.bar_chart.wait(ms)
        
        def close(self):
            """Closes the display and stops your program.
            """
            
            self.bar_chart.close()
        
        def stay_open(self):
            """Force the window to remain open.
            Only has effect on Mac OS to prevent the window from closing after the execution finishes.
            
            Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
            """
            
            global _ui_factory
            _ui_factory.mainroot.mainloop()
    
    class _BarChart(object):
        def __init__(self, bar_count, mainroot):
            #create queue to store changes to placings
            self.to_show_queue = _Queue.Queue(maxsize=0)
            self.to_show_names_queue = _Queue.Queue(maxsize=0)
            
            #variables used to keep the number of refreshes of names and values in check
            self.show_names_bool = False
            self.show_values_bool = True
            
            self.bar_count = bar_count
            
            #start the main window
            self.root = _tk.Toplevel(mainroot)
            self.root.title("BarChartUserInterface")
            self.root.protocol("WM_DELETE_WINDOW", self.callback)
            self.root.bind("<Escape>", self.callback)
            self.frame = _tk.Frame(self.root)
            self.frame.pack(fill=_tk.BOTH, expand=_tk.YES)
            self.height = 575
            self.width = 400
            self.c = _tk.Canvas(self.frame, width=self.width, height=self.height, bg='white', bd=0, highlightthickness=0)
            self.c.pack(fill=_tk.BOTH, expand=_tk.YES)
            self.c.focus_set()
            self.c.bind('<Configure>', self.redraw)
            self.bar_max = 0
            self.bars = []
            self.names = []
            self.create_bars()
            self.redraw()
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def callback(self, event=None):
            self.root.destroy()
            _os._exit(0)
        
        def set_bar_name(self, bar_index, text):
            element = _BarChartNameHolder(bar_index, text)
            self.to_show_names_queue.put(element)
        
        def raise_bar(self, bar_index):
            element = _BarChartHolder(bar_index)
            self.to_show_queue.put(element)
        
        def inc_bar(self, bar_index):
            if (self.bars[bar_index] + 1) > self.bar_max:
                self.bar_max = self.bars[bar_index] + 1
            self.bars[bar_index] += 1
        
        def show(self):
            try:
                while True:
                    element = self.to_show_queue.get_nowait()
                    self.inc_bar(element.bar_index)
            except _Queue.Empty:
                pass
            try:
                while True:
                    element = self.to_show_names_queue.get_nowait()
                    self.names[element.bar_index] = element.bar_name;
            except _Queue.Empty:
                pass
            self.redraw()
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def show_names(self, value):
            self.show_names_bool = value
        
        def show_values(self, value):
            self.show_values_bool = value
        
        def wait(self, ms):
            try:
              _time.sleep(ms * 0.001)
            except:
              self.close()
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def close(self):
            self.root.destroy()
            _os._exit(0)
            return
        
        def create_bars(self):
            for i in range(self.bar_count): #@UnusedVariable
                self.bars.append(0)
                self.names.append('')
        
        def redraw(self, event=None):
            if event != None:
                self.width = event.width
                self.height = event.height
            for e in self.c.find_all():
                self.c.delete(e)
            self.fill_canvas()
        
        def fill_canvas(self):
            xstep = self.width / (self.bar_count + 2)
            xpad = (self.width - xstep * self.bar_count) / 2
            xspacing = xstep / 10
            ypad = self.height / 10
            ypadtext = ypad / 3
            for i in range(self.bar_count):
                #draw the bar
                x0 = xpad + xstep * i + xspacing
                y0 = self.height - ypad
                x1 = xpad + xstep * (i + 1) - xspacing
                y1 = self.height - ypad
                color = 0
                if self.bar_max > 0:
                    y_len = self.bars[i] * (self.height - 2 * ypad) / self.bar_max
                    y1 -= y_len
                    color = self.bars[i] * 255 / self.bar_max
                coords = x0, y0, x1, y1
                hex_color = "#%02x%02x%02x" % (color, 0, 0) #red, green, blue
                self.c.create_rectangle(coords, fill=hex_color)
                
                #draw the values
                x1 = xpad + xstep * i + xstep / 2
                y1 -= ypadtext
                coords = x1, y1
                value = ("%d" % self.bars[i]) if self.show_values_bool else ''
                self.c.create_text(coords, text=value)
                
                #draw the names
                x0 = xpad + xstep * i + xstep / 2
                y0 += ypadtext
                coords = x0, y0
                name = self.names[i] if self.show_names_bool else ''
                self.c.create_text(coords, text=name)
    
    class SnakeUserInterface(object):
        def __init__(self, width, height, scale=1.0):
            """This class starts the SnakeUserInterface.
            Constants:
            - EMPTY
            - FOOD
            - SNAKE
            - WALL
            
            Parameters for the class:
            - width: at least 1
            - height: at least 1
            
            Optional parameters:
            - scale: 0.25 to 1.0
            """
            
            if not have_pil:
                value = "Snake: PIL wasn't found, can't use this interface right now."
                raise _IPyException(value)
            _verify_int(width, "Width", 1)
            _verify_int(height, "Height", 1)
            _verify_float(scale, 'Scale', 0.25, 1.0)
            global _ui_factory
            self.snake_interface = _Snake(width, height, _ui_factory.mainroot, scale)
            self.EMPTY = _Snake.EMPTY
            self.FOOD = _Snake.FOOD
            self.SNAKE = _Snake.SNAKE
            self.WALL = _Snake.WALL
        
        def place(self, x, y, color):
            """Place a Snake piece (defined by 'color') on the given X and Y coordinates.
            """
            
            _verify_int(x, 'X', 0, self.snake_interface.width - 1)
            _verify_int(y, 'Y', 0, self.snake_interface.height - 1)
            # 0 = empty, 1 = food, 2 = snake, 3 = wall, 4 = food_t, 5 = snake_t, 6 = wall_t
            _verify_int(color, 'Color', 0, 6)
            self.snake_interface.place(x, y, color)
        
        def place_transparent(self, x, y, color):
            """Place a semi-transparent Snake piece (defined by 'color') on the given X and Y coordinates.
            """
            
            _verify_int(x, 'X', 0, self.snake_interface.width - 1)
            _verify_int(y, 'Y', 0, self.snake_interface.height - 1)
            # 0 = empty, 1 = food_t, 2 = snake_t, 3 = wall_t (before next step in code)
            _verify_int(color, 'Color', 0, 6)
            if color == self.EMPTY:
                self.place(x, y, self.EMPTY)
            else:
                self.place(x, y, color+3)
        
        def clear(self):
            """Clears the display.
            Note: this does not clear the text area!
            """
            
            self.snake_interface.clear()
        
        def show(self):
            """Show the changes made to the display (i.e. after calling place or clear)
            """
            
            self.snake_interface.show()
        
        def get_event(self):
            """Returns an event generated from the display.
            The returned object has 2 properties:
            - name: holds the group which the event belongs to.
            - data: holds useful information for the user.
            """
            
            return self.snake_interface.get_event()
        
        def set_animation_speed(self, fps):
            """Set an event to repeat 'fps' times per second.
            If the value is set to 0 or less, the repeating will halt.
            In theory the maximum value is 1000, but this depends on activity of the system.
            
            The generated events (available by using get_event) have these properties:
            - name: 'alarm'.
            - data: 'refresh'.
            """
            
            _verify_float(fps, "Animation speed")
            self.snake_interface.set_animation_speed(fps)
        
        def print_(self, text):
            """Print text to the text area on the display.
            This function does not add a trailing newline by itself.
            """
            
            _verify_str(text, "Text")
            self.snake_interface.print_(text)
        
        def clear_text(self):
            """Clears the text area on the display.
            """
            
            self.snake_interface.clear_text()
        
        def wait(self, ms):
            """Let your program wait for an amount of milliseconds.
            
            This function only guarantees that it will wait at least this amount of time.
            If the system, i.e., is too busy, then this time might increase.
            - Python time module.
            """
            
            _verify_int(ms, "Waiting time", 0)
            self.snake_interface.wait(ms)
        
        def random(self, maximum):
            """Picks a random integer ranging from 0 <= x < maximum
            Minimum for maximum is 1
            """
            
            _verify_int(maximum, 'Random', 1)
            return self.snake_interface.random(maximum)
        
        def close(self):
            """Closes the display and stops your program.
            """
            
            self.snake_interface.close()
        
        def stay_open(self):
            """Force the window to remain open.
            Only has effect on Mac OS to prevent the window from closing after the execution finishes.
            
            Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
            """
            
            global _ui_factory
            _ui_factory.mainroot.mainloop()
    
    class _Snake(object):
        #one cannot prevent users from editing 'constants', as constants simply do not exist in Python
        EMPTY = 0
        FOOD = 1
        SNAKE = 2
        WALL = 3
        
        def __init__(self, width, height, mainroot, scale=1.0):
            #create queue to store changes to placings
            self.to_show_queue = _Queue.Queue(maxsize=0)
            self.event_queue = _Queue.Queue(maxsize=0)
            
            #copy params
            self.width = width
            self.height = height
            self.scale = scale
            
            self.closing_window = False
            
            #start the main window
            self.root = _tk.Toplevel(mainroot)
            self.root.title("SnakeUserInterface")
            self.root.protocol("WM_DELETE_WINDOW", self.callback)
            self.root.bind("<Escape>", self.callback)
            self.root.resizable(False, False)
            
            #calculate sizes
            self.size_per_coord = int(25 * scale)
            self.text_height = int(200 * scale)
            
            #create main frame
            self.frame = _tk.Frame(self.root, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height+self.text_height)
            self.frame.pack_propagate(0)
            self.frame.pack()
            
            #create board to hold references to snake-pieces
            self.food_board = [] # for storing references to create_image
            self.snake_board = []
            self.wall_board = []
            self.food_ghost_board = []
            self.snake_ghost_board = []
            self.wall_ghost_board = []
            self.img_refs = [] # for storing references to images - order: food, snake, wall, food_t, snake_t, wall_t
            
            #create and fill the canvas --> paintable area
            self.c = _tk.Canvas(self.frame, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height, bd=0, highlightthickness=0)
            self.c.pack()
            self.last_x = -1 # used to generate mouseOver/Exit events
            self.last_y = -1 # used to generate mouseOver/Exit events
            self.fill_canvas()
            
            #create the textholder
            self.scrollbar = _tk.Scrollbar(self.frame)
            self.scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
            self.textarea = _tk.Text(self.frame, yscrollcommand=self.scrollbar.set)
            self.textarea.pack(side=_tk.LEFT, fill=_tk.BOTH)
            self.scrollbar.config(command=self.textarea.yview)
            self.textarea.config(state=_tk.DISABLED)
            
            self.interval = 0
            self.alarm_speed = 0
            self.timer = self.milliseconds()
            
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def callback(self, event=None):
            self.root.destroy()
            _os._exit(0)
        
        def milliseconds(self):
            return _time.time() * 1000
        
        def place(self, x, y, color):
            element = _SnakeHolder(x, y, color)
            self.to_show_queue.put(element)
        
        def clear(self):
            for x in range(self.width):
                for y in range(self.height):
                    self.place(x, y, self.EMPTY)
        
        def show(self):
            try:
                while True:
                    element = self.to_show_queue.get_nowait()
                    position = []
                    position.append(self.food_board[element.x][element.y])
                    position.append(self.snake_board[element.x][element.y])
                    position.append(self.wall_board[element.x][element.y])
                    position.append(self.food_ghost_board[element.x][element.y])
                    position.append(self.snake_ghost_board[element.x][element.y])
                    position.append(self.wall_ghost_board[element.x][element.y])
                    for i in range(len(position)):
                        # add 1 to i, because 0 is empty [same as doing color - 1]
                        # thus, if 0, then it doesn't match with 1 to 6
                        # therefore putting the whole position to hidden
                        if element.color == i+1:
                            self.c.itemconfig(position[i], state=_tk.NORMAL)
                        else:
                            self.c.itemconfig(position[i], state=_tk.HIDDEN)
            except _Queue.Empty:
                pass
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def get_event(self):
            global _ui_factory
            _ui_factory.mainroot.update()
            while True:
                try:
                    self.refresh_event()
                    event = self.event_queue.get_nowait()
                    return event
                except _Queue.Empty:
                    wait_time = min(self.interval, 10)
                    self.wait(wait_time)
                    _ui_factory.mainroot.update()
        
        def set_animation_speed(self, fps):
            current_time = self.milliseconds()
            if fps <= 0:
                self.interval = 0
                self.timer = current_time
                return
            if fps > 1000:
                fps = 1000
            self.interval = int(1000.0 / fps)
            self.refresh_event()
        
        def print_(self, text):
            self.textarea.config(state=_tk.NORMAL)
            self.textarea.insert(_tk.END, text)
            self.textarea.see(_tk.END)
            self.textarea.config(state=_tk.DISABLED)
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def clear_text(self):
            self.textarea.config(state=_tk.NORMAL)
            self.textarea.delete(1.0, _tk.END)
            self.textarea.see(_tk.END)
            self.textarea.config(state=_tk.DISABLED)
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def wait(self, ms):
            try:
              _time.sleep(ms * 0.001)
            except:
              self.close()
        
        def close(self):
            self.root.destroy()
            _os._exit(0)
        
        def random(self, maximum=1):
            return int(_random.random() * maximum)
        
        def create_snake_pieces(self):
            boards = self.food_board, self.snake_board, self.wall_board, self.food_ghost_board, self.snake_ghost_board, self.wall_ghost_board
            for n in range(len(boards)):
                for i in range(self.width):
                    boards[n].append([])
                    for j in range(self.height):
                        x0 = self.size_per_coord * i
                        y0 = self.size_per_coord * j
                        img = self.c.create_image(x0, y0, anchor=_tk.NW, image=self.img_refs[n], state=_tk.HIDDEN)
                        boards[n][i].append(img)
        
        def create_images(self):
            relative_locations = "images/apple.png", "images/snake.png", "images/muur.png", "images/apple_t.png", "images/snake_t.png", "images/muur_t.png"
            locations = []
            for i in range(len(relative_locations)):
                locations.append(_os.path.join(_os.path.dirname(__file__), _os.path.normpath(relative_locations[i])))
            for i in locations:
                size = self.size_per_coord, self.size_per_coord
                img = _Image.open(i).resize(size, _Image.ANTIALIAS)
                ref = _ImageTk.PhotoImage(img)
                self.img_refs.append(ref)
        
        def create_background(self):
            location = "images/jungle.jpg"
            location = _os.path.join(_os.path.dirname(__file__), _os.path.normpath(location))
            size = int(self.c['width']), int(self.c['height'])
            img = _Image.open(location).resize(size, _Image.ANTIALIAS)
            ref = _ImageTk.PhotoImage(img)
            self.img_refs.append(ref)
            self.c.create_image(0, 0, anchor=_tk.NW, image=ref, state=_tk.NORMAL)
        
        def fill_canvas(self):
            self.bind_events()
            self.create_images()
            self.create_background()
            self.create_snake_pieces()
        
        def motion_event(self, event):
            if not self.mouse_on_screen:
                return
            x_old = self.last_x
            y_old = self.last_y
            x_new = event.x / self.size_per_coord
            y_new = event.y / self.size_per_coord
            x_change = int(x_old) != int(x_new)
            y_change = int(y_old) != int(y_new)
            if x_change or y_change:
                self.generate_event("mouseexit", "%d %d"%(x_old,y_old))
                self.generate_event("mouseover", "%d %d"%(x_new,y_new))
                self.last_x = x_new
                self.last_y = y_new
        
        def enter_window_event(self, event):
            x_new = event.x / self.size_per_coord
            y_new = event.y / self.size_per_coord
            self.generate_event("mouseover", "%d %d"%(x_new,y_new))
            self.last_x = x_new
            self.last_y = y_new
            self.mouse_on_screen = True
        
        def leave_window_event(self, event):
            self.generate_event("mouseexit", "%d %d"%(self.last_x,self.last_y))
            self.mouse_on_screen = False
        
        def alt_number_event(self, event):
            if event.char == event.keysym:
                if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
                    self.generate_event("alt_number", event.char)
        
        def key_event(self, event):
            if event.char == event.keysym:
                if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
                    self.generate_event("number", event.char)
                elif ord(event.char) >= ord('a') and ord(event.char) <= ord('z'):
                    self.generate_event("letter", event.char)
                elif ord(event.char) >= ord('A') and ord(event.char) <= ord('Z'):
                    self.generate_event("letter", event.char)
                else:
                    self.generate_event("other", event.char)
            elif event.keysym == 'Up':
                self.generate_event("arrow", "u")
            elif event.keysym == 'Down':
                self.generate_event("arrow", "d")
            elif event.keysym == 'Left':
                self.generate_event("arrow", "l")
            elif event.keysym == 'Right':
                self.generate_event("arrow", "r")
            elif event.keysym == 'Multi_Key':
                return
            elif event.keysym == 'Caps_Lock':
                self.generate_event("other", "caps lock")
            elif event.keysym == 'Num_Lock':
                self.generate_event("other", "num lock")
            elif event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
                self.generate_event("other", "shift")
            elif event.keysym == 'Control_L' or event.keysym == 'Control_R':
                self.generate_event("other", "control")
            elif event.keysym == 'Alt_L' or event.keysym == 'Alt_R':
                self.generate_event("other", "alt")
            else:
                self.generate_event("other", event.keysym)
        
        def click_event(self, event):
            x = event.x / self.size_per_coord
            y = event.y / self.size_per_coord
            self.generate_event("click", "%d %d"%(x,y))
        
        def refresh_event(self):
            current_time = self.milliseconds()
            threshold = current_time - self.timer - self.interval
            if threshold >= 0 and self.interval > 0:
                self.generate_event("alarm", "refresh")
                self.timer = current_time
        
        def generate_event(self, name, data):
            event = Event(name, data)
            self.event_queue.put(event)
        
        def bind_events(self):
            self.c.focus_set() # to redirect keyboard input to this widget
            self.c.bind("<Motion>", self.motion_event)
            self.c.bind("<Enter>", self.enter_window_event)
            self.c.bind("<Leave>", self.leave_window_event)
            self.c.bind("<Alt-Key>", self.alt_number_event)
            self.c.bind("<Key>", self.key_event)
            self.c.bind("<Button-1>", self.click_event)
    
    class LifeUserInterface(object):
        def __init__(self, width, height, scale=1.0):
            """This class starts the LifeUserInterface.
            Constants:
            - DEAD
            - ALIVE
            
            Parameters for the class:
            - width: at least 1
            - height: at least 1
            
            Optional parameters:
            - scale: 0.25 to 1.0
            """
            
            if not have_pil:
                value = "Life: PIL wasn't found, can't use this interface right now."
                raise _IPyException(value)
            _verify_int(width, "Width", 1)
            _verify_int(height, "Height", 1)
            _verify_float(scale, 'Scale', 0.25, 1.0)
            global _ui_factory
            self.life_interface = _Life(width, height, _ui_factory.mainroot, scale)
            self.DEAD = _Life.DEAD
            self.ALIVE = _Life.ALIVE
        
        def place(self, x, y, color):
            """Place a Life piece (defined by 'color') on the given X and Y coordinates.
            """
            
            _verify_int(x, 'X', 0, self.life_interface.width - 1)
            _verify_int(y, 'Y', 0, self.life_interface.height - 1)
            # 0 = empty, 1 = dead, 2 = alive
            _verify_int(color, 'Color', 0, 2)
            self.life_interface.place(x, y, color)
        
        def clear(self):
            """Clears the display.
            Note: this does not clear the text area!
            """
            
            self.life_interface.clear()
        
        def show(self):
            """Show the changes made to the display (i.e. after calling place or clear)
            """
            
            self.life_interface.show()
        
        def get_event(self):
            """Returns an event generated from the display.
            The returned object has 2 properties:
            - name: holds the group which the event belongs to.
            - data: holds useful information for the user.
            """
            
            return self.life_interface.get_event()
        
        def set_animation_speed(self, fps):
            """Set an event to repeat 'fps' times per second.
            If the value is set to 0 or less, the repeating will halt.
            In theory the maximum value is 1000, but this depends on activity of the system.
            
            The generated events (available by using get_event) have these properties:
            - name: 'alarm'.
            - data: 'refresh'.
            """
            
            _verify_float(fps, "Animation speed")
            self.life_interface.set_animation_speed(fps)
        
        def print_(self, text):
            """Print text to the text area on the display.
            This function does not add a trailing newline by itself.
            """
            
            _verify_str(text, "Text")
            self.life_interface.print_(text)
        
        def clear_text(self):
            """Clears the text area on the display.
            """
            
            self.life_interface.clear_text()
        
        def wait(self, ms):
            """Let your program wait for an amount of milliseconds.
            
            This function only guarantees that it will wait at least this amount of time.
            If the system, i.e., is too busy, then this time might increase.
            - Python time module.
            """
            
            _verify_int(ms, "Waiting time", 0)
            self.life_interface.wait(ms)
        
        def random(self, maximum):
            """Picks a random integer ranging from 0 <= x < maximum
            Minimum for maximum is 1
            """
            
            _verify_int(maximum, 'Random', 1)
            return self.life_interface.random(maximum)
        
        def close(self):
            """Closes the display and stops your program.
            """
            
            self.life_interface.close()
            
        def stay_open(self):
            """Force the window to remain open.
            Only has effect on Mac OS to prevent the window from closing after the execution finishes.
            
            Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
            """
            
            global _ui_factory
            _ui_factory.mainroot.mainloop()
    
    class _Life(object):
        #one cannot prevent users from editing 'constants', as constants simply do not exist in Python
        DEAD = 0
        ALIVE = 1
        
        BACKGROUND = "#000000"
        
        def __init__(self, width, height, mainroot, scale=1.0):
            if not have_pil:
                value = "Life: PIL wasn't found, can't use this interface right now."
                raise _IPyException(value)
            #create queue to store changes to placings
            self.to_show_queue = _Queue.Queue(maxsize=0)
            self.event_queue = _Queue.Queue(maxsize=0)
            
            #copy params
            self.width = width
            self.height = height
            self.scale = scale
            
            #start the main window
            self.root = _tk.Toplevel(mainroot)
            self.root.title("SnakeUserInterface")
            self.root.protocol("WM_DELETE_WINDOW", self.callback)
            self.root.bind("<Escape>", self.callback)
            self.root.resizable(False, False)
            
            #calculate sizes
            self.size_per_coord = int(25 * scale)
            self.text_height = int(200 * scale)
            
            #create main frame
            self.frame = _tk.Frame(self.root, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height+self.text_height)
            self.frame.pack_propagate(0)
            self.frame.pack()
            
            #create board to hold references to snake-pieces
            self.dead_board = [] # for storing references to create_image
            self.alive_board = []
            self.img_refs = [] # for storing references to images - order: dead, alive
            
            #create and fill the canvas --> paintable area
            self.c = _tk.Canvas(self.frame, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height, bg=self.BACKGROUND, bd=0, highlightthickness=0)
            self.c.pack()
            self.last_x = -1 # used to generate mouseOver/Exit events
            self.last_y = -1 # used to generate mouseOver/Exit events
            self.fill_canvas()
            
            #create the textholder
            self.scrollbar = _tk.Scrollbar(self.frame)
            self.scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
            self.textarea = _tk.Text(self.frame, yscrollcommand=self.scrollbar.set)
            self.textarea.pack(side=_tk.LEFT, fill=_tk.BOTH)
            self.scrollbar.config(command=self.textarea.yview)
            self.textarea.config(state=_tk.DISABLED)
            
            self.interval = 0
            self.alarm_speed = 0
            self.timer = self.milliseconds()
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def callback(self, event=None):
            self.root.destroy()
            _os._exit(0)
        
        def milliseconds(self):
            return _time.time() * 1000
        
        def place(self, x, y, color):
            element = _LifeHolder(x, y, color)
            self.to_show_queue.put(element)
        
        def clear(self):
            for x in range(self.width):
                for y in range(self.height):
                    self.place(x, y, self.DEAD)
        
        def show(self):
            try:
                while True:
                    element = self.to_show_queue.get_nowait()
                    position = []
                    position.append(self.dead_board[element.x][element.y])
                    position.append(self.alive_board[element.x][element.y])
                    for i in range(len(position)):
                        if element.color == i:
                            self.c.itemconfig(position[i], state=_tk.NORMAL)
                        else:
                            self.c.itemconfig(position[i], state=_tk.HIDDEN)
            except _Queue.Empty:
                pass
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def get_event(self):
            global _ui_factory
            _ui_factory.mainroot.update()
            while True:
                try:
                    self.refresh_event()
                    event = self.event_queue.get_nowait()
                    return event
                except _Queue.Empty:
                    wait_time = min(self.interval, 10)
                    self.wait(wait_time)
                    _ui_factory.mainroot.update()
        
        def set_animation_speed(self, fps):
            current_time = self.milliseconds()
            if fps <= 0:
                self.interval = 0
                self.timer = current_time
                return
            if fps > 1000:
                fps = 1000
            self.interval = int(1000.0 / fps)
            self.refresh_event()
        
        def print_(self, text):
            self.textarea.config(state=_tk.NORMAL)
            self.textarea.insert(_tk.END, text)
            self.textarea.see(_tk.END)
            self.textarea.config(state=_tk.DISABLED)
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def clear_text(self):
            self.textarea.config(state=_tk.NORMAL)
            self.textarea.delete(1.0, _tk.END)
            self.textarea.see(_tk.END)
            self.textarea.config(state=_tk.DISABLED)
            global _ui_factory
            _ui_factory.mainroot.update()
        
        def wait(self, ms):
            try:
              _time.sleep(ms * 0.001)
            except:
              self.close()
        
        def close(self):
            self.root.destroy()
            _os._exit(0)
        
        def random(self, maximum=1):
            return int(_random.random() * maximum)
        
        def create_life_pieces(self):
            boards = self.dead_board, self.alive_board
            for n in range(len(boards)):
                for i in range(self.width):
                    boards[n].append([])
                    for j in range(self.height):
                        x0 = self.size_per_coord * i
                        y0 = self.size_per_coord * j
                        state_ = _tk.HIDDEN
                        if n == 0:
                            state_ = _tk.NORMAL
                        img = self.c.create_image(x0, y0, anchor=_tk.NW, image=self.img_refs[n], state=state_)
                        boards[n][i].append(img)
        
        def create_images(self):
            relative_locations = "images/dead.png", "images/alive.png"
            locations = []
            for i in range(len(relative_locations)):
                locations.append(_os.path.join(_os.path.dirname(__file__), _os.path.normpath(relative_locations[i])))
            for i in locations:
                size = self.size_per_coord, self.size_per_coord
                img = _Image.open(i).resize(size, _Image.ANTIALIAS)
                ref = _ImageTk.PhotoImage(img)
                self.img_refs.append(ref)
        
        def fill_canvas(self):
            self.bind_events()
            self.create_images()
            self.create_life_pieces()
        
        def motion_event(self, event):
            if not self.mouse_on_screen:
                return
            x_old = self.last_x
            y_old = self.last_y
            x_new = event.x / self.size_per_coord
            y_new = event.y / self.size_per_coord
            x_change = int(x_old) != int(x_new)
            y_change = int(y_old) != int(y_new)
            if x_change or y_change:
                self.generate_event("mouseexit", "%d %d"%(x_old,y_old))
                self.generate_event("mouseover", "%d %d"%(x_new,y_new))
                self.last_x = x_new
                self.last_y = y_new
        
        def enter_window_event(self, event):
            x_new = event.x / self.size_per_coord
            y_new = event.y / self.size_per_coord
            self.generate_event("mouseover", "%d %d"%(x_new,y_new))
            self.last_x = x_new
            self.last_y = y_new
            self.mouse_on_screen = True
        
        def leave_window_event(self, event):
            self.generate_event("mouseexit", "%d %d"%(self.last_x,self.last_y))
            self.mouse_on_screen = False
        
        def alt_number_event(self, event):
            if event.char == event.keysym:
                if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
                    self.generate_event("alt_number", event.char)
        
        def key_event(self, event):
            if event.char == event.keysym:
                if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
                    self.generate_event("number", event.char)
                elif ord(event.char) >= ord('a') and ord(event.char) <= ord('z'):
                    self.generate_event("letter", event.char)
                elif ord(event.char) >= ord('A') and ord(event.char) <= ord('Z'):
                    self.generate_event("letter", event.char)
                else:
                    self.generate_event("other", event.char)
            elif event.keysym == 'Up':
                self.generate_event("arrow", "u")
            elif event.keysym == 'Down':
                self.generate_event("arrow", "d")
            elif event.keysym == 'Left':
                self.generate_event("arrow", "l")
            elif event.keysym == 'Right':
                self.generate_event("arrow", "r")
            elif event.keysym == 'Multi_Key':
                return
            elif event.keysym == 'Caps_Lock':
                self.generate_event("other", "caps lock")
            elif event.keysym == 'Num_Lock':
                self.generate_event("other", "num lock")
            elif event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
                self.generate_event("other", "shift")
            elif event.keysym == 'Control_L' or event.keysym == 'Control_R':
                self.generate_event("other", "control")
            elif event.keysym == 'Alt_L' or event.keysym == 'Alt_R':
                self.generate_event("other", "alt")
            else:
                self.generate_event("other", event.keysym)
        
        def click_event(self, event):
            x = event.x / self.size_per_coord
            y = event.y / self.size_per_coord
            self.generate_event("click", "%d %d"%(x,y))
        
        def refresh_event(self):
            current_time = self.milliseconds()
            threshold = current_time - self.timer - self.interval
            if threshold >= 0 and self.interval > 0:
                self.generate_event("alarm", "refresh")
                self.timer = current_time
        
        def generate_event(self, name, data):
            event = Event(name, data)
            self.event_queue.put(event)
        
        def bind_events(self):
            self.c.focus_set() # to redirect keyboard input to this widget
            self.c.bind("<Motion>", self.motion_event)
            self.c.bind("<Enter>", self.enter_window_event)
            self.c.bind("<Leave>", self.leave_window_event)
            self.c.bind("<Alt-Key>", self.alt_number_event)
            self.c.bind("<Key>", self.key_event)
            self.c.bind("<Button-1>", self.click_event)
    
    class Event(object):
        def __init__(self, name, data):
            """This class holds the name and data for each event in their respective variables.
            Variables:
            - name
            - data
            
            Example to access with SnakeUserInterface:
            
            ui = SnakeUserInterface(5,5) # 5 by 5 grid for testing purposes
            your_variable = ui.get_event() # code will block untill an event comes
            # your_variable now points to an event
            print your_variable.name, your_variable.data
            
            List of events:
            - name: mouseover
              data: x and y coordinates (as integers), separated by a space
                  generated when mouse goes over a coordinate on the window
            - name: mouseexit
              data: x and y coordinates (as integers), separated by a space
                  generated when mouse exits a coordinate on the window
            - name: click
              data: x and y coordinates (as integers), separated by a space
                  generated when the user clicks on a coordinate on the window
            - name: alarm
              data: refresh
                  generated as often per second as the user set the animation speed to; note that the data is exactly as it says: "refresh"
            - name: letter
              data: the letter that got pressed
                  generated when the user presses on a letter (A to Z; can be lowercase or uppercase depending on shift/caps lock)
            - name: number
              data: the number (as a string) that got pressed
                  generated when the user presses on a number (0 to 9)
            - name: alt_number
              data: the number (as a string) that got pressed
                  generated when the user presses on a number (0 to 9) while at the same time pressing the Alt key
            - name: arrow
              data: the arrow key that got pressed, given by a single letter
                  generated when the user presses on an arrow key, data is then one of: l, r, u, d
            - name: other
              data: data depends on key pressed
                  generated when the user pressed a different key than those described above
                  possible data:
                  - caps_lock
                  - num_lock
                  - alt
                  - control
                  - shift
                  more data can exist and are recorded (read: they generate events), but not documented
            """
            self.name = name
            self.data = data
    
    _ui_factory = _Factory()
else:
    _add_interface_queue = _Queue.Queue(maxsize=0)
    #boolean did not work here in conjuction with using the 'global' prefix inside functions, hence queue
    _set_interface_list = _Queue.Queue(maxsize=0)
    _active_interface_list = []
    
    def file_input():
        """This function lets the user select a file to use for input.
        Returns the file contents in a string.
        """
        isAdded = False
        global _add_interface_queue
        global _set_interface_list
        _add_interface_queue.put([0])
        while not isAdded:
            try:
                while True:
                    element = _set_interface_list.get_nowait()
                    isAdded = True
                    # if no file was given
                    if element == '':
                        return None
            except _Queue.Empty:
                pass
            _time.sleep(0.001)
        return str(_sys.stdin.read())
    
    def ask_user(question, *options):
        """Ask the user a question.
        Parameters:
        - question: the string to ask the user
        - options: arbitrary list of arguments (at least 1)
        Returns the chosen option by the user or None if nothing was chosen (e.g. hit Escape).
        """
        
        is_added = False
        global _add_interface_queue
        global _set_interface_list
        if len(options) == 0:
            value = "User needs to be able to select at least 1 answer"
            raise _IPyException(value)
        _add_interface_queue.put([-1, question, options])
        while not is_added:
            try:
                while True:
                    element = _set_interface_list.get_nowait()
                    is_added = True
                    return element
            except _Queue.Empty:
                pass
            _time.sleep(0.001)
        #statement below to let it compile
        return True
    
    class _Factory(_threading.Thread):
        def __init__(self):
            self.parent = _threading.current_thread()
            _threading.Thread.__init__(self)
            self.start()
        
        def run(self):
            self.mainroot = _tk.Tk()
            self.mainroot.withdraw()
            self.mainroot.after(1, self.poll)
            self.mainroot.mainloop()
        
        def poll(self):
            global _active_interface_list
            if len(_active_interface_list) == 0 and not self.parent.isAlive():
                self.mainroot.destroy()
                _os._exit(0)
            global _add_interface_queue
            try:
                while True:
                    element = _add_interface_queue.get_nowait()
                    global _set_interface_list
                    ref = None
                    if element[0] == -1:
                        ref = _AskUser(self.mainroot, element[1], element[2])
                        _set_interface_list.put(ref.answer)
                        continue
                    if element[0] == 0:
                        ref = _AskInput(self.mainroot)
                        _set_interface_list.put(ref.f)
                        continue
                    if element[0] == 1:
                        ref = _Othello(self.mainroot, element[1])
                    if element[0] == 2:
                        ref = _BarChart(element[1], self.mainroot)
                    if element[0] == 3:
                        ref = _Snake(element[1], element[2], self.mainroot, element[3])
                    if element[0] == 4:
                        ref = _Life(element[1], element[2], self.mainroot, element[3])
                    if element[0] > 0:
                        _active_interface_list.append(ref)
                    _set_interface_list.put(1)
            except _Queue.Empty:
                pass
            for element in _active_interface_list:
                element.poll()
            self.mainroot.after(1, self.poll)
    
    class _AskInput(object):
        def __init__(self, mainroot):
            root = _tk.Toplevel(mainroot)
            root.withdraw()
            self.f = _tkFileDialog.askopenfilename(parent=root)
            if self.f is not '':
                _sys.stdin = file(self.f)
            root.destroy()
    
    class _AskUser(object):
        def __init__(self, mainroot, question, options):
            root = _tk.Toplevel(mainroot)
            root.withdraw()
            dg = _Dialog.Dialog(None,
            title="",
            text=question,
            default=0,
            bitmap=_tkMessageBox.QUESTION,
            strings=options)
            self.answer = options[dg.num]
            root.destroy()
    
    class _PrintQueueHolder(object):
        def __init__(self, text, clear_text):
            self.text = text
            self.clear_text = clear_text
    
    class OthelloReplayUserInterface(object):
        def __init__(self, scale=1.0):
            """This class starts the OthelloReplayUserInterface.
            Constants:
            - NUMBER_OF_ROWS
            - NUMBER_OF_COLUMNS
            - EMPTY
            - WHITE
            - BLACK
            
            Parameters for the class: (none)
            
            Optional parameters:
            - scale: 0.25 to 1.0
            """
            
            if not have_pil:
                value = "OthelloReplay: PIL wasn't found, can't use this interface right now."
                raise _IPyException(value)
            _verify_float(scale, 'Scale', 0.25, 1.0)
            is_added = False
            global _add_interface_queue
            global _set_interface_list
            _add_interface_queue.put([1, scale])
            while not is_added:
                try:
                    while True:
                        _set_interface_list.get_nowait()
                        is_added = True
                except _Queue.Empty:
                    pass
                _time.sleep(0.001)
            global _active_interface_list
            self.othello_replay = _active_interface_list[-1]
            self.NUMBER_OF_ROWS = _Othello.NUMBER_OF_ROWS
            self.NUMBER_OF_COLUMNS = _Othello.NUMBER_OF_COLUMNS
            self.EMPTY = _Othello.EMPTY
            self.WHITE = _Othello.WHITE
            self.BLACK = _Othello.BLACK
        
        def place(self, x, y, color):
            """Place an Othello piece (defined by 'color') on the given X and Y coordinates.
            """
            
            _verify_int(x, 'X', 0, self.NUMBER_OF_COLUMNS - 1)
            _verify_int(y, 'Y', 0, self.NUMBER_OF_ROWS - 1)
            # 0 = empty, 1 = white, 2 = black, 3 = white_t, 4 = black_t
            _verify_int(color, 'Color', 0, 4)
            self.othello_replay.place(x, y, color)
        
        def place_transparent(self, x, y, color):
            """Place a semi-transparent Othello piece (defined by 'color') on the given X and Y coordinates.
            """
            
            _verify_int(x, 'X', 0, self.NUMBER_OF_COLUMNS - 1)
            _verify_int(y, 'Y', 0, self.NUMBER_OF_ROWS - 1)
            # 0 = empty, 1 = white_t, 2 = black_t (before next step in code)
            _verify_int(color, 'Color', 0, 2)
            if color == self.EMPTY:
                self.place(x, y, self.EMPTY)
            else:
                self.place(x, y, color+2)
        
        def clear(self):
            """Clears the display.
            Note: this does not clear the text area!
            """
            
            self.othello_replay.clear()
        
        def show(self):
            """Show the changes made to the display (i.e. after calling place or clear).
            """
            
            self.othello_replay.show()
        
        def print_(self, text):
            """Print text to the text area on the display.
            This function does not add a trailing newline by itself.
            """
            
            _verify_str(text, "Text")
            self.othello_replay.print_(text)
        
        def clear_text(self):
            """Clears the text area on the display.
            """
            
            self.othello_replay.clear_text()
        
        def wait(self, ms):
            """Let your program wait for an amount of milliseconds.
            
            This function only guarantees that it will wait at least this amount of time.
            If the system, i.e., is too busy, then this time might increase.
            - Python time module.
            """
            
            _verify_int(ms, "Waiting time", 0)
            self.othello_replay.wait(ms)
        
        def close(self):
            """Closes the display and stops your program.
            """
            
            self.othello_replay.close()
        
        def stay_open(self):
            """Force the window to remain open.
            Only has effect on Mac OS to prevent the window from closing after the execution finishes.
            
            Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
            """
            
            pass
    
    class _Othello(object):
        #one cannot prevent users from editing 'constants', as constants simply do not exist in Python
        NUMBER_OF_ROWS = 8
        NUMBER_OF_COLUMNS = 8
        EMPTY = 0
        WHITE = 1
        BLACK = 2
        
        BACKGROUND = "#147800"
        
        def __init__(self, mainroot, scale=1.0):
            #create queue to store changes to placings
            self.to_show_queue = _Queue.Queue(maxsize=0)
            self.place_queue = _Queue.Queue(maxsize=0)
            self.print_queue = _Queue.Queue(maxsize=0)
            
            self.closing_window = False
            
            #start the main window
            self.root = _tk.Toplevel(mainroot)
            self.root.title("OthelloReplayUserInterface")
            self.root.protocol("WM_DELETE_WINDOW", self.callback)
            self.root.bind("<Escape>", self.callback)
            self.root.resizable(False, False)
            
            #calculate sizes
            self.text_height = int(200 * scale)
            self.othello_size = int(800 * scale)
            
            #create main frame
            self.frame = _tk.Frame(self.root, width=self.othello_size, height=self.othello_size+self.text_height)
            self.frame.pack_propagate(0)
            self.frame.pack()
            
            #create board to hold references to othello-pieces
            self.white_board = [] # for storing references to create_image
            self.black_board = []
            self.white_ghost_board = []
            self.black_ghost_board = []
            self.img_refs = [] # for storing references to images - order: white, black
            
            #create and fill the canvas --> paintable area
            self.c = _tk.Canvas(self.frame, width=self.othello_size, height=self.othello_size, bg=self.BACKGROUND, bd=0, highlightthickness=0)
            self.c.pack()
            self.c.focus_set()
            self.fill_canvas()
            
            #create the textholder
            self.scrollbar = _tk.Scrollbar(self.frame)
            self.scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
            self.textarea = _tk.Text(self.frame, yscrollcommand=self.scrollbar.set)
            self.textarea.pack(side=_tk.LEFT, fill=_tk.BOTH)
            self.scrollbar.config(command=self.textarea.yview)
            self.textarea.config(state=_tk.DISABLED)
        
        def callback(self, event=None):
            self.root.destroy()
            _os._exit(0)
        
        def place(self, x, y, color):
            element = _OthelloReplayHolder(x, y, color)
            self.to_show_queue.put(element)
        
        def clear(self):
            for x in range(self.NUMBER_OF_COLUMNS):
                for y in range(self.NUMBER_OF_ROWS):
                    self.place(x, y, self.EMPTY)
        
        def show(self):
            try:
                while True:
                    element = self.to_show_queue.get_nowait()
                    self.place_queue.put(element)
            except _Queue.Empty:
                pass
        
        def update_config(self):
            if self.closing_window:
                self.root.destroy()
                _os._exit(0)
                return
            try:
                while True:
                    element = self.place_queue.get_nowait()
                    position = []
                    position.append(self.white_board[element.x][element.y])
                    position.append(self.black_board[element.x][element.y])
                    position.append(self.white_ghost_board[element.x][element.y])
                    position.append(self.black_ghost_board[element.x][element.y])
                    for i in range(len(position)):
                        if element.color == i+1:
                            self.c.itemconfig(position[i], state=_tk.NORMAL)
                        else:
                            self.c.itemconfig(position[i], state=_tk.HIDDEN)
            except _Queue.Empty:
                pass
            try:
                while True:
                    element = self.print_queue.get_nowait()
                    self.textarea.config(state=_tk.NORMAL)
                    if element.clear_text:
                        self.textarea.delete(1.0, _tk.END)
                    else:
                        self.textarea.insert(_tk.END, element.text)
                    self.textarea.see(_tk.END)
                    self.textarea.config(state=_tk.DISABLED)
            except _Queue.Empty:
                pass
        
        def print_(self, text):
            element = _PrintQueueHolder(text, False)
            self.print_queue.put(element)
        
        def clear_text(self):
            element = _PrintQueueHolder('', True)
            self.print_queue.put(element)
        
        def wait(self, ms):
            _time.sleep(ms * 0.001)
        
        def close(self):
            self.closing_window = True
        
        def create_othello_grid(self):
            for i in range(self.NUMBER_OF_COLUMNS+1):
                x0 = self.xpad + self.xstep * i
                y0 = self.ypad
                x1 = x0
                y1 = self.ypad + self.ystep * self.NUMBER_OF_ROWS + 1
                coords = x0, y0, x1, y1
                self.c.create_line(coords, fill='black')
            for j in range(self.NUMBER_OF_ROWS+1):
                x0 = self.xpad
                y0 = self.ypad + self.ystep * j
                x1 = self.xpad + self.xstep * self.NUMBER_OF_COLUMNS + 1
                y1 = y0
                coords = x0, y0, x1, y1
                self.c.create_line(coords, fill='black')
            for i in range(self.NUMBER_OF_COLUMNS):
                x0 = self.xpad + self.xstep / 2 + self.xstep * i
                y0 = self.ypad / 2
                x1 = x0
                y1 = self.othello_size - self.ystep / 2
                coords0 = x0, y0
                coords1 = x1, y1
                self.c.create_text(coords0, text=chr(ord('a')+i))
                self.c.create_text(coords1, text=chr(ord('a')+i))
            for j in range(self.NUMBER_OF_ROWS):
                x0 = self.xpad / 2
                y0 = self.ypad + self.ystep / 2 + self.ystep * j
                x1 = self.othello_size - self.xstep / 2
                y1 = y0
                coords0 = x0, y0
                coords1 = x1, y1
                self.c.create_text(coords0, text='%s'%(j+1))
                self.c.create_text(coords1, text='%s'%(j+1))
        
        def create_images(self):
            relative_locations = "images/white.png", "images/black.png", "images/white_t.png", "images/black_t.png"
            locations = []
            for i in range(len(relative_locations)):
                locations.append(_os.path.join(_os.path.dirname(__file__), _os.path.normpath(relative_locations[i])))
            for i in locations:
                size = int(self.xstep * 0.8), int(self.ystep * 0.8)
                img = _Image.open(i).resize(size, _Image.ANTIALIAS)
                ref = _ImageTk.PhotoImage(img)
                self.img_refs.append(ref)
        
        def create_othello_pieces(self):
            boards = self.white_board, self.black_board, self.white_ghost_board, self.black_ghost_board
            for n in range(len(boards)):
                for i in range(self.NUMBER_OF_COLUMNS):
                    boards[n].append([])
                    for j in range(self.NUMBER_OF_ROWS):
                        x0 = self.xpad + self.xstep * i + self.xstep/2
                        y0 = self.ypad + self.ystep * j + self.ystep/2
                        img = self.c.create_image(x0, y0, anchor=_tk.CENTER, image=self.img_refs[n], state=_tk.HIDDEN)
                        boards[n][i].append(img)
        
        def fill_canvas(self):
            self.xstep = self.othello_size / (self.NUMBER_OF_COLUMNS + 2)
            self.ystep = self.othello_size / (self.NUMBER_OF_ROWS + 2)
            self.xpad = (self.othello_size - self.NUMBER_OF_COLUMNS * self.xstep) / 2
            self.ypad = (self.othello_size - self.NUMBER_OF_ROWS * self.ystep) / 2
            self.create_images()
            self.create_othello_grid()
            self.create_othello_pieces()
        
        def poll(self):
            self.update_config()
    
    class BarChartUserInterface(object):
        def __init__(self, bar_count):
            """This class starts the BarChartUserInterface.
            Constants: (none)
            
            Parameters for the class:
            - bar_count: at least 1
            
            Optional parameters: (none)
            """
            
            _verify_int(bar_count, "Bar count", 1)
            is_added = False
            global _add_interface_queue
            global _set_interface_list
            _add_interface_queue.put([2, bar_count])
            while not is_added:
                try:
                    while True:
                        _set_interface_list.get_nowait()
                        is_added = True
                except _Queue.Empty:
                    pass
                _time.sleep(0.001)
            global _active_interface_list
            self.bar_chart = _active_interface_list[-1]
        
        def set_bar_name(self, bar_index, text):
            """Set a name, provided by 'text', to a given bar_index.
            Note: this function's effects are visible without calling show.
            """
            
            _verify_int(bar_index, "Bar index", 0, self.bar_chart.bar_count - 1)
            _verify_str(text, "Text")
            self.bar_chart.set_bar_name(bar_index, text);
        
        def raise_bar(self, bar_index):
            """Increment the given bar_index by 1.
            """
            
            _verify_int(bar_index, "Bar index", 0, self.bar_chart.bar_count - 1)
            self.bar_chart.raise_bar(bar_index)
        
        def show(self):
            """Show the changes made to the display (i.e. after calling raise_bar).
            """
            
            self.bar_chart.show()
        
        def show_names(self, value):
            """Whether or not to show the names of the bars.
            Value given must be a boolean.
            Default at start is False.
            """
            
            _verify_bool(value, "Show names")
            self.bar_chart.show_names(value)
        
        def show_values(self, value):
            """Whether or not to show the values of the bars.
            Value given must be a boolean.
            Default at start is True.
            """
            
            _verify_bool(value, "Show values")
            self.bar_chart.show_values(value)
        
        def wait(self, ms):
            """Let your program wait for an amount of milliseconds.
            
            This function only guarantees that it will wait at least this amount of time.
            If the system, i.e., is too busy, then this time might increase.
            - Python time module.
            """
            
            _verify_int(ms, "Waiting time", 0)
            self.bar_chart.wait(ms)
        
        def close(self):
            """Closes the display and stops your program.
            """
            
            self.bar_chart.close()
        
        def stay_open(self):
            """Force the window to remain open.
            Only has effect on Mac OS to prevent the window from closing after the execution finishes.
            
            Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
            """
            
            pass
    
    class _BarChart(object):
        def __init__(self, bar_count, mainroot):
            #create queue to store changes to placings
            self.to_show_queue = _Queue.Queue(maxsize=0)
            self.place_queue = _Queue.Queue(maxsize=0)
            self.to_show_names_queue = _Queue.Queue(maxsize=0)
            self.place_names_queue = _Queue.Queue(maxsize=0)
            
            #variables used to keep the number of refreshes of names and values in check
            self.show_names_bool_old = False
            self.show_names_bool = False
            self.show_values_bool_old = True
            self.show_values_bool = True
            
            self.bar_count = bar_count
            
            self.closing_window = False
            
            #start the main window
            self.root = _tk.Toplevel(mainroot)
            self.root.title("BarChartUserInterface")
            self.root.protocol("WM_DELETE_WINDOW", self.callback)
            self.root.bind("<Escape>", self.callback)
            self.frame = _tk.Frame(self.root)
            self.frame.pack(fill=_tk.BOTH, expand=_tk.YES)
            self.height = 575
            self.width = 400
            self.c = _tk.Canvas(self.frame, width=self.width, height=self.height, bg='white', bd=0, highlightthickness=0)
            self.c.pack(fill=_tk.BOTH, expand=_tk.YES)
            self.c.focus_set()
            self.c.bind('<Configure>', self.redraw)
            self.bar_max = 0
            self.bars = []
            self.names = []
            self.create_bars()
        
        def callback(self, event=None):
            self.root.destroy()
            _os._exit(0)
        
        def set_bar_name(self, bar_index, text):
            element = _BarChartNameHolder(bar_index, text)
            self.to_show_names_queue.put(element)
        
        def raise_bar(self, bar_index):
            element = _BarChartHolder(bar_index)
            self.to_show_queue.put(element)
        
        def inc_bar(self, bar_index):
            if (self.bars[bar_index] + 1) > self.bar_max:
                self.bar_max = self.bars[bar_index] + 1
            self.bars[bar_index] += 1
        
        def show(self):
            try:
                while True:
                    element = self.to_show_queue.get_nowait()
                    self.place_queue.put(element)
            except _Queue.Empty:
                pass
            try:
                while True:
                    element = self.to_show_names_queue.get_nowait()
                    self.place_names_queue.put(element)
            except _Queue.Empty:
                pass
        
        def show_names(self, value):
            self.show_names_bool = value
        
        def show_values(self, value):
            self.show_values_bool = value
        
        def wait(self, ms):
            _time.sleep(ms * 0.001)
        
        def close(self):
            self.closing_window = True
        
        def create_bars(self):
            for i in range(self.bar_count): #@UnusedVariable
                self.bars.append(0)
                self.names.append('')
        
        def show_changes(self):
            if self.closing_window:
                self.root.destroy()
                _os._exit(0)
                return
            changes = False
            try:
                while True:
                    element = self.place_queue.get_nowait()
                    self.inc_bar(element.bar_index)
                    changes = True
            except _Queue.Empty:
                pass
            try:
                while True:
                    element = self.place_names_queue.get_nowait()
                    self.names[element.bar_index] = element.bar_name;
                    changes = True
            except _Queue.Empty:
                pass
            saved_names_bool = self.show_names_bool
            saved_values_bool = self.show_values_bool
            if (self.show_names_bool_old != saved_names_bool) or (self.show_values_bool_old != saved_values_bool):
                changes = True
                self.show_names_bool_old = saved_names_bool
                self.show_values_bool_old = saved_values_bool
            if changes:
                self.redraw()
        
        def redraw(self, event=None):
            if event != None:
                self.width = event.width
                self.height = event.height
            for e in self.c.find_all():
                self.c.delete(e)
            self.fill_canvas()
        
        def fill_canvas(self):
            xstep = self.width / (self.bar_count + 2)
            xpad = (self.width - xstep * self.bar_count) / 2
            xspacing = xstep / 10
            ypad = self.height / 10
            ypadtext = ypad / 3
            for i in range(self.bar_count):
                #draw the bar
                x0 = xpad + xstep * i + xspacing
                y0 = self.height - ypad
                x1 = xpad + xstep * (i + 1) - xspacing
                y1 = self.height - ypad
                color = 0
                if self.bar_max > 0:
                    y_len = self.bars[i] * (self.height - 2 * ypad) / self.bar_max
                    y1 -= y_len
                    color = self.bars[i] * 255 / self.bar_max
                coords = x0, y0, x1, y1
                hex_color = "#%02x%02x%02x" % (color, 0, 0) #red, green, blue
                self.c.create_rectangle(coords, fill=hex_color)
                
                #draw the values
                x1 = xpad + xstep * i + xstep / 2
                y1 -= ypadtext
                coords = x1, y1
                value = ("%d" % self.bars[i]) if self.show_values_bool else ''
                self.c.create_text(coords, text=value)
                
                #draw the names
                x0 = xpad + xstep * i + xstep / 2
                y0 += ypadtext
                coords = x0, y0
                name = self.names[i] if self.show_names_bool else ''
                self.c.create_text(coords, text=name)
        
        def poll(self):
            self.show_changes()
    
    class SnakeUserInterface(object):
        def __init__(self, width, height, scale=1.0):
            """This class starts the SnakeUserInterface.
            Constants:
            - EMPTY
            - FOOD
            - SNAKE
            - WALL
            
            Parameters for the class:
            - width: at least 1
            - height: at least 1
            
            Optional parameters:
            - scale: 0.25 to 1.0
            """
            
            if not have_pil:
                value = "Snake: PIL wasn't found, can't use this interface right now."
                raise _IPyException(value)
            _verify_int(width, "Width", 1)
            _verify_int(height, "Height", 1)
            _verify_float(scale, 'Scale', 0.25, 1.0)
            is_added = False
            global _add_interface_queue
            global _set_interface_list
            _add_interface_queue.put([3, width, height, scale])
            while not is_added:
                try:
                    while True:
                        _set_interface_list.get_nowait()
                        is_added = True
                except _Queue.Empty:
                    pass
                _time.sleep(0.001)
            global _active_interface_list
            self.snake_interface = _active_interface_list[-1]
            self.EMPTY = _Snake.EMPTY
            self.FOOD = _Snake.FOOD
            self.SNAKE = _Snake.SNAKE
            self.WALL = _Snake.WALL
        
        def place(self, x, y, color):
            """Place a Snake piece (defined by 'color') on the given X and Y coordinates.
            """
            
            _verify_int(x, 'X', 0, self.snake_interface.width - 1)
            _verify_int(y, 'Y', 0, self.snake_interface.height - 1)
            # 0 = empty, 1 = food, 2 = snake, 3 = wall, 4 = food_t, 5 = snake_t, 6 = wall_t
            _verify_int(color, 'Color', 0, 6)
            self.snake_interface.place(x, y, color)
        
        def place_transparent(self, x, y, color):
            """Place a semi-transparent Snake piece (defined by 'color') on the given X and Y coordinates.
            """
            
            _verify_int(x, 'X', 0, self.snake_interface.width - 1)
            _verify_int(y, 'Y', 0, self.snake_interface.height - 1)
            # 0 = empty, 1 = food_t, 2 = snake_t, 3 = wall_t (before next step in code)
            _verify_int(color, 'Color', 0, 6)
            if color == self.EMPTY:
                self.place(x, y, self.EMPTY)
            else:
                self.place(x, y, color+3)
        
        def clear(self):
            """Clears the display.
            Note: this does not clear the text area!
            """
            
            self.snake_interface.clear()
        
        def show(self):
            """Show the changes made to the display (i.e. after calling place or clear)
            """
            
            self.snake_interface.show()
        
        def get_event(self):
            """Returns an event generated from the display.
            The returned object has 2 properties:
            - name: holds the group which the event belongs to.
            - data: holds useful information for the user.
            """
            
            return self.snake_interface.get_event()
        
        def set_animation_speed(self, fps):
            """Set an event to repeat 'fps' times per second.
            If the value is set to 0 or less, the repeating will halt.
            In theory the maximum value is 1000, but this depends on activity of the system.
            
            The generated events (available by using get_event) have these properties:
            - name: 'alarm'.
            - data: 'refresh'.
            """
            
            _verify_float(fps, "Animation speed")
            self.snake_interface.set_animation_speed(fps)
        
        def print_(self, text):
            """Print text to the text area on the display.
            This function does not add a trailing newline by itself.
            """
            
            _verify_str(text, "Text")
            self.snake_interface.print_(text)
        
        def clear_text(self):
            """Clears the text area on the display.
            """
            
            self.snake_interface.clear_text()
        
        def wait(self, ms):
            """Let your program wait for an amount of milliseconds.
            
            This function only guarantees that it will wait at least this amount of time.
            If the system, i.e., is too busy, then this time might increase.
            - Python time module.
            """
            
            _verify_int(ms, "Waiting time", 0)
            self.snake_interface.wait(ms)
        
        def random(self, maximum):
            """Picks a random integer ranging from 0 <= x < maximum
            Minimum for maximum is 1
            """
            
            _verify_int(maximum, 'Random', 1)
            return self.snake_interface.random(maximum)
        
        def close(self):
            """Closes the display and stops your program.
            """
            
            self.snake_interface.close()
        
        def stay_open(self):
            """Force the window to remain open.
            Only has effect on Mac OS to prevent the window from closing after the execution finishes.
            
            Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
            """
            
            pass
    
    class _Snake(object):
        #one cannot prevent users from editing 'constants', as constants simply do not exist in Python
        EMPTY = 0
        FOOD = 1
        SNAKE = 2
        WALL = 3
        
        def __init__(self, width, height, mainroot, scale=1.0):
            #create queue to store changes to placings
            self.to_show_queue = _Queue.Queue(maxsize=0)
            self.place_queue = _Queue.Queue(maxsize=0)
            self.event_queue = _Queue.Queue(maxsize=0)
            self.fps_queue = _Queue.Queue(maxsize=0)
            self.print_queue = _Queue.Queue(maxsize=0)
            
            #copy params
            self.width = width
            self.height = height
            self.scale = scale
            
            self.closing_window = False
            
            #start the main window
            self.root = _tk.Toplevel(mainroot)
            self.root.title("SnakeUserInterface")
            self.root.protocol("WM_DELETE_WINDOW", self.callback)
            self.root.bind("<Escape>", self.callback)
            self.root.resizable(False, False)
            
            #calculate sizes
            self.size_per_coord = int(25 * scale)
            self.text_height = int(200 * scale)
            
            #create main frame
            self.frame = _tk.Frame(self.root, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height+self.text_height)
            self.frame.pack_propagate(0)
            self.frame.pack()
            
            #create board to hold references to snake-pieces
            self.food_board = [] # for storing references to create_image
            self.snake_board = []
            self.wall_board = []
            self.food_ghost_board = []
            self.snake_ghost_board = []
            self.wall_ghost_board = []
            self.img_refs = [] # for storing references to images - order: food, snake, wall, food_t, snake_t, wall_t
            
            #create and fill the canvas --> paintable area
            self.c = _tk.Canvas(self.frame, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height, bd=0, highlightthickness=0)
            self.c.pack()
            self.last_x = -1 # used to generate mouseOver/Exit events
            self.last_y = -1 # used to generate mouseOver/Exit events
            self.fill_canvas()
            
            #create the textholder
            self.scrollbar = _tk.Scrollbar(self.frame)
            self.scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
            self.textarea = _tk.Text(self.frame, yscrollcommand=self.scrollbar.set)
            self.textarea.pack(side=_tk.LEFT, fill=_tk.BOTH)
            self.scrollbar.config(command=self.textarea.yview)
            self.textarea.config(state=_tk.DISABLED)
            
            self.auto_alarm_event = None
            self.auto_alarm_speed = None
            self.timer = self.milliseconds()
        
        def callback(self, event=None):
            self.root.destroy()
            _os._exit(0)
        
        def milliseconds(self):
            return _time.time() * 1000
        
        def place(self, x, y, color):
            element = _SnakeHolder(x, y, color)
            self.to_show_queue.put(element)
        
        def clear(self):
            for x in range(self.width):
                for y in range(self.height):
                    self.place(x, y, self.EMPTY)
        
        def show(self):
            try:
                while True:
                    element = self.to_show_queue.get_nowait()
                    self.place_queue.put(element)
            except _Queue.Empty:
                pass
        
        def get_event(self):
            return self.event_queue.get()
        
        def set_animation_speed(self, fps):
            self.fps_queue.put(fps)
        
        def update_config(self):
            if self.closing_window:
                self.root.destroy()
                _os._exit(0)
                return
            try:
                while True:
                    element = self.place_queue.get_nowait()
                    position = []
                    position.append(self.food_board[element.x][element.y])
                    position.append(self.snake_board[element.x][element.y])
                    position.append(self.wall_board[element.x][element.y])
                    position.append(self.food_ghost_board[element.x][element.y])
                    position.append(self.snake_ghost_board[element.x][element.y])
                    position.append(self.wall_ghost_board[element.x][element.y])
                    for i in range(len(position)):
                        # add 1 to i, because 0 is empty [same as doing color - 1]
                        # thus, if 0, then it doesn't match with 1 to 6
                        # therefore putting the whole position to hidden
                        if element.color == i+1:
                            self.c.itemconfig(position[i], state=_tk.NORMAL)
                        else:
                            self.c.itemconfig(position[i], state=_tk.HIDDEN)
            except _Queue.Empty:
                pass
            try:
                while True:
                    fps = self.fps_queue.get_nowait()
                    current_time = self.milliseconds()
                    if self.auto_alarm_event != None:
                        self.root.after_cancel(self.auto_alarm_event)
                        self.auto_alarm_event = None
                        self.auto_alarm_speed = None
                    if fps <= 0:
                        #self.timer = current_time
                        return
                    if fps > 1000:
                        fps = 1000
                    self.auto_alarm_speed = int(1000.0 / fps)
                    after_this_much = self.auto_alarm_speed - current_time + self.timer
                    if after_this_much < 0:
                        after_this_much = 0
                    self.auto_alarm_event = self.root.after(int(after_this_much), self.refresh_event)
                    
            except _Queue.Empty:
                pass
            try:
                while True:
                    element = self.print_queue.get_nowait()
                    self.textarea.config(state=_tk.NORMAL)
                    if element.clear_text:
                        self.textarea.delete(1.0, _tk.END)
                    else:
                        self.textarea.insert(_tk.END, element.text)
                    self.textarea.see(_tk.END)
                    self.textarea.config(state=_tk.DISABLED)
            except _Queue.Empty:
                pass
        
        def print_(self, text):
            element = _PrintQueueHolder(text, False)
            self.print_queue.put(element)
        
        def clear_text(self):
            element = _PrintQueueHolder('', True)
            self.print_queue.put(element)
        
        def wait(self, ms):
            _time.sleep(ms * 0.001)
        
        def close(self):
            self.closing_window = True
        
        def random(self, maximum=1):
            return int(_random.random() * maximum)
        
        def create_snake_pieces(self):
            boards = self.food_board, self.snake_board, self.wall_board, self.food_ghost_board, self.snake_ghost_board, self.wall_ghost_board
            for n in range(len(boards)):
                for i in range(self.width):
                    boards[n].append([])
                    for j in range(self.height):
                        x0 = self.size_per_coord * i
                        y0 = self.size_per_coord * j
                        img = self.c.create_image(x0, y0, anchor=_tk.NW, image=self.img_refs[n], state=_tk.HIDDEN)
                        boards[n][i].append(img)
        
        def create_images(self):
            relative_locations = "images/apple.png", "images/snake.png", "images/muur.png", "images/apple_t.png", "images/snake_t.png", "images/muur_t.png"
            locations = []
            for i in range(len(relative_locations)):
                locations.append(_os.path.join(_os.path.dirname(__file__), _os.path.normpath(relative_locations[i])))
            for i in locations:
                size = self.size_per_coord, self.size_per_coord
                img = _Image.open(i).resize(size, _Image.ANTIALIAS)
                ref = _ImageTk.PhotoImage(img)
                self.img_refs.append(ref)
        
        def create_background(self):
            location = "images/jungle.jpg"
            location = _os.path.join(_os.path.dirname(__file__), _os.path.normpath(location))
            size = int(self.c['width']), int(self.c['height'])
            img = _Image.open(location).resize(size, _Image.ANTIALIAS)
            ref = _ImageTk.PhotoImage(img)
            self.img_refs.append(ref)
            self.c.create_image(0, 0, anchor=_tk.NW, image=ref, state=_tk.NORMAL)
        
        def fill_canvas(self):
            self.bind_events()
            self.create_images()
            self.create_background()
            self.create_snake_pieces()
        
        def motion_event(self, event):
            if not self.mouse_on_screen:
                return
            x_old = self.last_x
            y_old = self.last_y
            x_new = event.x / self.size_per_coord
            y_new = event.y / self.size_per_coord
            x_change = int(x_old) != int(x_new)
            y_change = int(y_old) != int(y_new)
            if x_change or y_change:
                self.generate_event("mouseexit", "%d %d"%(x_old,y_old))
                self.generate_event("mouseover", "%d %d"%(x_new,y_new))
                self.last_x = x_new
                self.last_y = y_new
        
        def enter_window_event(self, event):
            x_new = event.x / self.size_per_coord
            y_new = event.y / self.size_per_coord
            self.generate_event("mouseover", "%d %d"%(x_new,y_new))
            self.last_x = x_new
            self.last_y = y_new
            self.mouse_on_screen = True
        
        def leave_window_event(self, event):
            self.generate_event("mouseexit", "%d %d"%(self.last_x,self.last_y))
            self.mouse_on_screen = False
        
        def alt_number_event(self, event):
            if event.char == event.keysym:
                if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
                    self.generate_event("alt_number", event.char)
        
        def key_event(self, event):
            if event.char == event.keysym:
                if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
                    self.generate_event("number", event.char)
                elif ord(event.char) >= ord('a') and ord(event.char) <= ord('z'):
                    self.generate_event("letter", event.char)
                elif ord(event.char) >= ord('A') and ord(event.char) <= ord('Z'):
                    self.generate_event("letter", event.char)
                else:
                    self.generate_event("other", event.char)
            elif event.keysym == 'Up':
                self.generate_event("arrow", "u")
            elif event.keysym == 'Down':
                self.generate_event("arrow", "d")
            elif event.keysym == 'Left':
                self.generate_event("arrow", "l")
            elif event.keysym == 'Right':
                self.generate_event("arrow", "r")
            elif event.keysym == 'Multi_Key':
                return
            elif event.keysym == 'Caps_Lock':
                self.generate_event("other", "caps lock")
            elif event.keysym == 'Num_Lock':
                self.generate_event("other", "num lock")
            elif event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
                self.generate_event("other", "shift")
            elif event.keysym == 'Control_L' or event.keysym == 'Control_R':
                self.generate_event("other", "control")
            elif event.keysym == 'Alt_L' or event.keysym == 'Alt_R':
                self.generate_event("other", "alt")
            else:
                self.generate_event("other", event.keysym)
        
        def click_event(self, event):
            x = event.x / self.size_per_coord
            y = event.y / self.size_per_coord
            self.generate_event("click", "%d %d"%(x,y))
        
        def refresh_event(self):
            self.generate_event("alarm", "refresh")
            self.timer = self.milliseconds()
            self.auto_alarm_event = self.root.after(self.auto_alarm_speed, self.refresh_event)
        
        def generate_event(self, name, data):
            event = Event(name, data)
            self.event_queue.put(event)
        
        def bind_events(self):
            self.c.focus_set() # to redirect keyboard input to this widget
            self.c.bind("<Motion>", self.motion_event)
            self.c.bind("<Enter>", self.enter_window_event)
            self.c.bind("<Leave>", self.leave_window_event)
            self.c.bind("<Alt-Key>", self.alt_number_event)
            self.c.bind("<Key>", self.key_event)
            self.c.bind("<Button-1>", self.click_event)
        
        def poll(self):
            self.update_config()
    
    class LifeUserInterface(object):
        def __init__(self, width, height, scale=1.0):
            """This class starts the LifeUserInterface.
            Constants:
            - DEAD
            - ALIVE
            
            Parameters for the class:
            - width: at least 1
            - height: at least 1
            
            Optional parameters:
            - scale: 0.25 to 1.0
            """
            
            if not have_pil:
                value = "Life: PIL wasn't found, can't use this interface right now."
                raise _IPyException(value)
            _verify_int(width, "Width", 1)
            _verify_int(height, "Height", 1)
            _verify_float(scale, 'Scale', 0.25, 1.0)
            is_added = False
            global _add_interface_queue
            global _set_interface_list
            _add_interface_queue.put([4, width, height, scale])
            while not is_added:
                try:
                    while True:
                        _set_interface_list.get_nowait()
                        is_added = True
                except _Queue.Empty:
                    pass
                _time.sleep(0.001)
            global _active_interface_list
            self.life_interface = _active_interface_list[-1]
            self.DEAD = _Life.DEAD
            self.ALIVE = _Life.ALIVE
        
        def place(self, x, y, color):
            """Place a Life piece (defined by 'color') on the given X and Y coordinates.
            """
            
            _verify_int(x, 'X', 0, self.life_interface.width - 1)
            _verify_int(y, 'Y', 0, self.life_interface.height - 1)
            # 0 = empty, 1 = dead, 2 = alive
            _verify_int(color, 'Color', 0, 2)
            self.life_interface.place(x, y, color)
        
        def clear(self):
            """Clears the display.
            Note: this does not clear the text area!
            """
            
            self.life_interface.clear()
        
        def show(self):
            """Show the changes made to the display (i.e. after calling place or clear)
            """
            
            self.life_interface.show()
        
        def get_event(self):
            """Returns an event generated from the display.
            The returned object has 2 properties:
            - name: holds the group which the event belongs to.
            - data: holds useful information for the user.
            """
            
            return self.life_interface.get_event()
        
        def set_animation_speed(self, fps):
            """Set an event to repeat 'fps' times per second.
            If the value is set to 0 or less, the repeating will halt.
            In theory the maximum value is 1000, but this depends on activity of the system.
            
            The generated events (available by using get_event) have these properties:
            - name: 'alarm'.
            - data: 'refresh'.
            """
            
            _verify_float(fps, "Animation speed")
            self.life_interface.set_animation_speed(fps)
        
        def print_(self, text):
            """Print text to the text area on the display.
            This function does not add a trailing newline by itself.
            """
            
            _verify_str(text, "Text")
            self.life_interface.print_(text)
        
        def clear_text(self):
            """Clears the text area on the display.
            """
            
            self.life_interface.clear_text()
        
        def wait(self, ms):
            """Let your program wait for an amount of milliseconds.
            
            This function only guarantees that it will wait at least this amount of time.
            If the system, i.e., is too busy, then this time might increase.
            - Python time module.
            """
            
            _verify_int(ms, "Waiting time", 0)
            self.life_interface.wait(ms)
        
        def random(self, maximum):
            """Picks a random integer ranging from 0 <= x < maximum
            Minimum for maximum is 1
            """
            
            _verify_int(maximum, 'Random', 1)
            return self.life_interface.random(maximum)
        
        def close(self):
            """Closes the display and stops your program.
            """
            
            self.life_interface.close()
        
        def stay_open(self):
            """Force the window to remain open.
            Only has effect on Mac OS to prevent the window from closing after the execution finishes.
            
            Make sure that this is the last statement you call when including it because the code does NOT continue after this. 
            """
            
            pass
    
    class _Life(object):
        #one cannot prevent users from editing 'constants', as constants simply do not exist in Python
        DEAD = 0
        ALIVE = 1
        
        BACKGROUND = "#000000"
        
        def __init__(self, width, height, mainroot, scale=1.0):
            #create queue to store changes to placings
            self.to_show_queue = _Queue.Queue(maxsize=0)
            self.place_queue = _Queue.Queue(maxsize=0)
            self.event_queue = _Queue.Queue(maxsize=0)
            self.fps_queue = _Queue.Queue(maxsize=0)
            self.print_queue = _Queue.Queue(maxsize=0)
            
            #copy params
            self.width = width
            self.height = height
            self.scale = scale
            
            self.closing_window = False
            
            #start the main window
            self.root = _tk.Toplevel(mainroot)
            self.root.title("SnakeUserInterface")
            self.root.protocol("WM_DELETE_WINDOW", self.callback)
            self.root.bind("<Escape>", self.callback)
            self.root.resizable(False, False)
            
            #calculate sizes
            self.size_per_coord = int(25 * scale)
            self.text_height = int(200 * scale)
            
            #create main frame
            self.frame = _tk.Frame(self.root, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height+self.text_height)
            self.frame.pack_propagate(0)
            self.frame.pack()
            
            #create board to hold references to snake-pieces
            self.dead_board = [] # for storing references to create_image
            self.alive_board = []
            self.img_refs = [] # for storing references to images - order: dead, alive
            
            #create and fill the canvas --> paintable area
            self.c = _tk.Canvas(self.frame, width=self.size_per_coord*self.width, height=self.size_per_coord*self.height, bg=self.BACKGROUND, bd=0, highlightthickness=0)
            self.c.pack()
            self.last_x = -1 # used to generate mouseOver/Exit events
            self.last_y = -1 # used to generate mouseOver/Exit events
            self.fill_canvas()
            
            #create the textholder
            self.scrollbar = _tk.Scrollbar(self.frame)
            self.scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
            self.textarea = _tk.Text(self.frame, yscrollcommand=self.scrollbar.set)
            self.textarea.pack(side=_tk.LEFT, fill=_tk.BOTH)
            self.scrollbar.config(command=self.textarea.yview)
            self.textarea.config(state=_tk.DISABLED)
            
            self.auto_alarm_event = None
        
        def callback(self, event=None):
            self.root.destroy()
            _os._exit(0)
        
        def place(self, x, y, color):
            element = _LifeHolder(x, y, color)
            self.to_show_queue.put(element)
        
        def clear(self):
            for x in range(self.width):
                for y in range(self.height):
                    self.place(x, y, self.DEAD)
        
        def show(self):
            try:
                while True:
                    element = self.to_show_queue.get_nowait()
                    self.place_queue.put(element)
            except _Queue.Empty:
                pass
        
        def get_event(self):
            return self.event_queue.get()
        
        def set_animation_speed(self, fps):
            self.fps_queue.put(fps)
        
        def update_config(self):
            if self.closing_window:
                self.root.destroy()
                _os._exit(0)
                return
            try:
                while True:
                    element = self.place_queue.get_nowait()
                    position = []
                    position.append(self.dead_board[element.x][element.y])
                    position.append(self.alive_board[element.x][element.y])
                    for i in range(len(position)):
                        if element.color == i:
                            self.c.itemconfig(position[i], state=_tk.NORMAL)
                        else:
                            self.c.itemconfig(position[i], state=_tk.HIDDEN)
            except _Queue.Empty:
                pass
            try:
                while True:
                    fps = self.fps_queue.get_nowait()
                    if self.auto_alarm_event != None:
                        self.root.after_cancel(self.auto_alarm_event)
                    if fps <= 0:
                        self.root.after_cancel(self.auto_alarm_event)
                        return
                    if fps > 1000:
                        fps = 1000
                    timeframe = int(1000.0 / fps)
                    self.auto_alarm_event = self.root.after(timeframe, self.refresh_event, timeframe)
            except _Queue.Empty:
                pass
            try:
                while True:
                    element = self.print_queue.get_nowait()
                    self.textarea.config(state=_tk.NORMAL)
                    if element.clear_text:
                        self.textarea.delete(1.0, _tk.END)
                    else:
                        self.textarea.insert(_tk.END, element.text)
                    self.textarea.see(_tk.END)
                    self.textarea.config(state=_tk.DISABLED)
            except _Queue.Empty:
                pass
        
        def print_(self, text):
            element = _PrintQueueHolder(text, False)
            self.print_queue.put(element)
        
        def clear_text(self):
            element = _PrintQueueHolder('', True)
            self.print_queue.put(element)
        
        def wait(self, ms):
            _time.sleep(ms * 0.001)
        
        def close(self):
            self.closing_window = True
        
        def random(self, maximum=1):
            return int(_random.random() * maximum)
        
        def create_life_pieces(self):
            boards = self.dead_board, self.alive_board
            for n in range(len(boards)):
                for i in range(self.width):
                    boards[n].append([])
                    for j in range(self.height):
                        x0 = self.size_per_coord * i
                        y0 = self.size_per_coord * j
                        state_ = _tk.HIDDEN
                        if n == 0:
                            state_ = _tk.NORMAL
                        img = self.c.create_image(x0, y0, anchor=_tk.NW, image=self.img_refs[n], state=state_)
                        boards[n][i].append(img)
        
        def create_images(self):
            relative_locations = "images/dead.png", "images/alive.png"
            locations = []
            for i in range(len(relative_locations)):
                locations.append(_os.path.join(_os.path.dirname(__file__), _os.path.normpath(relative_locations[i])))
            for i in locations:
                size = self.size_per_coord, self.size_per_coord
                img = _Image.open(i).resize(size, _Image.ANTIALIAS)
                ref = _ImageTk.PhotoImage(img)
                self.img_refs.append(ref)
        
        def fill_canvas(self):
            self.bind_events()
            self.create_images()
            self.create_life_pieces()
        
        def motion_event(self, event):
            if not self.mouse_on_screen:
                return
            x_old = self.last_x
            y_old = self.last_y
            x_new = event.x / self.size_per_coord
            y_new = event.y / self.size_per_coord
            x_change = int(x_old) != int(x_new)
            y_change = int(y_old) != int(y_new)
            if x_change or y_change:
                self.generate_event("mouseexit", "%d %d"%(x_old,y_old))
                self.generate_event("mouseover", "%d %d"%(x_new,y_new))
                self.last_x = x_new
                self.last_y = y_new
        
        def enter_window_event(self, event):
            x_new = event.x / self.size_per_coord
            y_new = event.y / self.size_per_coord
            self.generate_event("mouseover", "%d %d"%(x_new,y_new))
            self.last_x = x_new
            self.last_y = y_new
            self.mouse_on_screen = True
        
        def leave_window_event(self, event):
            self.generate_event("mouseexit", "%d %d"%(self.last_x,self.last_y))
            self.mouse_on_screen = False
        
        def alt_number_event(self, event):
            if event.char == event.keysym:
                if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
                    self.generate_event("alt_number", event.char)
        
        def key_event(self, event):
            if event.char == event.keysym:
                if ord(event.char) >= ord('0') and ord(event.char) <= ord('9'):
                    self.generate_event("number", event.char)
                elif ord(event.char) >= ord('a') and ord(event.char) <= ord('z'):
                    self.generate_event("letter", event.char)
                elif ord(event.char) >= ord('A') and ord(event.char) <= ord('Z'):
                    self.generate_event("letter", event.char)
                else:
                    self.generate_event("other", event.char)
            elif event.keysym == 'Up':
                self.generate_event("arrow", "u")
            elif event.keysym == 'Down':
                self.generate_event("arrow", "d")
            elif event.keysym == 'Left':
                self.generate_event("arrow", "l")
            elif event.keysym == 'Right':
                self.generate_event("arrow", "r")
            elif event.keysym == 'Multi_Key':
                return
            elif event.keysym == 'Caps_Lock':
                self.generate_event("other", "caps lock")
            elif event.keysym == 'Num_Lock':
                self.generate_event("other", "num lock")
            elif event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
                self.generate_event("other", "shift")
            elif event.keysym == 'Control_L' or event.keysym == 'Control_R':
                self.generate_event("other", "control")
            elif event.keysym == 'Alt_L' or event.keysym == 'Alt_R':
                self.generate_event("other", "alt")
            else:
                self.generate_event("other", event.keysym)
        
        def click_event(self, event):
            x = event.x / self.size_per_coord
            y = event.y / self.size_per_coord
            self.generate_event("click", "%d %d"%(x,y))
        
        def refresh_event(self, timeframe):
            self.generate_event("alarm", "refresh")
            self.auto_alarm_event = self.root.after(timeframe, self.refresh_event, timeframe)
        
        def generate_event(self, name, data):
            event = Event(name, data)
            self.event_queue.put(event)
        
        def bind_events(self):
            self.c.focus_set() # to redirect keyboard input to this widget
            self.c.bind("<Motion>", self.motion_event)
            self.c.bind("<Enter>", self.enter_window_event)
            self.c.bind("<Leave>", self.leave_window_event)
            self.c.bind("<Alt-Key>", self.alt_number_event)
            self.c.bind("<Key>", self.key_event)
            self.c.bind("<Button-1>", self.click_event)
        
        def poll(self):
            self.update_config()
    
    class Event(object):
        def __init__(self, name, data):
            """This class holds the name and data for each event in their respective variables.
            Variables:
            - name
            - data
            
            Example to access with SnakeUserInterface:
            
            ui = SnakeUserInterface(5,5) # 5 by 5 grid for testing purposes
            your_variable = ui.get_event() # code will block untill an event comes
            # your_variable now points to an event
            print your_variable.name, your_variable.data
            
            List of events:
            - name: mouseover
              data: x and y coordinates (as integers), separated by a space
                  generated when mouse goes over a coordinate on the window
            - name: mouseexit
              data: x and y coordinates (as integers), separated by a space
                  generated when mouse exits a coordinate on the window
            - name: click
              data: x and y coordinates (as integers), separated by a space
                  generated when the user clicks on a coordinate on the window
            - name: alarm
              data: refresh
                  generated as often per second as the user set the animation speed to; note that the data is exactly as it says: "refresh"
            - name: letter
              data: the letter that got pressed
                  generated when the user presses on a letter (A to Z; can be lowercase or uppercase depending on shift/caps lock)
            - name: number
              data: the number (as a string) that got pressed
                  generated when the user presses on a number (0 to 9)
            - name: alt_number
              data: the number (as a string) that got pressed
                  generated when the user presses on a number (0 to 9) while at the same time pressing the Alt key
            - name: arrow
              data: the arrow key that got pressed, given by a single letter
                  generated when the user presses on an arrow key, data is then one of: l, r, u, d
            - name: other
              data: data depends on key pressed
                  generated when the user pressed a different key than those described above
                  possible data:
                  - caps_lock
                  - num_lock
                  - alt
                  - control
                  - shift
                  more data can exist and are recorded (read: they generate events), but not documented
            """
            self.name = name
            self.data = data
    
    _Factory()
