import json
import ast
import logging
from datetime import datetime
from http.client import HTTPException

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from aiokafka import AIOKafkaConsumer
import certifi
import os
import asyncio
import jwt


class create_stream:
    def __init__(self, kafka_connection, mongo_connection=None, topicname="", timestamp_attr="timestamp"):
        self.topicname = topicname
        self.kafka_connection = kafka_connection
        self.mongo_connection = mongo_connection
        self.timestamp_attr = timestamp_attr
        self.stop_event = asyncio.Event()

    def is_epoch(self, timestamp):
        try:
            datetime.fromtimestamp(int(timestamp))
            return True
        except ValueError:
            return False

    async def _run(self, token):
        mongo_client = AsyncIOMotorClient(self.mongo_connection['uri'], server_api=ServerApi('1'),
                                          tlsCAFile=certifi.where())
        mongo_db = mongo_client[self.mongo_connection['database']]
        raw_data_collection = mongo_db[self.mongo_connection['rawcollection']]

        consumer = AIOKafkaConsumer(
            self.topicname,
            bootstrap_servers=self.kafka_connection["bootstrap.servers"],
            group_id=self.kafka_connection["group.id"],
            auto_offset_reset=self.kafka_connection["auto.offset.reset"],
            enable_auto_commit=self.kafka_connection['enable.auto.commit'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        await consumer.start()
        try:
            while not self.stop_event.is_set():
                msg = await consumer.getone()
                message_value = msg.value
                print(message_value)

                if self.timestamp_attr not in message_value:
                    print(
                        f"Error: Message does not contain the required timestamp attribute '{self.timestamp_attr}'. Skipping message.")
                    continue

                if self.is_epoch(message_value.get(self.timestamp_attr)):
                    if self.is_epoch(message_value.get(self.timestamp_attr)):
                        message_value[self.timestamp_attr] = int(message_value[self.timestamp_attr])
                    else:
                        message_value[self.timestamp_attr] = datetime.now().timestamp()

                await raw_data_collection.insert_one(message_value)
                print("Message received: {}".format(message_value))
        finally:
            await consumer.stop()

    async def start(self, token):
        if not hasattr(self, '_consumer_task') or self._consumer_task.done():
            self.stop_event.clear()
            self._consumer_task = asyncio.create_task(self._run(token))
            print('featurizerai: Started consumer task.')
        else:
            print("Task is already running. Cannot start it again.")

    async def stop(self):
        if hasattr(self, '_consumer_task') and not self._consumer_task.done():
            self.stop_event.set()
            await self._consumer_task
            print('featurizerai: Stopped consumer task.')
        else:
            print("Task is not running. Cannot stop it.")
