import json
from pathlib import Path

import pytest
from dirty_equals import HasLen
from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_generative_augmenter.generative_augmenter import (
    GenerativeAugmenterProcessor,
    GenerativeAugmenterParameters,
)


def test_generative_augmenter_basic():
    model = GenerativeAugmenterProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == GenerativeAugmenterParameters


@pytest.mark.parametrize("variant", ['preserve_entities', 'substitute_entities'])
def test_augment_doc(variant):
    parameters = GenerativeAugmenterParameters(
        to_lowercase=True,
        variant_altText=variant,
        variant_separator_regex="^- "
    )
    processor = GenerativeAugmenterProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        f"data/jinjadocs_{variant}.json",
    )
    with source.open("r") as fin:
        jdocs = json.load(fin)
        docs = [Document(**jdoc) for jdoc in jdocs]
        docs = processor.process(docs, parameters)
        assert docs == HasLen(3)
        sum_file = testdir / f"data/jinjadocs_{variant}_augmented.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501
