import tkinter as tk
from tkinter import ttk
import logging

from .ui_command import BlackCommand
from .ui_command import WhiteCommand
from .ui_command import AlternateCommand
from .ui_command import ResetCommand
# from .ui_command import LoadCommand


class SideMenu(ttk.Frame):
    """Represents the app's side menu, acts as an UI commands invoker and client"""

    def __init__(self, master):
        self.master = master

        super().__init__(master, width=100, height=400)
        self.grid(column=1, row=0, sticky=(tk.W, tk.E))

        # active button should be highlighted
        active_style = ttk.Style()
        active_style.configure(
            "Active.TButton", borderwidth="2", font=("calibri", 10, "bold")
        )
        self._active_button = None

        # stylize the default ttk Button
        default_style = ttk.Style()
        default_style.configure("TButton", focuscolor="none")

        # self.create_button("Save", save, column=0, row=0, sticky=tk.W)
        # self.create_button(
        #     "Load", LoadCommand(self.master, "game.sgf").execute, column=1, row=0, sticky=tk.E
        # )
        self._selected_value = tk.StringVar()
        self._dropdown = ttk.Combobox(self, textvariable=self._selected_value, state="readonly")
        self._dropdown["values"] = ("19", "13", "9")
        self._dropdown.set("Board size")     
        self._dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_change) 
        self._dropdown.grid(column=1, row=0, sticky=tk.W, pady=50)

        self.create_button(
            "Black",
            BlackCommand(self.master).execute,
            column=0,
            row=1,
            sticky=tk.W,
        )
        self.create_button(
            "White",
            WhiteCommand(self.master).execute,
            column=1,
            row=1,
            sticky=None,
        )
        self._alternate_btn = self.create_button(
            "Alternate",
            AlternateCommand(self.master).execute,
            column=2,
            row=1,
            sticky=tk.E,
        )
        self.set_active(self.alternate_btn)

        self.create_button(
            "Undo", self.master.undo_command, column=0, row=2, sticky=tk.W
        )
        self.create_button(
            "Reset", ResetCommand(self.master).execute, column=1, row=2, sticky=None
        )

    def set_active(self, button):
        if self._active_button is not None:
            self._active_button["style"] = "TButton"
        button["style"] = "Active.TButton"
        self._active_button = button

    def create_button(self, text, command, column, row, sticky):
        def button_click_handler():
            if row == 1:
                self.set_active(button)
            command()

        button = ttk.Button(self, text=text, command=button_click_handler)
        button.grid(column=column, row=row, sticky=sticky, padx=(10, 10), pady=50)

        return button
    
    def on_dropdown_change(self, event):
        self._dropdown.selection_clear()

        selected = self._selected_value.get()
        
        logging.debug(event)
        self.master.reset_board(int(selected))

    @property
    def alternate_btn(self):
        return self._alternate_btn
