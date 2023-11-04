from rest_framework.decorators import api_view
import MeCab


# 品詞の関数一覧


tagger = MeCab.Tagger(
    "-Ochasen")


def get_pos_detail(word):
    node = tagger.parse(word)
    if not node:
        return None, None

    items = node.split('\n')
    if len(items) < 1:
        return None, None

    parts = items[0].split('\t')
    if len(parts) < 4:
        return None, None

    features = parts[3].split('-')
    main_pos = features[0]
    sub_pos = features[1] if len(features) > 1 else None

    return main_pos, sub_pos


def get_pos(word):
    main_pos, _ = get_pos_detail(word)
    return main_pos

# 動詞判定


def is_verb_before_nai(word):
    return get_pos(word) == '動詞'


def is_verb_before_nai2(word):
    main_pos, sub_pos = get_pos_detail(word)
    return main_pos == '動詞' and sub_pos == '自立'
# 名詞判定


def is_noun(word):
    return get_pos(word) == '名詞'

# 代名詞判定


def is_pronoun(word):
    main_pos, sub_pos = get_pos_detail(word)
    return main_pos == '名詞' and sub_pos == '代名詞'

# 副詞判定


def is_Adverb(word):
    return get_pos(word) == '副詞'

# 助詞判定


def is_postposition(word):
    return get_pos(word) == '助詞'

# 形容詞判定


def is_adjective(word):
    return get_pos(word) == '形容詞'
