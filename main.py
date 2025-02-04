import os
import pygame
import random
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def split_image(image, rows, cols):
    """將圖片切割成 rows x cols 小片段"""
    img_width, img_height = image.get_size()
    tile_width = img_width // cols
    tile_height = img_height // rows
    tiles = []

    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
            tile = image.subsurface(rect)
            tiles.append((tile, rect))

    return tiles

def shuffle_tiles_on_screen(tiles, rows, cols, tile_width, tile_height):
    """打亂拼圖並隨機放置在屏幕上"""
    grid_positions = [
        pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
        for row in range(rows) for col in range(cols)
    ]
    random.shuffle(grid_positions)

    for i, (tile, _) in enumerate(tiles):
        tiles[i] = (tile, grid_positions[i])

def draw_grid(screen, rows, cols, tile_width, tile_height):
    """繪製提示網格"""
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

def main():
    # 使用 tkinter 跳出檔案選擇視窗
    Tk().withdraw()  # 隱藏 tkinter 的主視窗
    image_path = askopenfilename(
        title="選擇圖片檔案",
        # filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )

    if not image_path:
        print("未選擇圖片，程式結束。")
        sys.exit()

    # 初始化 pygame
    pygame.init()

    # 遊戲參數
    screen_width, screen_height = 800, 600
    rows, cols = 3, 3  # 切割成 3x3 拼圖

    # 初始化畫面
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("拼圖遊戲")

    try:
        image = pygame.image.load(image_path).convert()
    except pygame.error:
        print("無法載入圖片，請檢查檔案。")
        pygame.quit()
        sys.exit()

    # 縮放圖片以適應畫布
    image = pygame.transform.scale(image, (screen_width, screen_height))

    # 計算單個拼圖塊的大小
    tile_width = screen_width // cols
    tile_height = screen_height // rows

    # 切割圖片並打亂
    tiles = split_image(image, rows, cols)
    original_tiles = tiles[:]
    shuffle_tiles_on_screen(tiles, rows, cols, tile_width, tile_height)

    # 拼圖邏輯
    dragging = False
    selected_tile = None
    selected_index = None

    # 按鈕參數
    button_font = pygame.font.Font(None, 40)
    button_rect = pygame.Rect(screen_width // 2 - 50, screen_height - 60, 100, 40)
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))

        # 繪製網格
        draw_grid(screen, rows, cols, tile_width, tile_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左鍵點擊
                    pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(pos):
                        # 檢查是否完成
                        if tiles == original_tiles:
                            print("拼圖完成！")
                        else:
                            print("拼圖尚未完成。問題點如下：")
                            for i, ((current_tile, current_rect), (correct_tile, correct_rect)) in enumerate(zip(tiles, original_tiles)):
                                if current_rect != correct_rect:
                                    print(f"塊 {i} 錯誤：當前位置 {current_rect.topleft}，應該為 {correct_rect.topleft}")        
                    else:
                        for index, (_, rect) in enumerate(tiles):
                            if rect.collidepoint(pos):
                                dragging = True
                                selected_tile = tiles[index]
                                selected_index = index
                                break

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging:
                    dragging = False
                    if selected_tile:
                        _, rect = selected_tile
                        # 找到最近的網格位置
                        closest_row = round(rect.y / tile_height)
                        closest_col = round(rect.x / tile_width)
                        target_x = closest_col * tile_width
                        target_y = closest_row * tile_height

                        # 檢查目標位置是否被其他塊佔用
                        for index, (_, other_rect) in enumerate(tiles):
                            if other_rect.topleft == (target_x, target_y):
                                # 交換位置
                                other_rect.x, other_rect.y = rect.x, rect.y
                                rect.x, rect.y = target_x, target_y
                                break
                            else:
                                 # 如果沒有衝突，直接放置到目標位置
                                rect.x, rect.y = target_x, target_y

            if event.type == pygame.MOUSEMOTION and dragging:
                if selected_tile:
                    _, rect = selected_tile
                    rect.x, rect.y = event.pos

        # 繪製拼圖
        for tile, rect in tiles:
            screen.blit(tile, rect.topleft)

        # 繪製按鈕
        pygame.draw.rect(screen, (0, 128, 255), button_rect)
        button_text = button_font.render("Submit", True, (255, 255, 255))
        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
