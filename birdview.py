# Реализуетcя процесс калибровки камеры с использованием шахматной доски.
# Он включает в себя захват видео с камеры, обнаружение углов шахматной доски,
# коррекцию этих углов, интерполяцию координат и последующую обработку видео с использованием полученных данных.
import cv2
import numpy as np
import os
from time import sleep
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator

def plot_3d(arr, step): #Визуализация данных в трехмерном и двумерном виде
    arr_tn = arr[0::step, 0::step]

    # Создание фигуры для построения графиков
    fig_1 = plt.figure()

    # Добавление графиков к фигуре
    f1sp1 = fig_1.add_subplot(2, 2, 1, projection='3d')
    f1sp2 = fig_1.add_subplot(2, 2, 2, projection='3d')
    f1sp3 = fig_1.add_subplot(2, 2, 3)
    f1sp4 = fig_1.add_subplot(2, 2, 4)

    #Создание сетки через "вытягивание" входных координат
    X, Y = np.meshgrid(np.arange(0, arr_tn.shape[1], 1).astype(int), np.arange(0, arr_tn.shape[0], 1).astype(int))
    f1sp1.plot_wireframe(Y, X, arr_tn[:,:,0], rstride=7, cstride=7)
    f1sp2.plot_wireframe(Y, X, arr_tn[:,:,1], rstride=7, cstride=7)

    for i in range(0, arr.shape[0], step):
        flx = np.arange(0,arr.shape[1],1)
        f1sp3.plot(flx, arr[i, :, 0])
        f1sp4.plot(flx, arr[i, :, 1])

def process_image(arr, input_image): #Создание нового изображения на основе координат, указанных в массиве
    y_max = arr.shape[0]
    x_max = arr.shape[1]
    output_image = np.zeros((y_max, x_max + 1, 3), float)
    # Попиксельное создание картинки из входного массива
    for yo in range(0, y_max):
        for xo in range(0, x_max):
            output_image[yo, xo] = input_image[int(arr[yo, xo, 0]), int(arr[yo, xo, 1])]

    return np.clip(output_image, 0, 255).astype(np.uint8)

if __name__ == '__main__':

    # Инициализация камеры
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # Задание критериев для коррекции углов.
    # Будет выполняться до тех пор, пока не будет достигнуто максимальное количество итераций (30) или пока изменения не станут меньше 0.001
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # cbd_shape = (12, 7)
    cbd_shape = (9, 6)
    out_image_shape = (600, 400)
    arr = np.zeros((cbd_shape[0] * cbd_shape[1], 4))

    # Создание координат сетки
    X = np.flip(np.linspace(0, out_image_shape[0], cbd_shape[0], dtype=int))
    Y = np.linspace(0, out_image_shape[1], cbd_shape[1], dtype=int)
    # Заполнение 2-х первых столбцов массива "нужными" координатами
    arr[:, 0:2] = np.asarray(np.meshgrid(Y, X)).T.reshape((cbd_shape[0] * cbd_shape[1], 2))

    print("\nPlease press Q keyboard button to save calibration !")

    # Основной цикл для захвата кадров
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            exit(1)

        i_frame = np.copy(frame)
        # Каждый кадр преобразуется в оттенки серого (для удобства), и затем программа пытается найти углы шахматной доски.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, cbd_shape, None)

        # Проверка на успешность нахождения углов
        if ret == False:
            print("Chessboard not recognised!")
            oframe = np.hstack((i_frame, i_frame))
            cv2.imshow('frame', oframe)
            if cv2.waitKey(1) == ord('q'):
                print("Calibration aborted!")
                exit(1)
                break
            continue

        # Поиск пересечений на шахматной доске
        cv2.drawChessboardCorners(frame, cbd_shape, corners, ret)
        arr[:, 2:4] = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria).reshape((-1, 2)).astype(int)

        oframe = np.hstack((i_frame, frame))
        # Вывод обычного видео и видео с найденными пересечениями
        cv2.imshow('frame', oframe)
        if cv2.waitKey(1) == ord('q'):
            break

    print("Calibration result:")
    print(arr)
    np.save(os.path.join(os.getcwd(), "arrays", "calib.npy"), arr)

    # Здесь создается сетка точек для интерполяции, которая будет использоваться для
    # преобразования координат углов шахматной доски в пиксели изображения.
    # np.mgrid создает сетку с заданными размерами, а reshape преобразует ее в двумерный массив.
    interp_points = np.mgrid[0: out_image_shape[1], 0: out_image_shape[0]].reshape(2, -1).T

    # Интерполяция координат (вывод по всей картинке из отдельных точек) и обрезка
    x_intrpld = RBFInterpolator(arr[:, 0:2], arr[:, 2])(interp_points).reshape(out_image_shape[1], out_image_shape[0])
    y_intrpld = RBFInterpolator(arr[:, 0:2], arr[:, 3])(interp_points).reshape(out_image_shape[1], out_image_shape[0])

    # pix_mvr - объединение интерполированных координат и преобразование в трехмерный массив.
    pix_mvr = (np.vstack((y_intrpld.flatten(), x_intrpld.flatten())).T).reshape((out_image_shape[1],out_image_shape[0],2))

    # Вывод графиков
    plot_3d(pix_mvr, 8)
    plt.show()

    # Этот цикл повторно считывает кадры с камеры и обрабатывает их с помощью функции process_image,
    # которая использует интерполированные координаты для коррекции изображения.
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            exit(1)

        frame = process_image(pix_mvr, frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()