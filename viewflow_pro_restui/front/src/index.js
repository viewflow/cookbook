import React from 'react';
import ReactDOM from 'react-dom';
import { browserHistory, Router } from 'react-router';
import injectTapEventPlugin from 'react-tap-event-plugin';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import routes from './routes';
import Auth from './components/Auth';


// Needed for onTouchTap
injectTapEventPlugin();


ReactDOM.render(  
  <MuiThemeProvider>
    <Auth>
      <Router history={browserHistory} onUpdate={() => window.scrollTo(0, 0)}>
        {routes}
      </Router>
    </Auth>
  </MuiThemeProvider>,
  document.getElementById('root')
);


import "./index.css"
