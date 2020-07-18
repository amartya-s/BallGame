import tkinter as tk

from BallGame.services.service import GameService


class GameCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, kwargs)
        self.parent = parent
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        wscale = event.width / self.width
        hscale = event.height / self.height

        self.width = event.width
        self.height = event.height

        self.config(width=self.width, height=self.height)
        self.scale("all", 0, 0, wscale, hscale)


class Game(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.service = None

        self.setup_window()
        self.setup_widgets()

    def setup_window(self):
        master_window_width = 1100
        print(master_window_width)
        control_window = tk.Frame(self.master, bg='pink', width=master_window_width / 4)
        control_window.pack(side=tk.LEFT, fill=tk.BOTH)
        self.control_window = control_window

        game_window = tk.Frame(self.master, bg='green', width=(3 / 4) * master_window_width)
        game_window.pack(side=tk.RIGHT, fill=tk.BOTH)

        game_canvas = GameCanvas(game_window, bg='black', width=(3 / 4) * master_window_width)
        game_canvas.pack(expand=True, fill=tk.BOTH)
        self.game_canvas = game_canvas

    def setup_widgets(self):
        dummy_frame = tk.Frame(self.control_window, height=200, width=0, bg='pink').pack()

        var = tk.StringVar()
        var.set("0")

        text = tk.Entry(self.control_window, bg='rosybrown1', fg='green',
                        font="Times 20 bold", borderwidth=4, relief="groove", justify="center", width=10)
        text['textvariable'] = var
        text.pack()
        text = tk.Label(self.control_window, bg='rosybrown1', fg='black',
                        font="Times 20 bold", borderwidth=4, justify="center", width=10, text='Score')
        text.pack()

        self.score_var = var

        play_bt = tk.Button(self.control_window, text='Play', command=self.play, width=20, height=2)
        play_bt.pack(pady=100)

        status_label = tk.Label(self.control_window, width=30, height=5, bg='pink')
        status_label.pack()
        self.status_label = status_label

    def play(self):
        self.game_canvas.delete("all")
        self.service = GameService(self, self.score_var)
        self.service.initialize()
        self.service.start_game()


if __name__ == '__main__':
    root = tk.Tk()

    app = Game(master=root)

    app.master.title("BallGame")
    app.master.geometry("1100x900")

    app.mainloop()
