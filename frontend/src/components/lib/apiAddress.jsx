export let BASE_DOMAIN;
export let CAPTURE_DOMAIN;
export let WXBOT_DOMAIN;
export let NEWS_CRAWLER_DOMAIN;
export let NEWS_CRAWLER_WEBSOCKET_DOMAIN;
if(__DEV__) {
    BASE_DOMAIN = 'http://test.bao.wallstreetcn.com:3000';
    CAPTURE_DOMAIN = 'http://121.41.77.236:8080';
    WXBOT_DOMAIN = 'http://120.26.99.59:8087';
    NEWS_CRAWLER_DOMAIN = 'http://112.124.1.118';
    NEWS_CRAWLER_WEBSOCKET_DOMAIN = 'ws://112.124.1.118:8000';
} else {
    BASE_DOMAIN = 'http://bao.wallstreetcn.com';
    CAPTURE_DOMAIN = 'http://120.55.71.195:8080';
    WXBOT_DOMAIN = 'http://120.26.99.59:8087';
    NEWS_CRAWLER_DOMAIN = 'http://112.124.1.118';
    NEWS_CRAWLER_WEBSOCKET_DOMAIN = 'ws://112.124.1.118:8000';
}

const apiAddress = {
    topic: {
        list: BASE_DOMAIN + '/api/admin/subjects/list',
        search: BASE_DOMAIN + '/api/admin/search/subject',
        single: BASE_DOMAIN + '/api/admin/subjects/',
        add: BASE_DOMAIN + '/api/admin/subjects',
    },
    tag: {
        list: BASE_DOMAIN + '/api/admin/tags/list',
        single: BASE_DOMAIN + '/api/admin/tags/',
        add: BASE_DOMAIN + '/api/admin/tags',
        search: BASE_DOMAIN + '/api/admin/search/tag',
        relateTopic: BASE_DOMAIN + '/api/admin/tags/',
    },
    article: {
        list: BASE_DOMAIN + '/api/admin/messages/list',
        add: BASE_DOMAIN + '/api/admin/messages',
        single: BASE_DOMAIN + '/api/admin/messages/',
        search: BASE_DOMAIN + '/api/admin/search/message',
        top: BASE_DOMAIN + '/api/admin/messages/subject_status/',
        featureList: BASE_DOMAIN + '/api/admin/messages/featureList',
    },
    hs: {
        token: 'http://api.wallstreetcn.com/v2/itn/token/public',
    },
    qn: {
        token: BASE_DOMAIN + '/api/admin/file/upload_token?reuse=true',
        domain: 'https://baoimage.wallstreetcn.com/',
        upload: 'http://upload.qiniu.com/',
        fetchToken: BASE_DOMAIN + '/api/admin/file/fetch_token'
    },
    stock: {
        search: BASE_DOMAIN + '/api/search/stock',
    },
    user: {
        login: BASE_DOMAIN + '/api/account/mobile_login',
    },
    draft: {
        add: BASE_DOMAIN + '/api/admin/drafts',
        list: BASE_DOMAIN + '/api/admin/drafts/list',
        single: BASE_DOMAIN + '/api/admin/drafts/',
        search: BASE_DOMAIN + '/api/admin/search/draft',
    },
    homePageRec: {
        add: BASE_DOMAIN + '/api/admin/settings',
        list: BASE_DOMAIN + '/api/admin/settings',
        editorChoices: BASE_DOMAIN + '/api/admin/settings/editorChoices',
    },
    androidVersion: {
        fetch: BASE_DOMAIN + '/api/admin/settings/android_version',
        post: BASE_DOMAIN + '/api/admin/settings/android_version'
    },
    sector: {
        add: BASE_DOMAIN + '/api/admin/sset',
        single: BASE_DOMAIN + '/api/admin/sset/',
        list: BASE_DOMAIN + '/api/admin/sset/list',
        search: BASE_DOMAIN + '/api/admin/search/sset',
        range: BASE_DOMAIN + '/q/quote/v1/real',
        history: BASE_DOMAIN + '/q/quote/v1/daily-data',
        searchStock: BASE_DOMAIN + '/api/stocks/ssets'
    },
    capture: {
        sourceList: CAPTURE_DOMAIN + '/sources/list',
        single: CAPTURE_DOMAIN + '/sources',
        search: CAPTURE_DOMAIN + '/sources/search',
        tagList: CAPTURE_DOMAIN + '/tags/list',
        tag: CAPTURE_DOMAIN + '/tags',
        article: CAPTURE_DOMAIN + '/articles',
        articleWait: CAPTURE_DOMAIN + '/articles/wait',
        articleSearch: CAPTURE_DOMAIN + '/articles/search',
        articleList: CAPTURE_DOMAIN + '/articles/list',
        add: CAPTURE_DOMAIN + '/articles/publish/'
    },
    newsCrawler: {
        newsList: NEWS_CRAWLER_DOMAIN + '/api/news/',
        sourceList: NEWS_CRAWLER_DOMAIN + '/api/sources/',
        sourceSingle: NEWS_CRAWLER_DOMAIN + '/api/source/',
        sourceDefault: NEWS_CRAWLER_DOMAIN + '/api/source_default/',
        tagList: NEWS_CRAWLER_DOMAIN + '/api/tags/',
        newsRelateArticle: NEWS_CRAWLER_DOMAIN + '/news/relate/{{newsId}}/bao_article/{{baoArticleId}}/',
        websock: NEWS_CRAWLER_WEBSOCKET_DOMAIN,
        views: NEWS_CRAWLER_DOMAIN + '/api/views/',
        viewsSources: NEWS_CRAWLER_DOMAIN + '/api/views/sources/',
        viewsSourcesAll: NEWS_CRAWLER_DOMAIN + '/api/views/sources/all/',
    },
    wxbot: {
        status: WXBOT_DOMAIN + '/status',
        startOne: WXBOT_DOMAIN + '/start_one',
        killOne: WXBOT_DOMAIN + '/kill_one/',
        killAll: WXBOT_DOMAIN + '/kill_all'
    },
    splash: {
        list: BASE_DOMAIN + '/api/admin/splash/list',
        single: BASE_DOMAIN + '/api/admin/splashes/',
        post: BASE_DOMAIN + '/api/admin/splash',
        channel: BASE_DOMAIN + '/api/admin/channels/list?page=1&limit=30'
    },
    wallstreetcn: {
        slides: BASE_DOMAIN + '/api/admin/settings/wscnHomeSlides'
    }
}

export default apiAddress
