from tkinter import Tk, Canvas
from map.map import Map
from algos.annealing import Annealing
import pickle
import sys

def generate_maps():
    maps = []
    for i in range(3):
        maps = maps + [ Map((j+1)*10) for j in range(10)]
    pickle.dump(maps, open('./data/map_data.p', 'wb'))

def display_maps(maps):
    # Drawing code is commented out
    for map in maps:
        root=Tk()
        countries_to_draw = []
        borders_to_draw = []
        for country in map.countries:
            countries_to_draw.append({'x': country.x*500, 'y': country.y*500})
        for border in map.borders:
            borders_to_draw.append(
                {
                    'start_x': border.country_a.x * 500,
                    'start_y': border.country_a.y * 500,
                    'end_x': border.country_b.x * 500,
                    'end_y': border.country_b.y * 500
                }
            )

        w = Canvas(root, width=500, height=500,
            borderwidth=0,
            highlightthickness=0,
            background='white')
        for country in countries_to_draw:
            w.create_oval(country['x']-5, country['y']-5, country['x']+5, country['y']+5, fill="red")
        for border in borders_to_draw:
            w.create_line(border['start_x'], border['start_y'], border['end_x'], border['end_y'])
        w.pack()
        root.mainloop()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--g':
        generate_maps()
    display_maps(pickle.load(open('./data/map_data.p', 'rb')))
