# from ftplib import FTP
# import os
#
# ftp_params = {
#     'host': '77.222.57.185',  # Указать адрес FTP-сервера SpaceWeb
#     'port': 21,
#     'user': 'cubarrvgma_ftp',       # Ваш FTP-логин
#     'passwd': 'Post2564'      # Ваш FTP-пароль
# }

# #подключаемся к серверу
# ftp = FTP()
# ftp.connect(ftp_params['host'])
# ftp.login(ftp_params['user'], ftp_params['passwd'])
#
# local_file_path = 'spaceweb/spruce.jpg'
#
# remote_file_path = '/spruce.jpg'
#
# #бинарный
# with open(local_file_path, 'rb') as file:
#     # Загружаем файл на FTP-сервер SpaceWeb
#     ftp.storbinary(f'STOR {remote_file_path}', file)
#
# ftp.quit()
#
# print("Фотография успешно загружена.")