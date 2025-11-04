# 🎟️ Lottery Checker

**Lottery Checker** is a simple Python tool for checking Thai lottery results from a CSV file.  
You can use it to verify whether your ticket numbers match the winning numbers for a specific draw date.

---

## 📖 Features

- ✅ Load Thai Government Lottery results from a CSV file  
- 🎯 Check multiple ticket numbers at once  
- 🧾 Print readable check results (with the date of the draw)  
- ⚡ Simple and fast setup

---

## 🧩 Project Structure

```
lottery_checker/
│
├── lottery_checker.py          # Core module containing LotteryChecker class
├── lottery_results_YYYYMMDD_HHMMSS.csv   # Example CSV result file
├── main.py                     # Example script to run checker (your code)
└── README.md                   # This file
```

---

## 🚀 Quick Start

### 1. Clone or download this project
```bash
git clone https://github.com/yourusername/lottery_checker.git
cd lottery_checker
```

### 2. Prepare your CSV result file
Ensure your CSV file contains Thai lottery results in this format (example):

| รางวัลที่ | หมายเลขที่ถูกรางวัล |
|------------|---------------------|
| รางวัลที่ 1 | 980622 |
| เลขหน้า 3 ตัว | 852, 658 |
| เลขท้าย 3 ตัว | 401, 800 |
| เลขท้าย 2 ตัว | 77 |
| รางวัลที่ 2 | 132134, 196034, 948733 |

Save the file as something like:  
`lottery_results_20251104_211522.csv`

---

### 3. Example Usage

Create a file named `main.py` (or use your provided script):

```python
from lottery_checker import LotteryChecker

# สร้าง checker
checker = LotteryChecker('lottery_results_20251104_211522.csv')

# ตรวจสลาก
lottery_numbers = [
    "980622", "632741", "759544", "196584", "458884",
    "852966", "658604", "891320", "785401", "717800",
    "821077", "132134", "196034", "948733"
]

results = checker.check_lottery(lottery_numbers)

# แสดงผล
checker.print_results(results, '16 ตุลาคม 2568')
```

---

### 4. Run the Script
```bash
python main.py
```

You’ll get output like:
```
ผลการตรวจสลาก งวดวันที่ 16 ตุลาคม 2568
----------------------------------------
980622 : ถูกรางวัลที่ 1 🎉
632741 : ไม่ถูกรางวัล
196034 : ถูกรางวัลที่ 2 🏅
...
----------------------------------------
รวมถูกรางวัลทั้งหมด 3 ใบ
```

---

## 🧠 Class Overview

### `LotteryChecker(csv_path: str)`
Loads the result file and prepares it for checking.

### `.check_lottery(numbers: list[str]) -> dict`
Compares a list of ticket numbers against the official results.

### `.print_results(results: dict, draw_date: str)`
Pretty-prints the check results for a specific draw date.

---

## 🧰 Requirements

- Python 3.8+
- A CSV file with official Thai lottery results

(Optional)
```bash
pip install pandas
```
(if your implementation uses it internally)

---

## 📝 License

This project is open source and free to use for educational or personal purposes.
