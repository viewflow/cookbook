import React, { Component } from 'react';
import { Redirect, Route, Switch, NavLink as Link } from 'react-router-dom'
import { Nav, NavItem, NavLink } from 'reactstrap';

import {Inbox, Queue, Archive} from './containers/TaskList'
import Dashboard from './containers/Dashboard'


class App extends Component {
  render() {
    return (
      <div className="app-page">
        <div className="app-page__sidebar">
          <p>Tasks</p>
          <Nav vertical>
            <NavItem>
              <NavLink tag={Link} to="/tasks/inbox/">Inbox</NavLink>
            </NavItem>
            <NavItem>
              <NavLink tag={Link} to="/tasks/queue/">Queue</NavLink>
            </NavItem>
            <NavItem>
              <NavLink tag={Link} to="/tasks/archive/">Archive</NavLink>
            </NavItem>
          </Nav>
          <p>Dashboard</p>
          <Nav>
            <NavLink tag={Link} to="/dashboard/hellorest/">Hello Rest</NavLink>
          </Nav>
        </div>

        <div className="app-page__outlet">
          <Switch>
            <Redirect exact path="/" to="/dashboard/hellorest/"/>
            <Route path="/tasks/inbox/" component={Inbox}/>
            <Route path="/tasks/queue/" component={Queue}/>
            <Route path="/tasks/archive/" component={Archive}/>
          </Switch>
          <Route path="/dashboard/hellorest/" component={Dashboard} />
        </div>
      </div>

    );
  }
}

export default App;
