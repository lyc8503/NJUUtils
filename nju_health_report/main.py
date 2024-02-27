# -*- coding: utf-8 -*-
# 健康打卡（这段代码已经完成它的历史使命了）
# 谨以此代码纪念2021-2022年疫情期间的南京大学校园健康打卡（雾）

import logging
import requests
import datetime
from pytz import timezone

COOKIE_CASTGC = ""
LOCATION = "中国江苏省南京市栖霞区九乡河东路"
HEADERS = {
    "Referer": "http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html",
    "X-Requested-With": "com.wisedu.cpdaily.nju",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; MI 8 SE Build/SP2A.220405.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.61 Mobile Safari/537.36 cpdaily/9.0.15 wisedu/9.0.15",
}


def get_zjhs_time(method="YESTERDAY"):
    today = datetime.datetime.now(timezone("Asia/Shanghai"))
    yesterday = today + datetime.timedelta(-1)
    if method == "YESTERDAY":
        return yesterday.strftime("%Y-%m-%d %-H")


def apply():
    for _ in range(0, 3):
        try:
            sess = requests.Session()
            jar = requests.cookies.RequestsCookieJar()
            jar.set("CASTGC", COOKIE_CASTGC)
            sess.cookies.update(jar)

            r = sess.get(
                "http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.do",
                headers=HEADERS,
            )

            logging.info(sess.cookies)

            r = sess.get(
                "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do",
                headers=HEADERS,
            )
            logging.info(r.text[:1024])
            dk_info = r.json()["data"][0]

            has_applied = dk_info["TBZT"] == "1"

            if has_applied:
                requests.get(
                    "https://server.lyc8503.site/wepush?msg=[NJU打卡] 今日已打卡!&key=wepushkey"
                )
                return "ok"

            wid = dk_info["WID"]
            param = {
                "WID": wid,
                "IS_TWZC": 1,  # 是否体温正常
                "CURR_LOCATION": LOCATION,  # 位置
                "ZJHSJCSJ": get_zjhs_time(),  # 最近核酸检测时间
                "JRSKMYS": 1,  # 今日苏康码颜色
                "IS_HAS_JKQK": 1,  # 健康情况
                "JZRJRSKMYS": 1,  # 居住人今日苏康码颜色
                "SFZJLN": 0,  # 是否最近离宁
            }

            r = sess.get(
                "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do",
                params=param,
                headers=HEADERS,
            )

            logging.info(r.text)
            assert r.json()["code"] == "0"
            print("打卡成功!")
        except Exception as e:
            print("打卡发生异常: " + str(e))
            logging.error(e)

    print("打卡失败!")
    return "fail"


def handler(event, context):
    return apply()


if __name__ == "__main__":
    apply()
