import datetime
import pandas as pd
import pytz


def get_now():
    """
    現在時刻を取得します。
    :return:
    """
    return int(datetime.datetime.now().timestamp())


def get_how_many_days_ago(many_days, _date=None):
    """
    引数で指定した日付から、X日前の00:00:00のdatetimeを取得します。
    日付を指定しない場合、基準時刻を現在時刻とします。
    :param many_days: X日前
    :param _date: 指定時刻
    :return:
    """
    if not _date:
        _date = datetime.datetime.now()

    # 5日前を取得後, 時刻を全て0に変更する
    _date = _date - datetime.timedelta(days=many_days)
    _date = _date.replace(hour=0, minute=0, second=0, microsecond=0)

    return int(_date.timestamp())


def convert_iso_to_jst(iso_datetime):
    """
    指定したiso時刻をjstへ変換します
    :param iso_datetime:
    :return: jst_time
    """
    df = pd.DataFrame({'Date-Time': [iso_datetime]})
    df['Date-Time'] = pd.to_datetime(df['Date-Time'])
    conv_df = df['Date-Time'][0].replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Tokyo"))

    return conv_df.strftime('%Y/%m/%d %H:%M')
