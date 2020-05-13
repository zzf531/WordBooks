import json
import time

a = {'translateResult': [[{'tgt': '玩', 'src': 'play'}]], 'errorCode': 0, 'type': 'en2zh-CHS', 'smartResult': {'entries': ['', 'n. 游戏；比赛；剧本\r\n', 'vt. 游戏；扮演；演奏；播放；同…比赛\r\n', 'vi. 演奏；玩耍；上演；参加比赛\r\n'], 'type': 1}}
b = {'translateResult': [[{'tgt': 'blogproject', 'src': 'blogproject'}]], 'errorCode': 0, 'type': 'en2zh-CHS'}


def format_word(fy):
    try:
        msg = fy.get('translateResult')[0][0]
        word = {}
        word['tgt'] = msg.get('tgt')
        word['src'] = msg.get('src')
        s = fy.get('smartResult')
        if s:
            e = fy.get('smartResult').get('entries')
            lis = []
            for i in e[1:]:
                a = i.replace("\r\n", "")
                lis.append(a)
            word['entries'] = lis
        word['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return word
    except TypeError as f:
        print('什么错误', f)
