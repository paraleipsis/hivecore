import React, { Component } from  'react';
import Modal from 'react-bootstrap/Modal';
import ConfigsService  from  '../services/ConfigsService';
import Card from 'react-bootstrap/Card';

import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-html";
// import "ace-builds/src-noconflict/theme-twilight";
import "ace-builds/src-noconflict/ext-language_tools";

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider, PaginationListStandalone } from 'react-bootstrap-table2-paginator';
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";

import remove_button from '../../assets/images/remove_white.png';

const  configsService  =  new ConfigsService();

class  ConfigsList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		configs: [],
        configDetails: [],
        openModal : false,
        openModalRemove : false,
        signal: '',
        config: '',
        configs_ip: '',
	};
}

componentDidMount() {
    var self = this;
	configsService.getConfigs().then(function (data) {
		self.setState({configs:  data.result})
	});
}

detailsSide(object, cellContentName) {
    return <button onClick={() => {this.openNavDetails(object)}} className='button'>{cellContentName.length > 20 ? cellContentName.slice(0, 20) + ' ...' : cellContentName}</button>
}

openNavDetails(info) {
    document.getElementById("details-sidebar").style.width = "100%";
    this.setState({configDetails: info})
};

closeNavDetails() {
    document.getElementById("details-sidebar").style.width = "0";
};

handleRefresh = () => {
    this.componentDidMount();
};

hostStyle(cellContent) {
    return <span className='images-main-table-host-body'>{cellContent}</span>
}

action(config) {
    return <div>
        <button id='remove' onClick={() => {this.onClickButtonModalRemove(config, 'remove_configs')}} className='button button-delete'>
            Remove&nbsp;
            <img src={remove_button} className='action-img'/>
        </button>
        </div>
}

onClickButtonModalRemove = (config, signal) => {
    this.setState({
        openModalRemove: true,
        signal: signal,
        config: config.items.ID,
        config_ip: config.ip,
    })
}

onCloseModalRemove = ()=> {
    this.setState({openModalRemove : false})
}

handleRemove(config) {
	configsService.deleteConfig(config)
}

configsColumnsMain = [
{
    dataField: "name",
    text: "Name",
    sort: true,
    headerClasses: 'images-main-table-tags-header',
    editCellClasses: 'images-main-table-repotags-body'
},
{
    dataField: "host",
    text: "Host",
    sort: true,
    headerClasses: 'images-main-table-host-header',
},
{
    dataField: "created",
    text: "Created",
},
{
    dataField: "updated",
    text: "Updated",
},
{
    dataField: "actions",
    text: "Actions",
},
];

render() {
    if (this.state.configs == 'Unable to collect data. All hosts is unreacheable') {
        return <section className='images-section'>Unable to collect data. All hosts is unreacheable</section>
    }

    return (
            <section className='configs-section'>

                <div id="main" className="configs--list">

                    {/* remove config */}
                    <Modal show={this.state.openModalRemove} onHide={this.onCloseModalRemove} dialogClassName="removeConfirm">
                        <Modal.Header closeButton>
                            <Modal.Title>Remove config</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>Are you sure you want to remove config: {this.state.config.slice(0, 12)}</Modal.Body>
                        <Modal.Footer>
                                <div className='force_checkbox'>
                                    <input id="force_checkbox" type="checkbox"/>
                                    Force remove
                                </div>
                                <button className='button button-modal-cancel' onClick={this.onCloseModalRemove}>
                                    Cancel
                                </button>
                                <button className='button button-modal-remove' onClick={() =>{ 
                                    this.onCloseModalRemove(); 
                                    this.handleRemove({
                                        'config': this.state.config, 
                                        'config_ip': this.state.config_ip,
                                        'signal': 'remove_config',
                                        'force': document.getElementById('force_checkbox').checked,
                                        })}}>
                                    Remove
                                </button>
                        </Modal.Footer>
                    </Modal>

                    <div id="details-sidebar" className="sidenav">

                        <a className="closebtn" onClick={() => {this.closeNavDetails()}}>&times;</a>

                        <Card className='card-info card-image-details'>

                            <Card.Header className='image-info-header'>CONFIG DETAILS</Card.Header>
                            <Card.Body className='image-info'>
                                {/* config details table */}
                                {
                                    this.state.configDetails.length != 0 && (
                                        <table id="table-details" className="table" >
                                            <tbody>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>ID</th>
                                                <td>{this.state.configDetails.items.ID}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Name</th>
                                                <td>{this.state.configDetails.items.Spec.Name}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Created</th>
                                                <td>{this.state.configDetails.items.CreatedAt.replace('T', ' ').slice(0, this.state.configDetails.items.CreatedAt.indexOf('.'))}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Updated</th>
                                                <td>{this.state.configDetails.items.UpdatedAt.replace('T', ' ').slice(0, this.state.configDetails.items.UpdatedAt.indexOf('.'))}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    )
                                }
                                                            

                                {/* config labels table */}
                                {                         
                                    this.state.configDetails.length != 0 && (
                                        this.state.configDetails.items.Spec.Labels != null &&
                                        Object.keys(this.state.configDetails.items.Spec.Labels).length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            Object.keys(this.state.configDetails.items.Spec.Labels).map(c => (
                                                {
                                                    labels: c + '=' + this.state.configDetails.items.Spec.Labels[c]
                                                }
                                            ))
                                        }
                                        columns={[
                                            {
                                                dataField: "labels",
                                                text: "Labels",
                                            },
                                            ]}
                                        /> : 
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            [
                                                {labels: 'No Labels'}
                                            ]
                                        }
                                        columns={[
                                            {
                                                dataField: "labels",
                                                text: "Labels",
                                            },
                                            ]}
                                        />
                                    ) 
                                }
                                
                                
                            </Card.Body>

                        </Card>

                        <br/>
                        <br/>

                        <Card className='card-info card-dockerfile-details'>

                            <Card.Header className='image-info-header'>CONFIG DATA</Card.Header>
                            <Card.Body className='image-info'>

                                {/* config data area */}
                                {
                                    this.state.configDetails.items != undefined && (
                                        <AceEditor
                                            placeholder="Placeholder Text"
                                            className='editor'
                                            mode="html"
                                            // theme="twilight"
                                            name="blah2"
                                            onLoad={this.onLoad}
                                            onChange={this.onChange}
                                            fontSize={15}
                                            showPrintMargin={true}
                                            showGutter={true}
                                            highlightActiveLine={true}
                                            value={atob(this.state.configDetails.items.Spec.Data)}
                                            setOptions={{
                                            enableBasicAutocompletion: false,
                                            enableLiveAutocompletion: false,
                                            enableSnippets: false,
                                            showLineNumbers: true,
                                            tabSize: 2,
                                            readOnly: true,
                                        }}/>
                                    )
                                }
                                
                                
                                
                            </Card.Body>

                        </Card>

                        <br/>
                        <br/>

                    </div>


                    {/* main configs table */}
                    <div>
                        <PaginationProvider
                        pagination={ 
                            paginationFactory({ 
                                sizePerPage: 5, 
                                custom: true,
                                totalSize: this.state.configs.length
                            })}
                        >
                        {
                            ({
                            paginationProps,
                            paginationTableProps
                            }) => (
                            <div>

                                <BootstrapTable
                                bootstrap4
                                keyField="name"
                                headerClasses = 'tbl-header'
                                bordered = { false }
                                data={this.state.configs.map(
                                    c => ({
                                        name: this.detailsSide(c, c.items.Spec.Name),
                                        host: this.hostStyle(c.host),
                                        created: c.items.CreatedAt.replace('T', ' ').slice(0, c.items.CreatedAt.indexOf('.')),
                                        updated: c.items.UpdatedAt.replace('T', ' ').slice(0, c.items.UpdatedAt.indexOf('.')),
                                        actions: this.action(c),
                                        }
                                    )
                                )}
                                columns={this.configsColumnsMain}
                                { ...paginationTableProps }
                                />

                                <PaginationListStandalone
                                    {...paginationProps}
                                />

                            </div>
                            )
                        }
                        </PaginationProvider>
                    </div>

                </div>
                
                <div className='block'>CONFIG LIST</div>

            </section>
	);

  }
}

export  default  ConfigsList;