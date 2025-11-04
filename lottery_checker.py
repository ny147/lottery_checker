import pandas as pd
from datetime import datetime
import sys
import os

class LotteryChecker:
    def __init__(self, csv_file):
        """
        สร้างตัวตรวจสลาก
        
        Args:
            csv_file (str): ชื่อไฟล์ CSV ที่มีข้อมูลผลรางวัล
        """
        self.csv_file = csv_file
        self.df = None
        self.load_data()
    
    def load_data(self):
        """โหลดข้อมูลจากไฟล์ CSV"""
        try:
            self.df = pd.read_csv(self.csv_file,dtype=str, encoding='utf-8-sig')
            print(f"✅ โหลดข้อมูลจากไฟล์ {self.csv_file} สำเร็จ")
            print(f"📊 จำนวนข้อมูล: {len(self.df)} รายการ")
            
            # แสดงงวดที่มีในไฟล์
            periods = self.df['งวดวันที่'].unique()
            print(f"🗓️  งวดในไฟล์: {', '.join(periods)}")
            print()
        except FileNotFoundError:
            print(f"❌ ไม่พบไฟล์ {self.csv_file}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการโหลดไฟล์: {e}")
            sys.exit(1)
    
    def check_lottery(self, lottery_numbers, period=None):
        """
        ตรวจสลาก
        
        Args:
            lottery_numbers (list): ลิสต์ของเลขสลาก 6 หลัก
            period (str, optional): งวดที่ต้องการตรวจ (ถ้าไม่ระบุจะตรวจงวดล่าสุด)
        
        Returns:
            dict: ผลการตรวจสลาก
        """
        # ถ้าไม่ระบุงวด ให้ใช้งวดล่าสุด
        if period is None:
            period = self.df['งวดวันที่'].iloc[0]
        
        # กรองข้อมูลเฉพาะงวดที่ต้องการ
        period_df = self.df[self.df['งวดวันที่'] == period].copy()
        
        if len(period_df) == 0:
            print(f"⚠️ ไม่พบข้อมูลงวด {period}")
            return {}
        
        results = {}
        
        for lottery_num in lottery_numbers:
            # ทำให้เป็น string และตัดช่องว่าง
            lottery_num = str(lottery_num).strip()
            
            # ตรวจสอบว่าเป็นตัวเลข 6 หลัก
            if not lottery_num.isdigit() or len(lottery_num) != 6:
                results[lottery_num] = {
                    'status': 'invalid',
                    'message': 'เลขสลากต้องเป็นตัวเลข 6 หลักเท่านั้น'
                }
                continue
            
            # เริ่มตรวจรางวัล
            result = self._check_single_lottery(lottery_num, period_df)
            results[lottery_num] = result
        
        return results
    
    def _check_single_lottery(self, lottery_num, period_df):
        """
        ตรวจสลากเลขเดียว
        
        Args:
            lottery_num (str): เลขสลาก 6 หลัก
            period_df (DataFrame): ข้อมูลรางวัลของงวดนั้น
        
        Returns:
            dict: ผลการตรวจ
        """
        prizes = []
        total_prize = 0
        
        # ตรวจรางวัลที่ 1
        award1 = period_df[period_df['ประเภทรางวัล'].str.contains('รางวัลที่ 1', na=False)]
        print('debugging')
        print(award1['เลขรางวัล'].values)
        print(lottery_num)
        if len(award1) > 0 and lottery_num in award1['เลขรางวัล'].values:
            prizes.append({'ประเภท': 'รางวัลที่ 1', 'เงินรางวัล': 6000000})
            total_prize += 6000000
        
        # ตรวจรางวัลข้างเคียงรางวัลที่ 1
        award_near1 = period_df[period_df['ประเภทรางวัล'].str.contains('ข้างเคียงรางวัลที่ 1', na=False)]
        if len(award_near1) > 0 and lottery_num in award_near1['เลขรางวัล'].values:
            prizes.append({'ประเภท': 'รางวัลข้างเคียงรางวัลที่ 1', 'เงินรางวัล': 100000})
            total_prize += 100000
        
        # ตรวจรางวัลที่ 2
        award2 = period_df[period_df['ประเภทรางวัล'].str.contains('รางวัลที่ 2', na=False)]
        if len(award2) > 0 and lottery_num in award2['เลขรางวัล'].values:
            prizes.append({'ประเภท': 'รางวัลที่ 2', 'เงินรางวัล': 200000})
            total_prize += 200000
        
        # ตรวจรางวัลที่ 3
        award3 = period_df[period_df['ประเภทรางวัล'].str.contains('รางวัลที่ 3', na=False)]
        if len(award3) > 0 and lottery_num in award3['เลขรางวัล'].values:
            prizes.append({'ประเภท': 'รางวัลที่ 3', 'เงินรางวัล': 80000})
            total_prize += 80000
        
        # ตรวจรางวัลที่ 4
        award4 = period_df[period_df['ประเภทรางวัล'].str.contains('รางวัลที่ 4', na=False)]
        if len(award4) > 0 and lottery_num in award4['เลขรางวัล'].values:
            prizes.append({'ประเภท': 'รางวัลที่ 4', 'เงินรางวัล': 40000})
            total_prize += 40000
        
        # ตรวจรางวัลที่ 5
        award5 = period_df[period_df['ประเภทรางวัล'].str.contains('รางวัลที่ 5', na=False)]
        if len(award5) > 0 and lottery_num in award5['เลขรางวัล'].values:
            prizes.append({'ประเภท': 'รางวัลที่ 5', 'เงินรางวัล': 20000})
            total_prize += 20000
        
        # ตรวจเลขหน้า 3 ตัว
        front3 = lottery_num[:3]
        award_front3 = period_df[period_df['ประเภทรางวัล'].str.contains('เลขหน้า 3 ตัว', na=False)]
        if len(award_front3) > 0 and front3 in award_front3['เลขรางวัล'].values:
            prizes.append({'ประเภท': 'รางวัลเลขหน้า 3 ตัว', 'เงินรางวัล': 4000})
            total_prize += 4000
        
        # ตรวจเลขท้าย 3 ตัว
        last3 = lottery_num[-3:]
        award_last3 = period_df[period_df['ประเภทรางวัล'].str.contains('เลขท้าย 3 ตัว', na=False)]
        if len(award_last3) > 0 and last3 in award_last3['เลขรางวัล'].values:
            prizes.append({'ประเภท': 'รางวัลเลขท้าย 3 ตัว', 'เงินรางวัล': 4000})
            total_prize += 4000
        
        # ตรวจเลขท้าย 2 ตัว
        last2 = lottery_num[-2:]
        award_last2 = period_df[period_df['ประเภทรางวัล'].str.contains('เลขท้าย 2 ตัว', na=False)]
        if len(award_last2) > 0 and last2 in award_last2['เลขรางวัล'].values:
            prizes.append({'ประเภท': 'รางวัลเลขท้าย 2 ตัว', 'เงินรางวัล': 2000})
            total_prize += 2000
        
        # สรุปผล
        if prizes:
            return {
                'status': 'win',
                'prizes': prizes,
                'total_prize': total_prize,
                'message': f'🎉 ยินดีด้วย! ถูกรางวัล {len(prizes)} รางวัล'
            }
        else:
            return {
                'status': 'no_win',
                'prizes': [],
                'total_prize': 0,
                'message': '😔 เสียใจด้วย ไม่ถูกรางวัล'
            }
    
    def print_results(self, results, period):
        """
        แสดงผลการตรวจสลาก
        
        Args:
            results (dict): ผลการตรวจสลาก
            period (str): งวดที่ตรวจ
        """
        print("=" * 70)
        print(f"🎰 ผลการตรวจสลากกินแบ่งรัฐบาล งวดวันที่ {period}")
        print("=" * 70)
        print()
        
        total_win = 0
        total_amount = 0
        
        for lottery_num, result in results.items():
            print(f"🎫 เลขสลาก: {lottery_num}")
            print(f"   {result['message']}")
            
            if result['status'] == 'win':
                total_win += 1
                total_amount += result['total_prize']
                print(f"   💰 รางวัลที่ถูก:")
                for prize in result['prizes']:
                    print(f"      - {prize['ประเภท']}: {prize['เงินรางวัล']:,} บาท")
                print(f"   💵 รวมเงินรางวัล: {result['total_prize']:,} บาท")
            elif result['status'] == 'invalid':
                print(f"   ⚠️ {result['message']}")
            
            print()
        
        print("-" * 70)
        print(f"📊 สรุปผล:")
        print(f"   ตรวจสลากทั้งหมด: {len(results)} ใบ")
        print(f"   ถูกรางวัล: {total_win} ใบ")
        print(f"   ไม่ถูกรางวัล: {len(results) - total_win} ใบ")
        if total_amount > 0:
            print(f"   💰 เงินรางวัลรวม: {total_amount:,} บาท")
        print("=" * 70)
    
    def export_results(self, results, period, output_file=None):
        """
        ส่งออกผลการตรวจเป็นไฟล์ CSV
        
        Args:
            results (dict): ผลการตรวจสลาก
            period (str): งวดที่ตรวจ
            output_file (str, optional): ชื่อไฟล์ที่ต้องการบันทึก
        """
        if output_file is None:
            output_file = f'lottery_check_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        export_data = []
        for lottery_num, result in results.items():
            if result['status'] == 'win':
                for prize in result['prizes']:
                    export_data.append({
                        'งวดวันที่': period,
                        'เลขสลาก': lottery_num,
                        'ประเภทรางวัล': prize['ประเภท'],
                        'เงินรางวัล': prize['เงินรางวัล'],
                        'วันที่ตรวจ': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            else:
                export_data.append({
                    'งวดวันที่': period,
                    'เลขสลาก': lottery_num,
                    'ประเภทรางวัล': result['message'],
                    'เงินรางวัล': 0,
                    'วันที่ตรวจ': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        
        df_export = pd.DataFrame(export_data)
        df_export.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n💾 บันทึกผลการตรวจลงไฟล์ {output_file} สำเร็จ")


def main():
    """ฟังก์ชันหลัก"""
    print("=" * 70)
    print("🎰 โปรแกรมตรวจสลากกินแบ่งรัฐบาล")
    print("=" * 70)
    print()
    
    # ระบุไฟล์ CSV
    csv_file = input("📁 ชื่อไฟล์ CSV ที่มีผลรางวัล (กด Enter เพื่อค้นหาไฟล์ล่าสุด): ").strip()
    
    # ถ้าไม่ระบุไฟล์ ให้ค้นหาไฟล์ล่าสุด
    if not csv_file:
        csv_files = [f for f in os.listdir('.') if f.startswith('lottery_results_') and f.endswith('.csv')]
        if csv_files:
            csv_file = sorted(csv_files)[-1]
            print(f"   ใช้ไฟล์: {csv_file}")
        else:
            print("❌ ไม่พบไฟล์ CSV")
            return
    
    # สร้าง LotteryChecker
    checker = LotteryChecker(csv_file)
    
    # ระบุงวดที่ต้องการตรวจ (ถ้าไม่ระบุจะใช้งวดล่าสุด)
    periods = checker.df['งวดวันที่'].unique()
    print("เลือกงวดที่ต้องการตรวจ:")
    for i, period in enumerate(periods, 1):
        print(f"   {i}. {period}")
    
    period_choice = input(f"เลือกงวด (1-{len(periods)}, กด Enter เพื่อใช้งวดล่าสุด): ").strip()
    
    if period_choice and period_choice.isdigit():
        period_idx = int(period_choice) - 1
        if 0 <= period_idx < len(periods):
            period = periods[period_idx]
        else:
            period = periods[0]
    else:
        period = periods[0]
    
    print(f"📅 ตรวจสลากงวด: {period}")
    print()
    
    # รับเลขสลาก
    print("🎫 กรอกเลขสลาก 6 หลัก (คั่นด้วย , หรือ Enter)")
    print("   ตัวอย่าง: 123456,789012,345678")
    print("   หรือกด Enter แต่ละเลข (พิมพ์ 'done' เมื่อเสร็จ)")
    print()
    
    lottery_numbers = []
    input_text = input("เลขสลาก: ").strip()
    
    if ',' in input_text:
        # กรณีกรอกหลายเลขพร้อมกัน
        lottery_numbers = [num.strip() for num in input_text.split(',') if num.strip()]
    else:
        # กรณีกรอกทีละเลข
        if input_text and input_text.lower() != 'done':
            lottery_numbers.append(input_text)
        
        while True:
            num = input("เลขสลาก (หรือพิมพ์ 'done'): ").strip()
            if num.lower() == 'done':
                break
            if num:
                lottery_numbers.append(num)
    
    if not lottery_numbers:
        print("⚠️ ไม่มีเลขสลากที่ต้องการตรวจ")
        return
    
    print()
    print(f"🔍 กำลังตรวจสลาก {len(lottery_numbers)} ใบ...")
    print()
    
    # ตรวจสลาก
    results = checker.check_lottery(lottery_numbers, period)
    
    # แสดงผล
    checker.print_results(results, period)
    
    # ถามว่าต้องการบันทึกผลหรือไม่
    export = input("\n💾 ต้องการบันทึกผลการตรวจเป็นไฟล์ CSV หรือไม่? (y/n): ").strip().lower()
    if export == 'y':
        checker.export_results(results, period)


if __name__ == "__main__":
    main()