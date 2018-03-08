import React, { Component } from 'react'
import { Table, Icon, Popconfirm, message, Row, Col, Tooltip, Button, Spin, Form, Input, Select, BackTop, Modal, Checkbox, Radio } from 'antd'
const confirm = Modal.confirm;
const RadioGroup = Radio.Group;
const FormItem = Form.Item;
import EventEmitter from 'events'

// modules
import { renderSearchBar } from './lib/Search'
import apiAddress from './lib/apiAddress';
import { formatTime, reachBottom } from './lib/util'
import HttpService from './lib/HttpService';
import RequestParam from './lib/RequestBean';

// components
import NewsCrawlerSourceEditModal from './NewsCrawlerSourceEditModal'
import NewsCrawlerSourceDefaultEditModal from './NewsCrawlerSourceDefaultEditModal'

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

export default class NewsCrawlerSourceList extends Component {
    constructor(props, context) {
        super(props, context)
        var self = this
        this.state = {
            data: [],
            tagsList: [],
            sourceList: [],
            searchVal: '',
            keyword: undefined,
            urlkeyword: undefined,
            loading: false,
            loadingMore: false,
            pageSize: 1000,
            // newArticles: [],
            tagValue: ''
        }
        this.request = new HttpService()
        this.handleTagsChange = this.handleTagsChange.bind(this)
        this.handleUrlSearchInput = this.handleUrlSearchInput.bind(this)
        this.handleSearchInput = this.handleSearchInput.bind(this)
        this.handleCommentSearchInput = this.handleCommentSearchInput.bind(this)
        this.handleScrollEvent = this.handleScroll.bind(this);
        this.fetchScroll = this.fetchScroll.bind(this);
        this.handleTableChange = this.handleTableChange.bind(this);
        this.reloadCrawler = this.reloadCrawler.bind(this);
        this.ee = new EventEmitter()
        this.ee.on('reload_sources', () => {
            self.fetchScroll(true)
        });
    }
    initializeData() {
        this.setState({loading: true})
        this.fetchScroll()
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
    fetchScroll(refresh=false) {
        var self = this
        let lastMark
        if(!refresh && this.state.data.length) {
            lastMark = this.state.data[this.state.data.length-1].id
        }
        let hide = message.loading('加载数据中...')
        const data = {
            limit: this.state.pageSize,
            tagId: this.state.tagId || undefined,
            keyword: this.state.keyword || undefined,
            start_urls_keyword: this.state.urlkeyword || undefined,
            comment_keyword: this.state.commentkeyword || undefined,
            startwith: lastMark,
            offset: lastMark ? 1 : 0,
            sort: this.state.sortField || undefined,
        }
        let url = apiAddress.newsCrawler.sourceList
        let reqParam = new RequestParam().setUrl(url).setData(data)
            .setSuccess((result) => {
                let resultList = result.data
                if(resultList.length === 0) message.warning('没有更多数据')
                this.setState({
                    data: refresh ? resultList : self.mergeObjectList(this.state.data, resultList, 'id'),
                    loadingMore: false,
                    loading: false,
                }, () => {
                    hide()
                    if (!refresh) {
                        window.addEventListener('scroll', this.handleScrollEvent);
                    }
                })
            })
            .setError(() => {
                if (!refresh) {
                    window.addEventListener('scroll', this.handleScrollEvent);
                }
            })
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
    handleUrlSearchInput(value) {
        this.setState({
            tagId: undefined,
            keyword: undefined,
            urlkeyword: value.trim(),
            commentkeyword: undefined,
            tagValue: '',
            data: [],
        }, () => this.fetchScroll())
    }
    handleSearchInput(value) {
        this.setState({
            tagId: undefined,
            keyword: value.trim(),
            urlkeyword: undefined,
            commentkeyword: undefined,
            tagValue: '',
            data: [],
        }, () => this.fetchScroll())
    }
    handleCommentSearchInput(value) {
        this.setState({
            tagId: undefined,
            keyword: undefined,
            urlkeyword: undefined,
            commentkeyword: value.trim(),
            tagValue: '',
            data: [],
        }, () => this.fetchScroll())
    }
    handleTagsChange(tagId) {
        this.setState({
            tagValue: tagId,
            keyword: undefined,
            tagId,
            data: [],
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
    componentDidMount() {
        this.initializeData()
        this.fetchTagList()
        // this.waitArticles()
        window.addEventListener('scroll', this.handleScrollEvent);
    }
    componentWillUnmount() {
        window.removeEventListener('scroll', this.handleScrollEvent);
        // this.waitArticles = () => null
    }
    showEditModal(item) {
        this.setState({
            modalVisibleItem: item.id,
        });
    }
    handleEditModelOk(item) {
        this.setState({
            modalVisibleItem: '',
        });
    }
    handleEditModelCancel(item) {
        this.setState({
            modalVisibleItem: '',
        });
    }
    showDeleteConfirm(item) {
        var self = this;
        confirm({
            title: '确定删除吗',
            content: '',
            onOk() {
                let url = apiAddress.newsCrawler.sourceSingle;
                url = url+item.id+'/';
                let reqParam = new RequestParam().setUrl(url)
                    .setSuccess(() => {
                        message.success('删除成功！')
                        self.ee.emit('reload_sources');
                    })
                    .setError(() => {
                        message.error('删除失败！')
                    })
                self.request.doDelete(reqParam)
            },
            onCancel() {},
        });
    }
    reloadCrawler() {
        let url = apiAddress.newsCrawler.crawlerReload
        let reqParam = new RequestParam().setUrl(url)
            .setSuccess((result) => {
                console.log(result)
                message.success('正在刷新所有爬虫，一般5-10秒内完成...')
            })
            .setError(() => {
                console.log('err!')
            })
        this.request.doGet(reqParam)
    }
    render() {
        let self = this;
        const columns = [{
            title: '机器唯一码',
            dataIndex: 'machine_name',
            index: 'machine_name'
        }, {
            title: '机器抓取地址',
            dataIndex: 'start_urls',
            index: 'start_urls',
            width: '200',
            render(item) {
                // let arr = item ? item.map(tag => {
                //     return tag.name
                // }): []
                if (item) {
                    var toshow = []
                    for (var i in item) {
                        var indexToShow = parseInt(i)+1
                        toshow.push(<span key={i*2}>{'['+indexToShow+'] '+item[i]}</span>)
                        toshow.push(<br key={i*2+1}/>)
                    }

                    return <span>{toshow}</span>
                } else {
                    return <span>{ }</span>
                }
            }
        }, {
            title: '来源名称',
            dataIndex: 'title',
            index: 'title'
        }, {
            title: '是否启用',
            dataIndex: 'disabled',
            index: 'disabled',
            render(item) {
                if (item) {
                    return <span style={{color:'red'}}>✕</span>
                } else {
                    return <span>✔</span>
                }
            }
        }, {
            title: '星级',
            dataIndex: 'star',
            index: 'star',
            render(item) {
                if (item) {
                    return item
                } else {
                    return <span style={{color:'#bbb'}}>{"无"}</span>
                }
            }
        }, {
            title: '标签',
            dataIndex: 'tags',
            index: 'tags',
            render(item) {
                let arr = item ? item.map(tag => {
                    return tag.name
                }): []
                return <span>{arr.join(',')}</span>
            }
        }, {
            title: '抓取间隔时间(秒)',
            dataIndex: 'delay_sec',
            index: 'delay_sec',
            render(item) {
                if (item) {
                    return item
                } else {
                    return <span style={{color:'#bbb'}}>{"使用默认值"}</span>
                }
            }
        }, {
            title: '代理类型',
            dataIndex: 'proxy_type',
            index: 'proxy_type',
            render(item) {
                if (item) {
                    return item
                } else {
                    return <span style={{color:'#bbb'}}>{"使用默认值"}</span>
                }
            }
        }, {
            title: '备注',
            dataIndex: 'comments',
            index: 'comments',
            render(item) {
                return item && item.length > 20 ?
                item.substring(0, 17) + "..." :
                    item;
            }
        }, {
            title: '最新文章',
            index: 'latestArticle',
            dataIndex: 'latestArticleCreated',
            render(item, record, dataIndex) {
                function human_time_past(timestamp) {
                    if (!timestamp) {
                        return <span className="text-danger-4">{'从未'}</span>
                    }

                    var delta = Math.round((+new Date - timestamp * 1000) / 1000);

                    var minute = 60,
                        hour = minute * 60,
                        day = hour * 24,
                        week = day * 7;

                    var fuzzy;

                    if (delta < 30) {
                        fuzzy = <span className="text-danger-0">{'<1分钟'}</span>;
                    } else if (delta < minute) {
                        fuzzy = <span className="text-danger-0">{'1分钟'}</span>;
                    } else if (delta < 2 * minute) {
                        fuzzy = <span className="text-danger-0">{'1分钟前'}</span>;
                    } else if (delta < hour) {
                        fuzzy = <span className="text-danger-0">{Math.floor(delta / minute) + '分钟前'}</span>;
                    } else if (Math.floor(delta / hour) == 1) {
                        fuzzy = <span className="text-danger-0">{'1小时前'}</span>;
                    } else if (delta < day) {
                        fuzzy = <span className="text-danger-1">{Math.floor(delta / hour) + '小时前'}</span>;
                    } else if (delta < day * 2) {
                        fuzzy = <span className="text-danger-2">{'1天前'}</span>;
                    } else if (delta < day * 4) {
                        fuzzy = <span className="text-danger-3">{Math.floor(delta / day) + '天前'}</span>;
                    } else {
                        fuzzy = <span className="text-danger-4">{Math.floor(delta / day) + '天前'}</span>;
                    }

                    return fuzzy
                }


                return human_time_past(item)
            }
        }, {
            title: '操作',
            index: 'operation',
            render(item, record) {
                return (
                    <div>
                        <NewsCrawlerSourceEditModal
                            item={item}
                            ee={self.ee}
                        >
                            <Button>
                                <Icon type="edit"/>
                            </Button>
                        </NewsCrawlerSourceEditModal>

                        {!item['machine_name'] && <Button onClick={() => {self.showDeleteConfirm(item)}}>
                            <Icon type="delete"/>
                        </Button>}
                    </div>
                )
            }
        }]

        const tags = this.state.tagsList.map((item, index) => (
            <Option key={index+1} value={item.id}>{item.name}</Option>
        ))
        tags.unshift(<Option key={0} value=''>全部</Option>)


        return (
            <div>
                <Spin spinning={this.state.loading}>
                    <Row>
                        <Col span="2" push="0">
                            <NewsCrawlerSourceEditModal
                                ee={self.ee}
                            >
                                <Button type="primary" icon="plus">{"添加来源"}</Button>
                            </NewsCrawlerSourceEditModal>

                        </Col>
                        <Col span="2" push="1">
                            <NewsCrawlerSourceDefaultEditModal
                                ee={self.ee}
                            >
                                <Button type="primary" icon="edit">{"修改默认设置"}</Button>
                            </NewsCrawlerSourceDefaultEditModal>

                        </Col>
                        <Col span="4" push="3">
                            { renderSearchBar('搜索机器抓取地址...', this.state.urlkeyword, this.handleUrlSearchInput) }
                        </Col>
                        <Col span="4" push="4">
                            { renderSearchBar('搜索来源名称...', this.state.keyword, this.handleSearchInput) }
                        </Col>
                        <Col span="4" push="5">
                            { renderSearchBar('搜索备注...', this.state.commentkeyword, this.handleCommentSearchInput) }
                        </Col>
                        {/*<Col span="7" push="5">*/}
                        {/*筛选标签：*/}
                        {/*<Select*/}
                        {/*value={this.state.tagValue}*/}
                        {/*style={{ width: 200 }}*/}
                        {/*onChange={this.handleTagsChange}*/}
                        {/*>*/}
                        {/*{tags}*/}
                        {/*</Select>*/}
                        {/*</Col>*/}
                        <Col span="2" push="6">
                            <Button type="primary" icon="reload" onClick={this.reloadCrawler}>{"爬虫刷新"}</Button>
                        </Col>
                    </Row>
                    <Row>
                        {"温馨提示：只有列表内存在的（与机器唯一码匹配的）爬虫会爬，列表内不存在的（或机器码唯一为空的）不会爬喔！"}
                    </Row>
                    <Row>
                        <Col>
                            <Table
                                columns={columns}
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

NewsCrawlerSourceList.defaultProps = {
    // dependencies from upper component
};
