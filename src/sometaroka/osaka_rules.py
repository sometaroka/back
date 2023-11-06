
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import TranslatedText
from .serializers import TranslatedTextSerializer
from .part_of_speech import is_verb_before_nai, is_verb_before_nai2, is_pronoun, is_noun, is_postposition, is_adjective, is_Adverb
import gspread
import MeCab
from oauth2client.service_account import ServiceAccountCredentials
import gspread.exceptions

# 大阪弁の翻訳


@api_view(['POST'])
def translate_text_osaka(request):
    input_text = request.data.get("text", "")
    # MeCabを使って文章を単語に分割
    mecab = MeCab.Tagger(
        "-Ochasen ")
    parsed_lines = mecab.parse(input_text).split('\n')
    words = [line.split('\t')[0]
             for line in parsed_lines if line and line != 'EOS']

    # 単語ごとに変換処理を行う
    # ・方針
    # {
    # [１]先に助詞や助動詞などの変換処理おこなう（例：だめ、今日はゲームはしない！→だめ、今日はゲームはしいひん！）
    # [２]変換したあとにスプレッドシートの対応表をもとに形容詞や名詞などの単語を変換する（例：あかん、今日はゲームはしいひん！）
    # 　”注意！！”定義するときは必ずif,elifにする。elseだと無差別に変換してしまう。
    # なぜ、「ない」や「だ」などの定義を行っているかというと、「ない」や「だ」etcは色々なパターンの変換が考えられるから、
    # スプレッドシートで一つの対応表にしてしまうと自然な翻訳が行えない
    # }

    processed_words = []
    i = 0
    while i < len(words):
        word = words[i]

    # 「だっ」の処理
        if word == "だっ":
            # そうだった→そうやった
            word = "やっ"
    # 「よ」の変換
        if word == "よ":
            if i+1 < len(words) and (words[i+1] == "ね" or words[i+1] == "な"):
                if words[i-1] == "てる":
                    # もしその動詞が「てる」なら、「てんな」
                    # 計画してるよね→計画してるやんな
                    word = "てるやんな"
                    processed_words.pop()
                    i += 1

                elif words[i-1] == "いる":
                    word = "てるやんな"
                    processed_words.pop()
                    processed_words.pop()
                    i += 1

                else:
                    word = "やんな"
                    i += 1  # 「ね」の削除

            if is_verb_before_nai(words[i-1]) or words[i-1] == "ない":
                # 直前が動詞、「ない」の場合、「よ」を「で」に変換
                # 動詞：違うよ→違うで
                # 「ない」：そうじゃないよ→そうじゃないで

                if i >= 4 and (words[i-4] == "に" or words[i-3] == "に"):
                    # 例：楽しみにしてるよ→楽しみにしてるわ
                    if words[i-1] == "てる":
                        # もしその動詞が「てる」なら、「てんな」
                        # 計画してるよ→計画してんで
                        word = "てるわ"
                        i += 1

                    if words[i-1] == "いる":
                        word = "てるわ"

                if i >= 4 and (words[i-4] == "たり" or words[i-3] == "たり"):
                    # 例：計画したりしてるよ→計画したりしてんねん

                    if words[i-1] == "てる":
                        # もしその動詞が「てる」なら、「てんな」
                        # 計画してるよ→計画してんで
                        word = "てんねん"
                        processed_words.pop()

                    if words[i-1] == "いる":
                        word = "てんねん"
                        processed_words.pop()
                        processed_words.pop()
                        i += 1

                elif words[i-1] == "てる":
                    # もしその動詞が「てる」なら、「てんな」
                    # 計画してるよ→計画してんねん
                    if words[i-2] == "て":
                        processed_words.pop()
                        word = "んねん"
                    elif words[i-2] == "し":
                        word = "てんで"
                        processed_words.pop()
                    else:
                        word = "てんねん"
                        processed_words.pop()
                        i += 1

                elif words[i-1] == "いる":
                    if words[i-2] == "て":
                        processed_words.pop()
                        word = "んねん"
                    elif words[i-2] == "し":
                        word = "てんで"
                        processed_words.pop()
                    else:
                        word = "てんねん"
                        processed_words.pop()
                        i += 1

                elif words[i-1] == "みる":
                    word = "わ"

                elif words[i-1] == "し":
                    pass
                elif words[i-1] == "くれ":
                    word = "や"
                else:
                    word = "で"

            elif is_adjective(words[i-1]):
                if i+1 < len(words) and (words[i+1] == "ね" or words[i+1] == "な"):
                    word = "やんな"
                else:
                    word = "で"

            # 「ね」の処理
            if i+1 < len(words) and (words[i+1] == "ね" or words[i+1] == "な"):
                if is_verb_before_nai(words[i-2]) or is_Adverb(words[i-1]):
                    # 「よね」で、二個前が動詞or直前が代名詞のとき「よ」を「やんな」に変換
                    word = "やんな"
                    i += 1  # 「ね」の削除

                elif is_noun(words[i-1]):
                    # 直前が名詞のとき、「よ」を「やね」に変換

                    word = "やな"
                    i += 1  # 「ね」の削除

            elif is_noun(words[i-1]):
                # 直前が名詞なら変換
                # 例：天才よ→天才やで
                word = "やで"

            if words[i-1] == "た":
                # 直前が「た」のとき「た」を「で」に変換
                # 例：言ったよ→言ったで
                if words[i-2] == "て":
                    word = "とったで"
                    processed_words.pop()
                    processed_words.pop()
                elif words[i-2] == "だっ":
                    word = "た"
                    processed_words.pop()
                else:
                    word = "で"
            elif is_pronoun(words[i-1]) and (i+1 < len(words) and (words[i-1] != "なん" or words[i-1] != "何")):
                # 直前が代名詞のとき「よ」を「や」に変換
                word = "や"

    # 「ない」の変換処理
        if word == "ない":
            if words[i-1] == "し":
                # 直前が「し」の場合、「ない」を「しいひん」に変更
                # 勉強しない→勉強しいひん
                word = "しいひん"
                processed_words.pop()
            elif is_verb_before_nai(words[i-1]) or words[i-1] == "やら":
                if i+1 < len(words) and is_verb_before_nai(words[i-1]) and words[i+1] == "ん":
                    word = "へん"
                    i += 1
                else:
                    word = "ん"

      # 「だよ」の変換処理
        if word == "だ":
            if i < len(words) - 1 and words[i+1] == "よ":
                # 「だよね」、「だよな」の処理
                if i+2 < len(words) and (words[i+2] == "ね" or words[i+2] == "な"):
                    if is_noun(words[i-1]) or is_Adverb(words[i-1]) or is_postposition(words[i-1]) or is_adjective(words[i-1]):
                        if words[i-2] == "ない":
                            word = "ねんな"
                            i += 2
                        elif words[i-1] == "ん" and words[i-2] == "な":
                            # 好きなんだよね→好きやねんな
                            word = "やねんな"
                            processed_words.pop()
                            processed_words.pop()
                            i += 2
                        elif words[i-1] == "ん" and words[i-2] == "た":
                            word = "てんな"
                            processed_words.pop()
                            processed_words.pop()
                            i += 2
                        else:
                            word = "やんな"
                            i += 1
                            i += 1
                    # 直前が名詞、副詞、助詞の場合、「だよ」を「やで」に変更
                    elif is_pronoun(words[i-1]) and (i+1 < len(words) and (words[i-1] != "だれ" or words[i-1] != "誰" or words[i-1] != "なん" or words[i-1] != "何")) or (i+3 < len(words) and (words[i+3] == "?" or words[i+3] == "？")):
                        word = "やんな"
                        i += 1
                        i += 1

                    elif is_Adverb(words[i-1]):
                        word = "やんな"
                        i += 1
                        i += 1
                    elif i == 0 or words[i-1] == "。" or words[i-1] == "、" or words[i-2] == ":" or words[i-1] == "." or words[i-1] == "," or words[i-1] == "：":
                        # だよね単
                        word = "やんな"
                        i += 1
                        i += 1

                    else:
                        word = "ねん"
                        i += 1
                        i += 1
                        if processed_words:
                            processed_words.pop()

                elif words[i-1] == "ん":
                    # 直前が「ん」でその前が「な」の場合、「だよ」を「やねん」に変換
                    # 例：そうなんだよ→そうやねん
                    if words[i-2] == "な":
                        if i < len(words) - 2 and (words[i+2] == "ね" or words[i+2] == "な"):
                            word = "やねんな"
                            processed_words.pop()  # 「ん」の削除
                            processed_words.pop()  # 「な」の削除
                            i += 1  # 「よ」を削除
                            i += 1  # 「よ」を削除

                        else:
                            word = "やねん"
                            processed_words.pop()  # 「ん」の削除
                            processed_words.pop()  # 「な」の削除
                            i += 1  # 「よ」を削除

                    elif words[i-2] == "た" and words[i-3] != "なかっ":
                        # 直前が「ん」でその前が「た」の場合、「だよ」を「てん」に変換
                        # 例：行ったんだよ→行ってん
                        word = "てん"
                        processed_words.pop()  # 「ん」の削除
                        processed_words.pop()  # 「た」の削除
                        i += 1  # 「よ」を削除

                    elif words[i-1] == "ん" and words[i-2] != "な":
                        # 直前が「ん」の場合、「だよ」を「ねん」に変更し、「ん」を削除
                        # 例：遊園地に行くんだよ→遊園地に行くねん
                        if words[i-2] == "いる":
                            # 二個前が「いる」のとき「てんねん」に変換
                            # 例：そうしているんだよ→そうしてんねん
                            word = "てんねん"
                            processed_words.pop()
                            processed_words.pop()
                            processed_words.pop()
                            i += 1

                        elif words[i-2] == "てる":
                            # 二個前が「てる」のとき「てんねん」に変換
                            # 例：そうしてるんだよ→そうしてんねん
                            word = "てんねん"
                            processed_words.pop()
                            processed_words.pop()
                            i += 1
                            if i < len(words) - 2 and (words[i+2] != "？" or words[i+2] != "?"):
                                i += 1
                        elif words[i-2] == "ある":
                            word = "あんねん"
                            processed_words.pop()
                            processed_words.pop()
                            i += 1
                            i += 1
                        elif words[i-2] == "そうした":
                            word = "そうしてん"
                            processed_words.pop()
                            processed_words.pop()
                            i += 1

                        else:
                            word = "ねん"
                            processed_words.pop()  # 直前の「ん」を削除
                            i += 1  # 「よ」を削除
                            i += 1  # 「よ」を削除

                # 代名詞の処理
                elif is_pronoun(words[i-1]):
                    # 直前が代名詞の場合、「だよ」を「やねん」に変更
                    # 例：だれだよ→だれやねん、なんだよ→なんやねん
                    if words[i-1] == "だれ" or words[i-1] == "誰" or words[i-1] == "なん" or words[i-1] == "何":
                        word = "やねん"
                        i += 1  # 「よ」を削除
                    elif i+1 < len(words) and (words[i-1] != "だれ" or words[i-1] != "誰" or words[i-1] != "なん" or words[i-1] != "何"):
                        # 「だれ」、「何」は「やんな」に変換
                        word = "や"
                        i += 1  # 「よ」を削除

                    else:
                        word = "やで"
                        i += 1  # 「よ」を削除
                # 「だめ」の処理
                elif words[i-1] == "だめ":
                    # 直前が「だめ」の場合、「だ」を「で」に変換
                    # 例：だめだよ→あかんで
                    word = "で"
                    i += 1

                elif is_noun(words[i-1]) or is_Adverb(words[i-1]) or is_postposition(words[i-1]) or is_adjective(words[i-1]):
                    # 直前が名詞、副詞、助詞の場合、「だよ」を「やで」に変更
                    # 名詞：天才だよ→天才やで
                    # 副詞：そうだよ→そうやで
                    # 助詞：積極的にだよ→積極的にやで
                    # 形容詞：奇麗だよ→奇麗やで
                    if words[i-1] == "なんで":
                        word = "やねん"
                        i += 1  # 「よ」を削除
                    else:
                        word = "やで"
                        i += 1  # 「よ」を削除

      # 「だ」の処理
            else:
                if words[i-1] == "だめ":
                    # 直前が「だめ」の場合、「だ」を「で」に変換
                    # 例：だめだ→あかんで
                    word = "で"
                if i+1 < len(words) and words[i+1] == "っけ":
                    word = "や"
                # elif i+1 < len(words) and words[i+1] == "けど":
                #     #そこなんだけど→そこなんやけど
                #     word = "てん"
                #     processed_words.pop()
                #     processed_words.pop()
                elif words[i-1] == "ん" and words[i-2] == "た" and i+1 < len(words) and words[i+1] != "けど":
                    if i+1 < len(words) and (words[i+1] == "？" or words[i+1] == "?"):
                        word = "たん"
                        processed_words.pop()  # 「ん」の削除
                        processed_words.pop()  # 「た」の削除
                    elif words[i-3] == "なかっ":
                        word = "へんかってん"
                        processed_words.pop()
                        processed_words.pop()

                    else:
                        word = "てん"
                        processed_words.pop()  # 「ん」の削除
                        processed_words.pop()  # 「た」の削除
                        i += 1

                elif is_verb_before_nai(words[i-3]):
                    # 三個前の単語が動詞なら「だ」を「のや」に変換
                    # 例：なんで開かないんだ→なんで開かへんのや
                    if words[i-2] == "てる":
                        # もしその動詞が「し」なら「てんねん」に変換
                        # 計画してるんだ→計画してんねん
                        word = "てんねん"
                        processed_words.pop()
                        processed_words.pop()
                    else:
                        word = "のや"
                        processed_words.pop()
                elif words[i-2] == "いる":
                    # 二個前の単語が「いる」の場合「てんねん」に変換
                    # 例：そうしているんだ→そうしてんねん
                    word = "てんねん"
                    processed_words.pop()
                    processed_words.pop()
                    processed_words.pop()

                # 「だね：だね」の処理；なぜか「あれ」が変換できない
                elif i+1 < len(words) and (words[i+1] == "ね" or words[i+1] == "な"):
                    if is_noun(words[i-1]) or is_Adverb(words[i-1]) or is_postposition(words[i-1]) or is_adjective(words[i-1]):
                        if is_pronoun(words[i-1]) and (words[i-1] == "だれ" or words[i-1] == "誰" or words[i-1] == "なん" or words[i-1] == "何"):
                            word = "や"
                            i += 1
                        else:
                            word = "やな"
                            i += 1
                elif is_noun(words[i-3]) and words[i-2] == "な":
                    word = "やねん"
                    processed_words.pop()
                    processed_words.pop()
                elif words[i-1] == "ん" and (is_verb_before_nai(words[i-2]) or is_adjective(words[i-2])):
                    processed_words.pop()
                    word = "ねん"

                elif words[i-2] == "な" or is_noun(words[i-1]) or is_Adverb(words[i-1]) or is_postposition(words[i-1]) or is_adjective(words[i-1]) or is_pronoun(words[i-1]):
                    # 直前が「な」、名詞、副詞、助詞、代名詞の場合、「だ」を「や」に変更
                    # な：そうなんだ→そうなんや
                    # 名詞：天才だ→天才や
                    # 副詞：そうだ→そうや
                    # 助詞：積極的にだ→積極的にや
                    # 形容詞：奇麗だ→奇麗や
                    # 代名詞：だれだ→だれや
                    word = "や"

    # 「ね（な）」の処理
        if word == "ね" or word == "な" and (words[i-1] == "よ"):
            if is_adjective(words[i-1]):
                # 直前が形容詞の場合、「ね」を「なぁ」に変更
                # 形容詞：かわいいね→かわいいなぁ
                # 形容詞：悪いね→悪いなぁ
                word = "なぁ"
            elif words[i-1] == "でる":
                # 「でる」：混んでるね→混んでんなぁ
                word = "でんなぁ"
                processed_words.pop()  # 「でる」の削除

            elif is_verb_before_nai(words[i-1]):
                # 直前の単語が動詞の場合、「ね」を「で」に変換
                # 例：行くね→行くで
                if words[i-1] == "てる":
                    # もしその動詞が「てる」なら、「てんな」
                    # 知ってるね→知ってんねんな
                    word = "てんねんな"
                    processed_words.pop()
                elif words[i-1] == "いる":
                    word = "てんねんな"
                    processed_words.pop()
                    processed_words.pop()

                else:
                    word = "で"
            if words[i-4] == "に" or words[i-3] == "に":
                # 例：楽しみにしてるね→楽しみにしてるな
                if words[i-1] == "てる":
                    # もしその動詞が「てる」なら、「てんな」
                    # 計画してるよ→計画してんで
                    word = "てるわ"
                    i += 1

                if words[i-1] == "いる":
                    word = "てるわ"

            if words[i-3] == "てる":
                # もしその動詞が「てる」なら、「てんな」
                # 計画してるんだね→計画してんねんな
                word = "てんねんな"
                processed_words.pop()

            if words[i-3] == "いる":
                word = "てんねんな"
                processed_words.pop()

            if words[i-4] == "てる":
                # もしその動詞が「てる」なら、「てんな」
                # 計画してるんだよね→計画してるんやんな
                word = "てるんやんな"
                processed_words.pop()

            if words[i-4] == "いる":
                word = "てるんやんな"
                processed_words.pop()

            if words[i-1] == "みる":
                word = "わ"

            if word == "ね" and is_Adverb(words[i-1]):
                word = "やね"

    # 「ないか」の処理
        if word == "か" and words[i-1] == "ない" and words[i-3] != "ん" and words[i-4] != "ない":
            # 「か」かつ直前が「ない」の場合、「か」を「やんけ」に変更
            # 例：言ったじゃないか→言ったやんけ
            if i+1 < len(words) and (words[i+1] != "ね" or words[i+1] != "な"):
                pass
            else:
                word = "やんけ"
                processed_words.pop()  # ないの削除
                processed_words.pop()  # じゃの削除

    # 「じゃん」の処理
        if word == "じゃん":
            if words[i-1] == "ない" or is_verb_before_nai(words[i-1]) or is_verb_before_nai(words[i-2]) or is_noun(words[i-1]) or is_Adverb(words[i-1]) or is_postposition(words[i-1]) or is_adjective(words[i-1]):
                # 直前の単語が「ない」,動詞,名詞,副詞,助詞,形容詞,の場合、「じゃん」を「やん」に変換
                # 「ない」：そうじゃないじゃん→そうじゃないやん
                # 動詞：行くじゃん→行くやん、言ったじゃん→言ったやん
                # 名詞：天才じゃん→天才やん
                # 副詞：そうじゃん→そうやん
                # 助詞：積極的にじゃん→積極的にやん
                # 形容詞：奇麗じゃん→奇麗やん
                word = "やん"

    # 「た」の処理
        if word == "た":
            if i+1 < len(words) and words[i+1] == "の":
                if i+2 < len(words) and (words[i+2] == "?" or words[i+2] == "？"):
                    # 「たの」で二個後が「？」のとき「た」を「たん」に変換
                    # 例：言ってたの？→言ってたん？
                    word = "たん"
                    i += 1
                elif words[i-1] == "て":
                    word = "とった"
                    processed_words.pop()
                elif words[i-1] == "い" and words[i-2] == "て":
                    # されていたのがよかった→されとったのが良かった
                    word = "とった"
                    processed_words.pop()
                    processed_words.pop()
                elif words[i-1] == "経っ" and (i+2 < len(words) and words[i+2] == "か"):
                    word = "経つん"
                    processed_words.pop()
                    i += 1

                elif i+2 < len(words) and (words[i+2] == "か" or words[i+2] == "は"):
                    word = "たん"
                    i += 1

                else:
                    # 「たの」の場合、「た」を「てん」に変換
                    word = "てん"
                    i += 1

            elif is_verb_before_nai(words[i-2]):
                if i+1 < len(words) and (words[i+1] == "?" or words[i+1] == "？"):
                    # 「た」で1個後が「？」のとき「た」を「たん」に変換
                    # 例：言ってた？→言ってたん？
                    word = "たん"
                elif words[i-1] == "し" and words[i-2] == "ま" or (words[i-1] == "まし"):
                    # 直前が「ま」＋「し」または「まし」のとき変換を行わない→敬語表現はそのまま
                    # しました→しました
                    word = "た"

                elif i+1 < len(words) and is_noun(words[i+1]):
                    pass

                elif i+1 < len(words) and words[i+1] == "まし":
                    pass
                else:
                    word = "てん"

    # 「いるの」or「るの」の処理
        if word == "の":
            if words[i-1] == "てる":
                if i+1 < len(words) and (words[i+1] == "?" or words[i+1] == "？"):
                    word = "てんの"
                    processed_words.pop()

                # 例：走ってるの→走ってんの
                else:
                    word = "てんねん"
                    processed_words.pop()

            elif words[i-1] == "いる":
                if i+1 < len(words) and (words[i+1] == "?" or words[i+1] == "？"):
                    word = "んの"
                    processed_words.pop()

                else:
                    # 例：走っているの→走ってんの
                    word = "てんねん"
                    processed_words.pop()
                    processed_words.pop()

            elif words[i-1] == "な":
                if i+1 < len(words) and (words[i+1] == "?" or words[i+1] == "？"):
                    # 例：そうなの？→そうなん？
                    word = "ん"
                elif i+1 < len(words) and words[i+1] == "ね":
                    # 「なのね」のとき変換
                    # 例：そうなのね→そうなんやね
                    word = "んやね"
                    i += 1
                else:
                    # そうなの→そうやねん
                    word = "やねん"
                    processed_words.pop()

            elif i+1 < len(words) and words[i+1] == "ね":
                # 「の」の次が「ね」のとき「んやね」に変換
                # 例：そうなんね→そうなんやね
                word = "んやね"
                i += 1

            elif is_verb_before_nai(words[i-1]):
                if i+1 < len(words) and (words[i+1] == "?" or words[i+1] == "？"):
                    # 例：違うの？→違うん？
                    word = "ん"
                elif i == len(words)-1:
                    # 「の」が最後の文字列のとき「の」を「ねん」に変換
                    # 例：違うの→違うねん
                    word = "ねん"

            elif words[i-1] == "ない":
                word = "ねん"

        # 「あげる」の処理

        # 「～しようか」
    # 「ある」
    #     if word == "ある":
    #         if i+1 < len(words) and (words[i+1] == "か" and words[i+2] == "な"):

    # 例外まとめ
        # if word == "みる":
        #     if i+1 < len(words) and (words[i+1] == "?" or words[i+1] == "？"):
        #         word =
        if word == "で" and words[i-1] == "過ぎる":
            word = "過ぎんねん"
            processed_words.pop()
        if word == "みよ":
            if i+1 < len(words) and words[i+1] == "う" and words[i+2] == "か":
                # 言ってみようか→言ってみよか
                i += 1
        if word == "から":
            if words[i-1] == "た" and words[i-2] == "て":
                # 言ってたから→言っとったから
                word = "とったから"
                processed_words.pop()
                processed_words.pop()
        if word == "を":
            if words[i-1] == "な" or words[i-1] == "ね":
                pass
            else:
                word = ""
        if word == "ので":
            # 例：しまったので→しまったんで
            word = "んで"
        # if word == "する":
        #     if is_noun(words[i-1])  :
        #         word = "しとる"
        if word == "なかっ":
            if i+4 < len(words) and words[i+1] == "た" and words[i+2] == "ん" and words[i+3] == "だ" and words[i+4] == "よ":
                if words[i-1] == "良く" or words[i-1] == "よく":
                    word = "あかんかってんな"
                    processed_words.pop()
                    i += 5
                else:
                    word = "なかってん"
                    i += 4

                if i+5 < len(words) and (words[i+5] == "な" or words[i+5] == "ね"):
                    word = "なかってん"
                    i += 5
            if i+1 < len(words) and words[i+1] == "た":
                if words[i-1] == "良く" or words[i-1] == "よく":
                    word = "あかんかった"
                    i += 1
                    processed_words.pop()
                else:
                    word = "なかってん"
                    i += 1

        if word == "ちゃっ":
            if i+1 < len(words) and words[i+1] == "て":
                word = "てもうて"
                i += 1
            else:
                word = "てもうた"
                i += 1
        if word == "じゃ":
            word = "や"
        if word == "その":
            if i+1 < len(words) and words[i+1] == "とき":
                word = "そん"
        if word == "する":
            if i+1 < len(words) and (words[i+1] == "ね" or words[i+1] == "な"):
                word = "するわ"
                i += 1
        if word == "しまう":
            word = "まう"
        # if word == "そう" and i == 0 or (words[i-1] == "。" or words[i-1] == "、"):
        #     if i+1 < len(words) and words[i+1] == "だ" and words[i+2] != "よ":
        #         word = "せ"
        #     elif i+2 < len(words) and (words[i+1] == "だ" and (words[i+2] == "ね" or words[i+2] == "な")):
        #         word = "せ"
        if word == "ある":
            if i+1 < len(words) and words[i+1] == "ん":
                word = "あん"
        if word == "欲":
            if i+1 < len(words) and words[i+1] == "深い":
                word = "がめつい"
                i += 1
            elif i+1 < len(words) and words[i+1] == "深く":
                word = "がめつく"
                i += 1
        if word == "だらし":
            if i+1 < len(words) and words[i+1] == "ない":
                word = "ずぼら"
                i += 1
        if word == "で":
            if i+1 < len(words) and words[i+1] == "は" and words[i+2] == "ない":
                word = "とちゃう"
                i += 1
                i += 1
        if word == "じゃ":
            if i+1 < len(words) and words[i+1] == "ない":
                word = "や"
        if word == "束ね" and words[i-1] == "て":
            word = "くくっ"
        if word == "つまずい" and (words[i-2] == "足" or words[i-2] == "手" or words[i-2] == "首" or words[i-1] == "足" or words[i-1] == "手" or words[i-1] == "首"):
            if i+1 < len(words) and (words[i+1] == "た" or words[i+1] == "て"):
                word = "ぐねっ"
        if (word == "Y" or word == "y") and (i+1 < len(words) and (words[i+1] == "シャツ" or words[i+1] == "しゃつ")):
            word = "カッターシャツ"
            i += 1
        if word == "刺さ":
            if words[i-1] == "虫" or words[i-2] == "虫":
                word = "かま"
        if word == "つまみ" and words[i-1] == "お":
            word = "おつまみ"
            processed_words.pop()
        if word == "途中":
            if words[i-1] == "帰る":
                word = "帰りしな"
                processed_words.pop()
            elif words[i-1] == "行く":
                word = "行きしな"
                processed_words.pop()
        if word == "失" or word == "な":
            if i+1 < len(words) and words[i+1] == "くし":
                word = "どっか行っ"
                i += 1
        if word == "捨て":
            if i+1 < len(words) and words[i+1] == "ない" and words[i+2] == "で":
                if i+3 < len(words) and (words[i+3]) == "おい":
                    word = "ほかさんといて"
                    i += 1
                    i += 1
                    i += 1
                    i += 1
                else:
                    word = "ほかさんといて"
                    i += 1
                    i += 1
        if word == "どう":
            if i+1 < len(words) and (words[i+1] == "？" or words[i+1] == "?"):
                word = "どお"
        if word == "かけ" and (words[i-1] == "パーマ" or words[i-2] == "パーマ"):
            word = "あて"
        if word == "わたし" or word == "私":

            word = "うち"
        if word == "の" and i+1 < len(words) and words[i+1] == "家":
            word = "んち"
            i += 1
        if word == "ほど" and i+1 < len(words) and words[i+1] == "ほど":
            word = "大概"
            i += 1
        # if word == "な" and i+1 < len(words) and words[i+1] == "ん" and words[i+2] == "だ":
        #     word = "や"
        if word == "失敗":
            if i+1 < len(words) and words[i+1] == "し":
                word = "しくっ"
                i += 1
            elif i+1 < len(words) and words[i+1] == "さ":
                word = "しくら"
                i += 1
            elif i+1 < len(words) and words[i+1] == "する":
                word = "しくじる"
                i += 1

        processed_words.append(word)
        i += 1

    # Google Sheetsの認証とアクセス
    # APIが利用可能を超えて止められることがある。翻訳はかなりの量を行うのでAPI以外の方法を検討する
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'hougen-trans-6d7e0d024d8d.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(
        '166R1W9WwkelPu861pCQkjIfsmWF7xuIrqUy4BpB_ixY').sheet1

    # マッピングの取得
    translations = sheet.get_all_records()

    # スプレッドシートの変換を行う
    translated_sentence = []
    for word in processed_words:
        translated_word = word  # デフォルトでは元の単語を使用

        for item in translations:
            if word == item['標準語']:
                translated_word = item['大阪弁']
                break

        translated_sentence.append(translated_word)

        # 翻訳後の文章を結合
    translated_text = ' '.join(translated_sentence)

    translation_instance = TranslatedText(
        original_text=input_text, translated_text=translated_text)
    translation_instance.save()

    serializer = TranslatedTextSerializer(translation_instance)

    return Response(serializer.data)
