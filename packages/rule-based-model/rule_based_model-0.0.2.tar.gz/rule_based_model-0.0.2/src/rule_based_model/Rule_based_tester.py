import time
import pickle
import ahocorasick

# import spacy

from RB_model import RuleBasedSymbolExtractor, get_symbol_extractor

# from text_processing.text_processing import remove_misleading_string


start_time = time.time()

# load automation and fuzzy match list
# with open("src/name_detection/match_A.pkl", "rb") as f:
#     match_A = pickle.load(f)

# with open("src/name_detection/first_word.pkl", "rb") as f:
#     first_word = pickle.load(f)

# with open("src/name_detection/first_2word.pkl", "rb") as f:
#     first_2word = pickle.load(f)

# with open("src/name_detection/first_3word.pkl", "rb") as f:
#     first_3word = pickle.load(f)

test_text = """
Nordic Mining bykser opp ni\xa0prosent takket være Arne Fredly og Ketil Skorstad som tegnet seg for totalt tjugofem millioner aksjer.
"""

se = get_symbol_extractor()
# se = RuleBasedSymbolExtractor(match_A, first_word, first_2word, first_3word)

# print(se.exact_match_A.get("NORDIC MINING"))

res = se.get_result(test_text)
print(res)

cons_time = time.time() - start_time

print("Time consumed ", cons_time)
