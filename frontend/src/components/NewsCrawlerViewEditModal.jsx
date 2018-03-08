import React, { Component } from 'react'
import { Table, Icon, Popconfirm, message, Row, Col, Tooltip, Button, Spin, Form, Input, Select, BackTop, Modal, Checkbox, Radio, Switch } from 'antd'
const RadioGroup = Radio.Group;
import { Link } from 'react-router'
import EventEmitter from 'events'

// modules
import apiAddress from './lib/apiAddress';
import HttpService from './lib/HttpService';
import RequestParam from './lib/RequestBean';


class NewsCrawlerViewEditModal extends Component {
    constructor(props, context) {
        super(props, context)
        this.state = {
            modalVisible: false,
            editProcessing: false,
            sourceList: [],
            selfViewConfigs: {},
        }
        this.request = new HttpService()
    }
    showEditModal() {
        this.setState({
            modalVisible: true,
        });
    }
    handleEditModelOk() {
        this.setState({
            modalVisible: false,
        })
    }
    handleEditModelCancel() {
        this.setState({
            modalVisible: false,
        });
    }
    onRadioChange(e) {
        this.setState({
            proxy_type: e.target.value,
        });
    }
    handleFormSubmit(e) {

    }
    modifySourcesAll(checked) {
        var viewName = this.props.viewName
        let url = apiAddress.newsCrawler.viewsSourcesAll;
        let reqParam = new RequestParam().setUrl(url).setData({'viewName': viewName})
            .setSuccess((d) => {
                this.refreshSelfView()
            })
            .setError(() => {
                console.log('get selfViewConfigs err!');
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
            })
        if (checked) {
            this.request.doPut(reqParam)
        } else {
            this.request.doDelete(reqParam)
        }
    }
    componentDidMount() {
        this.initSources()
        this.refreshSelfView()
    }
    initSources() {
        var self = this
        let url = apiAddress.newsCrawler.sourceList;
        let reqParam = new RequestParam().setUrl(url).setData({'limit': 1000, 'showLatestArticle': 1})
            .setSuccess((d) => {
                var sourceList = d['data'];
                sourceList = sourceList.filter((item) => {
                    return item['machine_name'] && item['title']
                })
                self.setState({sourceList: sourceList})
            })
            .setError(() => {
                console.log('get sources err!');
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
            })
        this.request.doGet(reqParam)
    }
    refreshSelfView() {
        var viewName = this.props.viewName
        let url = apiAddress.newsCrawler.viewsSources;
        let reqParam = new RequestParam().setUrl(url).setData({'viewName': viewName})
            .setSuccess((d) => {
                var selfViewConfigsArr = d['data'];
                var selfViewConfigs = {}
                selfViewConfigsArr.forEach(function(item) {
                    selfViewConfigs[item['sourceName']] = item
                })
                this.setState({selfViewConfigs: selfViewConfigs})
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
    modifyViewSource(sourceName, checked, star) {
        var viewName = this.props.viewName
        let url = apiAddress.newsCrawler.viewsSources;
        var to_set = {'viewName': viewName, 'sourceName': sourceName}
        if (typeof star !== 'undefined' && star !== null) {
            to_set['importance'] = parseInt(star)
        }
        let reqParam = new RequestParam().setUrl(url).setData(to_set)
            .setSuccess((d) => {
                this.refreshSelfView()
            })
            .setError(() => {
                console.log('get selfViewConfigs err!');
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
            })
        if (checked) {
            this.request.doPut(reqParam)
        } else {
            this.request.doDelete(reqParam)
        }

    }
    componentWillUnmount() {

    }
    render() {
        var self = this;

        if (!self.state.selfViewConfigs) {
            return <div></div>
        }

        const columns = [{
            title: '来源名称',
            index: 'title',
            dataIndex: 'title',
            width: 200,
            sortOrder: 'ascend'
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
            title: '显示该来源文章',
            index: 'operation',
            render(item, record, dataIndex) {
                var sourceName = record['machine_name']
                var defaultChecked = self.state.selfViewConfigs[sourceName] ? true : false

                return (
                    <Switch defaultChecked={defaultChecked} checked={defaultChecked} onChange={(checked) => {
                        self.modifyViewSource(sourceName, checked)
                    }} />
                )
            }
        }, {
            title: '该视图内的重要度',
            index: 'imp',
            render(item, record, dataIndex) {
                var sourceName = record['machine_name']
                if (!self.state.selfViewConfigs[sourceName]) {
                    return <span> </span>
                }
                return <RadioGroup
                    onChange={(e) => {
                        self.modifyViewSource(sourceName, true, e.target.value)
                    }}
                    value={self.state.selfViewConfigs[sourceName]['importance'] || 0}
                >
                    <Radio key="0" value={0}>无星</Radio>
                    <Radio key="1" value={1}>1</Radio>
                    <Radio key="2" value={2}>2</Radio>
                    <Radio key="3" value={3}>3</Radio>
                </RadioGroup>
            }
        }]

        return (
            <div style={this.props.inline ? {display: 'inline-block'}: {display: 'block'}}>
                <div onClick={self.showEditModal.bind(this)}>
                    {this.props.children}
                </div>
                {this.state.modalVisible && <Modal width={800} title={"编辑视图来源: "+this.props.viewName} visible={self.state.modalVisible}
                                                   onOk={self.handleEditModelOk.bind(this)}
                                                   onCancel={self.handleEditModelCancel.bind(this)}
                                                   confirmLoading={this.state.editProcessing}
                                                   okText="OK" cancelText="Cancel"
                >
                    <Row>
                        <Col>
                            <div>
                                <div style={{margin: '5px 0'}}>
                                    <Button onClick={() => {self.modifySourcesAll(true)}} type="primary" style={{margin: '0 5px'}}>{'全部显示'}</Button>
                                    <Button onClick={() => {self.modifySourcesAll(false)}} type="primary" style={{margin: '0 5px'}}>{'全部隐藏'}</Button>
                                </div>
                                <Table
                                    className="views-sources-table"
                                    rowClassName={(record, index) => {return "views-sources-row "+ (index % 2 ? 'double': '')}}
                                    columns={typeof this.props.columnsAlter === 'function' ? this.props.columnsAlter(columns) : columns}
                                    dataSource={this.state.sourceList}
                                    onChange={function(){}}
                                    pagination={false}
                                    rowKey={record => record.id}
                                />
                            </div>
                        </Col>
                    </Row>
                </Modal>}
            </div>
        )
    }
}

export default NewsCrawlerViewEditModal