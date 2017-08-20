import 'bootstrap/dist/css/bootstrap.css';
import 'notie/dist/notie.css';
import './viewflow.css';

import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'

import App from './App';
import PrivateRoute from './components/PrivateRoute';
import Login from './views/Login';

ReactDOM.render((
  <Router>
    <Switch>
      <Route exact path="/login" component={Login} />
      <PrivateRoute path="/" component={App}/>
    </Switch>
  </Router>
), document.getElementById('root'));
