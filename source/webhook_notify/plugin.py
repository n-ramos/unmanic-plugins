#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import requests

from unmanic.libs.unplugins.settings import PluginSettings

# Configure plugin logger
logger = logging.getLogger("Unmanic.Plugin.webhook_notify")


class Settings(PluginSettings):
    settings = {
        "Url Address": "",
        "HTTP Method": "POST",
    }
    form_settings = {
        "HTTP Method": {
            "input_type":     "select",
            "select_options": [
                {
                    "value": 'GET',
                    "label": 'GET',
                },
                {
                    "value": 'POST',
                    "label": 'POST',
                },

            ],
            "label":  "Http Request Method",
        }
    }
def notify(url, method):
    if method == "POST" :
        result = requests.post(url, json={"pipeline_processed": True})
    else:
        result = requests.get(url)

def on_postprocessor_task_results(data):
    """
    Runner function - provides a means for additional postprocessor functions based on the task success.

    The 'data' object argument includes:
        task_processing_success         - Boolean, did all task processes complete successfully.
        file_move_processes_success     - Boolean, did all postprocessor movement tasks complete successfully.
        destination_files               - List containing all file paths created by postprocessor file movements.
        source_data                     - Dictionary containing data pertaining to the original source file.

    :param data:
    :return:
    
    """
    settings = Settings()

    if  data.get('task_processing_success'):
        notify(settings.get_setting("Url Address"), settings.get_setting("HTTP Method"))

    return data
