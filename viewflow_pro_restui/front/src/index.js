import 'bootstrap/dist/css/bootstrap.css';
import './viewflow.css';

import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'

import App from './App';
import PrivateRoute from './components/PrivateRoute';
import Login from './views/Login';

ReactDOM.render((
  <Router>
    <div id="content">
      <Switch>
        <Route exact path="/login" component={Login} />
        <PrivateRoute path="/" component={App}/>
      </Switch>
    </div>
  </Router>
), document.getElementById('root'));
