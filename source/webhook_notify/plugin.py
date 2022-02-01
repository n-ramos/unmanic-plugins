#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging

import PTN
import requests

from unmanic.libs.unplugins.settings import PluginSettings


# Configure plugin logger
logger = logging.getLogger("Unmanic.Plugin.webhook_notify")


class Settings(PluginSettings):
    settings = {
        "Url Address": "",
        "HTTP Method": "POST",
        "Tmdb API key": ""
    }
    form_settings = {
        "HTTP Method": {
            "input_type": "select",
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
            "label": "Http Request Method",
        }
    }


def notify(url, method, data):
    if method == "POST":
        json_object = json.dumps(data, indent=4)
        result = requests.post(url, json={"pipeline_processed": True, "infos": json_object})
    else:
        result = requests.get(url)
    logger.info("Notification sended status code response: " + str(result.status_code))


def format_notification_body(basename):
    nomFichier = PTN.parse(basename)
    return {
        "basename": nomFichier.get('title') + ".mp4"
    }


def on_postprocessor_task_results(data):
    settings = Settings()

    if data.get('task_processing_success'):
        source_data = data.get('source_data')
        file_name = source_data.get('basename')

        logger.info("Sending notification")
        notify(settings.get_setting("Url Address"), settings.get_setting("HTTP Method"),
               format_notification_body(file_name))

    return data
