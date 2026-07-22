// ==UserScript==
// @name         NJU Always Login
// @namespace    https://authserver.nju.edu.cn/
// @version      2026-07-21
// @description  NJU 统一认证长期登录; 使用方法: TamperMonkey BETA (一定要 BETA) 安装此脚本, 退出登陆后, 再次访问 https://authserver.nju.edu.cn/ 登录即可 (不要从别的跳转入口进入), 成功登陆后长期有效.
// @author       lyc8503
// @match        https://authserver.nju.edu.cn/authserver/*
// @grant        GM_cookie
// @grant        window.close
// ==/UserScript==

(function() {
    'use strict';

    if (window.location.href === "https://authserver.nju.edu.cn/authserver/login") {
        window.location = "https://authserver.nju.edu.cn/authserver/login?service=https%3A%2F%2Fauthserver.nju.edu.cn%2Fauthserver%2Fa"
    }

    if (window.location.href === "https://authserver.nju.edu.cn/authserver/login?service=https%3A%2F%2Fauthserver.nju.edu.cn%2Fauthserver%2Fa") {
        const dlltElem = document.querySelector("#dllt")
        if (dlltElem) {
            dlltElem.value = "mobileLogin"
            alert("NJU Always Login 插件已经找到 dllt 参数并修改, 请继续登录")
        } else {
            alert("NJU Always Login 插件未找到必须的 dllt 参数, 可能不会正常工作, 请联系开发者")
        }
    }

    if (window.location.pathname === "/authserver/a"){
        GM_cookie.list({name: "CASTGC"}, function(cookies, error) {
            if (error || cookies.length === 0){
                alert("NJU Always Login 读取 Cookie 出错或未找到 CASTGC 登录态, 请联系开发者: " + error)
                return
            }

            GM_cookie.delete({ name: 'CASTGC' }, function(error) {
                if (error) {
                    alert("NJU Always Login 删除 CASTGC 出错: " + error)
                } else {
                    const castgc = cookies[0].value
                    GM_cookie.set({
                        name: 'CASTGC',
                        value: castgc,
                        url: 'https://authserver.nju.edu.cn/authserver/login',
                        path: '/authserver',
                        secure: false,
                        httpOnly: true,
                        expirationDate: Math.floor(Date.now() / 1000) + (60 * 60 * 24 * 365)
                    }, function(error) {
                        if (error) {
                            alert("NJU Always Login 设置 CASTGC 出错: " + castgc)
                        } else {
                            alert("NJU Always Login 成功持久化登录态, 请忽略后面网页上的报错, 点击确定后此网页会自动关闭, 你可以保存你的 CASTGC Cookie 供需要的自动化脚本使用: " + castgc)
                            window.close()
                        }
                    })
                }
            })
        })
    }
})()
