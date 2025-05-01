import unittest
import numpy as np
from pathlib import Path
from data_processing.index_builder import IndexBuilder
from config import EMBED_MODEL_NAME
import tempfile
import faiss

class TestIndexBuilder(unittest.TestCase):
    """Tests for IndexBuilder methods including build_index and save_index."""

    def setUp(self):
        self.index_builder = IndexBuilder(EMBED_MODEL_NAME)
        self.docs = [
            {"text": "Document one."},
            {"text": "Document two."}
        ]

    def test_build_index(self):
        index, embeddings, texts = self.index_builder.build_index(self.docs)

        self.assertIsInstance(index, faiss.IndexFlatIP)
        self.assertEqual(embeddings.shape[0], len(self.docs))
        self.assertEqual(len(texts), len(self.docs))
        self.assertTrue(index.is_trained)

    def test_save_index(self):
        index, _, texts = self.index_builder.build_index(self.docs)
        expected_index_size = 2
        self.assertEqual(index.ntotal, expected_index_size)
        self.assertEqual(len(texts), expected_index_size)
        self.assertEqual(len(texts), expected_index_size)

        with tempfile.TemporaryDirectory() as tmpdir:
            dir = Path(tmpdir)
            self.index_builder.save_index(index, texts, self.docs, dir)
            self.index_builder.load_index(dir)
            self.assertEqual(self.index_builder.index.ntotal, expected_index_size)
            self.assertEqual(len(self.index_builder.docs), expected_index_size)
            self.assertEqual(len(self.index_builder.texts), expected_index_size)

    # add search test

    def test_embed_texts(self):
        texts = ["This is a test.", "Another test sentence."]
        embeddings = self.index_builder.embed_texts(texts)
        self.assertEqual(len(embeddings), len(texts))
        self.assertEqual(embeddings.shape[1], 768)  # Check vector dimension
        for row in embeddings:
            self.assertAlmostEqual(np.linalg.norm(row), 1.0, places=5)  # normalized