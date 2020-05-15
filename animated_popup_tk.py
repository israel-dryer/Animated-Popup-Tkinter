"""
    Animated Popup Demonstration
    Author: Israel Dryer
    Modified: 2020-05-14
    Font: https://www.1001fonts.com/accuratist-font.html
    Elixer Recipe: https://www.ancient-origins.net/news-history-archaeology/archaeologists-recreate-elixir-long-life-recipe-unearthed-bottle-001772
"""
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

STEPS = (
    "mixing in zedoary…", "breaking off a scrape of Peruvian bark…",
    "Bringing to a gentle boil…", "Cooling mixture…")

class Mixer:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Formula Loader")
        self.root.configure(background='#191f26')
        self.root.iconbitmap('physics.ico')

        # main window objects
        self.title = tk.Label(self.root, text="Click to Mix", anchor=tk.CENTER,
            font=('Accuratist', 40), background='#191F26', foreground='#E4E4E4')
        self.tech_img = ImageTk.PhotoImage(file='tech_button.png')
        self.tech_btn = tk.Button(self.root, image=self.tech_img, background='#191F26',
            relief=tk.FLAT, activebackground='#191F26', borderwidth=0, command=self.loading_popup)

        # arrange main window objects
        self.title.pack(side=tk.TOP, pady=(15, 0), fill=tk.X, expand=tk.YES)
        self.tech_btn.pack()
        self.root.eval('tk::PlaceWindow . center')

        # setup animated popup
        self.popup = None
        self.popup_img = None
        self.status_lbl = None
        self.mixing = False
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open('loading.gif'))]
        self.frame_duration = Image.open('loading.gif').info['duration']
        self.index = 0
        self.status_var = tk.StringVar()
        self.status_var.set(STEPS[0])

        # keep track of mix steps
        self.mix_step = 0

    def mix_formula(self):
        """Simulate a process"""
        try:
            self.status_var.set(STEPS[self.mix_step])
            self.mix_step += 1
            # schedule mix formula is steps still exist
            self.root.after(3000, self.mix_formula)
        except IndexError:
            # mix formula is done
            self.mix_step = 0
            self.mixing = False

    def loading_popup(self):
        """Open animated popup"""
        # minimize the main window
        self.root.iconify()

        # create popup window
        self.popup = tk.Toplevel(self.root)
        xpos = (self.root.winfo_screenwidth() - 300)//2
        ypos = (self.root.winfo_screenheight() - 300)//2
        self.popup.geometry(f'300x300+{xpos}+{ypos}')
        self.popup.overrideredirect(True) # make frameless window

        # create objects
        self.status_lbl = tk.Label(
            self.popup, textvariable=self.status_var, background='#191F26',
            foreground='#E4E4E4', font=('Century Gothic', 10, 'italic'), anchor=tk.CENTER)
        self.popup_img = tk.Label(self.popup, image=self.sequence[self.index])

        # arrange objects
        self.status_lbl.pack(side=tk.TOP, fill=tk.X, ipady=15, expand=tk.YES)
        self.popup_img.pack(side=tk.TOP)
        self.mixing = True
        self.mix_formula()
        self.root.after(self.frame_duration, self.animate_popup)

    def animate_popup(self):
        """Animate the loading popup"""
        if not self.mixing:
            self.popup.destroy()
            self.root.deiconify() # show the main window again
        else:
            if self.index == len(self.sequence):
                self.index = 0
            # change to next frame
            self.popup_img.configure(image=self.sequence[self.index])
            self.index += 1
            # schedule next frame change
            self.root.after(self.frame_duration, self.animate_popup)

if __name__ == '__main__':

    mixer = Mixer()
    mixer.root.mainloop()
