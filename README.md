ENG:
This code implements camera calibration using a 7x10 checkerboard. The implemented algorithm includes video capture from the camera, detection
of nodes of the checkerboard grid, correction of node data, coordinate interpolation and subsequent video processing using the received data. The algorithm is implemented in FPGAs and
is designed for low-performance devices that do not have enough computing power to use the OpenCV library, which contains 
necessary image processing algorithms. The program includes mechanisms for error and exception handling, which ensures reliable operation of the program even in
conditions of unstable video signal or poor image quality, as well as two functions for visualizing data in three-dimensional and two-dimensional form and for
creating a new image based on the coordinates specified in the auxiliary array.

RUS:
Данный код реализует калибровку камеры с использованием шахматной доски размером 7x10. Реализованный алгоритм включает в себя захват видео с камеры, обнаружение 
узлов сетки шахматной доски, коррекцию данных узлов, интерполяцию координат и последующую обработку видео с использованием полученных данных. Алгоритм реализуется в ПЛИС и 
предназначен для устройств с маленькой производительностью, в которых не достаточно вычислительной мощности для использования библиотеки OpenCv, которая содержит в себе 
необходимые алгоритмы обработки изображений. Программа включает в себя механизмы для обработки ошибок и исключений, что обеспечивает надежность работы программы даже в 
условиях нестабильного видеосигнала или низкого качества изображения, а также две функции для визуализации данных в трехмерном и двумерном виде и для 
создания нового изображения на основании координат, указанных в вспомогательном массиве.

中国语文科:
此代码使用7x10棋盘实现相机校准。 实现的算法包括来自摄像机的视频捕获，检测
棋盘格的节点，校正节点数据，坐标插值和随后的视频处理使用接收的数据。 该算法在Fpga和
是专为低性能的设备，没有足够的计算能力来使用OpenCV库，其中包含 
必要的图像处理算法。 该程序包括错误和异常处理机制，即使在
视频信号不稳定或图像质量差的条件，以及用于以三维和二维形式可视化数据和用于
根据辅助数组中指定的坐标创建新图像。
