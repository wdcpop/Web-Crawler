$(document).ready(function () {
    var old;
    var websocket_addr = 'ws://'+document.domain+':8000/';
    // var websocket_addr = 'ws://112.124.1.118:8000/';
    openWebSocket();
    function openWebSocket() {
        var s = new WebSocket(websocket_addr);
        s.onopen = function (e) {
            console.log('opened');
            if (window.location.href.indexOf('important')>0){
                s.send('important');
                console.log('important');
            }else{
                s.send('normal');
                console.log('normal');
            }
        };
        s.onclose = function (e) {
            console.log('closed');
            setTimeout(openWebSocket, 1000);
        };
        s.onmessage = function (e) {
            var res = JSON.parse(e.data);
            // console.log(res);
            if (res.code == 200) {
                var dataContent = {};
                res.results.map(function (item) {
                    appendTitle(item);
                    addContent(dataContent, item);
                });
                insertContent(dataContent);
                old=dataContent;
                $(".loading-title").css("display", "none");
                $("#loading-more").css("display", "block");
                $(".loading-p").css("display", "none");
                $(".jumbotron").css("display", "block");
            } else if (res.code == 201) {
                var newContent = [];
                $(".title-list").each(function () {
                    newContent.push($(this).attr("data-link"));
                });
                var str = newContent.join(",");
                var hasNewContent = false;
                var countNum = 0;
                for (var i = 0; i < res.results.length; i++) {
                    if (str.indexOf(res.results[i].link) == -1) {
                        beforeTitle(res.results[i]);
                        addContent(old, res.results[i]);
                        hasNewContent = true;
                        countNum++;
                    }
                }
                if (hasNewContent) {
                    // $("#loading-more-count").text(countNum + "条新内容");
                } else {
                    // $("#loading-more-count").text("没有更多内容");
                }
                insertContent(old);
            }else if(res.code==202){
                var name = res.results.name.split('.')[0].slice(1);
                $('#crawled').text(name);
                tb_ani(name);
            }
        }
    }


    function tb_ani(name){
        var items=$('.spider_name');
        items.map(function (k,item) {
            var spider=$(item);
            if (spider.text().indexOf(name)!=-1){
                // spider.animate({'font-size':'16px'},100,function () {
                //     spider.animate({'font-size':'14px'},100);
                // });
                spider.css({'font-weight':'bold'});
                setTimeout(function () {
                    spider.css({'font-weight':'normal'});
                },500)
            }
        })
    }
    function beforeTitle(item) {
        var insertTime = item.ctime_formatted;
        $('<li class="title-list" data-link="' + item.link + '" data-time="' + item.ctime + '">' +
            '<a href="#">' + item.title + '<br /><span class="title-source">' + " 来源: " +
            item.name + '</span><br /><span class="title-time">' + ' 入库时间: ' +
            insertTime + '</span></a></li>').insertBefore($(".title-list:eq(0)"));
    }

    function appendTitle(item) {
        var insertTime = item.ctime;
        $('<li class="title-list" data-link="' + item.link + '" data-time="' + item.ctime + '">' +
            '<a href="#">' + item.title + '<br /><span class="title-source">' + " 来源: " + item.name + '</span><br /><span class="title-time">' + ' 入库时间: ' + insertTime + '</span>' +
            '</a></li>').appendTo("#title");
    }

    var skip = 20;
    $("#loading-more").on("click", function () {
        loadingMore(skip);
        skip += 20;
    });


    function addContent(map, item) {
        var aTime;
        if (item.time) {
            aTime = item.time;
        } else {
            aTime = "";
        }
        map[item.link] = item.content;
        map[item.link + "title"] = item.title;
        map[item.link + "author"] = "作者: " + item.name;
        map[item.link + "time"] = "时间: " + aTime;
        map[item.link + "source"] = "来源: " + item.host;
        map[item.link + "link"] = item.link;
    }

    function insertContent(map) {
        $(".title-list").each(function () {
            $(this).off("click").on("click", function () {
                var link = $(this).attr("data-link");
                $(this).addClass("active").siblings().removeClass("active");
                $(this).find("a").addClass("clicked");
                $("#content-title").text(map[link + "title"]);
                $("#content").html(map[link]);
                $(".author").text(map[link + "author"]);
                $(".source").text(map[link + "source"]);
                $(".time").text(map[link + "time"]);
                if (map[link + "source"].indexOf("weibo") == -1 && map[link + "source"].indexOf("weixin") == -1) {
                    $(".link a").removeClass("display").attr("href", map[link + "link"]).text("原文链接");
                } else {
                    $(".link a").addClass("display");
                }
            })
        })
    }


    function loadingMore(skip) {
        $.ajax({
            url: '/api/news2/?limit=20&skip='+skip,
            type: "GET",
            dataType: "jsonp",
            beforeSend: function () {
                $(".loading-more-title").css("display", "block");
                $(".loading-more").css("display", "none");
            },
            statusCode: {
                404: function () {
                    $("#modal-text").text("没有更多内容了");
                    $("button").click();
                },
                500: function () {
                    $("#modal-text").text("数据加载失败");
                    $("button").click();
                }
            },
            success: function (res) {
                if (res.code != 0) {
                    $("#modal-text").text(res.msg);
                    $("button").click();
                } else {
                    res.results.map(function (item) {
                        var map = {};
                        appendTitle(item);
                        addContent(map, item);
                        insertContent(map);
                    })
                }
            },
            complete: function () {
                $(".loading-more-title").css("display", "none");
                $(".loading-more").css("display", "block");
            },
            error: function () {
                $("#modal-text").text("数据加载失败");
                $("button").click();
            }
        })
    }

});