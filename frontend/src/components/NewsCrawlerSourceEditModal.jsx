import React, { Component } from 'react'
import { Table, Icon, Popconfirm, message, Row, Col, Tooltip, Button, Spin, Form, Input, Select, BackTop, Modal, Checkbox, Radio } from 'antd'
const RadioGroup = Radio.Group;
const FormItem = Form.Item;
import { Link } from 'react-router'
import EventEmitter from 'events'

// modules
import apiAddress from './lib/apiAddress';
import HttpService from './lib/HttpService';
import RequestParam from './lib/RequestBean';


class NewsCrawlerSourceEditModal extends Component {
    constructor(props, context) {
        super(props, context)
        this.state = {
            modalVisible: false,
            editProcessing: false,
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

        let url = apiAddress.newsCrawler.sourceSingle;
        url = this.props.item && this.props.item.id ? url+this.props.item.id+'/' : url;
        let fieldsVals = this.props.form.getFieldsValue();
        console.log(fieldsVals);
        let reqParam = new RequestParam().setUrl(url).setData(fieldsVals)
            .setSuccess(() => {
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
                message.success('修改/添加成功！')
                self.props.ee.emit('reload_sources');
            })
            .setError(() => {
                this.setState({
                    editProcessing: false,
                    modalVisible: false
                })
                message.error('修改/添加失败！')
            })
        this.request.doPut(reqParam)
    }
    componentWillUnmount() {

    }
    render() {
        var self = this;
        var item = this.props.item || {}

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
                {this.state.modalVisible && <Modal title="Modal" visible={self.state.modalVisible}
                                                   onOk={self.handleEditModelOk.bind(this)}
                                                   onCancel={self.handleEditModelCancel.bind(this)}
                                                   confirmLoading={this.state.editProcessing}
                                                   okText="OK" cancelText="Cancel"
                >
                    <Form onSubmit={this.handleFormSubmit.bind(this)}>
                        <Row>
                            <Col>
                                <FormItem label="来源机器码（仅供码农修改）" {...formItemLayout}>
                                    {/*{getFieldDecorator('machine_name', { initialValue: item['machine_name'] })(*/}
                                        <Input
                                        {...getFieldProps('machine_name', {initialValue: item['machine_name']})}
                                        placeholder="请输入源机器码："
                                        />
                                    {/*)}*/}
                                </FormItem>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <FormItem label="来源名称" {...formItemLayout}>
                                    {/*{getFieldDecorator('title', { initialValue: item['title'] })(*/}
                                        <Input
                                        {...getFieldProps('title', {initialValue: item['title']})}
                                        placeholder="请输入来源名称："
                                        />
                                    {/*)}*/}
                                </FormItem>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <FormItem label="禁用此来源" {...formItemLayout}>
                                    {/*{getFieldDecorator('disabled', { initialValue: item['disabled'], valuePropName: 'checked' })(*/}
                                        <Checkbox
                                        {...getFieldProps('disabled', {initialValue: item['disabled'], valuePropName: 'checked'})}
                                        />
                                    {/*)}*/}
                                </FormItem>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <FormItem label="星级" {...formItemLayout}>
                                    {/*{getFieldDecorator('star', { initialValue: item['star'] })(*/}
                                        <RadioGroup
                                        {...getFieldProps('star', {initialValue: item['star'] || 0})}
                                        >
                                        <Radio key="0" value={0}>无星</Radio>
                                        <Radio key="1" value={1}>一星级</Radio>
                                        <Radio key="2" value={2}>二星级</Radio>
                                        <Radio key="3" value={3}>三星级</Radio>
                                        </RadioGroup>
                                    {/*)}*/}
                                </FormItem>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <FormItem label="抓取间隔(秒)" {...formItemLayout}>
                                    {/*{getFieldDecorator('delay_sec', { initialValue: item['delay_sec'] })(*/}
                                        <Input
                                        {...getFieldProps('delay_sec', {initialValue: item['delay_sec']})}
                                        placeholder="请输入间隔时间(秒), 留空设为默认值"
                                        />
                                    {/*)}*/}
                                </FormItem>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <FormItem label="代理类型" {...formItemLayout}>
                                    {/*{getFieldDecorator('proxy_type', { initialValue: item['proxy_type'] })(*/}
                                        <RadioGroup
                                        {...getFieldProps('proxy_type', {initialValue: item['proxy_type'] || ''})}
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
                        <Row>
                            <Col>
                                <FormItem label="备注" {...formItemLayout}>
                                    {/*{getFieldDecorator('comments', { initialValue: item['comments'] })(*/}
                                        <Input
                                        type="textarea"
                                        rows={4}
                                        {...getFieldProps('comments', {initialValue: item['comments']})}
                                        />
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

NewsCrawlerSourceEditModal = Form.create()(NewsCrawlerSourceEditModal);

// NewsCrawlerSourceEditModal.defaultProps = {
//     // dependencies from upper component
//     item: {}
// };

export default NewsCrawlerSourceEditModal