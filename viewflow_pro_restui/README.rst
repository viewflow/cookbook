===================================
Quick start with Viewflow and React
===================================

This tutorial demonstrates how to create a simple app using viewflow rest
and react.


Frontend
========

For the demo purpose the frontend is created using minimal about of 3d
party libraries. No complex state management is introduced. As
opposite we concentrate on making ready to use solution using React
basics with minimal amount of code.

In contrast with other react toturials, with the next few pages you
will learn, how to make real life app, perform user authentification,
make API calls, output the datatables with pagination, make and submit
forms, and all of it with production ready UI based on Google Material
Design.

For the start We use facebook `create-react-app` is an official command line
interface (CLI) for building React applications with no build
configuration.

Let's start with basics::

    $ npm install -g create-react-app
    $ create-react-app front

Go to the `front/` subdirectory and install dependencies that we need::
  
    $ npm install --save material-ui react-router react-tap-event-plugin

Basic structure
---------------

Let's create few placeholders for future code. Create a `components/pages/` folder, and place 3 files with following content

inbox.js::
  
  import React from 'react';

  export default () => <h1>Inbox</h1>

queue.js::
  
  import React from 'react';

  export default () => <h1>Queue</h1>

and archive.js::
  
  import React from 'react';

  export default () => <h1>Archive</h1>

Open the `App.js` and enter the required imports::

  import React, { Component, PropTypes } from 'react';

  import AppBar from 'material-ui/AppBar';
  import Drawer from 'material-ui/Drawer';
  import {List, ListItem, MakeSelectable} from 'material-ui/List';
  import IconButton from 'material-ui/IconButton';

  import ActionDashboard from 'material-ui/svg-icons/action/dashboard';
  import Alarm from 'material-ui/svg-icons/action/alarm';
  import Book from 'material-ui/svg-icons/action/book';
  import CommunicationEmail from 'material-ui/svg-icons/communication/email';

And the application component code itself::
  
  class App extends Component {
    handleChangeList = (event, value) => {
      this.context.router.push(value);
    }
    
    render() {
      const SelectableList = MakeSelectable(List);
      const location = this.props.location;
      const drawerWidth = this.context.muiTheme.drawer.width;

      return (
        <div>
          <Drawer>
            <AppBar title="Viewflow" iconElementLeft={<IconButton><ActionDashboard /></IconButton>}/>
            <SelectableList value={ location.pathname } onChange={ this.handleChangeList }>
              <ListItem primaryText="Inbox" leftIcon={<CommunicationEmail />} value="/"/>
              <ListItem primaryText="Queue" leftIcon={<Alarm />} value="/queue/"/>
              <ListItem primaryText="Archive" leftIcon={<Book />} value="/archive/"/>
            </SelectableList>
          </Drawer>
          <div style={{ marginLeft: drawerWidth }}>
            {this.props.children}
          </div>
        </div>
      )
    }
  }

  App.propTypes = {
    location: PropTypes.object.isRequired
  }
  
  App.contextTypes = {
    router: PropTypes.object.isRequired,
    muiTheme: PropTypes.object.isRequired,
  };
  
  export default App;

Let's see line by line, from bottom to top, what's happens here.

The application component going to be used inside the
react-router. The `this.props.location` would be initialized by parent
react `Router`, and with `App.contextTypes` we request `router` and
`theme` instance for the App context.

The application component would be used as the main container of our
application. On the left side we would have a `Drawer` with navigation
list, and the `{this.props.children}` would be located on the right.

Provided by Material-UI `SelectableList` would select one of children
`ListItem` with matched `value` We use `location.pathname` to select
the item points to hte current page.

To handle havifation, we user `OnChangeEvent`, and just request the
react router to change location to the value of selected ListItem


Let's create a router configuration. Put the following code into `routes.js` file::

  import React from 'react';
  import { IndexRoute, Route }  from 'react-router';

  import App from './App';
  import InboxPage from './components/pages/inbox';
  import QueuePage from './components/pages/queue';
  import ArchivePage from './components/pages/archive';

  export default (
    <Route component={App} path='/'>
      <IndexRoute component={InboxPage} />
      <Route component={QueuePage} path='queue' />
      <Route component={ArchivePage} path='archive' />
    </Route>
  );

Here we initialize a react-router with App component as the master
layout, and 3 subsequent pages to load.

At the last step, before firt run the project, change the `index.js` file::

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

Here we initialize `injectTapEventPlugin` required by Material-UI, set
the default Material-UI scheme and render the Router with our routes
config.


Now you can run `npm start` to see the working website with 3 pages navigation.
