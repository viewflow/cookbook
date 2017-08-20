import React, { Component } from 'react'
import { Route, Redirect, Switch, NavLink as Link } from 'react-router-dom'
import { Nav, NavItem, NavLink, Progress } from 'reactstrap';

import Inbox from './views/Inbox'
import Queue from './views/Queue'
import Archive from './views/Archive'
import Dashboard from './views/Dashboard'


export default class App extends Component {
  state = {
    inProgress: false
  }

  setProgress = inProgress => {
    this.setState({inProgress: inProgress})
  }
 
  render() {
    return (
      <div className="app-page">
        <div className="app-page__sidebar">
          <p>Tasks</p>
          <Nav vertical>
            <NavItem>
              <NavLink tag={Link} to="/inbox">Inbox</NavLink>
            </NavItem>
            <NavItem>
              <NavLink tag={Link} to="/queue">Queue</NavLink>
            </NavItem>
            <NavItem>
              <NavLink tag={Link} to="/archive">Archive</NavLink>
            </NavItem>
          </Nav>
          <p>Dashboard</p>
          <Nav>
            <NavLink tag={Link} to="/dashboard/hellorest/">Hello Rest</NavLink>
          </Nav>
        </div>
        <div className="app-page__outlet">
          <Switch>
            <Redirect exact from="/" to="/dashboard/hellorest" />
            <Route exact path="/inbox" render={props => (
              <Inbox setProgress={this.setProgress} {...props} />
            )}/>
            <Route exact path="/queue" render={props => (
              <Queue setProgress={this.setProgress} {...props} />
            )}/>
            <Route exact path="/archive" render={props => (
              <Archive setProgress={this.setProgress} {...props} />
            )}/>
            <Route exact path="/dashboard/hellorest" component={Dashboard} />
          </Switch>
        </div>
        {this.state.inProgress?<Progress animated value="100" className="progress--top"/>:""}
      </div>
    );
  }
}
