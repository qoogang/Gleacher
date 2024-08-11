from openai import OpenAI
import random
import io
import sys

PROJECT_ID = "proj_7gUKR9cm7IQPCH3q2XVEBZAT"

client = OpenAI(
    organization="org-2TXEkGhl0FgvXtEqD5jVe4t8",
    project=PROJECT_ID,
)

def communicate(chat_history: list = None, jp_sentences: list = None) -> list:
    for _ in range(2):
        user_input = input("Enter your text: ")
        chat_history.append({"role": "user", "content": user_input})
    
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            max_tokens=300,
        )
        assistant_reply = response.choices[0].message.content
        print("AI Response:\n", assistant_reply, "\n")
        if "-a1-" in assistant_reply:
            pass
        elif "-a2-" in assistant_reply:
            print("y")
            jp_sentences += [
                    sen.split("日本語訳：")[-1].split("\n")[0]
                    for sen in assistant_reply.split("\n\u3000")
                    if "日本語訳" in sen
                ]

        chat_history.append({"role": "assistant", "content": assistant_reply})
    return jp_sentences

def improve(jp_sentences: list = None) -> None:
    # chosen = random.choice(jp_sentences)
    template = """
    に対する英語訳がこの後Promptとして入力されます。
    それが文法的に正しければ、"-a1-"と出力してください。正しくない所があれば、"-a2-"と出力し、
    それに続けて、改善文を出力してください。フォーマットは下記：
    [改善文]
    """
    for k in range(2):
        print("問題文：", jp_sentences[k])
        user_input = input("Enter your text: ")
        prompt = user_input +template 
        # chat_history.append({"role": "user", "content": prompt})
        chat_history = [{"role": "user", "content": prompt}]
    
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            max_tokens=300,
        )
        assistant_reply = response.choices[0].message.content
        print("AI Response:\n", assistant_reply, "\n")
        if "-a1-" in assistant_reply:
            pass
        elif "-a2-" in assistant_reply:
            print("y")
            jp_sentences += [
                    sen.split("日本語訳：")[-1].split("\n")[0]
                    for sen in assistant_reply.split("\n\u3000")
                    if "日本語訳" in sen
                ]

        # chat_history.append({"role": "assistant", "content": assistant_reply})
    # return jp_sentences

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
    (入力が英文の場合) 入力される英文に対して、改善の余地がある場合、改善された英文を出力してください。
    (日本語の場合) それに対する英文を出力してください。
    B. 上記 A. について、英語の例文と日本語訳のセットを最大で3つ出力してください。
　　    また、入力に文法的におかしいところがない、かつ、英文として成立していれば、"合否"の欄に"-a1-"を、
       改善点が挙げられるようであれば"-a2-"と出力してください。
       さらに、改善すべき点は、{grammer_list}のうち、どれに関連するか？"""
    default_input += """
    フォーマット (入力が英語の場合)：
    --- A ---
　  改善された文：{A}
    --- B ---
　  英文：{B}
　  日本語訳：{B}
　  英文：{B}
　  日本語訳：{B}
　  英文：{B}
　  日本語訳：{B}
　  合否：{B}
    フォーマット (入力が日本語の場合)：
    --- A ---
　  英語訳：{A}
    --- B ---
　  英文：{B}
　  日本語訳：{B}
　  英文：{B}
　  日本語訳：{B}
　  英文：{B}
　  日本語訳：{B}
　  合否：{B}
    """

    # inputs = """This is the pen. \n
    # Which country do you from? \n
    # """
    # stdin = sys.stdin
    # sys.stdin = io.StringIO(inputs)

    jp_sentences = []

    prompt = [{"role": "user", "content": default_input}]
    jp_sentences = communicate(prompt, jp_sentences)

    print(jp_sentences)

    print("latter")
    jp_sentences = improve(jp_sentences)

    # sys.stdin = stdin