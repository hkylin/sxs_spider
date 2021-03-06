#coding=utf-8
__author__ = 'xiyuanbupt'
import random
from threading import Thread,Event
import signal,sys

from scrapy import signals
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self,settings,user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'):
        super(RandomUserAgentMiddleware,self).__init__()
        self.user_agent = user_agent
        user_agent_list_file = settings.get('USER_AGENT_LIST')
        if not user_agent_list_file:
            ua = settings.get('USER_AGENT',user_agent)
            self.user_agent_list = [ua,]
        else:
            with open(user_agent_list_file,'r') as f:
                self.user_agent_list = [
                    line.strip() for line in f.readlines()
                ]

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        crawler.signals.connect(obj.spider_opened,signal = signals.spider_opened)
        return obj

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)

