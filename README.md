#NewsCrawler
新版新闻增量抓取爬虫

## 来源
1. 阿斯达克 <http://www.aastocks.com/sc/stocks/news/aafn>
2. 百度百家-财经版 <http://baijia.baidu.com/?tn=listarticle&labelid=6>
3. 财新网 <http://www.caixin.com/search/scroll/index.jsp>
4. 中金所 <http://www.cffex.com.cn/tzgg/jysgg/>
5. 中国新闻网 <http://www.chinanews.com/cj/gd.shtml>
6. 华夏时报 <http://www.chinatimes.cc/finance>
7. 央广网-经济之声 <http://roll.cnr.cn/finance/>
8. 上证快讯 <http://news.cnstock.com/bwsd/index.html>
9. 证监会要闻 <http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/>
10. 郑商所 <http://www.czce.com.cn/portal/jysdt/ggytz/A090601index_1.htm>
11. 大商所 <http://www.dce.com.cn/portal/cate?cid=1272437227100>
12. 经济观察 <http://www.eeo.com.cn/politics/>
13. 中国政府-新闻 <http://www.gov.cn/xinwen/gundong.htm>
14. 中国政府-政策 <http://www.gov.cn/zhengce/zuixin.htm>
15. 航运界 <http://www.ship.sh/info.php>
16. 界面网 <http://www.jiemian.com/lists/9.html>
17. 21经济 <http://m.21jingji.com/>
18. 财新一线 <http://k.caixin.com/web/>
19. 证券时报 <http://kuaixun.stcn.com/>
20. 外交部 <http://www.mfa.gov.cn/web/zyxw/>
21. 工信部
>
                         http://www.miit.gov.cn/n1146290/n1146392/index.html
                         http://www.miit.gov.cn/n1146290/n1146402/index.html
                         http://www.miit.gov.cn/n1146290/n4388791/index.html
22. 财政部 <http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/>
23. 商务部 <http://www.mofcom.gov.cn/article/ae/ai/>
24. 人社部 <http://www.mohrss.gov.cn/SYrlzyhshbzb/shehuibaozhang/zcwj/yiliao/>
25. 网易财经 <http://money.163.com/special/00251G8F/news_json.js>
26. 发改委 
> 
        http://www.ndrc.gov.cn/zcfb/zcfbghwb/
        http://bgt.ndrc.gov.cn/zcfb/
        http://www.ndrc.gov.cn/xwzx/xwfb/
        http://tzs.ndrc.gov.cn/tzgz/
        http://gys.ndrc.gov.cn/gyfz/index.html
    
27. 新华网 
> 
            'http://www.news.cn/fortune/gd.htm',
            'http://www.xinhuanet.com/politics/24xsyw.htm',
            'http://www.news.cn/politics/leaders/gdxw.htm'
        
28. 卫计委 <http://www.nhfpc.gov.cn/zhuzhan/xwfb/lists.shtml>
29. 全景快讯 <http://www.p5w.net/kuaixun/tj/>
30. 中国人民银行 <http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html>
31. 路透中文 <http://cn.reuters.com/rssFeed/chinaNews/>，<http://cn.reuters.com/rssFeed/CNIntlBizNews/>
32. 国家外汇管理局 <http://www.safe.gov.cn/wps/portal/sy/news_ywfb>
33. 国资委 <http://www.sasac.gov.cn/n85881/n85901/index.html>
34. 食药监总局 <http://www.sda.gov.cn/WS01/CL0051/>
35. 上期所 <http://www.shfe.com.cn/news/notice/index.html>
36. 新浪财经 <http://roll.finance.sina.com.cn/finance/gncj/hgjj/index.shtml>
37. 体育总局 <http://www.sport.gov.cn/n10503/index.html>
38. 上交所 <http://www.sse.com.cn/disclosure/announcement/general/>
39. 统计局 <http://www.stats.gov.cn/tjsj/zxfb/>
40. 腾讯证券 <http://stock.qq.com/l/stock/list20150525114649.htm>
41. 深交所 <http://www.szse.cn/main/disclosure/bsgg_front/>
42. 腾讯科技 <http://n.rss.qq.com/rss/tech_rss.php>
43. 新浪科技 <http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=30&spec=&type=&date=&ch=05&k=&offset_page=0&offset_num=0&num=60&asc=&page=1>
44. TechWeb <http://www.techweb.com.cn/roll/>
45. 澎湃新闻-财经 <http://www.thepaper.cn/channel_scroll.jsp?channelID=25951>
46. 华尔街见闻 <https://api.wallstreetcn.com/v2/posts>
47. 第一财经
>
            'http://www.yicai.com/news/business/'
            'http://www.yicai.com/news/markets/'
            'http://www.yicai.com/news/technology/'
            'http://www.yicai.com/news/finance/'
            'http://www.yicai.com/news/economy/'
48. 经济通 <http://news.etnet.com.cn/all>
49. 香港经济日报 <http://inews.hket.com/sran001/>
50. 银行间商协会 <http://www.nafmii.org.cn/zdgz/>


## 部署
1. VPS： root@112.124.1.118
2. 方式：supervisor
3. 配置：`conf`文件夹


## Web管理界面
<http://112.124.1.118/>


## WEB端接口文档
备注：端口和Web管理界面一致，即80

| API | 批量获取新闻 |
| --- | --------- |
| url | /api/news/ |
| method | GET |

传递参数:
| 参数名称 | 默认值 | 备注 |
| --- | --------- | ----------- |
| limit | 1 | 列举的新闻条目 |
| skip | 0 | 列举新闻的起始处（用于遍历获取新闻） |
| source | 无 | 获取的新闻来源（爬虫名称）|

返回数据(JSON):
```
{
        data: [
                {
                        content: " <p></p><p></p><p> 《經濟通通訊社18日專訊》361度（01361）公布第三季度營運數據</p>... ",
                        ctime: 1476781576,
                        host: "invest.hket.com",
                        link: "http://invest.hket.com/article/1522811/《神州民企》361度第三季主品牌及童裝同店銷售各升7.3-",
                        name: "香港经济日报",
                        time: 1476781380,
                        title: "《神州民企》361度第三季主品牌及童裝同店銷售各升7.3%"
                }
        ],
        total: 287799
}
```

## WebSocket端接口文档
备注：WebSocket端口为8000

| API | 接收新闻推送 |
| --- | --------- |
| url | / |

数据格式(JSON):
```
{
        content: " <p></p><p></p><p> 《經濟通通訊社18日專訊》361度（01361）公布第三季度營運數據</p>... ",
        ctime: 1476781576,
        host: "invest.hket.com",
        link: "http://invest.hket.com/article/1522811/《神州民企》361度第三季主品牌及童裝同店銷售各升7.3-",
        name: "香港经济日报",
        time: 1476781380,
        title: "《神州民企》361度第三季主品牌及童裝同店銷售各升7.3%"
}
```