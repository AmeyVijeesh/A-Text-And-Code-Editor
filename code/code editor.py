from tkinter import *
from tkinter.filedialog import asksaveasfile
import tkinter.messagebox
import os
import time
from datetime import date
from text_editor import text_editor


def code_editor():
    root = Tk()
    root.title("Editor")
    root.geometry('853x453')
    root.resizable(False, False)

    def screen_menu():
        menu = Menu(root)
        root.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label="New", command=new)
        file_menu.add_command(label='Save', command=save)
        file_menu.add_command(label='Save As', command=save_as)
        file_menu.add_command(label='Exit', command=app_quit)

        edit_menu = Menu(menu)
        menu.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Select All', command=select_All)
        edit_menu.add_command(label='Cut', command=cut)
        edit_menu.add_command(label='Copy', command=copy)
        edit_menu.add_command(label='Paste', command=paste)
        edit_menu.add_command(label='Undo', command=undo)
        edit_menu.add_command(label='Redo', command=redo)
        edit_menu.add_command(label='Find', command=find)
        edit_menu.add_separator()

        edit_menu.add_command(label='Insert Date', command=insert_date)
        edit_menu.add_command(label='Insert Time', command=insert_time)
        edit_menu.add_command(label='Insert Date and time', command=insert_date_time)

        theme_menu = Menu(menu)
        menu.add_cascade(label='Themes', menu=theme_menu)
        theme_menu.add_command(label='Default theme', command=default_theme)
        theme_menu.add_command(label='Dark mode', command=dark_theme)
        theme_menu.add_command(label='Light mode', command=light_mode)

        help_menu = Menu(menu)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=about)
        help_menu.add_command(label="Help", command=editor_help)

    def write_to_file(name_of_file):
        try:
            content = text.get(1.0, 'end')
            with open(name_of_file, 'w') as the_file:
                the_file.write(content)
        except IOError:
            pass

    def save_as():
        global filename

        input_file_name = asksaveasfile(
            defaultextension=".txt",
            filetypes=[("All files", "*.*"),
                       ("Text Documents", "*.txt"),
                       ("Python Files", "*.py"),
                       ("Javascript Files", "*.js"),
                       ("PHP files", ".php"),
                       ("C#", "*.cs")]
        )

        if input_file_name:
            filename = input_file_name
            write_to_file(filename)
            root.title("{} - {}").format(os.path.basename(filename), "ATS Office")
            return 'break'

    def text_edit():
        root.destroy()
        text_editor()

    def find():
        search_window = Toplevel(root)
        search_window.title('Find Text')
        search_window.transient(root)
        search_window.resizable(False, False)
        search_window.config(bg='white')

        Label(search_window, text="Find All:", bg='white', fg='red').grid(row=0, column=0, sticky='e')
        search_entry_widget = Entry(search_window, width=25)
        search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
        search_entry_widget.focus_set()
        ignore_case_value = IntVar()
        Checkbutton(search_window, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e',
                                                                                        padx=2, pady=2)
        Button(search_window, text="Find All", underline=0, relief=FLAT,
               command=lambda: search_output(
                   search_entry_widget.get(), ignore_case_value.get(),
                   text, search_window, search_entry_widget)
               ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

        def close_search_window():
            text.tag_remove('match', '1.0', END)
            search_window.destroy()

        search_window.protocol('WM_DELETE_WINDOW', close_search_window)
        return "break"

    def search_output(needle, if_ignore_case, content_text, search_top_level, search_box):
        content_text.tag_remove('match', '1.0', END)
        matches_found = 0
        if needle:
            start_pos = '1.0'
            while True:
                start_pos = content_text.search(needle, start_pos, nocase=if_ignore_case, stopindex=END)
                if not start_pos:
                    break

                end_pos = '{} + {}c'.format(start_pos, len(needle))
                content_text.tag_add('match', start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos
            content_text.tag_config('match', background='yellow', foreground='blue')
        search_box.focus_set()
        search_top_level.title('{} matches found'.format(matches_found))

    def new():
        save_dialog = tkinter.messagebox.askokcancel(
            "Are you sure?",
            "Do you want to save this file before creating a new one?",
            icon='warning'
        )

        if save_dialog:
            save_as()

        global filename
        file_name = None
        text.delete("1.0", END)
        on_content_changed()

    file_name = None

    def save():
        global filename
        if not file_name:
            save_as()

        else:
            write_to_file(file_name)

        return 'break'

    def app_quit():
        message_box = tkinter.messagebox.askokcancel(
            "Quit?",
            "Do you want to exit ATS Editor?",
            icon="question"
        )

        if message_box:
            root.quit()

    filename = None

    def get_line_numbers():
        output = ''
        if show_line_number.get():
            row, col = text.index("end").split('.')
            for i in range(1, int(row)):
                output += str(i) + '\n'
        return output

    def on_content_changed(event=None):
        update_line_numbers()

    def update_line_numbers(event=None):
        line_numbers = get_line_numbers()
        line_number_bar.config(state='normal')
        line_number_bar.delete('1.0', 'end')
        line_number_bar.insert('1.0', line_numbers)
        line_number_bar.config(state='disabled')

    def select_All():
        text.tag_add(SEL, "1.0", END)
        text.mark_set(INSERT, "1.0")
        text.see(INSERT)
        return 'break'

    def dark_theme():
        text.config(background='#303132', fg='white')
        shortcut_bar.config(bg='#4D4747')
        line_number_bar.config(bg='#282828', fg='white')
        select_all_button.config(bg='black', fg='white')
        cut_button.config(bg='black', fg='white')
        copy_button.config(bg='black', fg='white')
        paste_button.config(bg='black', fg='white')
        clear_button.config(bg='black', fg='white')
        undo_button.config(bg='black', fg='white')
        redo_button.config(bg='black', fg='white')

    def default_theme():
        text.config(background='white', fg='black')
        shortcut_bar.config(bg='white')
        line_number_bar.config(bg='#282828', fg='white')
        select_all_button.config(bg='#282828', fg='white')
        cut_button.config(bg='#282828', fg='white')
        copy_button.config(bg='#282828', fg='white')
        paste_button.config(bg='#282828', fg='white')
        clear_button.config(bg='#282828', fg='white')
        undo_button.config(bg="#282828", fg='white')
        redo_button.config(bg='#282828', fg='white')

    def light_mode():
        text.config(bg='white', fg='black')
        shortcut_bar.config(bg='white')
        line_number_bar.config(bg='white', fg='black')
        select_all_button.config(fg='#282828', bg='white')
        cut_button.config(fg='#282828', bg='white')
        copy_button.config(fg='#282828', bg='white')
        paste_button.config(fg='#282828', bg='white')
        clear_button.config(fg='#282828', bg='white')
        undo_button.config(fg="#282828", bg='white')
        redo_button.config(fg='#282828', bg='white')

    def about():
        tkinter.messagebox.showinfo("About ATS Office: ",
                                    "ATS Office is Made by Amey V, a programmer")

    def editor_help():
        tkinter.messagebox.showinfo("ATS Help",
                                    """
                                    \nBeautiful interface!\n
                                    \nYou can save your work, so you can view it any time\n
                                    \nFeatures like find, line number display, etc.\n
                                    \nMany more features!
                                   """)

    def insert_date():
        today = date.today().strftime("%A, %d.%B %Y")
        text.insert("1.0", today)

    def insert_time():
        today = time.strftime("%H:%M Uhr ")
        text.insert("1.0", today)

    def insert_date_time():
        insert_date()
        insert_time()

    def undo():
        try:
            text.edit_undo()

        except TclError:
            tkinter.messagebox.showerror(
                "Nothing to Undo!",
                "You have not entered any text to undo!",
                icon="error"
            )

    def redo():
        try:
            text.edit_redo()

        except TclError:
            tkinter.messagebox.showerror(
                "Nothing to Redo!",
                "You have not done an Undo! Please do an undo and try again.",
                icon='error'
            )

    def copy():
        text.event_generate("<<Copy>>")

    def paste():
        text.event_generate("<<Paste>>")

    def cut():
        text.event_generate("<<Cut>>")

    def clear():
        text.delete("1.0", 'end')

    shortcut_bar = Frame(root, height=35, bg="white")
    shortcut_bar.pack(expand='no', fill='x')

    select_all_button = Button(shortcut_bar, text="Select All", relief=FLAT, bg='#282828', fg='white',
                               command=select_All)
    select_all_button.place(x=10, y=6)

    cut_button = Button(shortcut_bar, text='Cut', relief=FLAT, bg='#282828', fg='white', width=6, command=cut)
    cut_button.place(x=80, y=6)

    copy_button = Button(shortcut_bar, text='Copy', relief=FLAT, bg='#282828', fg='white', width=6, command=copy)
    copy_button.place(x=145, y=6)

    paste_button = Button(shortcut_bar, text='Paste', relief=FLAT, bg='#282828', fg='white', width=6, command=paste)
    paste_button.place(x=210, y=6)

    clear_button = Button(shortcut_bar, text='Clear', relief=FLAT, bg='#282828', fg='white', width=6, command=clear)
    clear_button.place(x=275, y=6)

    undo_button = Button(shortcut_bar, text='Undo', relief=FLAT, bg='#282828', fg='white', width=6, command=undo)
    undo_button.place(x=340, y=6)

    redo_button = Button(shortcut_bar, text='Redo', relief=FLAT, bg='#282828', fg='white', width=6, command=redo)
    redo_button.place(x=405, y=6)

    text_edit_button = Button(shortcut_bar, text='Open ATS Office', bg='#282828', fg='white', command=text_edit)
    text_edit_button.place(x=750, y=6)

    show_line_number = IntVar()
    show_line_number.set(1)
    show_cursor_info = IntVar()
    show_cursor_info.set(1)

    line_number_bar = Text(root, width=4, padx=3, takefocus=0, fg='white', border=0, background='#282828',
                           state='disabled',
                           wrap='none')
    line_number_bar.pack(side='left', fill='y')

    text = Text(root, wrap='word', undo=True, font="Courier")
    text.pack(expand='yes', fill='both')

    scroll_bar = Scrollbar(text)
    text.configure(yscrollcommand=scroll_bar.set)
    scroll_bar.config(command=text.yview)
    scroll_bar.pack(side='right', fill='y')

    text.insert("1.0", '# -- coding: utf-8 --\n')

    on_content_changed()

    text.bind('<Any-KeyPress>', on_content_changed)
    text.tag_configure('active_line', background='black')
    text.focus_set()

    screen_menu()
    root.protocol('WM_DELETE_WINDOW', app_quit)
    root.mainloop()
