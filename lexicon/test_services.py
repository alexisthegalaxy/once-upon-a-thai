import random
from typing import List
from lexicon.tests.grid_test import GrammarGridTest, SentenceGridTest
from lexicon.tests.tests import (
    EnglishFromSound4,
    EnglishFromSound6,
    ThaiFromSound6,
    ThaiFromSound4,
    EnglishFromThai6,
    EnglishFromThai4,
    ToneFromThaiAndSound,
    EnglishLetterFromThai4,
    ThaiLetterFromEnglish4,
    EnglishLetterFromThai16,
    ThaiLetterFromEnglish16,
    ThaiLettersFromSound4,
)
from lexicon.items import Letter


def can_be_tested_on_tone(word: "Word"):
    return "-" not in word.split_form


def pick_sentence_test(
    al,
    chosen_word: "Word",
    learning=False,
    test_success_callback=None,
    test_failure_callback=None,
):
    """
    Returns TappingTestSentence or SentenceGridTest or None if no sentence
    """
    can_be_selected_sentences: List["Sentence"] = []
    for sentence in chosen_word.get_sentences():
        sentence_can_be_learnt = True
        for word in sentence.words:
            if word.get_total_xp() < 5:
                sentence_can_be_learnt = False
        if sentence_can_be_learnt:
            can_be_selected_sentences.append(sentence)
    if len(can_be_selected_sentences) > 0:
        sentence = random.choice(can_be_selected_sentences)

        r = random.randint(0, 20)  # can be 0, ..., n-1
        if r == 0:
            from lexicon.tests.tapping_test_sentence import TappingTestSentence

            test = TappingTestSentence(
                al,
                correct=chosen_word,
                sentence=sentence,
                learning=learning,
                test_success_callback=test_success_callback,
                test_failure_callback=test_failure_callback,
            )
        else:
            test = SentenceGridTest(
                al,
                correct=chosen_word,
                sentence=sentence,
                learning=learning,
                test_success_callback=test_success_callback,
                test_failure_callback=test_failure_callback,
            )
        # else:
        #     test = GrammarGridTest(
        #         al,
        #         correct=chosen_word,
        #         sentence=sentence,
        #         learning=learning,
        #         test_success_callback=test_success_callback,
        #         test_failure_callback=test_failure_callback,
        #     )
    else:
        test = None
    return test


def pick_a_test_for_word(al, chosen_word, test_success_callback=None, test_failure_callback=None):
    test = None
    can_be_tested_on_sentence = True
    while test is None:
        r = random.randint(0, 16)  # can be 0, ..., n-1   (15)
        from lexicon.tests.tests import ThaiFromEnglish6, ThaiFromEnglish4

        if r == 0:
            test = ThaiFromEnglish4(al, correct=chosen_word, test_success_callback=test_success_callback, test_failure_callback=test_failure_callback)
        elif r == 1:
            test = ThaiFromEnglish6(al, correct=chosen_word, test_success_callback=test_success_callback, test_failure_callback=test_failure_callback)
        elif r == 2:
            test = EnglishFromSound4(al, correct=chosen_word, test_success_callback=test_success_callback, test_failure_callback=test_failure_callback)
        elif r == 3:
            test = EnglishFromSound6(al, correct=chosen_word, test_success_callback=test_success_callback, test_failure_callback=test_failure_callback)
        elif r == 4:
            test = ThaiFromSound4(al, correct=chosen_word, test_success_callback=test_success_callback, test_failure_callback=test_failure_callback)
        elif r == 5:
            test = ThaiFromSound6(al, correct=chosen_word, test_success_callback=test_success_callback, test_failure_callback=test_failure_callback)
        elif r == 6:
            test = EnglishFromThai4(al, correct=chosen_word, test_success_callback=test_success_callback, test_failure_callback=test_failure_callback)
        elif r == 7:
            test = EnglishFromThai6(al, correct=chosen_word, test_success_callback=test_success_callback, test_failure_callback=test_failure_callback)
        elif r == 8 or r == 9:
            if can_be_tested_on_tone(chosen_word):
                test = ToneFromThaiAndSound(al, correct=chosen_word, test_success_callback=test_success_callback, test_failure_callback=test_failure_callback)
        else:
            if can_be_tested_on_sentence:
                test = pick_sentence_test(al, chosen_word, test_success_callback=test_success_callback, test_failure_callback=test_failure_callback)
                if not test:
                    can_be_tested_on_sentence = False
    al.active_test = test


def pick_a_test_for_letter(al, chosen_letter):
    test = None
    while test is None:
        r = random.randint(0, 6)  # can be 0, ..., n-1   (5)
        if r == 0:
            test = EnglishLetterFromThai4(al, letter=chosen_letter)
        elif r == 1:
            test = ThaiLetterFromEnglish4(al, correct=chosen_letter)
        elif r == 2:
            test = EnglishLetterFromThai16(al, letter=chosen_letter)
        elif r == 3:
            test = ThaiLetterFromEnglish16(al, correct=chosen_letter)
        else:
            word_containing_letter = Letter.get_readable_word_containing_letter(
                chosen_letter
            )
            if word_containing_letter:
                test = ThaiLettersFromSound4(
                    al, correct=chosen_letter, word=word_containing_letter
                )
            else:
                test = ThaiLetterFromEnglish16(al, correct=chosen_letter)
    al.active_test = test


def pick_a_test_for_thai_word(
    al, chosen_word, test_success_callback=None, test_failure_callback=None
) -> None:
    """
    Here, the learner saw the word in thai already,
    so we don't want to ask the Thai word from English, for example
    """
    test = None
    can_be_tested_on_sentence = True
    while test is None:
        r = random.randint(0, 20)  # can be 0, ..., n-1
        if r == 0:
            test = EnglishFromSound4(
                al,
                correct=chosen_word,
                test_success_callback=test_success_callback,
                test_failure_callback=test_failure_callback,
            )
        elif r == 1:
            test = EnglishFromSound6(
                al,
                correct=chosen_word,
                test_success_callback=test_success_callback,
                test_failure_callback=test_failure_callback,
            )
        elif r == 2:
            test = EnglishFromThai4(
                al,
                correct=chosen_word,
                test_success_callback=test_success_callback,
                test_failure_callback=test_failure_callback,
            )
        elif r == 3:
            test = EnglishFromThai6(
                al,
                correct=chosen_word,
                test_success_callback=test_success_callback,
                test_failure_callback=test_failure_callback,
            )
        else:
            if can_be_tested_on_sentence:
                test = pick_sentence_test(
                    al,
                    chosen_word,
                    test_success_callback=test_success_callback,
                    test_failure_callback=test_failure_callback,
                )
                if not test:
                    can_be_tested_on_sentence = False
    al.active_test = test


def pick_a_test_for_english_word(
    al, chosen_word, test_success_callback=None, test_failure_callback=None
):
    """
    Here, the learner saw the word in english already,
    so we don't want to ask the English word from Thai, for example
    """
    test = None
    can_be_tested_on_sentence = True
    while test is None:
        r = random.randint(0, 20)  # can be 0, ..., n-1
        from lexicon.tests.tests import ThaiFromEnglish6, ThaiFromEnglish4

        if r == 0:
            test = ThaiFromEnglish4(
                al,
                correct=chosen_word,
                test_success_callback=test_success_callback,
                test_failure_callback=test_failure_callback,
            )
        elif r == 1:
            test = ThaiFromEnglish6(
                al,
                correct=chosen_word,
                test_success_callback=test_success_callback,
                test_failure_callback=test_failure_callback,
            )
        elif r == 2:
            test = ThaiFromSound4(
                al,
                correct=chosen_word,
                test_success_callback=test_success_callback,
                test_failure_callback=test_failure_callback,
            )
        elif r == 3:
            test = ThaiFromSound6(
                al,
                correct=chosen_word,
                test_success_callback=test_success_callback,
                test_failure_callback=test_failure_callback,
            )
        else:
            if can_be_tested_on_sentence:
                test = pick_sentence_test(
                    al,
                    chosen_word,
                    test_success_callback=test_success_callback,
                    test_failure_callback=test_failure_callback,
                )
                if not test:
                    can_be_tested_on_sentence = False
    al.active_test = test
