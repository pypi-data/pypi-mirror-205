from typing import List
import pytest
import json
from sptranslator.translator import Translator, divide_into_chunks, group_chunks, check_braces


def test_divide_into_chunks_multiple_chunks_3() -> None:
    text = "\n\n".join(f"Chunk {i}" for i in range(1, 4))

    result = divide_into_chunks(text)
    # Check if the result contains the expected number of chunks
    assert len(result) == 1
    # Check if the result contains the expected chunks
    assert result == ["Chunk 1\n\nChunk 2\n\nChunk 3"]


def test_divide_into_chunks_multiple_chunks_100() -> None:
    text = "\n\n".join(f"Chunk {i}" for i in range(1, 101))
    result = divide_into_chunks(text)
    # Check if the result contains the expected number of chunks
    assert len(result) == 2
    # Check if the result contains the expected chunks
    assert result == [
        'Chunk 1\n\nChunk 2\n\nChunk 3\n\nChunk 4\n\nChunk 5\n\nChunk 6\n\nChunk 7\n\nChunk 8\n\nChunk 9\n\nChunk 10\n\nChunk 11\n\nChunk 12\n\nChunk 13\n\nChunk 14\n\nChunk 15\n\nChunk 16\n\nChunk 17\n\nChunk 18\n\nChunk 19\n\nChunk 20\n\nChunk 21\n\nChunk 22\n\nChunk 23\n\nChunk 24\n\nChunk 25\n\nChunk 26\n\nChunk 27\n\nChunk 28\n\nChunk 29\n\nChunk 30\n\nChunk 31\n\nChunk 32\n\nChunk 33\n\nChunk 34\n\nChunk 35\n\nChunk 36\n\nChunk 37\n\nChunk 38\n\nChunk 39\n\nChunk 40\n\nChunk 41\n\nChunk 42\n\nChunk 43\n\nChunk 44\n\nChunk 45\n\nChunk 46\n\nChunk 47\n\nChunk 48\n\nChunk 49\n\nChunk 50\n\nChunk 51\n\nChunk 52\n\nChunk 53\n\nChunk 54\n\nChunk 55\n\nChunk 56\n\nChunk 57\n\nChunk 58\n\nChunk 59\n\nChunk 60\n\nChunk 61\n\nChunk 62\n\nChunk 63\n\nChunk 64\n\nChunk 65\n\nChunk 66\n\nChunk 67\n\nChunk 68\n\nChunk 69\n\nChunk 70\n\nChunk 71\n\nChunk 72\n\nChunk 73\n\nChunk 74\n\nChunk 75\n\nChunk 76\n\nChunk 77\n\nChunk 78\n\nChunk 79\n\nChunk 80',
        'Chunk 81\n\nChunk 82\n\nChunk 83\n\nChunk 84\n\nChunk 85\n\nChunk 86\n\nChunk 87\n\nChunk 88\n\nChunk 89\n\nChunk 90\n\nChunk 91\n\nChunk 92\n\nChunk 93\n\nChunk 94\n\nChunk 95\n\nChunk 96\n\nChunk 97\n\nChunk 98\n\nChunk 99\n\nChunk 100'
    ]


def test_divide_into_chunks_empty_text() -> None:
    text = ""
    
    result = divide_into_chunks(text)

    # Check if the result contains no chunks
    assert len(result) == 1
    # Check if the result contains an empty chunk
    assert result == [""]


def test_group_chunks_small_chunks() -> None:
    chunks = ["Chunk 1", "Chunk 2", "Chunk 3", "Chunk 4", "Chunk 5"]
    ntokens = [5, 5, 5, 5, 5]

    result = group_chunks(chunks, ntokens, max_len=19)

    # Check if the result contains the expected number of grouped chunks
    assert len(result) == 2
    # Check if the result contains the expected grouped chunks
    assert result == ["Chunk 1\n\nChunk 2\n\nChunk 3", "Chunk 4\n\nChunk 5"]


def test_group_chunks_large_chunks() -> None:
    chunks = ["Chunk 1", "Chunk 2", "Chunk 3"]
    ntokens = [10, 10, 10]

    result = group_chunks(chunks, ntokens, max_len=10)

    # Check if the result contains the expected number of grouped chunks
    assert len(result) == 3
    # Check if the result contains the expected grouped chunks
    assert result == ["Chunk 1", "Chunk 2", "Chunk 3"]


def test_group_chunks_empty_chunks_tokens() -> None:
    chunks = []
    ntokens = []

    result = group_chunks(chunks, ntokens, max_len=10)

    # Check if the result contains no grouped chunks
    assert len(result) == 0


def test_group_chunks_different_lengths_chunks_tokens():
    chunks = ["Chunk 1", "Chunk 2", "Chunk 3"]
    ntokens = [5, 5]

    # Expect a ValueError due to different lengths of chunks and tokens
    with pytest.raises(ValueError):
        group_chunks(chunks, ntokens, max_len=10)


@pytest.mark.parametrize("text", [
    "",
    "a",
    "a{b}",
    "a{b}c",
    "a{b{c}d}e",
    "{a{b}c}",
    "{a{b}{c}}",
    "{a{b{c}}}",
])
def test_check_braces_positive(text):
    assert check_braces(text) is True


@pytest.mark.parametrize("text", [
    "{",
    "}",
    "a{",
    "a{b",
    "a{b}c}",
    "{a{b}c",
    "{a{b}c}}",
    "{a{b{c}",
    "}}a{b{c}}",
])
def test_check_braces_negative(text):
    with pytest.raises(ValueError, match="Unmatched braces."):
        check_braces(text)

def test_translation() -> None:    
    texts = [
        "There are two steps in our framework: {\\em pre-training} and {\\em fine-tuning}.",
        "\\section{one two three}"
    ]
    source_lang = "English"
    target_lang = "French"
    syntax = "latex"

    expected_translations = [
        "Il y a deux étapes dans notre cadre: {\\em pré-entraînement} et {\\em ajustement fin}.",
        "\\section{un deux trois}"
    ]

    translator=Translator(source_lang, target_lang, syntax)
    translated_texts = translator.translation(texts)

    # Check if the translated_texts contains the expected number of translations
    assert len(translated_texts) == len(expected_translations)

    for expected_translation, translated_text in zip(expected_translations, translated_texts):
        # Check if each translated text contains the expected translation
        assert expected_translation in translated_text


def test_translate_text_latex() -> None:
    source_lang = "English"
    target_lang = "French"
    syntax = "latex"
    
    input_text = (
        r"\section{Introduction}\n\n"
        r"There are two steps in our framework: {\\em pre-training} and {\\em fine-tuning}.\n\n"
        r"\section{Conclusion}\n\n"
        r"Our experiments demonstrate the effectiveness of our method."
    )

    expected_result = (
        r"\section{Introduction}\n\n"
        r"Il y a deux étapes dans notre cadre: {\\em pré-entraînement} et {\\em ajustement fin}.\n\n"
        r"\section{Conclusion}\n\n"
        r"Nos expériences démontrent l'efficacité de notre méthode."
    )
    
    translator=Translator(source_lang, target_lang, syntax)
    result = translator.translate_text(input_text)

    # Check if the result contains the expected translated text
    assert expected_result in result


def test_translate_text_json() -> None:
    source_lang = "English"
    target_lang = "German"
    syntax = "json"

    input_json = {
        "Name": "John Doe",
        "Age": 30,
        "City": "New York",
        "Skills": ["Python", "JavaScript", "Java"]
    }

    expected_translated_json = {
        "Name": "John Doe",
        "Alter": 30,
        "Stadt": "New York",
        "Fähigkeiten": ["Python","JavaScript","Java"]
    }

    input_text = json.dumps(input_json, indent=2)

    translator=Translator(source_lang, target_lang, syntax)
    result = translator.translate_text(input_text)
    result = json.loads(result)

    # Check if the result contains the expected translated text
    assert expected_translated_json == result


def test_translate_file() -> None:
    source_lang = "English"
    target_lang = "French"
    syntax = "latex"
    input_path = "./tests/experiments_details.tex"
    output_path = "./tests/experiments_details_fr.tex"

    translator=Translator(source_lang, target_lang, syntax)
    
    assert translator.translate_file(input_path, output_path) is None

