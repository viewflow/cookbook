import React, { Component, PropTypes } from 'react'

import AppBar from 'material-ui/AppBar'
import Dialog from 'material-ui/Dialog'
import Drawer from 'material-ui/Drawer'
import FloatingActionButton from 'material-ui/FloatingActionButton'
import IconButton from 'material-ui/IconButton'
import {List, ListItem} from 'material-ui/List'

import ActionDashboard from 'material-ui/svg-icons/action/dashboard'
import ActionExitToApp from 'material-ui/svg-icons/action/exit-to-app'
import Alarm from 'material-ui/svg-icons/action/alarm'
import Book from 'material-ui/svg-icons/action/book'
import CommunicationEmail from 'material-ui/svg-icons/communication/email'
import ContentAdd from 'material-ui/svg-icons/content/add'

import NewFlowList from './components/NewFlowList'


const styles = {
  logout: {
    position: 'absolute',
    bottom: '0',
    width: '100%'
  },
  addButton: {
    position: 'absolute',
    right: 40,
    bottom: 40
  }
}


class App extends Component {
  state = {
    newDialogOpen: false,
  }

  constructor() {
    super()
    this.handleChangeList = this.handleChangeList.bind(this)
  }
  
  handleOpen = () => {
    this.setState({newDialogOpen: true})
  }

  handleClose = () => {
    this.setState({newDialogOpen: false})
  }
  
  handleChangeList(event, value) {
    this.context.router.push(value)
  }


  render() {
    const SelectableList = List
    const location = this.props.location
    const drawerWidth = this.context.muiTheme.drawer.width

    return (
      <div>
        <Drawer>
          <AppBar title="Viewflow" iconElementLeft={<IconButton><ActionDashboard /></IconButton>}/>
          <SelectableList value={ location.pathname } onChange={ this.handleChangeList }>
            <ListItem primaryText="Inbox" leftIcon={<CommunicationEmail />} value="/"/>
            <ListItem primaryText="Queue" leftIcon={<Alarm />} value="/queue/"/>
            <ListItem primaryText="Archive" leftIcon={<Book />} value="/archive/"/>
          </SelectableList>
          <SelectableList style={styles.logout} onChange={ this.handleChangeList }>
            <ListItem primaryText="Logout" leftIcon={<ActionExitToApp />} value="/logout/"/>
          </SelectableList>
        </Drawer>
        <div style={{ marginLeft: drawerWidth }}>
          {this.props.children}
        </div>
        <FloatingActionButton secondary={true} style={styles.addButton} onTouchTap={this.handleOpen} >
          <ContentAdd />
        </FloatingActionButton>
        <Dialog
            title="New Process"
            modal={false}
            open={this.state.newDialogOpen}
            onRequestClose={this.handleClose}>
          <NewFlowList />
        </Dialog>
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
}

export default App
