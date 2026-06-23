from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# دالة ذكية لمعرفة البرج الفلكي بناءً على اليوم والشهر
def get_zodiac_sign(day, month):
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "الجدي ♑"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "الدلو ♒"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "الحوت ♓"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "الحمل ♈"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "الثور ♉"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "الجوزاء ♊"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "السرطان ♋"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "الأسد ♌"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "العذراء ♍"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "الميزان ♎"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "العقرب ♏"
    else:
        return "القوس ♐"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    name = request.form.get('user_name')
    birth_day = int(request.form.get('birth_day'))
    birth_month = int(request.form.get('birth_month'))
    birth_year = int(request.form.get('birth_year'))
    
    today = datetime.now()
    
    try:
        birth_date = datetime(birth_year, birth_month, birth_day)
        diff = today - birth_date
        
        # 1. حساب العمر التفصيلي
        years = today.year - birth_year
        months = today.month - birth_month
        days = today.day - birth_day
        
        if days < 0:
            months -= 1
            days += 30
        if months < 0:
            years -= 1
            months += 12
            
        total_days = diff.days
        total_hours = total_days * 24
        
        # 2. معرفة البرج
        zodiac = get_zodiac_sign(birth_day, birth_month)
        
        # 3. حساب الوقت المتبقي ليوم الميلاد القادم
        next_birthday = datetime(today.year, birth_month, birth_day)
        if next_birthday < today:
            next_birthday = datetime(today.year + 1, birth_month, birth_day)
            
        time_to_birthday = next_birthday - today
        next_months = time_to_birthday.days // 30
        next_days = time_to_birthday.days % 30
        
        return render_template('index.html', 
                               result=True, name=name, 
                               years=years, months=months, days=days, 
                               total_days=total_days, total_hours=total_hours,
                               zodiac=zodiac, next_months=next_months, next_days=next_days)
    except Exception as e:
        return f"<div style='text-align:center; color:red; margin-top:50px;'><h2>التاريخ غير صحيح، تأكد من الأرقام!</h2><a href='/'>رجوع</a></div>"

if __name__ == '__main__':
    app.run(debug=True)