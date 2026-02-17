# Telegram Trade Yardım Bot

Bu repository Telegram üçün sadə yatırım və referal sistemi botudur. Kiçik sərmayələr (50, 100, 150 AZN) üçün investisiya qeydiyyatı, referal izləmə, balans və çıxarış sorğuları dəstəklənir. Ödənişlər üçün `payments.py` içində M10 inteqrasiyası üçün stub (placeholder) var.

Quraşdırma:

1. Virtualenv yaradın və aktiv edin.
2. Paketləri quraşdırın:

```bash
pip install -r requirements.txt
```

3. `.env` faylını `.env.example` faylından yaradın və `TELEGRAM_TOKEN`-ı yerləşdirin.

Çalışdırmaq:

```bash
python bot.py
```

Qısa istinad:
- `bot.py`: Botun əsas məntiqi
- `db.py`: SQLite üçün sadə ORM funksiyaları
- `payments.py`: M10 üçün ödəniş stub və əməliyyat gündəlik işləyicisi
- `utils.py`: köməkçi funksiyalar (referal kodu və s.)

Qeyd: Real ödəniş inteqrasiyası üçün `payments.py`-dəki stub-u M10 API sənədlərinə görə reallaşdırın və təhlükəsiz saxlama üçün `.env` faylından istifadə edin.

Admin qəbz yönləndirmə:

- Receipt (qəbz) göndərildikdə bot onu `ADMIN_CHAT_IDS`-də göstərilən Telegram chat ID-lərinə avtomatik yönləndirir.
- Bot telefon nömrəsinə birbaşa mesaj göndərə bilməz — adminlərin botu start etməsi və ya onların Telegram numeric ID-lərinin `.env`-də `ADMIN_CHAT_IDS` kimi əlavə edilməsi lazımdır.

Tez Başlatma və Windows Xidməti üçün Qısa Təlimat

1) Ətraf mühit və quraşdırma

```powershell
cd "c:\trader bot"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# .env faylını açıb TELEGRAM_TOKEN və ADMIN_CHAT_IDS dəyişənlərini yazın
```

2) Locally çalıştırmaq

```powershell
cd "c:\trader bot"
.\venv\Scripts\Activate.ps1
python bot.py
```

3) Windows-da avtomatik başladılma — İki metod

- A. Task Scheduler (sade, sistem başlanğıcında işlətmək üçün)

```powershell
# Bu komanda cari istifadəçi üçün botu hər login olduqda başlatacaq
$Action = New-ScheduledTaskAction -Execute "Powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -Command \"cd 'C:\trader bot'; .\venv\Scripts\Activate.ps1; python bot.py\""
$Trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "TraderBot" -Action $Action -Trigger $Trigger -Description "Start Trader Bot on login"
```

- B. NSSM ilə Windows Service (daha stabil, administrator hüquqları tələb edir)

1. NSSM (https://nssm.cc/) yükləyin və `nssm.exe`-i bir yola qoyun.
2. Administrator PowerShell-dən:

```powershell
nssm install TraderBot "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" "-NoProfile -WindowStyle Hidden -Command \"cd 'C:\trader bot'; .\venv\Scripts\Activate.ps1; python bot.py\""
nssm start TraderBot
```

Qeyd: NSSM parametrlərində `AppDirectory` olaraq `C:\trader bot` və `AppParameters` içində virtualenv aktivləşdirmə və `python bot.py` istifadə edin.

4) Fayllar

- `start_bot.ps1`: virtualenv aktivləşdirir və `bot.py`-ni işə salır.
- `start_bot.bat`: qısa batch skripti Windows üçün.

Problemlər və yoxlama

- Əgər bot fərqli bir bot accountu göstərirsə, `.env`-dəki `TELEGRAM_TOKEN` yanlış ola bilər — `getMe` çağırışı ilə tokeni yoxlayın.
- Admin qəbzlərinin çatdırılması üçün `ADMIN_CHAT_IDS`-ə numeric Telegram ID-ləri əlavə edin (telefon nömrələri işləməyəcək).