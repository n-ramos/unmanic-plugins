#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import os

import PTN
import requests

from unmanic.libs.unplugins.settings import PluginSettings
from tmdbv3api import TMDb, Search

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


def get_tmdb_information(title):
    settings = Settings()
    tmdb = TMDb()
    tmdb.api_key = settings.get_setting("Tmdb API key")
    search = Search()
    tmdb.language = 'fr'
    logger.info("Torrent name search " + title)
    results = search.movies({"query": title})
    return results[0]


def format_notification_body(basename, tmdb_info):
    return {
        "basename": basename,
        "tdmb_name": tmdb_info.get('original_title'),
        "tmdb_id": tmdb_info.get('id')
    }


def on_postprocessor_task_results(data):
    settings = Settings()

    if data.get('task_processing_success'):
        source_data = data.get('source_data')
        file_name = source_data.get('basename')
        logger.info("Parse torrent name of " + file_name)
        torrent_parsed = PTN.parse(file_name)
        logger.info("Torrent name parsed " + torrent_parsed.get('title'))
        tmdb_info = get_tmdb_information(torrent_parsed.get('title'))
        logger.info("Sending notification")
        notify(settings.get_setting("Url Address"), settings.get_setting("HTTP Method"),
               format_notification_body(file_name, tmdb_info))

    return data
