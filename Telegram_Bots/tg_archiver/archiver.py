# import os
# import telebot
# from PyPDF2 import PdfReader, PdfWriter
# from docx import Document
# from pdf2image import convert_from_path
# from openpyxl import load_workbook
# from pptx import Presentation
# from reportlab.pdfgen import canvas
# from PIL import Image
#
# API_TOKEN = '7261178345:AAGYx1RSaukNFeBqrXuJb-_XJHZkducTenM'
#
# bot = telebot.TeleBot(API_TOKEN)
#
# # Приветствие и информация о боте
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message, "Привет! Я бот для архивирования и конвертирования файлов. Вот что я умею:\n"
#                           "1. Convert PDF to Word\n"
#                           "2. Convert Word to PDF\n"
#                           "3. Convert PDF to JPG\n"
#                           "4. Convert JPG to PDF\n"
#                           "5. Convert PDF to Excel\n"
#                           "6. Convert Excel to PDF\n"
#                           "7. Convert PDF to PowerPoint\n"
#                           "8. Convert PowerPoint to PDF\n"
#                           "9. Compress PDF\n"
#                           "10. Edit PDF\n"
#                           "Отправьте мне файл, и я помогу вам его обработать!")
#
# # Обработчик документов
# @bot.message_handler(content_types=['document'])
# def handle_document(message):
#     file_info = bot.get_file(message.document.file_id)
#     downloaded_file = bot.download_file(file_info.file_path)
#
#     file_name = message.document.file_name
#     file_extension = os.path.splitext(file_name)[1].lower()
#
#     # Сохранение файла
#     with open(file_name, 'wb') as new_file:
#         new_file.write(downloaded_file)
#
#     # Определение действия в зависимости от расширения файла
#     if file_extension == '.pdf':
#         bot.reply_to(message, "Вы прислали PDF файл. Что вы хотите с ним сделать?")
#         # Добавить опции: конвертировать или сжать
#
#     elif file_extension == '.docx':
#         output_file = 'output.pdf'
#         convert_word_to_pdf(file_name, output_file)
#         bot.reply_to(message, "Конвертация Word в PDF завершена.")
#         send_converted_file(message.chat.id, output_file)
#
#     elif file_extension == '.jpg':
#         output_file = 'output.pdf'
#         convert_jpg_to_pdf(file_name, output_file)
#         bot.reply_to(message, "Конвертация JPG в PDF завершена.")
#         send_converted_file(message.chat.id, output_file)
#
#     elif file_extension == '.xlsx':
#         output_file = 'output.pdf'
#         convert_excel_to_pdf(file_name, output_file)
#         bot.reply_to(message, "Конвертация Excel в PDF завершена.")
#         send_converted_file(message.chat.id, output_file)
#
#     # Добавьте другие конвертации по необходимости
#
# # Функция отправки файла
# def send_converted_file(chat_id, file_path):
#     with open(file_path, 'rb') as file:
#         bot.send_document(chat_id, file)
#
# # Конвертация PDF в Word
# def convert_pdf_to_word(pdf_file, output_file):
#     reader = PdfReader(pdf_file)
#     doc = Document()
#
#     for page in reader.pages:
#         doc.add_paragraph(page.extract_text())
#
#     doc.save(output_file)
#
# # Конвертация Word в PDF
# def convert_word_to_pdf(word_file, output_file):
#     doc = Document(word_file)
#     pdf = canvas.Canvas(output_file)
#
#     for para in doc.paragraphs:
#         pdf.drawString(100, 750, para.text)
#         pdf.showPage()
#
#     pdf.save()
#
# # Конвертация JPG в PDF
# def convert_jpg_to_pdf(jpg_file, output_file):
#     image = Image.open(jpg_file)
#     pdf_image = image.convert('RGB')
#     pdf_image.save(output_file)
#
# # Конвертация PDF в JPG
# def convert_pdf_to_jpg(pdf_file, output_folder):
#     images = convert_from_path(pdf_file)
#     for i, image in enumerate(images):
#         image.save(f'{output_folder}/page_{i + 1}.jpg', 'JPEG')
#
# # Конвертация Excel в PDF
# def convert_excel_to_pdf(excel_file, output_file):
#     wb = load_workbook(excel_file)
#     ws = wb.active
#     pdf = canvas.Canvas(output_file)
#
#     for row in ws.iter_rows(values_only=True):
#         pdf.drawString(100, 750, str(row))
#         pdf.showPage()
#
#     pdf.save()
#
# # Конвертация PDF в Excel (упрощенный вариант, можно улучшить)
# def convert_pdf_to_excel(pdf_file, output_file):
#     reader = PdfReader(pdf_file)
#     wb = load_workbook(output_file)
#     ws = wb.active
#
#     for page in reader.pages:
#         ws.append([page.extract_text()])
#
#     wb.save(output_file)
#
# # Конвертация PowerPoint в PDF
# def convert_powerpoint_to_pdf(pptx_file, output_file):
#     presentation = Presentation(pptx_file)
#     pdf = canvas.Canvas(output_file)
#
#     for slide in presentation.slides:
#         for shape in slide.shapes:
#             if hasattr(shape, "text"):
#                 pdf.drawString(100, 750, shape.text)
#                 pdf.showPage()
#
#     pdf.save()
#
# # Сжатие PDF (пример)
# def compress_pdf(input_file, output_file):
#     reader = PdfReader(input_file)
#     writer = PdfWriter()
#
#     for page in reader.pages:
#         writer.add_page(page)
#
#     with open(output_file, 'wb') as f:
#         writer.write(f)
#
# # Запуск бота
# bot.polling()


import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from docx2pdf import convert as convert_word_pdf
from PIL import Image
from pdf2docx import Converter
import logging
import time  # Импорт для демонстрации прогресса (необязательно)

API_TOKEN = '7261178345:AAGYx1RSaukNFeBqrXuJb-_XJHZkducTenM'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(API_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()

    # Добавляем кнопку "Рестарт"
    restart_button = InlineKeyboardButton("Рестарт", callback_data="restart")
    markup.add(restart_button)

    bot.send_message(message.chat.id,
                     "Привет! Я бот для архивирования и конвертирования файлов. Вот что я умею:\n"
                     "1. Convert PDF to Word\n"
                     "2. Convert Word to PDF\n"
                     "3. Convert PDF to JPG\n"
                     "4. Convert JPG to PDF\n"
                     "Отправьте мне файл, и я помогу вам его обработать!",
                     reply_markup=markup)


# Обработчик документов
@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    file_name = message.document.file_name
    file_extension = os.path.splitext(file_name)[1].lower()

    # Сохранение файла
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Определение действия в зависимости от расширения файла
    try:
        if file_extension == '.pdf':
            output_file = 'output.docx'
            convert_pdf_to_word(message, file_name, output_file)

        elif file_extension == '.docx':
            output_file = 'output.pdf'
            convert_word_to_pdf(message, file_name, output_file)

        elif file_extension == '.jpg':
            output_file = 'output.pdf'
            convert_jpg_to_pdf(message, file_name, output_file)

    except Exception as e:
        logging.error(f"Ошибка при обработке файла {file_name}: {e}")
        bot.reply_to(message, "Произошла ошибка при обработке файла. Пожалуйста, попробуйте еще раз.")


def send_converted_file(chat_id, file_path):
    with open(file_path, 'rb') as file:
        bot.send_document(chat_id, file)


def convert_pdf_to_word(message, pdf_file, output_file):
    logging.info(f"Конвертация {pdf_file} в Word начинается...")

    # Отправляем начальное сообщение о прогрессе
    progress_message = bot.send_message(message.chat.id, "Конвертация PDF в Word... 0%")

    cv = Converter(pdf_file)
    total_pages = len(cv.get_page_list())

    for i in range(total_pages):
        cv.convert(output_file, start=i, end=i + 1)

        # Обновление сообщения о прогрессе
        progress_percent = int((i + 1) / total_pages * 100)
        bot.edit_message_text(f"Конвертация PDF в Word... {progress_percent}%", chat_id=message.chat.id,
                              message_id=progress_message.message_id)

    cv.close()
    bot.edit_message_text("Конвертация PDF в Word завершена.", chat_id=message.chat.id,
                          message_id=progress_message.message_id)
    send_converted_file(message.chat.id, output_file)


def convert_word_to_pdf(message, word_file, output_file):
    logging.info(f"Конвертация {word_file} в PDF начинается...")

    # Отправляем начальное сообщение о прогрессе
    progress_message = bot.send_message(message.chat.id, "Конвертация Word в PDF... 0%")

    convert_word_pdf(word_file, output_file)

    # Обновление сообщения о прогрессе (в данном случае только одно действие)
    bot.edit_message_text("Конвертация Word в PDF завершена.", chat_id=message.chat.id,
                          message_id=progress_message.message_id)
    send_converted_file(message.chat.id, output_file)


def convert_jpg_to_pdf(message, jpg_file, output_file):
    logging.info(f"Конвертация {jpg_file} в PDF начинается...")

    # Отправляем начальное сообщение о прогрессе
    progress_message = bot.send_message(message.chat.id, "Конвертация JPG в PDF... 0%")

    # Здесь можно добавить задержку для демонстрации (удалить в реальном приложении)
    time.sleep(2)  # Демонстрация длительности процесса

    image = Image.open(jpg_file)
    pdf_image = image.convert('RGB')
    pdf_image.save(output_file)

    bot.edit_message_text("Конвертация JPG в PDF завершена.", chat_id=message.chat.id,
                          message_id=progress_message.message_id)
    send_converted_file(message.chat.id, output_file)


# Обработчик для нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "restart":
        bot.answer_callback_query(call.id, "Перезапуск...")
        # Вызываем команду /start
        send_welcome(call.message)


# Запуск бота
bot.polling()
