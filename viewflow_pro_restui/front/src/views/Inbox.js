import React, { Component } from 'react'

import Start from '../components/flows/hellorest/Start'
import * as API from '../api'

export default class Inbox extends Component {
  state = {
    startModalVisible: false,
    tasks: []
  }

  toggleStartFlowModal = () => {
    this.setState({
      startModalVisible: !this.state.startModalVisible
    })
  }

  constructor(props) {
    super(props)
    this.setProgress = props.setProgress
  }
    
  componentDidMount() {
    this.setProgress(true)
    API.inbox().then(
      response => {
        this.setState({'tasks':response})
        this.setProgress(false)
      }
    ).catch(() => this.setProgress(false))
  }

  render() {
    return (
        <div className="tasklist">
          {!!this.state.tasks?<h1>No tasks in an inbox</h1>: ""}
          {!!this.state.startModalVisible?<Start close={this.toggleStartFlowModal}/>: ""}
          <button onClick={this.toggleStartFlowModal} className="btn btn-primary btn-circle btn-action">+</button>
        </div>
    )
  }
}
