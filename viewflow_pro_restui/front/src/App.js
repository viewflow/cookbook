import React, { Component, PropTypes } from 'react';

import AppBar from 'material-ui/AppBar';
import Drawer from 'material-ui/Drawer';
import {List, ListItem, MakeSelectable} from 'material-ui/List';
import IconButton from 'material-ui/IconButton';

import ActionDashboard from 'material-ui/svg-icons/action/dashboard';
import Alarm from 'material-ui/svg-icons/action/alarm';
import Book from 'material-ui/svg-icons/action/book';
import CommunicationEmail from 'material-ui/svg-icons/communication/email';


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
