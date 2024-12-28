import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from perlin_noise import PerlinNoise

# Ustawienia mapy
map_width, map_height = 200, 200  # Rozdzielczość mapy
seed = random.randint(1, 1000000)  # Seed szumu Perlin'a


# Generowanie wartości szumu i przypisanie typów terenu
def generate_terrain_map(map_width, map_height):

    # Inicjalizacja mapy
    terrain_map = np.zeros((map_height, map_width))

    scale = map_width * 0.8  # Skala szumu Perlin'a
    noise_water = PerlinNoise(octaves=4, seed=seed)
    noise_terrain = PerlinNoise(octaves=5, seed=(seed*10))

    for y in range(map_height):
        for x in range(map_width):
            value = (abs(noise_water([x/scale*1.5, y/scale*1.5])) +
                     abs(noise_water([x/scale*0.5, y/scale*0.5])) / 2)

            if value < 0.18:               # Sprawdzamy wartość szumu Perlin'a dla wody
                terrain_map[y][x] = 0      # Woda

            elif value < 0.19:             # Sprawdzamy co dzieje sie na wybrzezu
                terrain_map[y][x] = 1      # Piasek
                value = (abs(noise_terrain([x/scale, y/scale])))
                if value < 0.6 and value >= 0.2:  # Sprawdzamy wartość szumu Perlin'a dla wybrzeza
                    terrain_map[y][x] = 2 # Trawa
                elif value >= 0.6:
                    terrain_map[y][x] = 3  # Las

            else:
                terrain_map[y][x] = 1      # Piasek
                value = (abs(noise_terrain([x/scale*1.5, y/scale*1.5])) +
                         abs(noise_terrain([x/scale*0.5, y/scale*0.5])) / 2)
                if value < 0.25 and value > 0.02: # Sprawdzamy wartość szumu Perlin'a dla terenu
                    terrain_map[y][x] = 2 # Trawa
                elif value < 0.8 and value > 0.25:
                    terrain_map[y][x] = 3  # Las
    return terrain_map

terrain_map = generate_terrain_map(map_width, map_height)

# Definiowanie mapy kolorów
colors = ["#0000ff", "#ffff99", "#00ff00", "#006400"]  # Kolory dla wody, piasku, trawy i lasu
cmap = mcolors.ListedColormap(colors)

# Wizualizacja mapy
plt.figure(figsize=(10, 8))
plt.imshow(terrain_map, cmap=cmap)
cbar = plt.colorbar(ticks=[0, 1, 2, 3], label="Typ terenu")
cbar.ax.set_yticklabels(['Woda', 'Piasek', 'Trawa', 'Las'])
plt.clim(-0.5, 3.5)
plt.show()
