import pytest
from src.labeling_functions import get_all_lfs


@pytest.mark.filterwarnings("ignore:DeprecationWarning")
def test_get_all_lfs():
    lfs = get_all_lfs()
    print(f"[test]: len(lfs) = {len(lfs)}")
    assert len(lfs) > 0
