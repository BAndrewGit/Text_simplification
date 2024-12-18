import logging
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet
from wordfreq import top_n_list

nltk.download('punkt')
nltk.download('wordnet')

valid_words = set(top_n_list('en', 50000))

def load_banned_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    banned_words = content.split()
    return set(banned_words)

# Example usage
banned_words = load_banned_words('banned_words.txt')
print(banned_words)

def get_synonym(word, context, banned_words):
    if word[0].isupper():
        return word
    synonyms = wordnet.synsets(word)
    for syn in synonyms:
        for lemma in syn.lemmas():
            synonym = lemma.name()
            if synonym != word and synonym in valid_words and synonym.lower() not in banned_words:
                return synonym
    return word

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text)

def preserve_punctuation(original_sentence, simplified_sentence):
    match = re.search(r'[.!?]$', original_sentence)
    if match:
        punctuation = match.group(0)
        if not re.search(r'[.!?]$', simplified_sentence):
            simplified_sentence += punctuation
    return simplified_sentence

def capitalize_sentence(sentence):
    return sentence[0].upper() + sentence[1:] if sentence else sentence

def simplify_sentence(sentence, pipeline, banned_words):
    try:
        paraphrased = pipeline(f"paraphrase: {sentence}", max_length=30, num_return_sequences=1)
        if paraphrased and 'generated_text' in paraphrased[0]:
            paraphrased_sentence = paraphrased[0]['generated_text']
            paraphrased_sentence = re.sub(r'^(paraphrasis|paraphrase)\s*', '', paraphrased_sentence, flags=re.IGNORECASE)
            words = word_tokenize(paraphrased_sentence)
            simplified_words = [get_synonym(word, sentence, banned_words) for word in words if word.lower() not in banned_words]
            cleaned_sentence = clean_text(' '.join(simplified_words))
            final_sentence = preserve_punctuation(sentence, cleaned_sentence)
            final_sentence = capitalize_sentence(final_sentence)
            return final_sentence
    except Exception as e:
        logging.error(f"Error in simplifying sentence: {e}")
    return sentence

def simplify_text(text, pipeline, banned_words):
    sentences = sent_tokenize(text)
    simplified_sentences = [simplify_sentence(sentence, pipeline, banned_words) for sentence in sentences]
    return ' '.join(simplified_sentences)