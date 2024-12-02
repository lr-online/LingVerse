from datetime import datetime, timedelta, timezone


def get_china_now() -> datetime:
    """获取中国当前时间(UTC+8)"""
    return datetime.now(timezone(timedelta(hours=8)))


def to_china_timezone(dt: datetime) -> datetime:
    """将任意时间转换为中国时区"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone(timedelta(hours=8)))

if __name__ == '__main__':
    print(get_china_now())