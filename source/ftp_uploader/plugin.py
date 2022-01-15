#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ftplib
import logging

from unmanic.libs.unplugins.settings import PluginSettings

# Configure plugin logger
logger = logging.getLogger("Unmanic.Plugin.ftp_uploader")


class Settings(PluginSettings):
    settings = {"Ftp Host": "",
                "Ftp Port": 21,
                "Ftp Username": "",
                "Ftp Password": "",
                "Source Folder": "",
                "Delete source file": True,
                "Destination folder": "/files"}

    def __init__(self):
        self.form_settings = {
            "Delete source file": {
                "label": "Delete source file",
            }
        }


def upload_to_ftp_server(filename):
    settings = Settings()
    ftp = ftplib.FTP_TLS()
    ftp.connect(settings.get_setting('Ftp Host'), int(settings.get_setting('Ftp Port')))
    ftp.login(settings.get_setting('Ftp Username'), settings.get_setting('Ftp Password'))
    ftp.prot_p()
    source_filename = "{}.{}".format(filename.split('.')[0], 'mp4')
    logger.info("Upload file to ftp server: " + source_filename)
    file = open(settings.get_setting('Source Folder') + '/' + source_filename, 'rb')  # file to send
    ftp.cwd(settings.get_setting('Destination folder'))
    ftp.storbinary('STOR ' + source_filename, file)  # send the file
    logger.info("File uploaded successfully")
    file.close()  # close file and FTP
    ftp.quit()


def on_postprocessor_task_results(data):
    if data.get('task_processing_success'):
        source_data = data.get('source_data')
        file_name = source_data.get('basename')
        upload_to_ftp_server(file_name)
    return data
