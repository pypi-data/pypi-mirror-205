import pprint
import re
from typing import Callable

import zhipuai


def punctuation_converse_auto(msg):
    punkts = [
        [",", "，"],
        ["!", "！"],
        [":", "："],
        [";", "；"],
        ["\?", "？"],
    ]
    for item in punkts:
        msg = re.sub(r"([\u4e00-\u9fff])%s" % item[0], r"\1%s" % item[1], msg)
        msg = re.sub(r"%s([\u4e00-\u9fff])" % item[0], r"%s\1" % item[1], msg)
    return msg


def prepare_print_diff(nextStr: Callable[[any], str], printError: Callable[[], None]):
    previous = ""

    def print_diff(input):
        nonlocal previous
        str = nextStr(input)
        if not str.startswith(previous):
            last_line_index = str.rfind("\n") + 1
            if previous.startswith(str[0:last_line_index]):
                print("\r%s" % str[last_line_index:], end="", flush=True)
            else:
                print()
                print(1, "[[previous][%s]]" % previous)
                printError(input)
        else:
            print(str[len(previous):], end="", flush=True)
        previous = str

    return print_diff


if __name__ == "__main__":
    zhipuai.api_key = ""
    zhipuai.api_base = "https://test-maas.aminer.cn/stage-api/paas/v3/model-api"
    response = zhipuai.APIResource.query_async_invoke_result("1014907516268634316357633")
    print(response)
    '''
    response = zhipuai.APIResource.invoke(
        model="title-creation",
        prompt="新闻 炸裂",
        topP=1,
        topK=3,
        temperature=1,
        presencePenalty=1,
        frequencyPenalty=1,
        generatedLength=128,
    )

    print(response)


    '''
'''
client = zhipuai.APIResource.sse_invoke(model="chatGLM_6b_SSE", prompt="你都可以做些什么事",
                                        history=[{"query": "你好", "answer": "我是人工智能助手"},
                                                 {"query": "你叫什么名字", "answer": "我叫chatGLM"}]
                                        )
print_diff = prepare_print_diff(lambda e: e.data, lambda e: pprint.pprint(e.__dict__))
print()
print('Response: ')
for event in client.events():
    if (event.data):
        event.data = punctuation_converse_auto(event.data)
    if (event.event == "add"):
        print_diff(event)
    elif (event.event == "error"):
        print_diff(event)
    elif (event.event == "finish" or event.event == "interrupted"):
        print_diff(event)
    elif (event.event == "finish"):
        print_diff(event)
        print()

    else:
        pprint.pprint(event)
print("-----finished--------")
'''