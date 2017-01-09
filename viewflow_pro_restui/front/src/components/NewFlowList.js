import React, { Component } from 'react';

import {List, ListItem, MakeSelectable} from 'material-ui/List';
import FileCreateNewFolder from 'material-ui/svg-icons/file/create-new-folder'

import {flows} from '../api/workflow'
import LoadIndicator from './LoadIndicator'
import FlowDialog from './FlowDialog'


class NewFlowList extends Component {
  state = {
    inProgress: false,
    error: null,
    flows: [],
    currentTask: null
  }

  constructor() {
    super()
    this.handleChangeList = this.handleChangeList.bind(this)
  }

  componentDidMount() {
    this.setState({inProgress: true})
    flows().then(
      response => this.setState({inProgress: false, error: null, flows: response})
    ).catch(
      response => this.setState({inProgress: false, error: response.detail, flows: []})
    )
  }

  handleChangeList(event, value) {
    alert(value.name)
  }

  renderFlowActions(flow) {
    return flow.start_actions.map((action) => {
      const actionTitle = action.name.replace(/^[a-z]/, function (x) {return x.toUpperCase()})
      return  <ListItem key="1" primaryText={flow.title + " - " + actionTitle}
                        secondaryText={flow.description}
                        secondaryTextLines={2}
                        leftIcon={<FileCreateNewFolder />}
                        value={action} />
    })
  }

  renderTaskDialog() {
    if(this.state.currentTask) {
      return <FlowDialog task={this.state.currentTask}/>
    }
    return null
  }

  render() {
    const SelectableList = MakeSelectable(List)

    return (
      <SelectableList onChange={ this.handleChangeList }>
        {this.state.error?<span style={{ color: 'red' }}>{this.state.error}</span>:""}
        <LoadIndicator inProgress={this.state.inProgress} />
        {this.state.flows.map(this.renderFlowActions)}
        {this.renderTaskDialog()}
      </SelectableList>
    )
  }
}

export default NewFlowList
