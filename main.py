import re
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.platform import AstrBotMessage
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.provider import LLMResponse
from openai.types.chat.chat_completion import ChatCompletion

@register("keyinterceptor", "Futureppo", "屏蔽获取不到model列表导致key泄露", "1.0.0")
class keyinterceptor(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.IsError_filter = self.config.get('iskeyinterceptor', True)
    
    @filter.on_decorating_result()
    async def on_decorating_result(self, event: AstrMessageEvent):
        result = event.get_result()
        message_str = result.get_plain_text()
        if self.IsError_filter:
            if '获取模型列表失败' in message_str:
                logger.info(message_str)
                event.stop_event() # 停止事件传递
