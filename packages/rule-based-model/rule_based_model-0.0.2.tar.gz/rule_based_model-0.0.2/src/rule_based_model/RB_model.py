from typing import List
import pickle
import pkg_resources

class RuleBasedSymbolExtractor:
    """
    Rule based model to detect company names
    """

    def __init__(self, exact_match_A, first_word, first_2word, first_3word) -> None:
        self.exact_match_A = exact_match_A
        self.first_word = first_word
        self.first_2word = first_2word
        self.first_3word = first_3word

    def get_result(self, text):
        symbol_list = self.get_symbols(text)
        symbol_list1 = self.get_symbol_with_indicator(text)

        result = []

        if symbol_list and symbol_list1:
            start_indices_1 = [symbol[0] for symbol in symbol_list]
            start_indices_2 = [symbol[0] for symbol in symbol_list1]
            unique_start_indices = list(set(start_indices_1 + start_indices_2))
            unique_start_indices.sort()

            for start_index in unique_start_indices:
                if start_index in start_indices_1 and start_index in start_indices_2:
                    idx1 = start_indices_1.index(start_index)
                    idx2 = start_indices_2.index(start_index)
                    if symbol_list[idx1][1] < symbol_list1[idx2][1]:
                        result.append(symbol_list[idx1])
                    else:
                        result.append(symbol_list1[idx2])
                elif start_index in start_indices_1:
                    idx1 = start_indices_1.index(start_index)
                    result.append(symbol_list[idx1])
                else:
                    idx2 = start_indices_2.index(start_index)
                    result.append(symbol_list1[idx2])
        elif symbol_list:
            result.extend(symbol_list)
        elif symbol_list1:
            result.extend(symbol_list1)

        return result

    def get_symbols(self, text: str) -> List[str]:  # , same_1st:list
        # remove punctuations
        text = " ".join(text.split())
        text_upper = text.upper()
        strip_s = [",", ".", "-", "?", "!", "»", "'", ":", ";", "´", "’"]
        symbols = []

        # find aker and its next word to decide if aker or aker something
        # the stock end with aksjen
        for item in self.exact_match_A.iter(text_upper):
            end_index = item[0]
            start_index = item[0] - len(item[1][1]) + 1
            # if the matched word in the first position
            if start_index == 0:
                test_word = text_upper[start_index : end_index + 2]
                for s in strip_s:
                    if s in test_word:
                        test_word = test_word.replace(s, "")
                test_word = test_word.strip()
                if test_word == item[1][1]:
                    # check for Norwegian
                    if test_word == "NORWEGIAN":
                        sep_norwegian = [
                            "DRILLING",
                            "OCEAN",
                            "BLOCK",
                            "ENERGY",
                            "CRUISE",
                            "CRYSTALS",
                            "PROPERTY",
                        ]
                        test_word2 = text_upper[end_index + 1 : end_index + 10].strip()
                        if not any(word in test_word2 for word in sep_norwegian):
                            symbols.append(
                                {
                                    "entities": (
                                        start_index,
                                        end_index + 1,
                                        "ORG",
                                        text[start_index : end_index + 1],
                                        item[1][2],
                                    ),
                                    "start_index": start_index,
                                }
                            )
                    else:
                        symbols.append(
                            {
                                "entities": (
                                    start_index,
                                    end_index + 1,
                                    "ORG",
                                    text[start_index : end_index + 1],
                                    item[1][2],
                                ),
                                "start_index": start_index,
                            }
                        )
                elif (test_word[-1] == "S") & (test_word[:-1] == item[1][1]):
                    symbols.append(
                        {
                            "entities": (
                                start_index,
                                end_index + 1,
                                "ORG",
                                text[start_index : end_index + 1],
                                item[1][2],
                            ),
                            "start_index": start_index,
                        }
                    )
            # if the matched word in the middle position
            elif start_index > 0 & end_index + 2 < len(text_upper):
                test_word = text_upper[start_index - 1 : end_index + 2]
                for s in strip_s:
                    if s in test_word:
                        test_word = test_word.replace(s, "")
                test_word = test_word.strip()
                if test_word == item[1][1]:
                    # check for Norwegian
                    if test_word == "NORWEGIAN":
                        sep_norwegian = [
                            "DRILLING",
                            "OCEAN",
                            "BLOCK",
                            "ENERGY",
                            "CRUISE",
                            "CRYSTALS",
                            "PROPERTY",
                        ]
                        test_word2 = text_upper[end_index + 1 : end_index + 10].strip()
                        if not any(word in test_word2 for word in sep_norwegian):
                            symbols.append(
                                {
                                    "entities": (
                                        start_index,
                                        end_index + 1,
                                        "ORG",
                                        text[start_index : end_index + 1],
                                        item[1][2],
                                    ),
                                    "start_index": start_index,
                                }
                            )
                    else:
                        symbols.append(
                            {
                                "entities": (
                                    start_index,
                                    end_index + 1,
                                    "ORG",
                                    text[start_index : end_index + 1],
                                    item[1][2],
                                ),
                                "start_index": start_index,
                            }
                        )
                elif (test_word[-1] == "S") & (test_word[:-1] == item[1][1]):
                    symbols.append(
                        {
                            "entities": (
                                start_index,
                                end_index + 1,
                                "ORG",
                                text[start_index : end_index + 1],
                                item[1][2],
                            ),
                            "start_index": start_index,
                        }
                    )
            # if the matched word in the last position
            elif end_index == len(text_upper):
                test_word = text_upper[start_index - 1 : end_index]
                for s in strip_s:
                    if s in test_word:
                        test_word = test_word.replace(s, "")
                test_word = test_word.strip()
                if test_word == item[1][1]:
                    # check for Norwegian
                    if test_word == "NORWEGIAN":
                        sep_norwegian = [
                            "DRILLING",
                            "OCEAN",
                            "BLOCK",
                            "ENERGY",
                            "CRUISE",
                            "CRYSTALS",
                            "PROPERTY",
                        ]
                        test_word2 = text_upper[end_index + 1 : end_index + 10].strip()
                        if any(word in test_word2 for word in sep_norwegian):
                            pass
                        else:
                            symbols.append(
                                {
                                    "entities": (
                                        start_index,
                                        end_index + 1,
                                        "ORG",
                                        text[start_index : end_index + 1],
                                        item[1][2],
                                    ),
                                    "start_index": start_index,
                                }
                            )
                    else:
                        symbols.append(
                            {
                                "entities": (
                                    start_index,
                                    end_index + 1,
                                    "ORG",
                                    text[start_index : end_index + 1],
                                    item[1][2],
                                ),
                                "start_index": start_index,
                            }
                        )
                elif (test_word[-1] == "S") & (test_word[:-1] == item[1][1]):
                    symbols.append(
                        {
                            "entities": (
                                start_index,
                                end_index + 1,
                                "ORG",
                                text[start_index : end_index + 1],
                                item[1][2],
                            ),
                            "start_index": start_index,
                        }
                    )

        symbols_sorted = sorted(symbols, key=lambda d: (d["start_index"], -d["entities"][1]))
        filtered_symbols = []
        prev_start_index = None

        for symbol in symbols_sorted:
            start_index = symbol["start_index"]
            if prev_start_index != start_index:
                filtered_symbols.append(symbol)
            prev_start_index = start_index

        res = [e["entities"] for e in filtered_symbols]
        if res:
            return res

    def get_symbol_with_indicator(self, text):
        # split sentences into words
        text = " ".join(text.split())
        splitted_sent = text.upper().split()
        strip_s = [",", ".", "?", "!", "»", "'", ":"]
        symbols_sorted = []
        # suffix list
        before_list = [
            "-AKSJE",
            "-AKSJEN",
            "-AKSJER",
            "-AKSJENE",
            "-RESULTATET",
            "-RESULTATENE",
            "-SELSKAP",
            "-SELSKAPET",
        ]
        # prefix list
        after_list = [
            "SELSKAP",
            "SELSKAPET",
            "BANKEN",
            "PRODUSENTEN",
            "OPPDRETTEREN",
            "NOTERTE",
        ]

        for count, word in enumerate(splitted_sent):
            # cut point of the orginal sentence and join them
            if word[-1] in strip_s:
                word = word[:-1]

            for sl in before_list:
                sl_length = len(sl)
                if word.endswith(sl):
                    test_names = self.generate_test_name_before(
                        count, word, splitted_sent
                    )
                    test_name1, test_name2, test_name3 = tuple(test_names[:3])
                    symbol = self.generate_symbol_before(
                        count,
                        splitted_sent,
                        text,
                        sl_length,
                        test_name1,
                        test_name2,
                        test_name3,
                    )
                    if symbol:
                        symbols_sorted.append(symbol)

            for pl in after_list:
                if word.endswith(pl):
                    test_names = self.generate_test_name_after(count, splitted_sent)
                    test_name1, test_name2, test_name3 = tuple(test_names[:3])
                    symbol = self.generate_symbol_after(
                        count,
                        word,
                        splitted_sent,
                        text,
                        test_name1,
                        test_name2,
                        test_name3,
                    )
                    if symbol:
                        symbols_sorted.append(symbol)

        symbols_sorted = sorted(symbols_sorted, key=lambda d: d["start_index"])
        return [e["entities"] for e in symbols_sorted] if symbols_sorted else None

    def generate_test_name_before(self, count, word, splitted_sent):
        # split the word with '-', e.g. NORWEGIAN-AKSJEN
        splitted = word.split("-")
        context_words = splitted_sent[max(0, count - 2) : count]
        context = " ".join(context_words)
        test_names = [None, None, None]
        for i in range(len(splitted) - 1):
            name = " ".join(splitted[: i + 1])
            if i == 0 and count >= 1:
                name = context_words[-1] + " " + name
            elif i > 0 and count >= 2:
                name = context + " " + name
            test_names[i] = name
        return tuple(test_names[:3])

    def generate_test_name_after(self, count, splitted_sent):
        test_name1 = test_name2 = test_name3 = None
        num_words_remaining = len(splitted_sent) - count - 1

        if num_words_remaining >= 1:
            test_name1 = " ".join(splitted_sent[count + 1 : count + 2])
        if num_words_remaining >= 2:
            test_name2 = " ".join(splitted_sent[count + 1 : count + 3])
        if num_words_remaining >= 3:
            test_name3 = " ".join(splitted_sent[count + 1 : count + 4])

        return test_name1, test_name2, test_name3

    def generate_symbol_before(
        self, count, splitted_sent, text, sl_length, *test_names
    ):
        symbol = None
        for test_name in test_names:
            for i, lst in enumerate(
                [self.first_word, self.first_2word, self.first_3word]
            ):
                if test_name in [item[0] for item in lst]:
                    sym = next((item[1] for item in lst if item[0] == test_name), None)
                    # cut point of the orginal sentence and join them
                    cut_p = " ".join(splitted_sent[: count - i])
                    start_index = len(cut_p) if count == 0 else len(cut_p) + 1
                    end_index = start_index + len(test_name) + sl_length
                    symbol = {
                        "entities": (
                            start_index,
                            end_index,
                            "ORG",
                            text[start_index:end_index],
                            sym,
                        ),
                        "start_index": start_index,
                    }
                    break
            if symbol is not None:
                break
        return symbol

    def generate_symbol_after(self, count, word, splitted_sent, text, *test_names):
        # cut point of the original sentence and join them
        cut_p = " ".join(splitted_sent[:count])
        start_index = len(word) + len(cut_p) + 2 if count > 0 else len(word) + 1
        symbol = None
        for test_name in test_names:
            for i, lst in enumerate(
                [self.first_word, self.first_2word, self.first_3word]
            ):
                if test_name in [item[0] for item in lst]:
                    sym = next((item[1] for item in lst if item[0] == test_name), None)
                    end_index = start_index + len(test_name)
                    symbol = {
                        "entities": (
                            start_index,
                            end_index,
                            "ORG",
                            text[start_index:end_index],
                            sym,
                        ),
                        "start_index": start_index,
                    }
                    break
            if symbol is not None:
                break
        return symbol


def get_symbol_extractor():
    match_A = _load_pickle_file('match_A.pkl')
    first_word = _load_pickle_file('first_word.pkl')
    first_2word = _load_pickle_file('first_2word.pkl')
    first_3word = _load_pickle_file('first_3word.pkl')
    return RuleBasedSymbolExtractor(match_A, first_word, first_2word, first_3word)

def _get_file_path(file_name):
    return pkg_resources.resource_filename('rule_based_model', file_name)

def _load_pickle_file(file_name):
    file_path = _get_file_path(file_name)
    with open(file_path, "rb") as f:
        return pickle.load(f)
