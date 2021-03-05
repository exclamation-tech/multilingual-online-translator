# Requests to load page
# BeautifulSoup to parse page
# Sys to get command line arguments
import sys

import requests
from bs4 import BeautifulSoup


# Online Translator Class
class OnlineTranslator:
    def __init__(self, native_lang, translate_lang, translate_string):
        self.language_list = ["all", "arabic", "german", "english", "spanish", "french", "hebrew", "japanese", "dutch",
                              "polish", "portuguese", "romanian", "russian", "turkish"]
        self.native_lang = native_lang
        self.translate_lang = translate_lang
        self.translate_string = translate_string
        self.r = None

    def run(self):
        self.what_to_request()

    def what_to_request(self):
        if self.translate_lang == "all":
            self.request_all()
        elif self.translate_string in self.language_list:
            self.request(self.native_lang, self.translate_lang, self.translate_string)
        else:
            print(f"Sorry, the program doesn't support {self.translate_lang}")

    def request_all(self):
        for i in range(len(self.language_list) - 1):
            self.translate_lang = self.language_list[i + 1]
            if self.translate_lang == self.native_lang:
                pass
            else:
                self.request(self.native_lang, self.translate_lang, self.translate_string)

    def request(self, native, translate, string):
        try:
            self.r = requests.get(
                f"https://context.reverso.net/translation/{native}-{translate}/{string}",
                headers={'User-Agent': 'Mozilla/5.0'})
        except requests.ConnectTimeout:
            print("There's something wrong with the translation service. Please try again later.")
        except requests.ConnectionError:
            print("There's something wrong with your internet connection. "
                  "Please fix the problem and try again.")

        # If it succeeds, continue, if not, fail.
        if self.r:
            self.scrape()
        else:
            print(f"Unable to find a translation for {self.translate_string}. Please try again.")

    def scrape(self):
        soup = BeautifulSoup(self.r.content, 'html.parser')
        words = soup.find_all("a", {"class": "translation"})
        sentences = soup.find_all("div", {"class": ["src", "trg"]})
        self.output_to_file(list_text_cleaner(words), list_text_cleaner(sentences))

    def output_to_file(self, words_list, sentences_list):
        with open(f"{self.translate_string}.txt", "a+", encoding="utf-8") as file:
            file.write(f"{self.translate_lang} Translations:\n")
            for words in words_list:
                file.write(f"{words}\n")
            first_sentences = sentences_list[::2]
            second_sentences = sentences_list[1::2]
            file.write(f"\n{self.translate_lang} Examples:\n")
            for i in range(len(first_sentences)):
                file.write(f"{second_sentences[i]}:\n")
                file.write(f"{first_sentences[i]}\n\n")
            file.write("\n")
        self.output_to_console()

    def output_to_console(self):
        with open(f"{self.translate_string}.txt", "r", encoding="utf-8") as file:
            for line in file.read().split("\n"):
                print(line)


def list_text_cleaner(wordlist):
    output_list = []
    for words in wordlist:
        # Strips output
        words_stripped = words.text.strip("\n").strip()
        # If it contains content, then append
        if words_stripped:
            output_list.append(words_stripped)
    return output_list


if __name__ == "__main__":
    args = sys.argv
    OnlineTranslator(args[1], args[2], args[3]).run()
