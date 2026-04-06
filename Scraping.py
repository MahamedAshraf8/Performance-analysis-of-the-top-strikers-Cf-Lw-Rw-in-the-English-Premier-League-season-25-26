import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# 1. تحديد مسار العمل بدقة (المسار اللي طلبته)
target_path = r"C:\Users\Mohamed\OneDrive\Desktop\python's things"

try:
    if not os.path.exists(target_path):
        os.makedirs(target_path) # لو الفولدر مش موجود هيكريه لك
    os.chdir(target_path)
    print(f"✅ تم تغيير المسار بنجاح لـ: {os.getcwd()}")
except Exception as e:
    print(f"⚠️ مشكلة في المسار، سيتم الحفظ في المكان الحالي للـ Notebook. الخطأ: {e}")

# 2. إعدادات السحب (Scraping)
url = "https://www.transfermarkt.com/premier-league/transfers/wettbewerb/GB1/plus/?saison_id=2025&s_w=&leihe=1&intern=0&pos=14"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

print("🌐 جاري سحب البيانات من Transfermarkt...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    players_list = []
    
    rows = soup.find_all('tr')
    for row in rows:
        name_tag = row.find('span', class_='hide-for-small')
        if name_tag and name_tag.find('a'):
            player_name = name_tag.find('a').text.strip()
            cols = row.find_all('td')
            if len(cols) > 8:
                age = cols[1].text.strip()
                pos = cols[3].text.strip()
                val = cols[4].text.strip()
                fee = cols[8].text.strip()
                players_list.append([player_name, age, pos, val, fee])

    # 3. معالجة البيانات بـ Pandas
    df = pd.DataFrame(players_list, columns=['Name', 'Age', 'Position', 'MarketValue', 'Fee'])
    
    # تنظيف الأرقام (حذف العملات والحروف)
    df['Fee_Cleaned'] = (df['Fee']
                         .str.replace('€', '', regex=False)
                         .str.replace('m', '', regex=False)
                         .str.replace('k', '', regex=False)
                         .str.replace('loan transfer', '0', regex=False)
                         .str.replace('free transfer', '0', regex=False)
                         .str.strip())

    # 4. الحفظ النهائي بترميز Excel
    file_name = 'PL_Forwards_Transfers_25_26.csv'
    try:
        # تأكد إن أي ملف إكسيل بنفس الاسم مقفول
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        print("-" * 30)
        print(f"🎉 عاش يا بطل! الملف اتحفظ بسلام في:\n{os.path.join(os.getcwd(), file_name)}")
        print(f"📊 عدد المهاجمين اللي سحبناهم: {len(df)}")
    except PermissionError:
        print("❌ فشل الحفظ: الملف مفتوح في Excel. اقفله وجرب تاني.")
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")

else:
    print(f"❌ الموقع رفض الدخول. كود الخطأ: {response.status_code}")

# عرض النتائج
df.head()