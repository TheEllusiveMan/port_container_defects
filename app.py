import io
import csv
import streamlit as st
from PIL import Image as PILImage

from models import *


# Заголовок приложения
st.title("Container Damage Classifier")

# Инструкция для пользователя
st.write("Загрузите изображение, чтобы получить предсказание модели")

# Загрузка изображения
uploaded_files = st.file_uploader("Выберите изображение...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

model_container = ModelContainer()
model_container_number = ModelContainerNumber()
model_container_damage = ModelContainerDamage()

# cont_result = []
dmg_translate = {'DAMAGE - HOLE': 'пробоина'}


def container_predict(image_rgb):
    # предсказываем контейнеры
    results_cont = model_container.predict(image_rgb)
    # получаем координаты рамок с контейнерами
    frame, xyxys, confidences, class_ids = model_container.plot_bbboxes(results_cont, image_rgb)
    # image1 = cv2.imread(image_rgb)

    # # Преобразуйте изображение в формат RGB
    # image_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

    # # Сделайте предсказание
    # results = model.predict(source=response, conf=0.25)  # Укажите уровень уверенности

    # Отобразите результаты
    for result in results_cont:
        boxes = result.boxes  # Получите ограничивающие рамки
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Координаты bbox
            conf = box.conf[0]  # Уверенность
            cls = box.cls[0]  # Класс

            # Нарисуйте bbox на изображении
            cv2.rectangle(image_rgb, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)  # Красный цвет
            cv2.putText(image_rgb, f'Class: {int(cls)}, Conf: {conf:.2f}', (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    st.write("Найденный контейнер для:", im_name)
    st.image(image_rgb, use_column_width=True)

    return xyxys


def damage_predict(image, xyxys):
    results_dmg = model_container_damage.predict(frame=image, box=xyxys)

    image1 = np.array(image)

    # Преобразуйте изображение в формат RGB
    image_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    #
    # # Сделайте предсказание
    # # results = model.predict(source=response, conf=0.25)  # Укажите уровень уверенности

    xyxy_1 = xyxys[0]
    xyxy = xyxy_1[0]
    x_min, y_min, x_max, y_max = xyxy[0], xyxy[1], xyxy[2], xyxy[3]
    x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
    cropped_img = image_rgb[y_min:y_max, x_min:x_max]

    # Отобразите результаты
    for result_list in results_dmg:
        for result in result_list:
            boxes = result.boxes  # Получите ограничивающие рамки
            names = result.names
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]  # Координаты bbox
                conf = box.conf[0]  # Уверенность
                cls = box.cls[0]  # Класс
                class_name = names[int(cls)]

                # Нарисуйте bbox на изображении
                cv2.rectangle(cropped_img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 5)  # Красный цвет
                cv2.putText(cropped_img, f'Class: {class_name}, Conf: {conf:.2f}', (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    st.write("Найденные повреждения для:", im_name)
    st.image(cropped_img, use_column_width=True)

    return results_dmg

    # for result_list in results_dmg:
    #     for result in result_list:
    #         names = result.names
    #         for box in boxes:
    #             class_name = names[int(box.cls[0])]
    #             print('class_name', class_name)
    #             cont_result.append(dmg_translate[class_name])
    # print('cont_result', cont_result)


def find_cont_number(image, xyxys):
    results_number = model_container_number.predict(frame=image, box=xyxys)

    image1 = np.array(image)

    # Преобразуйте изображение в формат RGB
    image_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    #
    # # Сделайте предсказание
    # # results = model.predict(source=response, conf=0.25)  # Укажите уровень уверенности

    # print('xyxys', xyxys)
    xyxy_1 = xyxys[0]
    xyxy = xyxy_1[0]
    x_min, y_min, x_max, y_max = xyxy[0], xyxy[1], xyxy[2], xyxy[3]
    x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
    cropped_img = image_rgb[y_min:y_max, x_min:x_max]

    # Отобразите результаты
    for result_list in results_number:
        for result in result_list:
            boxes = result.boxes  # Получите ограничивающие рамки
            names = result.names
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]  # Координаты bbox
                conf = box.conf[0]  # Уверенность
                cls = box.cls[0]  # Класс
                class_name = names[int(cls)]

                # Нарисуйте bbox на изображении
                cv2.rectangle(cropped_img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 5)  # Красный цвет
                cv2.putText(cropped_img, f'Class: {class_name}, Conf: {conf:.2f}', (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    st.write("Найденная маркировка для:", im_name)
    st.image(cropped_img, use_column_width=True)

    # print('cont_result', cont_result)


def make_report(results_dmg, result_number):
    cont_result = [None, None]
    cont_result[0] = result_number

    for result_list in results_dmg:
        for result in result_list:
            names = result.names
            boxes = result.boxes
            for box in boxes:
                class_name = names[int(box.cls[0])]
                print('class_name', class_name)
                # cont_result.append(dmg_translate[class_name])
                cont_result[1] = dmg_translate[class_name]

    print('cont_result', cont_result)

    filename = 'Отчет по контейнеру ' + result_number
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(cont_result)


# names = model.names
if uploaded_files is not None:
    images = []
    for uploaded_file in uploaded_files:
        # Отображение загруженного изображения
        image = PILImage.open(uploaded_file)
        with io.BytesIO() as output:
            image.save(output, format="JPEG")  # Adjust format if needed
            contents = output.getvalue()
            with open('temp.jpg', 'wb') as f:
                f.write(contents)

        images.append(image)
        st.image(image, caption="Загруженное изображение", use_column_width=True)

    # Кнопка для запуска классификации
    ct = 0
    if st.button("Классифицировать"):
        # cont_result = []
        for image in images:
            im_name = uploaded_files[ct]
            im_name = im_name.name

            image_bbs = cv2.imread('temp.jpg')
            image_rgb = cv2.cvtColor(image_bbs, cv2.COLOR_BGR2RGB)

            # # Предсказание
            # results = model.predict(source=image_rgb, conf=0.25)

            # st.image(image, caption="Загруженное изображение", use_column_width=True)

            # Предсказание контейнера
            container_xyxys = container_predict(image_rgb)
            # Предсказание повреждений
            result_dmg = damage_predict(image, container_xyxys)
            # Предсказание маркировки
            find_cont_number(image, container_xyxys)
            # Распознование номера
            result_number = 'TCLO 531461 4' # Пока заглушка

            make_report(result_dmg, result_number)
