#!/usr/sup/bin/python3
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode(400,400)
    background = surface(400,400)

    pygame.draw.rect(background,(0,255,255),(20,20,40,40))
    pygame.draw.rect(background,(255,0,255),(120,120,50,50))

    screen.blit(background, (0,0))
    pygame.display.flip()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    #### Update the the display and wait ####
    
    pygame.quit()

class Grid(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        #self.create_tiles()

   # def create_tiles(self):
   #     self.grid()
        #self.minsize(25, 25)
        #self.maxsize(25, 25)


root = tk.Tk()
root.geometry('250x250')
app = Grid(master=root)
tileList = []
for _y in range(25):
    for _x in range(25):
        t = tk.Label(app, text="TILE")
        t.place(x = _x, y = _y)
        tileList.append(t.copy())

        
app.mainloop()
