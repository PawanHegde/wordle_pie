import random
from dataclasses import dataclass
from enum import Enum
from typing import Counter, List, Set

from colorama import Back, Style


class State(Enum):
    NO_MATCH = Back.WHITE
    PARTIAL_MATCH = Back.YELLOW
    FULL_MATCH = Back.GREEN

    def __init__(self, background: Back):
        self.background = background


@dataclass
class DisplayLetter:
    value: str
    state: State


def get_five_letter_words() -> Set[str]:
    with open("/usr/share/dict/words", "r") as source:
        return {
            word.lower()
            for word in source.read().splitlines(keepends=False)
            if len(word) == 5
        }


def choose_a_random_word(words: Set[str]) -> str:
    return random.choice(tuple(words))


def get_a_valid_guess(words: Set[str]) -> str:
    # TODO: Should a user be allowed to try the same (incorrect) guess again?
    guess = None

    while guess is None or len(guess) != 5 or not is_a_valid_word(guess, words):
        guess = input("Guess a word: ")
        if len(guess) != 5:
            print("Please enter a 5 letter word.")
        elif not is_a_valid_word(guess, words):
            print("That word is not in our dictionary.")

    return guess


def is_a_valid_word(word: str, words: Set[str]) -> bool:
    return word in words


def compare(reference: str, candidate: str) -> List[DisplayLetter]:
    result: List[DisplayLetter] = [
        DisplayLetter(letter, State.NO_MATCH) for letter in candidate
    ]

    letters_yet_to_match = Counter(reference)

    # Green pass
    for result_letter, reference_letter, candidate_letter in zip(
        result, reference, candidate
    ):
        if reference_letter == candidate_letter:
            result_letter.state = State.FULL_MATCH
            letters_yet_to_match[reference_letter] -= 1

    # Yellow pass
    for result_letter, candidate_letter in zip(result, candidate):
        if (
            candidate_letter in letters_yet_to_match
            and letters_yet_to_match[candidate_letter] > 0
        ):
            result_letter.state = State.PARTIAL_MATCH
            letters_yet_to_match[candidate_letter] -= 1

    return result


def display(display_words: List[List[DisplayLetter]]) -> None:
    for word in display_words:
        for letter in word:
            print(f"{letter.state.value}{letter.value}{Style.RESET_ALL}", end="")
        print()


if __name__ == "__main__":
    words = get_five_letter_words()
    target = choose_a_random_word(words)

    # For display
    results_so_far = []

    # Provide at most 5 chances
    for _ in range(5):
        guess = get_a_valid_guess(words, results_so_far)
        result = compare(target, guess)
        results_so_far.append(result)
        display(results_so_far)

        if guess == target:
            print("You win!")
            break
    else:
        print(f"Better luck next time! The correct answer was {target}")
