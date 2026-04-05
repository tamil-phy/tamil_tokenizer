"""Performance benchmark tests using pytest-benchmark."""

import pytest
from tamil_tokenizer import TamilTokenizer
from .benchmark_data import (
    BENCHMARK_CORPUS_SHORT,
    BENCHMARK_CORPUS_MEDIUM,
    BENCHMARK_CORPUS_LONG,
)


@pytest.fixture(scope="module")
def tokenizer():
    return TamilTokenizer()


class TestPerformanceBenchmarks:
    """Benchmark tokenization speed across corpus sizes and levels."""

    # ── Word tokenization benchmarks ────────────────────────────

    def test_bench_word_short(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_SHORT, level="word")

    def test_bench_word_medium(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_MEDIUM, level="word")

    def test_bench_word_long(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_LONG, level="word")

    # ── Character tokenization benchmarks ───────────────────────

    def test_bench_character_short(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_SHORT, level="character")

    def test_bench_character_medium(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_MEDIUM, level="character")

    def test_bench_character_long(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_LONG, level="character")

    # ── Sentence tokenization benchmarks ────────────────────────

    def test_bench_sentence_short(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_SHORT, level="sentence")

    def test_bench_sentence_medium(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_MEDIUM, level="sentence")

    def test_bench_sentence_long(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_LONG, level="sentence")

    # ── Morpheme tokenization benchmarks ────────────────────────

    def test_bench_morpheme_short(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_SHORT, level="morpheme")

    def test_bench_morpheme_medium(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_MEDIUM, level="morpheme")

    def test_bench_morpheme_long(self, tokenizer, benchmark):
        benchmark(tokenizer.tokenize, BENCHMARK_CORPUS_LONG, level="morpheme")
