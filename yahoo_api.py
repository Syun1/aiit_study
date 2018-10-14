'''
YahooのOpenAPIであるキーフレーズ抽出APIを使用して、2016年の東京都知事選挙の候補者名の文章をリクエストURLに送り、
抽出したキーフレーズの結果を出力するGUIアプリケーション。
STARTボタンを押すと、キーフレーズ抽出APIが実行し、コマンドラインに各候補者の名称と検索スコアを出力する。
EXITボタンを押すと、プログラムが終了する。
'''

#coding: utf-8 
import sys
import urllib
import urllib2
import json
import Tkinter

def keyphrase(url, sentence, appid):
    sentence = urllib.quote_plus(sentence.encode("utf-8"))
    query = "%s?appid=%s&output=%s&sentence=%s" % (url, appid, "json", sentence)

    url_open = urllib2.urlopen(query)
    json_url = url_open.read()
    result = json.loads(json_url)

    return result

def print_result(event):
    url = "http://jlp.yahooapis.jp/KeyphraseService/V1/extract"
    appid = "dj0zaiZpPVFJbGhCRUFxdUVlNCZzPWNvbnN1bWVyc2VjcmV0Jng9ZTA-"
    sentence = u"小池百合子 増田寛也 鳥越俊太郎 マック赤坂 桜井誠 高橋しょうご 谷山ゆうじろう 山口敏夫 山中まさあき 後藤輝樹 岸本雅吉 上杉隆 七海ひろこ 中川ちょうぞう せきくち安弘 立花孝志 宮崎孝志 今尾貞夫 望月義彦 武井直子 内藤久遠"
    result = keyphrase(url, sentence, appid)
    
    for result, score in sorted(result.items(), key = lambda x:x[1], reverse=True):
         print(u"'%s' score: %s" % (result, score))

root = Tkinter.Tk()
root.title(u"Yahoo 検索スコア")
root.geometry("300x100")

Static = Tkinter.Label(text = u"Yahoo 都知事選挙候補者検索スコア")
Static.pack()

S_Button = Tkinter.Button(text = u"START")
S_Button.bind("<Button-1>", print_result)
S_Button.pack()

E_Button = Tkinter.Button(text = u"EXIT")
E_Button.bind("<Button-1>", sys.exit)
E_Button.pack()

root.mainloop()
