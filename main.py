from lottery_checker import LotteryChecker

# สร้าง checker
checker = LotteryChecker('lottery_results_20251104_211522.csv')

# ตรวจสลาก
lottery_numbers = lottery_numbers = [

    "980622", "632741", "759544", "196584", "458884", 
    "852966", "658604", "891320", "785401", "717800","821077" ,"132134","196034","948733"

]
results = checker.check_lottery(lottery_numbers)

# แสดงผล
checker.print_results(results, '16 ตุลาคม 2568')

