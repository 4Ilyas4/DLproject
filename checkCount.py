
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import re
import numpy as np
import cv2  # Используем OpenCV для эффективного рисования

def create_mask_from_shape_path_efficient(shape_path, image_size):

    tokens = re.findall(r'[mlxe]|\d+,\d+', shape_path, flags=re.IGNORECASE)

    polygon_list = []      # Список для хранения полигонов в формате NumPy для OpenCV
    current_path_pts = []  # Текущий список точек [[x1, y1], [x2, y2], ...]
    start_point = None     # Начальная точка [[x, y]]

    i = 0
    while i < len(tokens):
        token = tokens[i].lower()

        if token == 'm':
            i += 1
            if i < len(tokens) and ',' in tokens[i]:
                x, y = map(float, tokens[i].split(','))
                # Если предыдущий путь не был закрыт, завершаем его перед началом нового
                if current_path_pts:
                    # Конвертируем в NumPy (N, 2), округляем и приводим к int32
                    poly = np.array(current_path_pts, dtype=np.float32).round().astype(np.int32)
                    # OpenCV ожидает формат (N, 1, 2)
                    if poly.size > 0:
                         polygon_list.append(poly.reshape((-1, 1, 2)))
                # Начинаем новый путь
                current_path_pts = [[x, y]]
                start_point = [x, y] # Запоминаем как список для сравнения

        elif token == 'l':
            i += 1
            if i < len(tokens) and ',' in tokens[i]:
                x, y = map(float, tokens[i].split(','))
                if current_path_pts: # Добавляем, только если путь начат
                    current_path_pts.append([x, y])

        # Обрабатываем 'x' (закрыть) и 'e' (завершить) схожим образом в конце
        elif token == 'x' or token == 'e':
            # Для 'x' добавляем замыкающую точку, если нужно
            if token == 'x':
                if start_point and current_path_pts and len(current_path_pts) > 1:
                    # Сравниваем последнюю точку с начальной
                    if current_path_pts[-1] != start_point:
                        current_path_pts.append(start_point) # Замыкаем контур

            # Завершаем текущий контур (общий код для 'x' и 'e')
            if current_path_pts:
                poly = np.array(current_path_pts, dtype=np.float32).round().astype(np.int32)
                if poly.size > 0:
                    polygon_list.append(poly.reshape((-1, 1, 2)))
            current_path_pts = [] # Сбрасываем для следующего контура
            start_point = None

        i += 1

    # Добавляем последний контур, если строка не заканчивалась на 'x' или 'e'
    if current_path_pts:
        poly = np.array(current_path_pts, dtype=np.float32).round().astype(np.int32)
        if poly.size > 0:
            polygon_list.append(poly.reshape((-1, 1, 2)))
    
    # Задаем размеры: OpenCV использует (высота, ширина)
    height, width = image_size[1], image_size[0]
    # Создаем черную маску как NumPy массив типа uint8
    mask = np.zeros((height, width), dtype=np.uint8)

    # Если список полигонов пуст, возвращаем пустую маску
    if not polygon_list:
        return mask

    try:
        # cv2.fillPoly рисует ЗАПОЛНЕННЫЕ полигоны
        # Она модифицирует массив `mask` на месте (in-place)
        # pts=polygon_list: список полигонов для отрисовки
        # color=1: цвет заливки (белый на черном фоне)
        cv2.fillPoly(mask, pts=polygon_list, color=1)
    except Exception as e:
        print(f"Предупреждение: OpenCV не смог отрисовать полигоны. Ошибка: {e}")
        # В качестве запасного варианта можно попробовать нарисовать контуры:
        # try:
        #     cv2.drawContours(mask, contours=polygon_list, contourIdx=-1, color=1, thickness=1)
        # except Exception as ec:
        #      print(f"Предупреждение: OpenCV не смог отрисовать и контуры. Ошибка: {ec}")

    return mask # Возвращаем маску как NumPy массив

# --- Пример использования ---
path_example = "m975,1767 l1025,1767 l1025,1818 l975,1818 x e"
image_dimensions = (1595, 1890) # (ширина, высота)

# Создаем маску с помощью эффективной функции
digit_mask_efficient_np = create_mask_from_shape_path_efficient(path_example, image_dimensions)

# Вывод информации о результате
print(f"Размер эффективной маски (ВxШ): {digit_mask_efficient_np.shape}")
print(f"Уникальные значения в эффективной маске: {np.unique(digit_mask_efficient_np)}") # Должны быть [0 1]

# --- Визуализация (опционально, требует установленного OpenCV) ---
# import matplotlib.pyplot as plt
# plt.imshow(digit_mask_efficient_np, cmap='gray')
# plt.title("Эффективная Маска")
# plt.show()

# Или с помощью OpenCV:
# cv2.imshow("Efficient Mask", digit_mask_efficient_np * 255) # Умножаем на 255 для отображения
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# def parse_shape_path(shape_path):

#     tokens = re.findall(r'[mlxe]|\d+,\d+', shape_path, flags=re.IGNORECASE)
    
#     paths = []           
#     current_path = []    
#     start_point = None   

#     i = 0
#     while i < len(tokens):
#         token = tokens[i].lower()
#         if token == 'm':  
#             i += 1
#             if i < len(tokens) and ',' in tokens[i]:
#                 x, y = map(float, tokens[i].split(','))
#                 current_path = [(x, y)]
#                 start_point = (x, y)
#         elif token == 'l':  
#             i += 1
#             if i < len(tokens) and ',' in tokens[i]:
#                 x, y = map(float, tokens[i].split(','))
#                 current_path.append((x, y))
#         elif token == 'x':  
#             if start_point and current_path and current_path[-1] != start_point:
#                 current_path.append(start_point)
#             paths.append(current_path)
#             current_path = []
#             start_point = None
#         elif token == 'e':  
#             if current_path:
#                 paths.append(current_path)
#                 current_path = []
#                 start_point = None
#         i += 1
#     return paths


# img = mpimg.imread("C:/Users/user/Desktop/Work/DeepLearning/JCB/decrypted_images/132441.tif_06C0A2F4-0718-407A-9B8B-673215FED2B7.tiff")

# plt.figure(figsize=(8, 6))
# plt.imshow(img)
# for path in paths:
#     if len(path) > 1:
#         xs, ys = zip(*path)
#         plt.plot(xs, ys, marker='o', color='red', linewidth=2)
# plt.title("Изображение с наложенным ShapePath")
# plt.axis('off')
# plt.show()