import tkinter
from os.path import isfile, join
import numpy as np
import PIL.Image
import PIL.ImageTk
import time
import random

armour_colours = {
    4: "blue",
    3: "red",
    2: "orange",
    1: "yellow",
    0: "white"
}

armour_strength = {
    "blue": 4,
    "red": 3,
    "orange": 2,
    "yellow": 1,
    "white": 0
}

colours = {
  "blue": (55, 171, 200),
  "red": (255, 0, 0),
  "orange": (255, 102, 0),
  "yellow": (244, 218, 66),
  "white": (255, 255, 255)
}

class AppLabels:
    def __init__(self, window, window_title):
        self.index = 0
        self.index_ann = 0
        self.window = window
        self.window.title(window_title)

        #Population
        self.population_size = 8
        self.population = self.generate_population()
        self.pop_evaluate = self.evaluate_population(self.population)
        self.iterations = 0


        # Create the timeline element
        self.width = 215
        self.height = 215

        # Create a canvas that can fit the above image
        # self.canvas = tkinter.Canvas(window, width=self.width*6, height=self.height*6)
        # self.canvas.pack()

        self.robots_canvas = []
        self.text_canvas = []
        for i in range(0, int(self.population_size/2)):
            canvas = tkinter.Canvas(window, width = self.width, height = self.height, )
            canvas.grid(row=0, column = i)
            T = tkinter.Text(window, height=2, width=30)
            T.insert(tkinter.END, "Just a text Widget\nin two lines\n")
            T.grid(row=1, column=i)
            self.text_canvas.append(T)
            self.robots_canvas.append(canvas)

        for i in range(0, int(self.population_size/2)):
            canvas = tkinter.Canvas(window, width = self.width, height = self.height)
            canvas.grid(row=2, column = i)

            T = tkinter.Text(window, height=2, width=30)
            T.insert(tkinter.END, "Just a text Widget\nin two lines\n")
            T.grid(row=3, column=i)

            self.text_canvas.append(T)
            self.robots_canvas.append(canvas)

        # add children
        for i in range(0,2):
            canvas = tkinter.Canvas(window, width=self.width, height=self.height)
            canvas.grid(row=4, column=i)
            self.robots_canvas.append(canvas)

            T = tkinter.Text(window, height=2, width=30)
            T.insert(tkinter.END, "")
            T.grid(row=5, column=i)
            self.text_canvas.append(T)

        self.IterationNo_canvas = tkinter.Text(window, height=2, width=30)
        self.IterationNo_canvas.insert(tkinter.END, "Iteration Number: 0")
        self.IterationNo_canvas.config(font=("Courier", 24))
        self.IterationNo_canvas.grid(row=5, column=3, columnspan=2, sticky="nsew")

        self.robots = []
        self.window.bind('p', self.animate)
        self.draw_robots(select=False)
        #self.animate()
        self.window.mainloop()

    def animate(self, event):
        print("-----------------")
        self.play()

    def select_parents(self):
        p1 = random.randint(0, self.population_size-1)
        p2 = random.randint(0, self.population_size-1)
        while p1 == p2:
            p2 = random.randint(0, self.population_size-1)
        return p1, p2

    def play(self):
        if self.iterations < 100:
            print("Iterations: --------->",self.iterations)
            self.iterations += 1
            # Select parents
            p1, p2 = self.select_parents()

            self.draw_robots(select=False)

            self.draw_robot2(p1, True)
            self.draw_robot2(p2, True)

            # Combine robots
            child1, child2 = self.combine_robots(p1, p2)
            self.population.append(child1)
            self.population.append(child2)

            robot1 = self.draw_robot(armour=child1, select=False)
            self.robots.append(robot1)
            robot1 = self.draw_robot(armour=child2, select=False)
            self.robots.append(robot1)

            # Evaluate population
            self.pop_evaluate = self.evaluate_population(self.population)

            # Draw children
            self.draw_robot2(len(self.population)-2, False)
            self.draw_robot2(len(self.population)-1, False)

            self.window.update_idletasks()
            self.window.update()
            # self.window.after(100, self.play())
            self.update_iterations()
            time.sleep(0.5)

            # clear selection
            self.draw_robot2(p1, False)
            self.draw_robot2(p2, False)

            # Survival
            indices_sort = np.argsort(self.pop_evaluate)
            del self.population[indices_sort[0]]
            del self.pop_evaluate[indices_sort[0]]
            indices_sort = np.argsort(self.pop_evaluate)
            del self.population[indices_sort[0]]
            del self.pop_evaluate[indices_sort[0]]

            self.play()

    def draw_robots(self, select = True):
        self.robots = []
        print("Draw robots", select)
        for i in range(0, self.population_size):
            robot1 = self.draw_robot(armour=self.population[i], select=select)
            self.robots.append(robot1)

        for i in range(0, self.population_size):
            self.robots_canvas[i].create_image(0, 0, image=self.robots[i], anchor=tkinter.NW)
            self.text_canvas[i].delete("1.0", "end")
            self.text_canvas[i].insert(tkinter.END, "Power: " + str(self.pop_evaluate[i]))

    def draw_robot2(self, robot_id, select=True):
        print("Draw robots2", select, robot_id, len(self.population))
        robot1 = self.draw_robot(armour=self.population[robot_id], select=select)
        self.robots[robot_id] = robot1
       # self.robots.append(robot1)

        self.robots_canvas[robot_id].create_image(0, 0, image=self.robots[robot_id], anchor=tkinter.NW)
        self.text_canvas[robot_id].delete("1.0", "end")
        self.text_canvas[robot_id].insert(tkinter.END, "Power: " + str(self.pop_evaluate[robot_id]))

    def update_iterations(self):
        self.IterationNo_canvas.delete("1.0", "end")
        self.IterationNo_canvas.insert(tkinter.END, "Iteration Number: " + str(self.iterations))

    def sel(self):
        selection = "You selected the option " + str(self.var.get())
        print(selection)
        #label.config(text=selection)

    def combine_robots(self, p1, p2):
        ind1 = self.population[p1]
        ind2 = self.population[p2]

        cutting_line = random.randint(0, len(ind1)-1)

        c1 = []
        c2 = []

        for i in range(0, cutting_line):
            c1.append(ind1[i])
        for i in range(cutting_line, len(ind1)):
            c1.append(ind2[i])
            c2.append(ind1[i])
        for i in range(0, cutting_line):
            c2.append(ind2[i])
        print("=============")
        print(ind1, ind2, cutting_line)
        print(c1)
        print(c2)
        return c1, c2

    def draw_canvas(self):
        self.draw_timeline()

    def generate_population(self):
        population = []
        for i in range(0, self.population_size):
            armour = []
            for j in range(0, 6):
                armour.append(random.randint(0, 4))
            population.append(armour)
        return population


    def evaluate_population(self, population):
        rez = []
        print("*****************")
        for individual in population:
            fitness = 0
            for gene in individual:
                fitness += armour_strength[armour_colours[gene]]
                # if individual.count(gene) == 2:
                #     fitness += 2*armour_strength[armour_colours[gene]]
            rez.append(fitness)
            print(individual, fitness)
        return rez

    def draw_robot(self, armour = [0, 4, 3, 0, 0, 0], select=False):
        #set image to gray
        robot = np.zeros((self.width, self.height, 3), np.uint8)

        if select:
            for i in range(0, self.width):
                for j in range(0, self.height):
                    robot[i,j] = (100, 100, 100)

        # head
        for i in range(40, 40+50):
            for j in range(82, 82+62):
                robot[i, j] = colours[armour_colours[armour[0]]]#100, 200, 100)

        # body
        for i in range(40+55, 90+70):
            for j in range(72, 72+82):
                robot[i, j] = colours[armour_colours[armour[1]]]

        # right leg 1
        for i in range(90+75, 90+75+15):
            for j in range(82, 82+30):
                robot[i, j] = colours[armour_colours[armour[5]]]
        # right leg 2
        for i in range(90+75+20, 90+75+20+15):
            for j in range(82, 82+30):
                robot[i, j] = colours[armour_colours[armour[5]]]
        # left leg 1
        for i in range(90+75, 90+75+15):
            for j in range(82+35, 82+35+30):
                robot[i, j] = colours[armour_colours[armour[4]]]
        # left leg 2
        for i in range(90+75+20, 90+75+20+15):
            for j in range(82 + 35, 82 + 35 + 30):
                robot[i, j] = colours[armour_colours[armour[4]]]

        # right arm
        for i in range(105,105+30):
            for j in range(50, 50 + 20):
                robot[i, j] = colours[armour_colours[armour[3]]]

        # left arm
        for i in range(105,105+30):
            for j in range(155, 155 + 20):
                robot[i, j] = colours[armour_colours[armour[2]]]

        # left eye
        for i in range(50, 50+15):
            for j in range(97, 97+10):
                robot[i, j] = (50, 50, 50)
        # right eye
        for i in range(50, 50+15):
            for j in range(120, 120+10):
                robot[i, j] = (50, 50, 50)

        # left ear
        for i in range(55, 55+20):
            for j in range(70, 70+10):
                robot[i, j] = (200, 200, 200)

        # right ear
        for i in range(55, 55+20):
            for j in range(147, 147+10):
                robot[i, j] = (200, 200, 200)

       # self.robot1[0:self.time_height, self.position:self.position + 2] = (100, 200, 100)
        return PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(robot))
       # self.photo_timeline = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.robot1))
        # Add a PhotoImage to the Canvas
       # self.timeline.create_image(0, 0, image=self.photo_timeline, anchor=tkinter.NW)


def main():
    #
    AppLabels(tkinter.Tk(), "RoboWars")
    for i in range(0,6):
        print("===========")
        for j in range(0,6):
            print(random.randint(0, 4))
    # Head; Body; Left Arm; Right Arm; Left Leg; Right Leg


if __name__ == "__main__":
    main()

