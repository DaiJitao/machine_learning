__M.define("douyin_falcon:page/reflow_user/index", function (require, exports, module) {
    "";

    function _interopRequireDefault(e) {
        return e && e.__esModule ? e : {"default": e}
    }

    function downloadApp(e, t) {
        var a = "aweme://user/profile/" + t.params.uid,
            i = appTrack.getParams({reflow_page_uid: t.params.uid, __type__: "app_track"}, a),
            n = e + "?" + urlUtil.getQueryStr(i);
        t.useDl = !0, downloadAction.downloadApp(n, t)
    }

    function getQueryString(e) {
        var t = new RegExp("(^|&)" + e + "=([^&]*)(&|$)", "i"), a = window.location.search.substr(1).match(t);
        return null != a ? unescape(a[2]) : null
    }

    function bind(e) {
        var t = e;
        _utils.default.initScrollEvents(50, 100), $(window).on("scrollEnd", function () {
            getWorkList(listType)
        }), $(".get-list").on("click", function (e) {
            var t = $(e.currentTarget).data("type");
            $(e.currentTarget).hasClass("active") !== !0 && ($(e.currentTarget).addClass("active").siblings(".tab").removeClass("active"), reload(), isLoading = !1, loadEnd = !1, params.max_cursor = 0, getWorkList(t))
        }), $(".go-author").on("click", function () {
            return isTypeSMS ? void goUser(e.uid) : void downloadApp(DOWNLOAD_URL_SETTING["reflow-user"], {
                type: "user",
                params: {uid: e.uid, type: "need_follow", gd_label: "profile_follow"}
            })
        }), pageletWorklist.on("click", ".music-item", function (e) {
            var t = $(e.currentTarget).attr("data-id");
            _tea.default.send("tap", {type: "feature", target: "work_list"});
            var a = storage.getSession("com.aweme.reflow-music-count") || 1;
            return +a >= 3 ? (_tea.default.send("tap", {
                type: "download_feature",
                target: "work_list"
            }), void downloadApp(DOWNLOAD_URL_SETTING["reflow-user"], {
                type: "music",
                params: {id: t, gd_label: "profile_feature"}
            })) : (storage.setSession("com.aweme.reflow-music-count", ++a), void(location.href = "/share/music/" + t))
        }), pageletWorklist.on("click", ".goWork", function (e) {
            var a = (this.config, $(e.currentTarget).attr("data-id")), i = $(e.currentTarget).attr("data-type"),
                n = $(e.currentTarget).attr("data-url");
            if (GA.gaevent("reflow-user", "feature", a), _tea.default.send("tap", {
                    type: "feature",
                    target: "work_list"
                }), isTypeSMS) return void goUser(t.uid);
            if ("image" === i) return void scaleImage(e.currentTarget, n);
            var o = storage.getSession("com.aweme.reflow-user-count") || 1;
            return +o >= DOWNLOAD_CLICK_LIMIT ? (GA.gaevent("reflow-user", "download_feature", a), _tea.default.send("tap", {
                type: "download_feature",
                target: "work_list"
            }), void downloadApp(DOWNLOAD_URL_SETTING["reflow-user"], {
                type: "detail",
                params: {id: a, gd_label: "profile_feature"}
            })) : (storage.setSession("com.aweme.reflow-user-count", ++o), void(location.href = "/share/video/" + a))
        }), $(".close").click(function () {
            $("#scaleImageWrapper").removeClass("full-screen"), $("#scaleImageWrapper .enlarge-wrapper").css({
                top: rectObject.top,
                left: rectObject.left
            }), setTimeout(function () {
                $("#scaleImageWrapper").hide()
            }, 300)
        }), $("#scaleImageWrapper").on("touchmove", function (e) {
            e.preventDefault()
        })
    }

    function scaleImage(e, t) {
        rectObject = e.getBoundingClientRect();
        var a = $("#scaleImageWrapper")[0];
        $("#scaleImageWrapper .enlarge-wrapper").css({
            "background-image": "url(" + t + ")",
            top: rectObject.top,
            left: rectObject.left
        }), $(a).show(), setTimeout(function () {
            $(a).addClass("full-screen"), $("#scaleImageWrapper .enlarge-wrapper").css({top: 0, left: 0})
        }, 0)
    }

    function format(e) {
        return 1e4 > e ? e : e / 1e4 + "w"
    }

    function getWorkList(e) {
        if (listType = e, !isLoading && !loadEnd) {
            isLoading = !0, loading.show();
            var t = $.extend({}, params), a = "/web/api/v2/aweme/" + e + "/";
            if ("music" === e) {
                a = "/web/api/v2/music/list/original/";
                var i = {
                    user_id: params.user_id,
                    sec_uid: params.sec_uid,
                    count: params.count,
                    cursor: params.max_cursor
                };
                t = i
            }
            t._signature = signature, t.dytk = dytk, $.ajax({
                url: a,
                type: "get",
                dataType: "json",
                data: t,
                success: function (t) {
                    if (0 !== t.status_code) return loading.hide(), void tips.show("鍔犺浇鍒楄〃澶辫触锛岃鍒锋柊閲嶈瘯");
                    if (params.max_cursor = t.max_cursor || t.cursor, t.has_more || (loadEnd = !0, loading.hide()), t.music_list && t.music_list.length) {
                        hasListData[e] = !0;
                        var a = t.music_list.map(function (e) {
                            return {
                                mid: e.mid,
                                count: e.use_count_desc,
                                imgUrl: _utils.default.getDeepValue(e, "cover_thumb.url_list[0]") || "",
                                name: e.title,
                                duration: number.formatSecond(e.duration)
                            }
                        });
                        renderWorkList(MUSIC_TMPL, a)
                    } else if (t.aweme_list && t.aweme_list.length) {
                        hasListData[e] = !0;
                        var i = t.aweme_list.map(function (e) {
                            return {
                                id: e.aweme_id,
                                cover: _utils.default.getDeepValue(e, "video.cover.url_list[0]") || "",
                                good_choice: e.good_choice || 0,
                                label_url: _utils.default.getDeepValue(e, "label_large.url_list[0]") || "",
                                digg_num: format(_utils.default.getDeepValue(e, "statistics.digg_count") || 0),
                                isImage: 2 === e.aweme_type ? !0 : !1,
                                imageUrl: _utils.default.getDeepValue(e, "image_infos[0].label_large.url_list[0]")
                            }
                        });
                        renderWorkList(LIST_TMPL, i), params.max_cursor === t.max_cursor
                    } else 0 == hasListData[e] && showEmpty({type: listType})
                },
                error: function (e) {
                    console.log("error>", e)
                },
                complete: function () {
                    isLoading = !1
                }
            })
        }
    }

    function showEmpty(e) {
        pageletWorklist.show().find(".js-list").html(EMPTY_TMPL({text: EMPTY_TEXT[e.type]}))
    }

    function reload() {
        pageletWorklist.show().find(".js-list").empty()
    }

    function renderWorkList(e, t) {
        pageletWorklist.show().find(".js-list").append(e({list: t || []}))
    }

    function createDOM() {
        var e = getQueryString("code");
        if (e) {
            var t = document.createElement("span");
            t.className = "sms-code", t.innerText = e, t.id = "js-copy-text", document.body.appendChild(t)
        }
    }

    function smsInvite() {
        -1 !== window.location.href.indexOf("sms_invite") && (isTypeSMS = !0, setTimeout(createDOM, 500))
    }

    function goUser(e) {
        copyText("js-copy-text"), downloadApp(DOWNLOAD_URL_SETTING["sms-invite"], {
            type: "user",
            params: {uid: e, gd_label: "profile_follow"}
        })
    }

    function copyText(e) {
        var t = document.getElementById(e);
        if (window.getSelection && t) {
            var a = document.createRange();
            return a.selectNode(t), window.getSelection().removeAllRanges(), window.getSelection().addRange(a), document.execCommand("copy")
        }
        if (document.selection) {
            var i = document.body.createTextRange();
            return i.moveToElementText(t), i.select().createTextRange(), document.execCommand("copy")
        }
    }

    var _utils = _interopRequireDefault(require("douyin_falcon:common/util/utils")),
        _tea = _interopRequireDefault(require("douyin_falcon:common/tea/tea")),
        _bytedAcrawler = require("douyin_falcon:node_modules/byted-acrawler/dist/runtime"), LIST_TMPL = function (obj) {
            {
                var __t, __p = "";
                Array.prototype.join
            }
            with (obj || {}) __p += "", _.each(list, function (e) {
                __p += '\n\n    <li class="item goWork" data-id="' + (null == (__t = e.id) ? "" : __t) + '" data-type="' + (null == (__t = e.isImage ? "image" : "video") ? "" : __t) + '" data-url="' + (null == (__t = e.imageUrl || "") ? "" : __t) + '">\n\n        ', e.isImage ? (__p += '\n            <div class="cover lazy" data-src="' + (null == (__t = e.imageUrl || "") ? "" : __t) + '" >\n                <img src="" alt="" class="image-icon">\n\n                ', 1 === e.good_choice && (__p += '\n                    <div class="label" style="background-image: url(' + (null == (__t = e.label_url) ? "" : __t) + ') "></div>\n                '), __p += '\n                <div class="digg">\n                    <span class="digg-icon"></span>\n                    <span class="digg-num">' + (null == (__t = e.digg_num) ? "" : __t) + "</span>\n                </div>\n            </div>\n        ") : (__p += '\n            <div class="cover lazy" data-src="' + (null == (__t = e.cover) ? "" : __t) + '" >\n                ', 1 === e.good_choice && (__p += '\n                <div class="label" style="background-image: url(' + (null == (__t = e.label_url) ? "" : __t) + ') "></div>\n                '), __p += '\n                <div class="digg">\n                    <span class="digg-icon"></span>\n                    <span class="digg-num">' + (null == (__t = e.digg_num) ? "" : __t) + "</span>\n                </div>\n            </div>\n        "), __p += "\n\n    </li>\n\n"
            }), __p += "";
            return __p
        }, MUSIC_TMPL = function (obj) {
            {
                var __t, __p = "";
                Array.prototype.join
            }
            with (obj || {}) __p += "", _.each(list, function (e) {
                __p += '\n    <li class="music-item" data-id="' + (null == (__t = e.mid) ? "" : __t) + '" >\n        <div class="item-pic">\n            <div class="pic-cover"></div>\n            <img src="' + (null == (__t = e.imgUrl) ? "" : __t) + '" />\n            <i class="icon-music-play"></i>\n        </div>\n        <div class="item-content">\n            <h4 class="item-content-name">' + (null == (__t = e.name) ? "" : __t) + '</h4>\n            <p class="item-content-used">' + (null == (__t = e.count) ? "" : __t) + ' 浜轰娇鐢�</p>\n            <p class="item-content-duration">' + (null == (__t = e.duration) ? "" : __t) + '</p>\n        </div>\n        <div class="item-opt"></div>\n    </li>\n'
            }), __p += "";
            return __p
        }, EMPTY_TMPL = function (obj) {
            {
                var __t, __p = "";
                Array.prototype.join
            }
            with (obj || {}) __p += '<div class="empty">' + (null == (__t = text) ? "" : __t) + "</div>\n";
            return __p
        }, number = require("douyin_falcon:common/util/number"), urlUtil = require("douyin_falcon:common/util/url"),
        storage = require("douyin_falcon:common/util/storage"),
        appTrack = require("douyin_falcon:common/util/appTrack"),
        downloadAction = require("douyin_falcon:common/download_sdk/download_sdk"),
        banner = require("douyin_falcon:component/banner/index"),
        loading = require("douyin_falcon:component/loading/index"),
        tips = require("douyin_falcon:component/tips/index"), GA = require("douyin_falcon:common/ga/ga");
    GA.gapageview();
    var isTypeSMS = !1, COUNT = 21, DOWNLOAD_CLICK_LIMIT = 0, nonce = "", signature = "", isLoading = !1, loadEnd = !1,
        hasListData = {post: !1, favorite: !1},
        params = {user_id: "", sec_uid: "", count: COUNT, max_cursor: 0, aid: 1128},
        DOWNLOAD_URL_SETTING = {"reflow-user": "//d.dyvideotape.com/PxRW/", "sms-invite": "//d.douyin.com/fMcS/"},
        EMPTY_TEXT = {post: "TA杩樻病鏈夊彂甯冭繃浣滃搧", favorite: "TA杩樻病鏈夊枩娆㈢殑浣滃搧"}, stickyEl = $(".tab-wrap"),
        pageletWorklist = $("#pagelet-worklist"), listType = stickyEl.find(".tab").eq(0).attr("data-type"),
        stickyHolder = $(".video-tab"), rect = stickyEl.get(0).getBoundingClientRect();
    stickyHolder.attr("height", rect.height + "px");
    var stickyT = stickyEl.get(0).offsetTop, dytk = "", rectObject = null;
    window.onscroll = function () {
        var e = document.body.scrollTop;
        e > stickyT ? stickyEl.addClass("tab-box-fixed") : stickyEl.removeClass("tab-box-fixed")
    }, exports.init = function (e) {
        dytk = e.dytk, params.user_id = e.uid, params.sec_uid = _utils.default.getUrlParam(window.location.href, "sec_uid"), "" != params.sec_uid && delete params.user_id, nonce = e.uid, signature = _bytedAcrawler.sign(nonce), _tea.default.setEventCommonParams({page_name: "reflow_user"}), _tea.default.send("page_view", {}), bind(e), getWorkList(listType), smsInvite(e.uid);
        var t = function () {
            goUser(e.uid)
        };
        banner.init({
            dl: DOWNLOAD_URL_SETTING["reflow-user"],
            callback: isTypeSMS ? t : null,
            opts: {type: "user", useDl: !0, params: {uid: e.uid, type: "need_follow", gd_label: "profile_bottom"}},
            teaLogger: _tea.default,
            pageTag: "reflow-user"
        })
    }
});