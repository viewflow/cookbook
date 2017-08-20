import React, { Component } from 'react'
import {
  Card,
  CardBlock,
  Button,
  ButtonGroup,
  CardTitle,
  CardText,
} from 'reactstrap';


import * as API from '../api'

export default class Queue extends Component {
  state = {
    tasks: []
  }

  constructor(props) {
    super(props)
    this.setProgress = props.setProgress
  }
    
  componentDidMount() {
    this.setProgress(true)
    API.queue().then(
      response => {
        this.setState({'tasks':response})
        this.setProgress(false)
      }
    ).catch(() => this.setProgress(false))
  }

  render() {
    return (
      <div className="tasklist">
        {this.state.tasks?"":<h1>No tasks in a queue</h1>}
        {
          this.state.tasks.map(task => (
            <div className="tasklist__task" key={task.id}>
              <Card>
                <CardBlock>
                  <CardTitle>#{task.process.id} {task.title}</CardTitle>
                  <CardText>{task.description}</CardText>
                </CardBlock>
                <CardBlock className="tasklist__actions">
                  <ButtonGroup>
                  {
                    task.actions.map(action => (
                      <Button>{action.name}</Button>
                    ))
                  }
                  </ButtonGroup>
                </CardBlock>
              </Card>
            </div>
          ))
        }
      </div>
    )
  }
}
