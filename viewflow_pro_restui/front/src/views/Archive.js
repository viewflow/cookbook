import React, { Component } from 'react'
import * as API from '../api'

export default class Archive extends Component {
  state = {
    tasks: []
  }

  constructor(props) {
    super(props)
    this.setProgress = props.setProgress
  }
    
  componentDidMount() {
    this.setProgress(true)
    API.archive().then(
      response => {
        this.setState({'tasks':response})
        this.setProgress(false)
      }
    ).catch(() => this.setProgress(false))
  }

  render() {
    return (
        <div className="tasklist">
        {!!this.state.tasks?<h1>No tasks in an archive</h1>: ""}
        </div>
    )
  }
}
