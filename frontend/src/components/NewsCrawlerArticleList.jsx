import React, { Component } from 'react'
import { Icon, Popconfirm, message, Row, Col, Tooltip, Button, Spin, Form, Select, BackTop, notification, Switch, Popover, Badge } from 'antd'
import { Link } from 'react-router'

// modules
import { renderSearchBar } from './lib/Search'
import apiAddress from './lib/apiAddress';
import { formatTime, reachBottom } from './lib/util'
import HttpService from './lib/HttpService';
import RequestParam from './lib/RequestBean';
import FavBox from './FavBox';
var { OperationHeart, FavTable } = new FavBox('newsCrawler')

var Table = require('antd/lib/table');
import {tableDecoratorAddColumnCloseButton} from './lib/AntOverride/overrideTable'
Table = tableDecoratorAddColumnCloseButton(Table);

// components
import NewsCrawlerViewAddModal from './NewsCrawlerViewAddModal'
import NewsCrawlerViewEditModal from './NewsCrawlerViewEditModal'
import NewsCrawlerViewDeleteModal from './NewsCrawlerViewDeleteModal'

// css
import './NewsCrawlerArticleList.css';

var newsListSample = {
    data: [
        {
            id: "",
            content: " <p></p><p></p><p> 《經濟通通訊社18日專訊》361度（01361）公布第三季度營運數據</p>... ",
            ctime: 1476781576,
            host: "invest.hket.com",
            link: "http://invest.hket.com/article/1522811/《神州民企》361度第三季主品牌及童裝同店銷售各升7.3-",
            name: "香港经济日报",
            time: 1476781380,
            title: "《神州民企》361度第三季主品牌及童裝同店銷售各升7.3%"
        },
        {
            id: "",
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


export default class NewsCrawlerArticleList extends Component {
    constructor(props, context) {
        super(props, context)
        this.state = {
            data: [],
            tagsList: [],
            sourceList: [],
            searchVal: '',
            keyword: undefined,
            is_keyword_full: 0,
            loading: false,
            loadingMore: false,
            pageSize: 30,
            // newArticles: [],
            tagValue: '',
            sourceTempValue: '',
            sourceValue: '',
            websockIsOpened: false,
            viewList: [],
        }
        this.defaultSoucesConfigs = {};
        this.currentViewName = undefined;
        this.currentViewSourcesConfigs = undefined;
        this.websock = null;
        this.componentIsUnmounting = false;
        this.socketReopenedTimes = 0;
        this.request = new HttpService()
        this.handleTagsChange = this.handleTagsChange.bind(this)
        this.handleSearchSource = this.handleSearchSource.bind(this)
        this.handleSetSource = this.handleSetSource.bind(this)
        this.handleSearchInput = this.handleSearchInput.bind(this)
        this.handleScrollEvent = this.handleScroll.bind(this);
        this.fetchScroll = this.fetchScroll.bind(this);
        this.handleRefresh = this.handleRefresh.bind(this);
        this.handleTableChange = this.handleTableChange.bind(this);
        this.sourceTempValue = ''
    }
    _refreshList() {
        this.handleRefresh();
    }
    initializeData() {
        var self = this;
        this.setState({loading: true})
        this.fetchDefaultSourcesConfigs(function(){
            self.fetchScroll()
        })
        this.refreshViews()
    }
    mergeObjectList(arr1, arr2, prop) {
        var arr3 = [];
        for(var i in arr1){
            var shared = false;
            for (var j in arr2)
                if (arr2[j][prop] == arr1[i][prop]) {
                    shared = true;
                    break;
                }
            if(!shared) arr3.push(arr1[i])
        }
        return arr3.concat(arr2);
    }
    fetchScroll(start_fresh) {
        var self = this
        let lastMark
        if(this.state.data.length) {
            lastMark = this.state.data[this.state.data.length-1].id
        }
        if (start_fresh) {
            lastMark = ''
        }
        let hide = message.loading('加载数据中...')
        const data = {
            limit: this.state.pageSize,
            tagId: this.state.tagId || undefined,
            source: this.state.sourceMachineName || undefined,
            keyword: this.state.keyword || undefined,
            is_keyword_full: this.state.is_keyword_full || 0,
            source_keyword: this.state.source_keyword || undefined,
            startwith: lastMark,
            offset: lastMark ? 1 : 0,
            sort: this.state.sortField || undefined,
        }
        let url = apiAddress.newsCrawler.newsList
        let reqParam = new RequestParam().setUrl(url).setData(data)
            .setSuccess((result) => {
                let resultList = result.data
                if(resultList.length === 0) {message.warning('没有更多数据'); return;}

                if (start_fresh) {
                    var newData = self.viewAlterAll(resultList)
                } else {
                    var newData = self.viewAlterAll(self.mergeObjectList(this.state.data, resultList, 'id'))
                }

                this.setState({
                    data: newData,
                    loadingMore: false,
                    loading: false,
                }, () => {
                    hide()
                    window.addEventListener('scroll', this.handleScrollEvent);
                })
            })
            .setError(() => window.addEventListener('scroll', this.handleScrollEvent))
        this.request.doGet(reqParam)
    }
    fetchTagList() {
        let reqParam = new RequestParam().setUrl(apiAddress.newsCrawler.tagList)
            .setSuccess((result) => {
                this.setState({
                    tagsList: result
                })
            })
        this.request.doGet(reqParam)
    }
    fetchDefaultSourcesConfigs(callback) {
        var self = this
        let url = apiAddress.newsCrawler.sourceList
        let reqParam = new RequestParam().setUrl(url).setData({
            limit: 1000
        })
            .setSuccess((d) => {
                var viewConfigsArr = d['data'];
                var viewConfigs = {}
                viewConfigsArr.forEach(function(item) {
                    if (!item['machine_name']) {
                        return
                    }
                    viewConfigs[item['machine_name']] = item
                })
                this.defaultSoucesConfigs = viewConfigs;
                callback()
            })
            .setError(() => {})
        this.request.doGet(reqParam)
    }
    handleSearchInput(value, is_keyword_full) {
        this.setState({
            tagId: undefined,
            source_keyword: undefined,
            sourceMachineName: undefined,
            keyword: value.trim(),
            is_keyword_full: is_keyword_full || 0,
            tagValue: '',
            sourceValue: '',
            data: [],
        }, () => this.fetchScroll())
    }
    handleTagsChange(tagId) {
        this.setState({
            tagValue: tagId,
            keyword: undefined,
            source_keyword: undefined,
            sourceMachineName: undefined,
            sourceValue: '',
            tagId,
            data: [],
        }, () => this.fetchScroll())
    }
    handleSetSource(sourceMachineName) {
        this.setState({'sourceTempValue': sourceMachineName})
        this.setState({
            keyword: undefined,
            source_keyword: undefined,
            tagId: undefined,
            tagValue: '',
            sourceMachineName,
            sourceValue: sourceMachineName,
            data: [],
        }, () => this.fetchScroll())
    }
    handleSetSourceKeyword(sourceKeyword) {
        this.setState({
            keyword: undefined,
            source_keyword: sourceKeyword,
            tagId: undefined,
            tagValue: '',
            sourceMachineName: undefined,
            sourceValue: undefined,
            data: [],
        }, () => this.fetchScroll())
    }
    handleSearchSource(value){
        this.sourceTempValue = value
        const val = value.trim()
        if(val) {
            let reqParam = new RequestParam().setUrl(apiAddress.newsCrawler.sourceList).setData({keyword: val})
                .setSuccess((result) => {
                    this.setState({ sourceList: result.data })
                })
            this.request.doGet(reqParam)
        }
    }
    handleRefresh() {
        this.setState({
            loading: true,
            source_keyword: undefined,
            keyword: undefined,
            sourceMachineName: undefined,
            data: [],
            // newArticles: [],
            tagValue: this.state.tagId ? this.state.tagValue : '',
            sourceValue: '',
        }, () => this.fetchScroll())
    }
    handleTableChange(pagination, filters, sorter) {
        if(sorter.order) {
            const order = sorter.order.indexOf('desc') > -1 ? 'desc' : 'asc'
            const sortField = `${sorter.field}_${order}`
            this.setState({
                sortField,
                data: []
            }, () => this.fetchScroll())
        } else {
            this.setState({
                sortField: undefined,
                data: []
            }, () => this.fetchScroll())
        }
    }
    handleScroll() {
        if(reachBottom()) {
            this.setState({loadingMore: true})
            this.fetchScroll()
            window.removeEventListener('scroll', this.handleScrollEvent);
        }
    }
    renderLoading() {
        if(this.state.loadingMore) {
            return (
                <p style={{margin: 50, textAlign: 'center'}}>Loading...</p>
            )
        }
    }
    toggleAutoRefresh() {
        if (this.state.websockIsOpened) {
            this.closeWebSocketAndCleanup()
        } else {
            this.openNewWebSocket()
        }
    }
    refreshViews() {
        var self = this
        let url = apiAddress.newsCrawler.views;
        let reqParam = new RequestParam().setUrl(url)
            .setSuccess((d) => {
                var viewList = d['data'];
                self.setState({viewList: viewList})
            })
            .setError(() => {
                console.log('get views err!');
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
            })
        this.request.doGet(reqParam)
    }
    openNewWebSocket() {
        var self = this;

        function makeid(num)
        {
            var text = "";
            var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

            for( var i=0; i < num; i++ )
                text += possible.charAt(Math.floor(Math.random() * possible.length));

            return text;
        }

        this.latest_ctime_after_socket_opened = self.state.data[0]['ctime']


        var websocket_addr = apiAddress.newsCrawler.websock;

        this.closeWebSocketAndCleanup();
        var s = new WebSocket(websocket_addr);
        this.websock = s;

        s.onopen = function (e) {
            console.log('socket truly opened');
            self.setState({websockIsOpened: true});

            if (window.location.href.indexOf('important')>0){
                s.send('important');
                console.log('important');
            }else{
                s.send('normal');
                console.log('normal');
            }
        }.bind(this);
        s.onclose = function (e) {
            console.log('socket onclose triggered');
            setTimeout(function(){
                if (self.socketReopenedTimes <= 20 && !self.componentIsUnmounting) {
                    console.log('reopenning socket');
                    self.openNewWebSocket();
                    self.socketReopenedTimes = self.socketReopenedTimes + 1;
                } else {
                    console.log('Reopened too many times, stop websocket reopening.')
                }
            }, 5000);
        }.bind(this);
        s.onmessage = function (e) {
            var self = this;
            var res = JSON.parse(e.data);
            // console.log(res);
            if (res.code == 200) {

            } else if (res.code == 201) {
                // console.log(res);
                var newData = this.state.data.slice(0)
                var updated = false
                for (var i = 0; i < res.results.length; i++) {
                    var data = res.results[i]
                    if (typeof newData[0] == 'object' && data['ctime'] <= self.latest_ctime_after_socket_opened) {
                        continue
                    }
                    data = self.viewAlterOne(data)
                    if (!data) {
                        continue
                    }
                    newData.unshift(data)
                    if (newData.length > 100) {
                        newData = newData.slice(0, 100)
                    }
                    updated = true
                }

                if (updated) {
                    self.setState({
                        data: newData
                    })
                }

            }else if(res.code==202){

            }
        }.bind(this)
    }
    closeWebSocketAndCleanup() {
        if (!this.state.websockIsOpened) {
            return;
        }
        if (!this.websock || !this.websock['close']) {
            return;
        }

        this.websock.onclose = function () {};
        this.websock.close();
        this.websock = null;
        console.log('socket truly closed');
        this.setState({
            websockIsOpened: false
        })

    }
    componentDidMount() {
        var self = this
        this.initializeData()
        this.fetchTagList()

        // only open socket after article initialized
        self.initOpenSocketLoop = setInterval(() => {
            console.log('loop waiting for articles initializing');
            if (self.state.data.length > 0) {
                if (!self.componentIsUnmounting) {
                    this.openNewWebSocket()
                }
                clearInterval(self.initOpenSocketLoop)
            }
            if (self.componentIsUnmounting) {
                clearInterval(self.initOpenSocketLoop)
            }
        }, 500);

        window.addEventListener('scroll', this.handleScrollEvent);

    }
    viewAlterOne(item) {
        if (!this.defaultSoucesConfigs && !this.currentViewSourcesConfigs) {
            return item
        }

        // 如果已启用一个视图
        if (this.currentViewSourcesConfigs) {
            var conf = this.currentViewSourcesConfigs[item['source']]

            // 如果视图没有设置显示这个来源，则返回false，跳过该条目
            if (!conf) {
                return false
            }
            if (conf['importance']) {
                item['importance'] = conf['importance']
                return item
            }
        }
        if (this.defaultSoucesConfigs) {
            var conf = this.defaultSoucesConfigs[item['source']] || {}
            item['importance'] = conf['star'] || 0
            return item
        }

    }
    viewAlterAll(data) {
        console.log(this.currentViewSourcesConfigs)
        var self = this;
        var newData = [];
        data.forEach((item, index) => {
            var newItem = self.viewAlterOne(item)
            console.log(newItem)
            if (newItem) {
                newData[index] = newItem
            }
        })

        return newData
    }
    setView(viewName) {
        var self = this;
        if (!viewName) {
            this.currentViewName = undefined;
            this.currentViewSourcesConfigs = undefined;
            this.fetchScroll(true)
            return
        }
        let url = apiAddress.newsCrawler.viewsSources;
        let reqParam = new RequestParam().setUrl(url).setData({'viewName': viewName})
            .setSuccess((d) => {
                var viewConfigsArr = d['data'];
                var viewConfigs = {}
                viewConfigsArr.forEach(function(item) {
                    viewConfigs[item['sourceName']] = item
                })
                this.currentViewName = viewName;
                this.currentViewSourcesConfigs = viewConfigs;
                this.fetchScroll(true)
            })
            .setError(() => {
                console.log('get selfViewConfigs err!');
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
            })
        this.request.doPost(reqParam)
    }
    componentWillUnmount() {
        window.removeEventListener('scroll', this.handleScrollEvent);
        this.componentIsUnmounting = true;
        this.closeWebSocketAndCleanup();

    }


    render() {
        // console.log('rerender')
        let self = this;
        const columns = [{
            title: '收藏',
            index: 'heart',
            width: 30,
            render(item, record, dataIndex) {
                return (
                    <OperationHeart key={dataIndex} record={item}/>
                )
            }
        }, {
            title: '标题',
            dataIndex: 'title',
            index: 'title',
            className: 'news-title-column',
            render(item, record, dataIndex) {
                return (
                    <div className="table-cell-wrap" key={item.id}>
                        <div className="news-title-main">
                            <a href="javascript:void(0)" onClick={(e) => {
                                console.log(jQuery(e.target));
                                jQuery(e.target).addClass('news-viewed');
                                self.props.onClickTitle(item, record, dataIndex)
                            }}>
                                {item}
                            </a>
                        </div>
                        <div className="news-title-sub">{record.name}</div>
                    </div>
                )
            }
        }, {
            title: '网站发表时间',
            dataIndex: 'ctime',
            index: 'ctime',
            sorter: true,
            render(item, record, dataIndex) {
                return <span key={dataIndex}>{item && formatTime(item * 1000)}</span>
            }
        }, {
            title: '编辑发表时间',
            dataIndex: 'related_bao_article_published',
            index: 'related_bao_article_published',
            sorter: true,
            render(item, record, dataIndex) {
                // return <span>{item && formatTime(item * 1000)}</span>
                return (
                    <div className="table-cell-wrap" key={dataIndex}>
                        {record.related_bao_article_id &&
                        <Link to={`/article/edit/${record.related_bao_article_id}`} target='_blank'>
                            {item && formatTime(item * 1000)}
                        </Link>
                        }
                    </div>
                )
            }
        }, {
            title: '来源',
            dataIndex: 'name',
            index: 'source'
        },
            // {
            //   title: '话题',
            //   dataIndex: 'source.defaultSubjects',
            //   index: 'source.defaultSubjects',
            //   render(items) {
            //     let arr = items ? items.map(subject => {
            //       return subject.Title
            //     }) : []
            //     return <span>{arr.join(',')}</span>
            //   }
            // },
            // {
            //   title: '标签',
            //   dataIndex: 'source.tags',
            //   index: 'tags',
            //   render(item) {
            //     let arr = item ? item.map(tag => {
            //       return tag.name
            //     }): []
            //     return <span>{arr.join(',')}</span>
            //   }
            // }
            // , {
            //   title: '操作',
            //   index: 'operation',
            //   render: this.props.renderOperation.bind(this)
            // }
        ]

        const tags = this.state.tagsList.map((item, index) => (
            <Option key={index+1} value={item.id}>{item.name}</Option>
        ))
        tags.unshift(<Option key={0} value=''>全部</Option>)

        const sourceOptions = this.state.sourceList.map((item, index) => (
            <Option key={index+1} value={item.machine_name}>{item.title}</Option>
        ))
        sourceOptions.unshift(<Option key={0} value=''>全部</Option>)

        var favContent = (<FavTable handleSearchInput={this.handleSearchInput} onClickTitle={this.props.onClickTitle}/>)


        const views_tabs = this.state.viewList.map(function(item, key){
            return <div style={{marginRight: 20, display: 'inline-block'}} key={key}>
                <Badge count={item['count']} key="1">
                    <Button
                        type={self.currentViewName == item['name'] ? "primary" : "ghost"}
                        onClick={() => {self.setView(item['name'])}}>{item['name']}</Button>
                </Badge>
                <NewsCrawlerViewEditModal
                    key="2"
                    inline
                    viewName={item['name']}
                >
                    <Button shape="circle" icon="edit" style={{marginLeft: 5}}/>
                </NewsCrawlerViewEditModal>
            </div>
        });
        views_tabs.unshift(
            <div style={{marginRight: 20, display: 'inline-block'}} key="-100">
                <Button type={self.currentViewName ? "ghost" : "primary"} onClick={() => {self.setView()}}>{"默认视图"}</Button>
            </div>
        )

        return (
            <div>
                <Spin spinning={this.state.loading}>
                    <Row>
                        <Col span="2">
                            <Popover placement="bottom" title={""} content={favContent} trigger="click">
                                <Button type="primary">
                                    {"收藏夹"}
                                </Button>
                            </Popover>
                        </Col>
                        <Col span="2">
                            <NewsCrawlerViewAddModal
                                ee={self.ee}
                            >
                                <Button type="primary">{"添加视图"}</Button>
                            </NewsCrawlerViewAddModal>

                        </Col>
                        <Col span="2">
                            <NewsCrawlerViewDeleteModal
                                ee={self.ee}
                            >
                                <Button type="primary">{"删除视图"}</Button>
                            </NewsCrawlerViewDeleteModal>

                        </Col>
                        <Col span="6" push="1">
                            { renderSearchBar('搜索文章标题...', this.state.keyword, this.handleSearchInput, (v)=>{
                                this.setState({keyword: v})
                            }) }
                        </Col>
                        {false && <Col span="7" push="2">
                            筛选标签：
                            <Select
                                value={this.state.tagValue}
                                style={{ width: 150 }}
                                onChange={this.handleTagsChange}
                            >
                                {tags}
                            </Select>
                        </Col>}
                        <Col span="7" push="2">
                            筛选来源：
                            <Select
                                showSearch
                                value={this.sourceTempValue}
                                style={{ width: 150 }}
                                placeholder="请选择来源"
                                optionFilterProp="children"
                                notFoundContent="not found"
                                showArrow={false}
                                onSearch={this.handleSearchSource}
                                onChange={this.handleSetSource}
                            >
                                {sourceOptions}
                            </Select>
                            <Button icon="search" type="ghost" shape="circle" onClick={() => {this.handleSetSourceKeyword(this.sourceTempValue)}}>
                            </Button>
                        </Col>

                        <Col span="4" push="2">
                            <span>{'自动获取：'}</span>
                            <Switch checked={this.state.websockIsOpened} onChange={this.toggleAutoRefresh.bind(this)} />
                            {this.state.websockIsOpened && <Spin />}
                        </Col>
                    </Row>
                    <Row style={{margin: '10px 0'}}>
                        <span>{'选择一个视图: '}</span>
                        {views_tabs}
                    </Row>
                    <Row>
                        <Col>
                            <Table
                                className="news-list-table"
                                rowClassName={(record, index) => {
                                    return "news-article-row row-importance-"+record['importance']+" "+ (index % 2 ? 'double': '')
                                }}
                                columns={typeof this.props.columnsAlter === 'function' ? this.props.columnsAlter(columns) : columns}
                                dataSource={this.state.data}
                                onChange={this.handleTableChange}
                                pagination={false}
                                rowKey={record => record.id}
                            />
                        </Col>
                    </Row>
                    <BackTop />
                    {this.renderLoading()}
                </Spin>
            </div>
        )
    }
}

NewsCrawlerArticleList.defaultProps = {
    // dependencies from upper component
    renderOperation: (item, record, dataIndex) => { return <div>operation area</div> },
    onClickTitle: (item, record, dataIndex) => {},
    columnsAlter: (columns) => {return columns}
};