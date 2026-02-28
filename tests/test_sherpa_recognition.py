#!/usr/bin/env python3

import os
import unittest
import wave

import numpy as np
import sherpa_onnx

MODEL_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "vosk-models",
    "sherpa-onnx-streaming-zipformer-small-bilingual-zh-en-2023-02-16",
)


def create_recognizer(model_dir=MODEL_DIR):
    kwargs = dict(
        encoder=os.path.join(model_dir, "encoder-epoch-99-avg-1.int8.onnx"),
        decoder=os.path.join(model_dir, "decoder-epoch-99-avg-1.onnx"),
        joiner=os.path.join(model_dir, "joiner-epoch-99-avg-1.int8.onnx"),
        tokens=os.path.join(model_dir, "tokens.txt"),
        num_threads=2,
        sample_rate=16000,
        feature_dim=80,
        enable_endpoint_detection=True,
        rule1_min_trailing_silence=2.4,
        rule2_min_trailing_silence=1.2,
        rule3_min_utterance_length=300,
    )
    for provider in ("cuda", "cpu"):
        kwargs["provider"] = provider
        # try-catch approved: GPU provider may fail, fall back to CPU
        try:
            return sherpa_onnx.OnlineRecognizer.from_transducer(**kwargs)
        except RuntimeError:
            if provider == "cpu":
                raise


def recognize_wav(recognizer, wav_path):
    with wave.open(wav_path, "rb") as f:
        sample_rate = f.getframerate()
        num_channels = f.getnchannels()
        raw = f.readframes(f.getnframes())

    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if num_channels > 1:
        samples = samples[::num_channels]

    stream = recognizer.create_stream()
    chunk_size = int(0.1 * sample_rate)
    for i in range(0, len(samples), chunk_size):
        stream.accept_waveform(sample_rate, samples[i:i + chunk_size])
        while recognizer.is_ready(stream):
            recognizer.decode_stream(stream)

    tail_padding = np.zeros(int(0.5 * sample_rate), dtype=np.float32)
    stream.accept_waveform(sample_rate, tail_padding)
    while recognizer.is_ready(stream):
        recognizer.decode_stream(stream)

    return recognizer.get_result(stream).strip()


class TestSherpaRecognition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recognizer = create_recognizer()

    def _test_wav(self, filename, expected_substrings):
        wav_path = os.path.join(MODEL_DIR, "test_wavs", filename)
        if not os.path.exists(wav_path):
            self.skipTest(f"{wav_path} not found")
        result = recognize_wav(self.recognizer, wav_path)
        print(f"  {filename}: \"{result}\"")
        self.assertTrue(len(result) > 0, f"Empty result for {filename}")
        for substr in expected_substrings:
            self.assertIn(substr, result.lower(), f"Expected '{substr}' in '{result}'")

    def test_wav_0(self):
        self._test_wav("0.wav", ["昨天", "monday", "tomorrow", "星期三"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
