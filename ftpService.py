from ftplib import FTP, error_perm
import os
from dotenv import load_dotenv
from io import BytesIO


class FtpService:
    def __init__(self):
        try:
            load_dotenv()
            self.ftp = FTP()
            self.config = {
                "host": os.getenv("FTP_HOST"),
                "user": os.getenv("FTP_USER"),
                "passwd": os.getenv("FTP_PASSWD")
            }
        except error_perm as e:
            print(f"FTP Error: {e}")

    def connect(self):
        try:
            self.ftp.connect(self.config["host"])
            self.ftp.login(self.config["user"], self.config["passwd"])
        except error_perm as e:
            print(f"FTP Error: {e}")

    def disconnect(self):
        if self.ftp:
            self.ftp.quit()

    def save_file(self, file, file_index):
        try:
            self.connect()
            _, file_extension = os.path.splitext(file.filename)
            remote_file_path = '/' + str(file_index) + file_extension.lower()
            print(f'файл {remote_file_path}')
            self.ftp.storbinary(f'STOR {remote_file_path}', file)

            self.disconnect()
        except error_perm as e:
            print(f"FTP Error: {e}")

    def get_file(self, file_id):
        try:
            self.connect()

            file_list = self.ftp.nlst('/')
            matching_files = [file for file in file_list if file_id in file]
            if len(matching_files) == 1:
                remote_path = matching_files[0]
                buffer = BytesIO()
                self.ftp.retrbinary(f'RETR {remote_path}', buffer.write)
                file_data = buffer.getvalue()
            else:
                print(f"Файл <{id}> не найден или найдено более одного совпадения.")
                return None

            self.disconnect()

            return {"file_data": file_data, "remote_path": remote_path}
        except error_perm as e:
            print(f"FTP Error: {e}")
