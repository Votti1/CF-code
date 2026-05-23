import math
import matplotlib.pyplot as plt
import PIL as pl


def transalte(word):
    translated_word = []
    for letter in word:
        translated_word.append(bin(int(letter, 16))[2:].zfill(len(letter) * 4))
    return translated_word


def divide_letters(word):
    diveded_word = []
    for doublletter in word:
        let1 = doublletter[:4]
        let2 = doublletter[4:]
        diveded_word.append(let1)
        diveded_word.append(let2)
    return diveded_word

def creat_base_pixel_matrix(size):
    pixel_matrix = [[0 for i in range(size)] for i in range(size)]
    centers_cord = []
    idx_x = 4
    idx_y = 4
    end_x = size - 3
    end_y = size - 3
    while idx_y < end_y:
        while idx_x < end_x:
            pixel_matrix[idx_y][idx_x] = 1
            centers_cord.append((idx_y, idx_x))
            idx_x += 3
        idx_x = 4
        idx_y += 3
    return pixel_matrix, centers_cord

def print_word_into_matrix(word, matrix, cord):
    i = 0
    next_r = 1
    for letter in word:
        next_r = (next_r + 1) % 2
        center_y, center_x = cord[i]
        matrix = print_around_center(matrix,center_x, center_y, letter, next_r)
        if next_r and i < len(cord):
            i += 1
    return matrix

def print_around_center(matrix, center_x, center_y, letter, next_r):
    next_bit = 0
    for bit in letter:
        if next_r == 0:
            y = center_y - 1 * (1 if next_bit < 2 else -1)
            x = center_x - 1 * (-1 if next_bit in [1, 2] else 1)
            matrix[y][x] = int(bit) + 3
        else:
            y = center_y - 1 * ((-1 if next_bit > 1 else 1) if next_bit % 2 == 0 else 0)
            x = center_x - 1 * ((-1 if next_bit < 2 else 1) if next_bit % 2 == 1 else 0)
            matrix[y][x] = int(bit) + 2
        next_bit = (next_bit + 1) % 4
    return matrix

def clear_extra_center(matrix, cord):
    for y, x in cord:
        if matrix[y+1][x+1] == 0:
            matrix[y][x] = 0
    return matrix


def print_into_img(pixels, matrix, scale=11):
    colors = [(232, 225, 219), (54, 46, 35), (58, 60, 38), (109, 108, 60), (169, 172, 93)]
  
    color = 0
    for i in range(len(matrix)):
        n = 0 + (3 if 3 > (i % 6) else 0)
        for j in range(len(matrix)):
            if matrix[i][j] == 0: 
                color = colors[matrix[i][j]]
            else: 
                color = colors[matrix[i][j] if n < 3 else abs(5 - matrix[i][j])]
                n = (n + 1) % 6
            for y in range(scale):
                for x in range(scale):
                    pixels[scale * j + x, scale * i + y] = color


def beautify():
    pass

def main():
    scale = 11
    word = input().encode('utf-8').hex(" ").split()
    size = math.ceil(math.sqrt(math.ceil(len(word)))) * 3 + 6
    word = transalte(word)
    word = divide_letters(word)
    pixel_matrix, center_cord = creat_base_pixel_matrix(size)
    pixel_matrix = print_word_into_matrix(word, pixel_matrix, center_cord)
    pixel_matrix = clear_extra_center(pixel_matrix, center_cord)
    img = pl.Image.new("RGB", (size * scale, size * scale), color="white")
    pixels = img.load()
    print_into_img(pixels, pixel_matrix, scale)
    print(word)
    print (pixel_matrix)
    print(size)
    img.save("resuld_new.png")
 

if "__main__" == __name__:
   main()
   
    