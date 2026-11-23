import json
import pytest
from memor import Reasoning, ReasoningSegment, MemorValidationError

TEST_CASE_NAME = "Reasoning tests"


def test_segment_text1():
    segment = ReasoningSegment(text="Let me think.")
    assert segment.text == "Let me think."


def test_segment_text2():
    segment = ReasoningSegment()
    segment.update_text("Hmm.")
    assert segment.text == "Hmm."


def test_segment_text3():
    with pytest.raises(MemorValidationError, match=r"Invalid value. `text` must be a string."):
        _ = ReasoningSegment(text=2)


def test_segments():
    with pytest.raises(MemorValidationError, match=r"Invalid value. `segments` must be a list of `ReasoningSegment`."):
        _ = Reasoning(segments=["Step 1."])


def test_add_segment1():
    reasoning = Reasoning(segments=[ReasoningSegment(text="Step 1.")])
    reasoning.add_segment(ReasoningSegment(text="Step 2."))
    assert reasoning.text == "Step 1.\nStep 2."


def test_add_segment2():
    reasoning = Reasoning()
    with pytest.raises(MemorValidationError, match=r"Invalid value. `segment` must be a list of `ReasoningSegment`."):
        reasoning.add_segment("Step 1.")


def test_text():
    reasoning = Reasoning(segments=[ReasoningSegment(text="Step 1."), ReasoningSegment(text="Step 2.")])
    assert reasoning.text == "Step 1.\nStep 2."
    assert str(reasoning) == "Step 1.\nStep 2."
    assert repr(reasoning) == "Reasoning(text=Step 1.\nStep 2.)"


def test_json1():
    reasoning1 = Reasoning(segments=[ReasoningSegment(text="Step 1."), ReasoningSegment(text="Step 2.")])
    reasoning2 = Reasoning()
    reasoning2.from_json(reasoning1.to_json())
    assert reasoning1 == reasoning2


def test_json2():
    reasoning1 = Reasoning(segments=[ReasoningSegment(text="Step 1.")])
    reasoning2 = Reasoning()
    reasoning2.from_json(json.dumps(reasoning1.to_json()))
    assert reasoning1 == reasoning2


def test_json3():
    assert Reasoning(segments=[ReasoningSegment(text="Step 1.")]).to_dict() == {
        "type": "Reasoning", "segments": [{"type": "ReasoningSegment", "text": "Step 1."}]}


def test_json4():
    reasoning = Reasoning()
    with pytest.raises(MemorValidationError, match=r"Invalid reasoning structure. It should be a JSON object with proper fields."):
        reasoning.from_json({"segments": [{"text": 2}]})

