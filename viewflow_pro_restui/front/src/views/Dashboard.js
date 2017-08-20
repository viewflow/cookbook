import React, { Component } from 'react'
import {
  Card,
  CardText,
  Button
} from 'reactstrap';

import FlowGraph from '../components/FlowGraph'

export default class Dashboard extends Component {
  render() {
    return (
      <div className="dashboard">
        <div className="dashboard__column">
          <div className="dashboard__title">Start</div>
          <div className="dashboard__content">
             <Card block>
               <CardText>This process demonstrates hello world approval request flow.</CardText>
               <FlowGraph url='/api/flows/hellorest/chart/'/>
               <Button>Start</Button>
             </Card>
          </div>
        </div>
        <div className="dashboard__column">
          <div className="dashboard__title">Approve</div>
          <div className="dashboard__content"></div>
        </div>
        <div className="dashboard__column">
          <div className="dashboard__title">Send</div>
          <div className="dashboard__content"></div>
        </div>
        <div className="dashboard__column">
          <div className="dashboard__title">Complete</div>
          <div className="dashboard__content"></div>
        </div>
      </div>
    );
  }  
}
