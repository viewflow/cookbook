import React from 'react';
import ReactDOM from 'react-dom';
import { browserHistory, Router } from 'react-router';
import injectTapEventPlugin from 'react-tap-event-plugin';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import routes from './routes';


// Needed for onTouchTap
injectTapEventPlugin();


ReactDOM.render(
  <MuiThemeProvider>
    <Router history={browserHistory} onUpdate={() => window.scrollTo(0, 0)}>
      {routes}
    </Router>
  </MuiThemeProvider>,
  document.getElementById('root')
);


import "./index.css"
