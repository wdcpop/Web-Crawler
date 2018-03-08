var ReactDOM = require('react-dom');
var React = require('react');
import { Tabs } from 'antd';
const TabPane = Tabs.TabPane;

import { WXBOT_DOMAIN } from './components/lib/apiAddress';
import SpiderTeamBasicAuth from './components/lib/SpiderTeam/SpiderTeamBasicAuth'
import NewsCrawlerSourceList from './components/NewsCrawlerSourceList'
import NewsCrawlerArticleListWithSiderPopup from './components/NewsCrawlerArticleListWithSiderPopup'
import './index.css'

function renderOperation(item, record, dataIndex) {
    return <div>operation area</div>
}

ReactDOM.render(
    <SpiderTeamBasicAuth
        authAddress={WXBOT_DOMAIN+'/'}
    >
        <Tabs type="card" defaultActiveKey="1" animated={false}>
            <TabPane tab="文章列表" key="1">
                <NewsCrawlerArticleListWithSiderPopup
                    renderOperation={renderOperation}
                />
            </TabPane>
            <TabPane tab="来源编辑" key="2">
                <NewsCrawlerSourceList
                    renderOperation={renderOperation}
                />
            </TabPane>
        </Tabs>
    </SpiderTeamBasicAuth>,
    document.getElementById('react-content')
);