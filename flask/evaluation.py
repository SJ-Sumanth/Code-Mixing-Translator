import nltk
from nltk.translate.bleu_score import sentence_bleu

intake = input("Enter the Reference Sentence")
nltk_tokens = nltk.sent_tokenize(intake)
assume = input("\nEnter the translated Sentence")
nltk_tokens1 = nltk.sent_tokenize(assume)
print('BLEU score -> {}'.format(sentence_bleu(nltk_tokens, nltk_tokens1)))

# Nenu kaaddi adagalanu