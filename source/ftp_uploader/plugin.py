#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ftplib
import logging
import os
import PTN

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
    ftp = ftplib.FTP()
    ftp.connect(settings.get_setting('Ftp Host'), int(settings.get_setting('Ftp Port')))
    ftp.login(settings.get_setting('Ftp Username'), settings.get_setting('Ftp Password'))

    basename = os.path.basename(filename)
    basename_splitted = os.path.splitext(basename)
    basename_mp4 = "{}.{}".format(basename_splitted[0], 'mp4')
    foldername_mp4 = os.path.dirname(filename)
    source_filename = foldername_mp4 + "/" + basename_mp4
    dest_filename = PTN.parse(basename_splitted[0]).get('title')
    dest_filename = dest_filename.replace(".", "")
    dest_filename = dest_filename + ".mp4"

    logger.info("Upload file to ftp server source : " + source_filename + " destination file: " + dest_filename)
    file = open(source_filename, 'rb')  # file to send
    ftp.cwd(settings.get_setting('Destination folder'))
    ftp.storbinary('STOR ' + dest_filename, file)  # send the file
    logger.info("File uploaded successfully")
    file.close()  # close file and FTP
    ftp.quit()
    if settings.get_setting("Delete source file"):
        logger.info("Delete source file: " + source_filename)
        os.remove(source_filename)
        os.remove(source_filename.replace(settings.get_setting('Source Folder') + '/', "/library/"))


def on_postprocessor_task_results(data):
    if data.get('task_processing_success'):
        source_data = data.get('source_data')

        file_name = source_data.get('abspath')
        upload_to_ftp_server("/compiled" + file_name)

    return data
