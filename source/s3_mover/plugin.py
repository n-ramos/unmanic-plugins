#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


import boto3
from boto3.s3.transfer import TransferConfig
from unmanic.libs.unplugins.settings import PluginSettings

# Configure plugin logger
logger = logging.getLogger("Unmanic.Plugin.s3_store")


class Settings(PluginSettings):
    settings = {
        "Bucket Name": "",
        "Endpoint Url": "",
        "Aws Access key": "",
        "Aws Secret Key": ""
    }


def multi_part_upload_with_s3(basename, bucket_name, endpoint_url, access_key, secret_key):

    file_path = '/library/' + basename
    s3 = boto3.client(
        's3',
        use_ssl=True,
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    transfer = boto3.s3.transfer.TransferConfig()
    init_transfer = boto3.s3.transfer.S3Transfer(client=s3, config=transfer)
    init_transfer.upload_file(file_path, bucket_name, basename)


def on_postprocessor_task_results(data):
    settings = Settings()
    if data.get('task_processing_success'):
        source_data = data.get('source_data')
        file_name = source_data.get('basename')
        multi_part_upload_with_s3(file_name,
                                  settings.get_setting('Bucket Name'),
                                  settings.get_setting('Endpoint Url'),
                                  settings.get_setting('Aws Access key'),
                                  settings.get_setting('Aws Secret Key')

                                  )
    return data
