import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize
from utils.text_processing import simplify_text

def get_sentence_vector(sentence, ft, valid_words):
    words = word_tokenize(sentence)
    word_vectors = [ft.get_word_vector(word) for word in words if word in valid_words]
    if not word_vectors:
        return np.zeros(ft.get_dimension())
    return np.mean(word_vectors, axis=0)

def cosine_similarity_score(vec1, vec2):
    return cosine_similarity([vec1], [vec2])[0][0]

def calculate_bleu(reference, hypothesis):
    smoothie = SmoothingFunction().method4
    return sentence_bleu([reference], hypothesis, smoothing_function=smoothie)

def evaluate_model(data, ft, valid_words, pipeline, banned_words):
    total_bleu_score = 0
    for entry in data:
        original_text = entry["normal"]
        simplified_text = simplify_text(original_text, pipeline, banned_words)
        original_vector = get_sentence_vector(original_text, ft, valid_words)
        simplified_vector = get_sentence_vector(simplified_text, ft, valid_words)
        similarity_score = cosine_similarity_score(original_vector, simplified_vector)
        similarity_percentage = f"{similarity_score * 100:.2f}%"

        reference = word_tokenize(entry["simplified"][0])
        hypothesis = word_tokenize(simplified_text)
        bleu_score = calculate_bleu(reference, hypothesis)
        total_bleu_score += bleu_score

        print(f"Text original: {original_text}")
        print(f"Text simplificat: {simplified_text}")
        print(f"Scor de similitudine: {similarity_percentage}")
        print(f"BLEU score: {bleu_score:.4f}\n")

    average_bleu_score = total_bleu_score / len(data)
    print(f"Average BLEU score: {average_bleu_score:.4f}")