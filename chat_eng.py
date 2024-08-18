from openai import OpenAI
import random
import io
import sys
from utils import load_openai_config
import pandas as pd
import os
from typing import Any, List
from logging import getLogger, ERROR


logger = getLogger(__name__)
logger.setLevel(ERROR)
logger.error("Starting the program...")


yaml_file = 'config.yaml'
organization, PROJECT_ID, OPENAI_API_KEY = load_openai_config(yaml_file)
if os.environ.get("OPENAI_API_KEY") is None:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

client = OpenAI(
    organization=organization,
    project=PROJECT_ID,
)

def communicate(chat_history: List = None, jp_sentences: List = None) -> List:
    for _ in range(2):
        user_input = input("Enter your text: ")
        chat_history.append({"role": "user", "content": user_input})
    
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            max_tokens=300,
        )
        assistant_reply = response.choices[0].message.content
        logger.error(f"AI Response:\n {assistant_reply} \n")
        if "-a1-" in assistant_reply:
            pass
        elif "-a2-" in assistant_reply:
            logger.error("y")
            # print(assistant_reply.split("\n\u3000")[0].split("日本語訳："))
            # breakpoint()
            jp_sentence = [
                    sen.split("日本語訳：")[-1].split("\n")
                    for sen in assistant_reply.split("\n")
                    if "日本語訳" in sen
                ]
            jp_sentences += [item[0] for item in jp_sentence]

        chat_history.append({"role": "assistant", "content": assistant_reply})
    return jp_sentences

def improve(jp_sentences: list = None) -> List:
    # chosen = random.choice(jp_sentences)
    template = """
    に対する英語訳がこの後Promptとして入力されます。
    それが文法的に正しければ、"-a1-"と出力してください。正しくない所があれば、"-a2-"と出力し、
    それに続けて、改善文を出力してください。フォーマットは下記：
    [改善文]
    """
    for k in range(len(jp_sentences)):
        logger.error(f"問題文： {jp_sentences[k]}")
        prompt = jp_sentences[k] + template 
        chat_history = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            max_tokens=300,
        )
        res_message = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": res_message})

        user_input = input("Enter your text: ")
        chat_history.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            max_tokens=300,
        )
        assistant_reply = response.choices[0].message.content
        logger.error(f"AI Response:\n {assistant_reply} \n")
        if "-a1-" in assistant_reply:
            pass
        elif "-a2-" in assistant_reply:
            logger.error("y")
            jp_sentences += [
                    sen.split("日本語訳：")[-1].split("\n")[0]
                    for sen in assistant_reply.split("\n\u3000")
                    if "日本語訳" in sen
                ]

        # chat_history.append({"role": "assistant", "content": assistant_reply})
    return jp_sentences

grammer_list = [
"冠詞", 
"名詞", 
"代名詞", 
"動詞", 
"形容詞", 
"副詞", 
"前置詞", 
"接続詞", 
"時制", 
"句と節", 
"感嘆詞",
"文型",
"態",
"仮定法",
"直接/間接話法",
]

if __name__ == "__main__":
    default_input = f"""
        以降、以下を実行してください。
        A.
          入力される英文書に対して、改善の余地がある場合、改善された英文を出力してください。(A-1)
          また、どう改善すべきか、アドバイスを書いてください。(A-2)
        B. 上記 A. について、類似する英語の例文とその日本語訳のセットを最大で3つ出力してください。
          また、Aが、入力に文法的におかしいところがない、かつ、英文として成立していれば、"合否"の欄に"-a1-"を、
          改善点が挙げられるようであれば"-a2-"と出力してください。
          さらに、改善すべき点は、{grammer_list}のうち、どれに関連するか？"""
    default_input += """
        フォーマット：
        --- A ---
        改善された文：{A}
        アドバイス：{A-2}
        --- B ---
        英文：{B}
        日本語訳：{B}
        英文：{B}
        日本語訳：{B}
        英文：{B}
        日本語訳：{B}
        合否：{B}
    """

    # class IoSwitch():
    #     def std2sio(self, inputs: str = None) -> Any:
    #         self.real_stdin = sys.stdin
    #         sys.stdin = io.StringIO(inputs)
    #         # self.real_stdout = sys.stdout
    #         # sys.stdout = io.StringIO()

    #     def sio2std(self) -> None:
    #         sys.stdin = self.real_stdin
    #         # sys.stdout = self.real_stdout

    inputs = """This is the pen. 
    We prefer 20th Tue. except for 2-3pm SGT. 19th Mon all day is also okay. 
    Which country do you from?
    Which country do you want to visit?
    this is a car. 
    which do you live in?
    what do you do?
    where do you from?
    """

    # ioswitcher = IoSwitch()
    # ioswitcher.std2sio(inputs)
    real_stdin = sys.stdin
    sys.stdin = io.StringIO(inputs)

    jp_sentences = []

    prompt = [{"role": "user", "content": default_input}]
    jp_sentences = communicate(prompt, jp_sentences)
    logger.error(jp_sentences)

    logger.error("latter")
    jp_sentences = improve(jp_sentences)

    # ioswitcher.sio2std()
    sys.stdin = real_stdin

    df = pd.DataFrame(jp_sentences, columns=["Japanese Sentences"])
    fn = 'output/jp_sentences.csv'
    if os.path.exists(fn):
        df_orig = pd.read_csv(fn)
        df = pd.concat([df_orig, df])
    df.to_csv(fn, index=False, encoding='utf-8-sig')
