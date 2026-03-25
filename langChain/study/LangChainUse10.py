"""
长期会话记忆：FileChatMessageHistory类实现
核心思路：基于文件存储会话记录，以session_id为文件名，不同session_id有不同文件存储消息
继承BaseChatMessageHistory实现如下3个方法：
1.add_messages:同步模式，添加消息
2.messages:同步模式，获取消息
3.clear：同步模式，清除消息
"""
import os, json
from typing import Sequence
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        super(FileChatMessageHistory, self).__init__()
        self.session_id = session_id
        self.storage_path = storage_path
        # 完整的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)
        # 确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        # 将BaseMessage消息转为字典
        new_messages = [message_to_dict(message) for message in all_messages]
        # 将数据写入文件
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(new_messages, f,ensure_ascii=False,indent=4)

    @property
    def messages(self) -> list[BaseMessage]:
        # 当前文件内： list[字典]
        try:
            with open(self.file_path,"r",encoding="utf-8")as f:
                messages_data = json.load(f) # list[字典]
            return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


model = ChatTongyi(model="qwen3-max")

prompt = ChatPromptTemplate.from_messages( [
        ("system", "你需要根据会话历史回应用户问题。对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{now_input}")
    ]
)
str_parser = StrOutputParser()

# 增强打印：查看中间过程
def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*20)
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser


def get_history(session_id):
    return FileChatMessageHistory(session_id, "./resource/history/chat")


# 创建一个新的链，对原有链增强功能：自动附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain, # 被增强的原有chain
    get_history,    # 通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="now_input",  # 表示用户输入在模板中的占位符
    history_messages_key="chat_history" # 表示用户输入在模板中的占位符
)

if __name__ == '__main__':
    # 固定格式，添加LangChain的配置，为当前程序配置所属的session_id
    session_config = {
        "configurable":{
            "session_id":"user_001"
        }
    }
    # res = conversation_chain.invoke({"now_input":"小明有2个猫"},session_config)
    # print("第1次执行：", res)
    # res = conversation_chain.invoke({"now_input": "小刚有1只狗"}, session_config)
    # print("第2次执行：", res)
    res = conversation_chain.invoke({"now_input": "总共有几个宠物"}, session_config)
    print("第3次执行：", res)


