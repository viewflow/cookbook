import React from 'react';
import ReactDOM from 'react-dom';
import createHistory from 'history/createBrowserHistory'
import { ConnectedRouter } from 'react-router-redux'
import { Provider } from 'react-redux'
import { Route, Switch } from 'react-router'

import './index.css';
import 'bootstrap/dist/css/bootstrap.css';
import App from './App';
import Login from './containers/Login';
import configureStore from './store'
import AppLayout from './components/AppLayout'
import Companies from './containers/Companies'
import CompanyDetails from './containers/CompanyDetails'
import About from './containers/About'

const history = createHistory()

const store = configureStore(history)

ReactDOM.render((
  <Provider store={store}>
    <ConnectedRouter history={history}>
      <Switch>
        <Route exact path="/login/" component={Login} />
        <AppLayout exact path="/" component={App}/>
        <AppLayout exact path="/companies" component={Companies}/>
        <AppLayout exact path="/about" component={About}/>
        <AppLayout exact path="/company/:id" component={CompanyDetails}/>
      </Switch>
    </ConnectedRouter>
  </Provider>
), document.getElementById('root'));
