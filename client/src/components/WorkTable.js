import React from "react";
import WorkItem from "./WorkItem";
import cfg from "../config"
import axios from "axios";
import PopupWorkDetail from "./PopupWorkDetail";

class WorkTable extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            list: [],
            isOpen: false,
            date: new Date(),
            popupItem: {}
        };
    }

    componentDidMount() {
        this.updateID = setInterval(
            () => this.update(),
            1000
        );
    }

    update() {
        this.getWorGroupList();
    }

    componentWillUnmount() {
        clearInterval(this.updateID);
    }

    openPopup = (item) => {
        this.setState({isOpen: !this.state.isOpen, popupItem: item})
    };

    closePopup = () => {
        this.setState({isOpen: false})
    };

    getWorGroupList = () => {
        axios.post(`http://${cfg.host}:${cfg.proxyPort}/action/get_work_group_list`).then( (response) => {
            const list = response.data.list;
            this.setState({list: list})
        });
    };

    render() {

        let listItems = <div

            style={{
                margin: 'auto',
                height: 120,
                marginTop: 70,
                fontSize: 18,
                color: '#ACACAC',
                borderBottom: '1px solid black',
            }}

            >수집 작업이 존재하지 않습니다.</div>
        if(this.state.list.length > 0) {
            listItems = this.state.list.map((item) =>
                <WorkItem value={item} openPopup={this.openPopup.bind(this, item)}/>
            );
        }

        return (

            <div
                style={{
                    margin: 'auto',
                    width: '80%',
                    borderTop: '1px solid black',
                }}>

                {listItems}

                {this.state.isOpen && <PopupWorkDetail
                    item={this.state.popupItem}
                    content={<>
                    </>}
                    handleClose={this.closePopup}
                />}
            </div>
        );
    }
}

export default WorkTable;