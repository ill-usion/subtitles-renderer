import pysrt
import threading
from time import sleep
from ctypes import windll
from tkinter import Tk
from tkhtmlview import HTMLLabel
from htmlBuilder.tags import P
from htmlBuilder.attributes import Style


should_quit = False


def play_subtitles(label: HTMLLabel):
    subtitles = pysrt.open("subtitles.srt")
    style = Style(
        color="white", text_align="center", font_size="25px", font_family="Helvetica"
    )

    for line in subtitles:
        if should_quit:
            break
        
        html = P((style,), line.text.replace('\n', '<br>'))

        label.set_html(html.render())
        sleep(line.duration.seconds)


windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x80+0+{int(screen_height - (screen_height * 0.12))}")
root.wm_attributes("-topmost", 1)
root.wm_attributes("-transparentcolor", "grey")
root.attributes("-alpha", 0.7)
root.config(bg="grey")
root.bind("<Escape>", lambda e: root.destroy())

label = HTMLLabel(root, background="black", borderwidth=0)
label.pack()

t = threading.Thread(target=play_subtitles, args=(label,))
t.start()

root.overrideredirect(True)
root.mainloop()

should_quit = True
t.join()
