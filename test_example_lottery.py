import pandas as pd
import pytest
from lottery_checker import LotteryChecker


@pytest.fixture
def example_csv(tmp_path):
    csv_file = tmp_path / "example_lottery.csv"
    data = {
        'งวดวันที่': [
            '16 ตุลาคม 2568', '16 ตุลาคม 2568', '16 ตุลาคม 2568', '16 ตุลาคม 2568'
        ],
        'ประเภทรางวัล': [
            'รางวัลที่ 1', 'เลขหน้า 3 ตัว', 'เลขท้าย 3 ตัว', 'เลขท้าย 2 ตัว'
        ],
        'เลขรางวัล': [
            '123456', '111', '456', '56'
        ]
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    return str(csv_file)


def test_load_data(example_csv):
    checker = LotteryChecker(example_csv)
    assert checker.df is not None
    assert len(checker.df) > 0


def test_check_lottery_win(example_csv):
    checker = LotteryChecker(example_csv)
    results = checker.check_lottery(['123456'], '16 ตุลาคม 2568')
    assert '123456' in results
    assert results['123456']['status'] == 'win'
    assert results['123456']['total_prize'] >= 6000000


def test_check_lottery_no_win_and_invalid(example_csv):
    checker = LotteryChecker(example_csv)
    results = checker.check_lottery(['999999', '12345'], '16 ตุลาคม 2568')
    assert results['999999']['status'] == 'no_win'
    assert results['12345']['status'] == 'invalid'


def test_export_results_creates_file(example_csv, tmp_path):
    checker = LotteryChecker(example_csv)
    results = checker.check_lottery(['123456'], '16 ตุลาคม 2568')
    out_file = tmp_path / 'export_example.csv'
    checker.export_results(results, '16 ตุลาคม 2568', str(out_file))
    assert out_file.exists()
    df = pd.read_csv(out_file, encoding='utf-8-sig')
    assert 'เลขสลาก' in df.columns
