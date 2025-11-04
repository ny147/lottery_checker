from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time

def scrape_lottery_results(url='https://www.glo.or.th/mission/awarding/orderby-time', dir_path='./data'):
    """
    ดึงข้อมูลผลรางวัลสลากกินแบ่งจาก glo.or.th ด้วย Selenium
    """
    
    # ตั้งค่า Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # รันแบบไม่เปิดหน้าต่าง
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = None
    lottery_data = []
    
    try:
        print("=" * 60)
        print("🎰 โปรแกรมดึงข้อมูลผลรางวัลสลากกินแบ่งรัฐบาล")
        print("=" * 60)
        print("\n🌐 กำลังเริ่มต้น Chrome WebDriver...")
        
        # สร้าง WebDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        print(f"🔗 กำลังเข้าถึง: {url}")
        driver.get(url)
        
        # รอให้หน้าเว็บโหลดเสร็จ
        print("⏳ รอให้เนื้อหาโหลด...")
        time.sleep(5)  # รอให้ JavaScript โหลดข้อมูล
        
        # รอจนกว่าจะมีข้อมูลรางวัล
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "award-lotto-item"))
            )
            print("✅ โหลดข้อมูลสำเร็จ!")
        except:
            print("⚠️ ไม่พบข้อมูลรางวัล กำลังลองดึงข้อมูลที่มีอยู่...")
        
        # ดึงข้อมูลงวดสลาก
        lottery_items = driver.find_elements(By.CLASS_NAME, "award-lotto-item")
        
        print(f"\n📊 พบข้อมูลงวดสลาก: {len(lottery_items)} งวด")
        
        if len(lottery_items) == 0:
            print("\n⚠️ ไม่พบข้อมูลรางวัล กำลังบันทึก HTML สำหรับตรวจสอบ...")
            with open('page_debug.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("💾 บันทึกไฟล์ page_debug.html สำเร็จ")
            return None
        
        # วนลูปดึงข้อมูลแต่ละงวด
        for idx, item in enumerate(lottery_items, 1):
            print(f"\n🔍 กำลังประมวลผลงวดที่ {idx}...")
            
            try:
                # ดึงวันที่งวด
                try:
                    date_elem = item.find_element(By.CSS_SELECTOR, "h2.topic")
                    period_date = date_elem.text.replace('ประจำวันที่', '').strip()
                except:
                    period_date = "ไม่ระบุวันที่"
                
                print(f"   📅 งวดวันที่: {period_date}")
                
                # รางวัลที่ 1
                try:
                    award1_div = item.find_element(By.CLASS_NAME, "award1")
                    award1_name = award1_div.find_element(By.CLASS_NAME, "award-name").text
                    award1_num = award1_div.find_element(By.CLASS_NAME, "number-bold").text.strip()
                    lottery_data.append({
                        'งวดวันที่': period_date,
                        'ประเภทรางวัล': award1_name,
                        'เลขรางวัล': award1_num,
                        'วันที่ดึงข้อมูล': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    print(f"   ✓ รางวัลที่ 1: {award1_num}")
                except Exception as e:
                    print(f"   ✗ ไม่พบรางวัลที่ 1")
                
                # รางวัลเลขหน้า 3 ตัว
                try:
                    award_3first = item.find_element(By.CLASS_NAME, "award-3first")
                    award_name = award_3first.find_element(By.CLASS_NAME, "award-name").text
                    award_nums = award_3first.find_elements(By.CLASS_NAME, "number-bold")
                    for num in award_nums:
                        lottery_data.append({
                            'งวดวันที่': period_date,
                            'ประเภทรางวัล': award_name,
                            'เลขรางวัล': num.text.strip(),
                            'วันที่ดึงข้อมูล': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                    print(f"   ✓ เลขหน้า 3 ตัว: {len(award_nums)} รางวัล")
                except:
                    print(f"   ✗ ไม่พบเลขหน้า 3 ตัว")
                
                # รางวัลเลขท้าย 3 ตัว
                try:
                    award_3last = item.find_element(By.CLASS_NAME, "award-3last")
                    award_name = award_3last.find_element(By.CLASS_NAME, "award-name").text
                    award_nums = award_3last.find_elements(By.CLASS_NAME, "number-bold")
                    for num in award_nums:
                        lottery_data.append({
                            'งวดวันที่': period_date,
                            'ประเภทรางวัล': award_name,
                            'เลขรางวัล': num.text.strip(),
                            'วันที่ดึงข้อมูล': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                    print(f"   ✓ เลขท้าย 3 ตัว: {len(award_nums)} รางวัล")
                except:
                    print(f"   ✗ ไม่พบเลขท้าย 3 ตัว")
                
                # รางวัลเลขท้าย 2 ตัว
                try:
                    award_2last = item.find_element(By.CLASS_NAME, "award-2last")
                    award_name = award_2last.find_element(By.CLASS_NAME, "award-name").text
                    award_num = award_2last.find_element(By.CLASS_NAME, "number-bold").text.strip()
                    lottery_data.append({
                        'งวดวันที่': period_date,
                        'ประเภทรางวัล': award_name,
                        'เลขรางวัล': award_num,
                        'วันที่ดึงข้อมูล': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    print(f"   ✓ เลขท้าย 2 ตัว: {award_num}")
                except:
                    print(f"   ✗ ไม่พบเลขท้าย 2 ตัว")
                
                # รางวัลข้างเคียงรางวัลที่ 1
                try:
                    award_near1 = item.find_element(By.CLASS_NAME, "award-near1")
                    award_name = award_near1.find_element(By.CLASS_NAME, "award-name").text
                    award_nums = award_near1.find_elements(By.CLASS_NAME, "number")
                    for num in award_nums:
                        lottery_data.append({
                            'งวดวันที่': period_date,
                            'ประเภทรางวัล': award_name,
                            'เลขรางวัล': num.text.strip(),
                            'วันที่ดึงข้อมูล': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                    print(f"   ✓ ข้างเคียงรางวัลที่ 1: {len(award_nums)} รางวัล")
                except:
                    print(f"   ✗ ไม่พบข้างเคียงรางวัลที่ 1")
                
                # รางวัลที่ 2, 3, 4, 5
                for award_class, award_label in [('award2', 'รางวัลที่ 2'), 
                                                 ('award3', 'รางวัลที่ 3'), 
                                                 ('award4', 'รางวัลที่ 4'), 
                                                 ('award5', 'รางวัลที่ 5')]:
                    try:
                        award_div = item.find_element(By.CLASS_NAME, award_class)
                        award_name = award_div.find_element(By.CLASS_NAME, "award-name").text
                        award_nums = award_div.find_elements(By.CLASS_NAME, "number")
                        count = 0
                        for num in award_nums:
                            num_text = num.text.strip()
                            if num_text:
                                lottery_data.append({
                                    'งวดวันที่': period_date,
                                    'ประเภทรางวัล': award_name,
                                    'เลขรางวัล': num_text,
                                    'วันที่ดึงข้อมูล': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                })
                                count += 1
                        print(f"   ✓ {award_label}: {count} รางวัล")
                    except:
                        print(f"   ✗ ไม่พบ{award_label}")
                
            except Exception as e:
                print(f"   ❌ เกิดข้อผิดพลาดในการดึงข้อมูลงวดที่ {idx}: {str(e)}")
        
        # สร้าง DataFrame และบันทึกเป็น CSV
        if lottery_data:
            df = pd.DataFrame(lottery_data)
            filename = f'lottery_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            df.to_csv(f"{dir_path}/{filename}", index=False, encoding='utf-8-sig')
            
            print("\n" + "=" * 60)
            print("✅ บันทึกข้อมูลสำเร็จ!")
            print("=" * 60)
            print(f"📁 ชื่อไฟล์: {filename}")
            print(f"📊 จำนวนข้อมูลทั้งหมด: {len(df)} รายการ")
            print(f"\n📋 สรุปข้อมูลตามประเภทรางวัล:")
            print(df['ประเภทรางวัล'].value_counts())
            print(f"\n🎯 ตัวอย่างข้อมูล 10 แถวแรก:")
            print(df.head(10).to_string(index=False))
            
            return df
        else:
            print("\n⚠️ ไม่มีข้อมูลถูกดึงมา")
            return None
            
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {str(e)}")
        if driver:
            with open('error_page.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("💾 บันทึก HTML ไว้ที่ error_page.html เพื่อการตรวจสอบ")
        return None
    
    finally:
        if driver:
            driver.quit()
            print("\n🔚 ปิด WebDriver เรียบร้อย")

if __name__ == "__main__":
    result = scrape_lottery_results()
    
    if result is not None:
        print("\n✨ เสร็จสิ้นการทำงาน")
    else:
        print("\n⚠️ กรุณาตรวจสอบไฟล์ HTML ที่บันทึกไว้")