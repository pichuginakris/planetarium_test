# Клиент серверное приложение на основе сокетов библиотеки PyZMQ

## Запуск
Устанавливаем необходимые для проекта библиотеки.
```python
    pip install -r requirements.txt
```

## Часть 1. Передача массива случайных чисел (папка random_numbers_transmission).
Для демонстрации работы необходимо запустить файлы server.py, client1.py, client2.py, client3.py.
Сервер отправляет массив случайных чисел. Для генерации случайных чисел и отправки списка используется метод sending_messages. Он принимает нижнюю (lower), верхнюю (upper) границу 
для генерации случайных чисел, а также счетчик (count), сколько в массиве должно быть случайных чисел. По умолчанию lower=0, upper=10000, count=6.
```python
def sending_messages(lower: int = 0, upper: int = 10000, count: int = 6):
    while True:
        messages = numpy.random.uniform(lower, upper, count)
        print(messages)
        time.sleep(1)
        try:
            socket.send_pyobj(messages)
        except Exception as ex:
            logging.error(
                'SERVER ERROR: Exception of type {!s} : {!s}'.format(type(ex).__name__, str(ex)))
```
Первый клиент (client1) получает массив, печатает только числа, находящиеся на четных местах в массиве.
Второй клиент (client2) получает массив, печатает только числа, находящиеся на нечетных местах в массиве.
Третий клиент (client3) получает и печатает все число из массива.



## Часть 2. Передача видеопотока (video_transmission).
Сервер транслирует видео (в данном случае shrek-best-life.mp4). Клиенты подключаются к трансляции и также транслируют полученные кадры видео.
Для этого использовалась библиотека opencv-python. В бесконечном цикле захватывается видео, лежащие по пути Video_path. Далее читаются кадры и выводятся видео с названием Server.
Для клиентов видео экраны называются Client 1 и Client 2 соответственно.
```python
while True:
    vid_capture = cv2.VideoCapture(Video_path)
    if not vid_capture.isOpened():
        logging.warning('SERVER: Opening video warning')
    while vid_capture.isOpened():
        ret, frame = vid_capture.read()
        if ret:
            cv2.imshow('Server', frame)
            socket.send_pyobj(frame)
            key = cv2.waitKey(30)
        else:
            break
    vid_capture.release()
else:
    cv2.destroyAllWindows()
```
## Примечание
Для отслеживания ошибок, их запись ведется в файл логов errors_log.log. 
Создание файла логов
```python
logging.basicConfig(filename='errors_log.log', filemode='a',
                        format='%(process)s - %(asctime)s - %(levelname)s - %(message)s')
```
Пример вывода одного из логов в случае, если сервер пытается подключиться к занятому порту.
```python
5080 - 2022-08-04 17:47:01,977 - ERROR - SERVER ERROR: Exception of type ZMQError : Address in use
```
