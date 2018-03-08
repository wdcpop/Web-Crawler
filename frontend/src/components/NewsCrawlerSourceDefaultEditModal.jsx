import React, { Component } from 'react'
import { Table, Icon, Popconfirm, message, Row, Col, Tooltip, Button, Spin, Form, Input, Select, BackTop, Modal, Checkbox, Radio } from 'antd'
const RadioGroup = Radio.Group;
const FormItem = Form.Item;
import { Link } from 'react-router'
import EventEmitter from 'events'

// modules
import { renderSearchBar } from './lib/Search'
import apiAddress from './lib/apiAddress';
import { formatTime, reachBottom } from './lib/util'
import HttpService from './lib/HttpService';
import RequestParam from './lib/RequestBean';


class NewsCrawlerSourceDefaultEditModal extends Component {
    constructor(props, context) {
        super(props, context)
        this.state = {
            modalVisible: false,
            editProcessing: false,
            defaultConfigs: {}
        }
        this.request = new HttpService()
    }
    componentDidMount() {
        this.initDefaultConfigs()
    }
    initDefaultConfigs() {
        var self = this
        let url = apiAddress.newsCrawler.sourceDefault;
        let reqParam = new RequestParam().setUrl(url)
            .setSuccess((configs) => {
                self.setState({defaultConfigs: configs})
            })
            .setError(() => {
                console.log('get sourceDefault err!');
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
            })
        this.request.doGet(reqParam)
    }
    showEditModal() {
        this.initDefaultConfigs()
        this.setState({
            modalVisible: true,
        });
    }
    handleEditModelOk() {
        this.setState({
            editProcessing: true
        })
        this.handleFormSubmit()
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
        var self = this
        typeof e !== 'undefined' && e.preventDefault();
        console.log('Received values of form:', this.props.form.getFieldsValue());

        let url = apiAddress.newsCrawler.sourceDefault;
        let fieldsVals = this.props.form.getFieldsValue();
        console.log(fieldsVals);
        let reqParam = new RequestParam().setUrl(url).setData(fieldsVals)
            .setSuccess(() => {
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
                message.success('修改成功！')
            })
            .setError(() => {
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
                message.error('修改失败！')
            })
        this.request.doPut(reqParam)
    }
    render() {
        var self = this;
        var item = this.state.defaultConfigs || {}

        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        }

        const { getFieldProps, getFieldsValue } = this.props.form;

        return (
            <div>
                <div onClick={self.showEditModal.bind(this)}>
                    {this.props.children}
                </div>
                {self.state.modalVisible && <Modal title="Modal" visible={self.state.modalVisible}
                                                   onOk={self.handleEditModelOk.bind(this)}
                                                   onCancel={self.handleEditModelCancel.bind(this)}
                                                   confirmLoading={this.state.editProcessing}
                                                   okText="OK" cancelText="Cancel"
                >
                    <Form onSubmit={this.handleFormSubmit.bind(this)}>
                        <Row>
                            <Col>
                                <FormItem label="默认抓取间隔(秒)" {...formItemLayout}>
                                    {/*{getFieldDecorator('delay_sec', { initialValue: item['delay_sec'] })(*/}
                                        <Input
                                        {...getFieldProps('default_delay', {initialValue: item['default_delay']})}
                                        placeholder="请输入默认间隔时间(秒)"
                                        />
                                    {/*)}*/}
                                </FormItem>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <FormItem label="默认代理类型" {...formItemLayout}>
                                    {/*{getFieldDecorator('proxy_type', { initialValue: item['proxy_type'] })(*/}
                                        <RadioGroup
                                        {...getFieldProps('default_proxy', {initialValue: item['default_proxy'] || ''})}
                                        >
                                            <Radio key="z" value={-1}>不使用代理</Radio>
                                            <Radio key="b" value={1}>1 - 国内固定代理</Radio>
                                            <Radio key="c" value={2}>2 - 国外固定代理</Radio>
                                            <Radio key="d" value={3}>3 - 香港代理</Radio>
                                            <Radio key="e" value={10}>10 - 国内不稳定随机代理</Radio>
                                            <Radio key="f" value={20}>20 - 国外不稳定随机代理</Radio>
                                        </RadioGroup>
                                    {/*)}*/}
                                </FormItem>
                            </Col>
                        </Row>
                    </Form>
                </Modal>}
            </div>
        )
    }
}

NewsCrawlerSourceDefaultEditModal = Form.create()(NewsCrawlerSourceDefaultEditModal);

// NewsCrawlerSourceEditModal.defaultProps = {
//     // dependencies from upper component
//     item: {}
// };

export default NewsCrawlerSourceDefaultEditModal

