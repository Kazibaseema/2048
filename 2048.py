import tkinter as tk
from tkinter import *
import colors as c #colors.py hold color palatte and font selection
import random
from PIL import Image, ImageTk  # for jpg support
import subprocess


# 1]__INITIAL SETUP:  
class Game(tk.Frame):
    def __init__(self):
        self.ws = Tk()
        Frame.__init__(self, self.ws)
        self.grid()

        self.ws.title("2048")
        self.ws.state('zoomed')  # ✅ Start maximized on Windows

        # Get screen width and height
        screen_width = self.ws.winfo_screenwidth()
        screen_height = self.ws.winfo_screenheight()

        # Load and resize background image to screen size
        bg_image = Image.open("play.jpg").resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Set background image
        bg_label = tk.Label(self.ws, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Set icon
        icon_img = Image.open("icon.jpg")
        icon_photo = ImageTk.PhotoImage(icon_img)
        self.ws.iconphoto(False, icon_photo)

        
        

        # Main grid centered
        self.main_grid = Frame(self.ws, bg="#654321", width=600, height=600)##C19A6B #333333

        self.main_grid.place(relx=0.5, rely=0.5, anchor="center")

        self.make_GUI()
        self.start_game()

        # Bindings
        self.ws.bind("<Configure>", self.resize_bg)
        self.ws.bind("<Left>", self.left)
        self.ws.bind("<Right>", self.right)
        self.ws.bind("<Up>", self.up)
        self.ws.bind("<Down>", self.down)

        self.ws.mainloop()

    def resize_bg(self, event):
        # ✅ Resize the background to match window size
        resized = self.original_bg.resize((event.width, event.height), Image.ANTIALIAS)
        self.bg_photo = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.bg_photo)
        self.bg_label.image = self.bg_photo
        # Recenter grid
        self.main_grid.place(relx=0.5, rely=0.5, anchor="center")





    def make_GUI(self):
        #make a grid :cells contains information of grid
        self.cells = []
        for i in range(4):
            row= []
            for j in range(4):
                cell_frame =tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=150,
                    height=150

                )
                #for each cell there is...
                cell_frame.grid(row=i,column=j,padx=5,pady=5)#here padding allows for the grid lines to appear bet.cells
                cell_number =tk.Label(self.main_grid,bg=c.EMPTY_CELL_COLOR)#label will display each cells no. value
                cell_number.grid(row=i,column=j)
                cell_data={"frame":cell_frame,"number":cell_number}#dict of a cell
                row.append(cell_data)
            self.cells.append(row)

        #make a score header
        score_frame =tk.Frame(self)
        score_frame.place(relx=0.5,y=45,anchor="center")
        tk.Label(
            score_frame,
            text="score",
            font=c.SCORE_LABEL_FONT

        ).grid(row=0)
        self.score_label =tk.Label(score_frame,text="0",font=c.SCORE_FONT)
        self.score_label.grid(row=1)

#GAME()

    def start_game(self):

        #create matrix of zeroes
        self.matrix =[[0]*4 for _ in range(4)]

        #fill 2 random cells with 2s
        row = random.randint(0,3)
        col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2"
        
        )
        while(self.matrix[row][col] !=0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2"
        
        )
        # TO KEEP TRACK OF THE PLAYERS WE'LL CREATE A VARIABLE
        self.score = 0

    # 2]__MATRIX MANIPULATION FUNCTION:
    #there are 4 fun. that will manipulate our 4x4 matrix we created in start game.
    #& there'll be called  diffrent combinations and sequences based on the move by player,    
    #each fun will use a nested for loop to change the values and/or  positions of the values in the matrix.

    #stack fun:will compress all nonzero numbers in the matrix towards one side of the board & eliminating all the gaps of empty cells bet. them
    def stack(self):
        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            fill_position =0
            for j in range(4):
                if self.matrix[i][j] !=0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position +=1
        self.matrix = new_matrix

    #comb fun:adds together all horizontally adjacent non zero numbers of the same value in the matrix and merges them to the left position
    #GUI says this is the step when 2 tiles of the same value merge together and collapse in one tile of their sum e.g. 4+4=8
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] !=0 and self.matrix[i][j] == self.matrix[i][j+1]: #in this conditional exp,2 adjacent tiles  are having same value
                     self.matrix[i][j] *= 2 #multiplying value by 2
                     self.matrix[i][j+1] =0
                     self.score += self.matrix[i][j]

    #reverse fun:will reverse the order of each row on the matrix
    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([]) 
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix

    #trans fun:will flip the matrix over its diagonal
    def transpose(self):
        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    # add_new_tile:Add a new 2 or 4 tile randomly to an empty cell
    def add_new_tile(self):
         row = random.randint(0,3)
         col = random.randint(0,3)
         while(self.matrix[row][col] !=0):
            row = random.randint(0,3)
            col = random.randint(0,3)
         self.matrix[row][col] = random.choice([2,4])

    #update th e GUI to match the  newly generated matrix
    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value =self.matrix[i][j]
                if cell_value ==0: #if the cell is empty,set empty  cell color
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR, text="")
                else: #else show background color specififed in cell color,font color is specified in the cell number colors
                #font type is specified in cell number fonts
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.CELL_NUMBER_COLORS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value)
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks() #call the fun update idletasks which is tkinter frame member function,usef fto immediately update the  widget displays

    # 3]__Arrow-Press Functions:
    def left(self,event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def right(self,event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    def up(self,event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    def down(self,event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over(

        )

    #check if any moves are possible
    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    #Check if game is over (win/lose)
    def game_over(self, won=False):
        self.grid_cells[1][1].configure(text="")
        game_over_frame = tk.Frame(self, borderwidth=0, highlightthickness=0, bg="", padx=0, pady=0)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Load and place transparent PNG
        img = Image.open("gameover.png").resize((250, 150), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(game_over_frame, image=photo, borderwidth=0, highlightthickness=0, bg="")
        label.image = photo  # Keep a reference
        label.pack()

        # Delay and then open play.py
        self.after(2000, lambda: subprocess.Popen(["python", "play.py"]))  # Opens play.py
        self.after(2000, self.destroy)  # Closes current game window


def main():
    Game()

if __name__ == "__main__":
    main()