import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import createHistory from 'history/createBrowserHistory'
import { ConnectedRouter } from 'react-router-redux'
import { Provider } from 'react-redux'
import { Route, Switch } from 'react-router'
import { persistStore } from 'redux-persist'

import './index.css';
import 'bootstrap/dist/css/bootstrap.css';

import App from './App';
import Login from './containers/Login';
import PrivateRoute from './containers/PrivateRoute';
import configureStore from './store'

const history = createHistory()

const store = configureStore(history)

class Root extends Component {
  state = {
    rehydrated: false
  }

  componentWillMount(){
    persistStore(store, {}, () => {
      this.setState({ rehydrated: true })
    })
  }

  render() {
    if (!this.state.rehydrated) {
      return <h1>Loading...</h1>
    }

    return (
      <Provider store={store}>
        <ConnectedRouter history={history}>
          <Switch>
            <Route exact path="/login/" component={Login} />
            <PrivateRoute path="/" component={App}/>
          </Switch>
        </ConnectedRouter>
      </Provider>
    )
  }
}

ReactDOM.render(<Root/>, document.getElementById('root'));
