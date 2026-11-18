from pathlib import Path

import pytest

from load_scores import load_scores

DATA_DIR = Path(__file__).parent


def test_정상_파일을_읽는다():
    kept, skipped = load_scores(DATA_DIR / "scores.csv")
    assert len(kept) == 5

def test_유효한_점수만_읽는다():
    kept, skipped = load_scores(DATA_DIR / "scores.csv")
    assert len(kept) == 5

def test_빈_줄은_건너뛴다():
    kept, skipped = load_scores(DATA_DIR / "scores.csv")
    assert len(skipped) > 0

def test_이름에_쉼표가_있어도_읽는다():
    kept, skipped = load_scores(DATA_DIR / "scores.csv")
    names = [item[0] for item in kept]
    assert "최,네번" in names

@pytest.mark.parametrize(
    ("score_val", "expected_kept"),
    [(0, True), (100, True), (101, False)],
)
def test_점수_경계값(score_val, expected_kept, tmp_path):
    csv_path = tmp_path / "scores.csv"
    csv_path.write_text(f"name,score\n테스트,{score_val}\n", encoding="utf-8")

    kept, skipped = load_scores(csv_path)

    if expected_kept:
        assert kept == [("테스트", score_val)]
        assert skipped == []
    else:
        assert kept == []
        assert len(skipped) == 1
        assert skipped[0][2] == "점수가 0~100 밖"

import pytest
from load_scores import load_scores

def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")

def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []

import pytest
@pytest.mark.parametrize("점수, 유효한가", [
    (-1, False), # 경계 바로 아래
    (0, True), # ★ 아래쪽 경계
    (1, True),
    (99, True),
    (100, True), # ★ 위쪽 경계
    (101, False), # 경계 바로 위
])
def test_점수_경계값(점수, 유효한가):
    쓰기(f"임시.csv", 점수)
    kept, skipped = load_scores("임시.csv")
    assert (len(kept) == 1) == 유효한가