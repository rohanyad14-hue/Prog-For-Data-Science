"""Notes M1: ChatterBot behaviour - training, matching and confidence (ChatterBot 1.2.x)."""
import logging

from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.trainers import ListTrainer

logging.disable(logging.CRITICAL)

bot = ChatBot("Demo", storage_adapter="chatterbot.storage.SQLStorageAdapter", database_uri="sqlite:///notes_cb.sqlite3",
              logic_adapters=[{"import_path": "chatterbot.logic.BestMatch", "default_response": "Sorry, I do not know that.",
                               "maximum_similarity_threshold": 0.90}], read_only=True)
trainer = ListTrainer(bot)
trainer.train(["Hi", "Hello! How can I help?",
               "What are the mess timings?", "Breakfast 7:30-9:00, lunch 12:30-2:00, dinner 7:30-9:00.",
               "Who is the warden?", "The warden office is in Block A."])

print("--- retrieval, not generation: the reply is a stored answer to the closest stored question ---")
for msg in ["Hi", "what are the mess timing", "who is the warden", "tell me a joke", "asdf qwerty"]:
    r = bot.get_response(msg)
    print(f"{msg!r:<28} -> {r.text!r:<62} confidence={r.confidence:.2f}")

print("\n--- the similarity measure used to find the closest known statement ---")
from chatterbot.conversation import Statement
from chatterbot.languages import ENG
cmp = LevenshteinDistance(ENG)
for a, b in [("what are the mess timings", "what are the mess timing"), ("what are the mess timings", "who is the warden")]:
    print(f"{a!r} vs {b!r}: {cmp.compare(Statement(a), Statement(b)):.2f}")
print("storage: SQLite file holds statements; trainers: ListTrainer here, ChatterBotCorpusTrainer for ready-made corpora")
