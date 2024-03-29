import datetime
import arrow
from ics import Calendar, Event

def generateCalendar(jikanwari:list) -> str:

    # カレンダーの作成
    cal = Calendar()
    cal.creator = 'MU-Calendar-Generator'

    # 学期
    semester = {
        0: [datetime.date(2023,4,15), datetime.date(2023,6,10)],
        1: [datetime.date(2023,6,15), datetime.date(2023,8,2)],
        2: [datetime.date(2023,9,22), datetime.date(2023,11,13)],
        3: [datetime.date(2023,11,21), datetime.date(2024,1,27)],
    }

    # 休日
    holiday = [
        datetime.date(2023,4,29), datetime.date(2023,5,1), datetime.date(2023,5,2),
        datetime.date(2023,5,3), datetime.date(2023,5,4), datetime.date(2023,5,5),
        datetime.date(2023,5,20), datetime.date(2023,10,6), datetime.date(2023,10,9),
        datetime.date(2023,12,26), datetime.date(2023,12,27), datetime.date(2023,12,28),
        datetime.date(2023,12,29), datetime.date(2023,12,30), datetime.date(2024,1,1),
        datetime.date(2024,1,2), datetime.date(2024,1,3), datetime.date(2024,1,4),
        datetime.date(2024,1,5), datetime.date(2024,1,6), datetime.date(2024,1,8),
        datetime.date(2024,1,9), datetime.date(2024,1,12), datetime.date(2024,1,13),
        datetime.date(2024,1,24), datetime.date(2024,1,25),
    ]

    # 時間
    class_time = {
        0: ['08:50:00', '10:30:00'],
        1: ['10:40:00', '12:20:00'],
        2: ['13:10:00', '14:50:00'],
        3: ['15:00:00', '16:40:00'],
        4: ['16:50:00', '18:30:00'],
        5: ['18:40:00', '20:20:00'],
        6: ['20:20:00', '22:00:00'],
        }

    # 学期を判定
    now_semester = None
    today = datetime.date.today()
    if (semester[0][0] <= today) & (today <= semester[0][1]):
        now_semester = 0
    elif (semester[1][0] <= today) & (today <= semester[1][1]):
        now_semester = 1
    elif (semester[2][0] <= today) & (today <= semester[2][1]):
        now_semester = 2
    elif (semester[3][0] <= today) & (today <= semester[3][1]):
        now_semester = 3

    # 学期の開始日
    start = semester[now_semester][0]

    # 学期の終了日
    stop = semester[now_semester][1]

    while start <= stop:

        # 曜日を取得
        weekday = start.weekday()

        for i in range(len(jikanwari)):

            rele = jikanwari[i]

            # 日曜日ではない/授業がある/休日ではない を全て満たす場合にイベントを作成
            if weekday != 6 and rele[weekday] != '' and start not in holiday:

                # イベントを作成
                event = Event()

                # イベント名
                event.name = jikanwari[i][weekday]

                # 開始時刻
                event.begin = arrow.get(f"{start} {class_time[i][0]}", "YYYY-MM-DD HH:mm:ss").replace(tzinfo="Asia/Tokyo")

                # 終了時刻
                event.end = arrow.get(f"{start} {class_time[i][1]}" ,"YYYY-MM-DD HH:mm:ss").replace(tzinfo="Asia/Tokyo")

                # イベントをカレンダーに追加
                cal.events.add(event)

        start += datetime.timedelta(days=1)

    return str(cal)
