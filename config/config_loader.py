from .models import (
    NotificationConfig,
    EmailConfig,
    QQConfig,
    WeixinConfig,
    StockMonitor,
)


def get_config():
    """
    返回一个整合后的通知 + 股票监控配置 dict
    """
    cfg = NotificationConfig.objects.first()

    # 防止系统还没配置任何 NotificationConfig
    if not cfg:
        return {
            "email": None,
            "qq": None,
            "weixin": None,
            "market_time_limit": False,
            "check_interval": 300,
            "stocks": [],
        }

    email_cfg = EmailConfig.objects.filter(config=cfg).first()
    qq_cfg = QQConfig.objects.filter(config=cfg).first()
    wx_cfg = WeixinConfig.objects.filter(config=cfg).first()

    return {
        "email": {
            "enabled": cfg.email_enabled if email_cfg else False,
            "host": email_cfg.host if email_cfg else "",
            "user": email_cfg.user if email_cfg else "",
            "password": email_cfg.password if email_cfg else "",
            "sender": email_cfg.sender if email_cfg else "",
            "receivers": email_cfg.receivers.split(",") if (email_cfg and email_cfg.receivers) else [],
            "title": email_cfg.title if email_cfg else "",
        } if email_cfg else None,

        "qq": {
            "enabled": cfg.qq_enabled if qq_cfg else False,
            "api_url": qq_cfg.api_url if qq_cfg else "",
            "qq_id": qq_cfg.qq_id if qq_cfg else "",
            "access_token": qq_cfg.access_token if qq_cfg else "",
        } if qq_cfg else None,

        "weixin": {
            "enabled": cfg.weixin_enabled if wx_cfg else False,
            "corp_id": wx_cfg.corp_id if wx_cfg else "",
            "agent_id": wx_cfg.agent_id if wx_cfg else "",
            "corp_secret": wx_cfg.corp_secret if wx_cfg else "",
            "to_user": wx_cfg.to_user if wx_cfg else "",
        } if wx_cfg else None,

        "market_time_limit": cfg.market_time_limit,
        "check_interval": cfg.check_interval,
        "stocks": [
            {
                "code": s.code,
                "name": s.name,
                "buy_price": float(s.buy_price),
                "sell_price": float(s.sell_price),
            }
            for s in StockMonitor.objects.all()
        ],
    }
