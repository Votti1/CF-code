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
    pixel_matrix = [[ for i in range(size)] for i in range(size)]
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
            matrix[y][x] = int(bit) 
        else:
            y = center_y - 1 * ((-1 if next_bit > 1 else 1) if next_bit % 2 == 0 else 0)
            x = center_x - 1 * ((-1 if next_bit < 2 else 1) if next_bit % 2 == 1 else 0)
            matrix[y][x] = int(bit) 
        next_bit = (next_bit + 1) % 4
    return matrix

def clear_extra_center(matrix, cord):
    for y, x in cord:
        if matrix[y+1][x+1] == 0:
            matrix[y][x] = 0
    return matrix


def print_into_img(pixels, matrix, scale=11):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            color = (0, 0, 0) if matrix[i][j] else (255, 255, 255)
            for y in range(scale):
                for x in range(scale):
                    pixels[scale * j + x, scale * i + y] = color


def draw_corner(pixels, size, scale=11):
    color = (0, 0, 0)
    for edge in range(2):
        for i in range(math.floor(size / 2) + 3):
            j = 0 if edge == 0 else size - 1
            for y in range(scale):
                for x in range(scale):
                    x_start = scale * j
                    y_start = scale * (math.floor(size/2) + i - 3)
                    pixels[x_start + x, y_start + y] = color

    for length in range(math.ceil(math.log2(size))):
        for y in range(scale):
                    for x in range(scale):
                        pixels[length * scale + x, (size - 1) * scale + y] = color
        for y in range(scale):
                for x in range(scale):
                    pixels[(size - 1 - length) * scale + x, (size - 1) * scale + y] = color
    

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
    draw_corner(pixels, size, scale)
    print(word)
    print (pixel_matrix)
    print(size)
    img.save("result_bnw.png")
 

if "__main__" == __name__:
   main()
   
    