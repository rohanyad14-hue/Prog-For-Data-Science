"""Sample answer M1-Q3: an object-oriented student-support chatbot built with NLTK, ChatterBot, exceptions and suitable data structures."""
import logging
import os
import tempfile
from collections import Counter, deque
from dataclasses import dataclass

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

logging.disable(logging.CRITICAL)
os.chdir(tempfile.mkdtemp(prefix="sa_chatbot_"))


class EmptyQueryError(ValueError):
    """The user sent nothing usable."""


@dataclass
class Interaction:                                   # one line of the conversation history
    query: str
    answer: str
    source: str                                      # keywords / chatterbot / clarify / fallback / empty


class Preprocessor:                                  # NLTK: tokenise, remove stop words, stem
    def __init__(self):
        self.stop = set(stopwords.words("english"))
        self.stem = PorterStemmer().stem

    def keywords(self, text):
        if not text or not text.strip():
            raise EmptyQueryError("empty question")
        return {self.stem(t) for t in word_tokenize(text.lower()) if t.isalpha() and t not in self.stop}


class KnowledgeBase:                                 # frequently asked questions: dict + inverted index of sets
    def __init__(self, prep):
        self.prep = prep
        self.answers = {}                            # intent -> answer
        self.index = {}                              # keyword -> set of intents

    def add(self, intent, example_questions, answer):
        self.answers[intent] = answer
        for q in example_questions:
            for kw in self.prep.keywords(q):
                self.index.setdefault(kw, set()).add(intent)

    def rank(self, keywords):                        # how many query keywords point to each intent
        score = Counter()
        for kw in keywords:
            for intent in self.index.get(kw, ()):
                score[intent] += 1
        return score.most_common()


class SupportBot:
    UNKNOWN = "__unknown__"

    def __init__(self):
        self.prep = Preprocessor()
        self.kb = KnowledgeBase(self.prep)
        self.history = []                            # list of Interaction objects
        self.unanswered = Counter()                  # how often each unknown question was asked
        self.review_queue = deque()                  # unknown questions waiting for a human answer (FIFO)
        self.brain = ChatBot("SupportBot", storage_adapter="chatterbot.storage.SQLStorageAdapter", database_uri="sqlite:///bot.sqlite3",
                             logic_adapters=[{"import_path": "chatterbot.logic.BestMatch", "default_response": self.UNKNOWN,
                                              "maximum_similarity_threshold": 0.90}], read_only=True)
        self.trainer = ListTrainer(self.brain)

    def ask(self, text):
        try:
            words = self.prep.keywords(text)
        except EmptyQueryError:
            return self._log(text, "Please type your question.", "empty")
        ranked = self.kb.rank(words)
        if ranked and (len(ranked) == 1 or ranked[0][1] > ranked[1][1]):
            return self._log(text, self.kb.answers[ranked[0][0]], "keywords")
        if len(ranked) > 1:                          # two intents fit equally well: ask instead of guessing
            options = " or ".join(i for i, score in ranked if score == ranked[0][1])
            return self._log(text, f"Do you mean {options}?", "clarify")
        reply = self.brain.get_response(text).text   # nothing in the FAQ: try ChatterBot's stored conversations
        if reply != self.UNKNOWN:
            return self._log(text, reply, "chatterbot")
        self.unanswered[text] += 1
        if self.unanswered[text] == 1:
            self.review_queue.append(text)
        return self._log(text, "I do not know yet. A staff member will answer this question.", "fallback")

    def learn(self, question, answer):               # supervised learning: only reviewed answers are trained
        self.trainer.train([question, answer])

    def _log(self, query, answer, source):
        self.history.append(Interaction(query, answer, source))
        return answer


bot = SupportBot()
bot.kb.add("exams", ["When is the semester exam timetable?", "Exam dates and hall tickets"], "Exams start on 4 December. Hall tickets are on the student portal.")
bot.kb.add("courses", ["Which courses are offered?", "How do I register for a course?"], "Course registration is open on the student portal until 20 November.")
bot.kb.add("placements", ["Which companies visit for placement?", "How do I register for the placement drive?"], "Register for placements on the career portal.")
bot.trainer.train(["What are the library timings?", "The library is open from 9 am to 8 pm."])

for q in ["When are the exams?", "Tell me about placement companies", "Which courses and exams are there?", "   ",
          "What are the library timings?", "How is the weather on campus?"]:
    print(f"{q!r:<42} -> {bot.ask(q)}")

print("\n--- continuous learning with a human in the loop ---")
print("waiting for review:", list(bot.review_queue))
question = bot.review_queue.popleft()
bot.learn(question, "Please check the campus notice board for weather alerts.")
print(f"{question!r} -> {bot.ask(question)}")

print("\n--- statistics from the history ---")
print("answers by source:", dict(Counter(i.source for i in bot.history)))
print("keywords of 'Which courses and exams are there?':", sorted(bot.prep.keywords("Which courses and exams are there?")))
print("questions still unanswered:", dict(bot.unanswered), "| queue length:", len(bot.review_queue))
