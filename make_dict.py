from janome.tokenizer import Tokenizer
import json

# テキストファイルを読み込む
sjis = open('original_sentence.txt', 'rb').read()
text = sjis.decode('utf_8')

# 文末と見做す文字
end_list = ["。", '？', '！']

# テキストを形態素解析
t = Tokenizer()
words = t.tokenize(text)
#for w in words:
#    print(w)

# マルコフモデルを生成
def make_dic(words):
    tmp = ["@"]
    dic = {}
    for i in words:
        word = i.surface #形態素を取り出す
        if word == "" or word == "\r\n" or word == "\n": continue # 空文字や改行を飛ばす
        tmp.append(word) # tmp配列に形態素を順次append
        if len(tmp) < 3: continue
        if len(tmp) > 3: tmp = tmp[1:] # tmpを見る場所を一つ次へずらす
        set_3_gram(dic, tmp)
        if word in end_list:
            # 文末を検出したらtmpを初期化して次へ
            tmp = ["@"]
            continue
    return dic

# 三要素のリストを入れ子のdictにする
# 3-gramのマルコフモデル生成
def set_3_gram(dic, s3):
    w1, w2, w3 = s3
    if not w1 in dic: dic[w1] = {}
    if not w2 in dic[w1]: dic[w1][w2] = {}
    if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0
    dic[w1][w2][w3] += 1

dic = make_dic(words)
json.dump(dic, open("markov_chain_dic.json", "w", encoding="utf-8"))
