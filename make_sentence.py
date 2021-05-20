import json
import random

# マルコフモデルの読み込み
dic = open("markov_chain_dic.json" , "r")
dic = json.load(dic)

# 文末と見做す文字
end_list = ["。", '？', '！']

# マルコフモデルから単語を出現頻度で重み付けした乱数で選択
def word_choice(sel, is_top):
    keys = sel.keys()
    if is_top:
        # 先頭の単語はランダムに選ぶ
        rand_key = random.choice(list(keys))
        return rand_key
    else:
        # 2番目以降の単語は出現頻度で重み付けした乱数で選択
        weights = list(sel.values()) # 3-gram内の次の単語の出現頻度
        dice = list(range(0, len(weights))) 
        rand_key_idx_list = random.choices(dice, k=1, weights=weights)
        rand_key_idx = rand_key_idx_list[0] # 要素数1のlistで得られるので[0]でアクセス
        return list(keys)[rand_key_idx]

# 文章生成
def make_sentence(dic):
    ret = []
    if not "@" in dic: return "no dic"
    top = dic["@"]
    w1 = word_choice(top, True)
    w2 = word_choice(top[w1], False)
    ret.append(w1)
    ret.append(w2)
    if w2 in end_list:
        # w2にマルコフモデル生成時の文末判定に使用した文字が来た場合、そこまでで文章生成
        return "".join(ret)
    else:
        while True:
            w3 = word_choice(dic[w1][w2], False)
            ret.append(w3)
            if w3 in end_list: break
            w1, w2 = w2, w3
        return "".join(ret)
    
if __name__ == "__main__":
    print(make_sentence(dic))




