import React from 'react';

import AppBar from 'material-ui/AppBar';
import CommunicationEmail from 'material-ui/svg-icons/communication/email';
import IconButton from 'material-ui/IconButton';
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table';


export default (
  () => {
    return (
      <div>
        <AppBar title="Inbox" iconElementLeft={<IconButton>{<CommunicationEmail />}</IconButton>}/>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHeaderColumn>ID</TableHeaderColumn>
              <TableHeaderColumn>Description</TableHeaderColumn>
              <TableHeaderColumn>Summary</TableHeaderColumn>
              <TableHeaderColumn>Task</TableHeaderColumn>
              <TableHeaderColumn>Process</TableHeaderColumn>
              <TableHeaderColumn>Assigned</TableHeaderColumn>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableRowColumn>759/17094</TableRowColumn>
              <TableRowColumn>Decision required</TableRowColumn>
              <TableRowColumn>Decision on Frange1<br/>1 of 3 completed</TableRowColumn>
              <TableRowColumn>Make Decision</TableRowColumn>
              <TableRowColumn>Dynamic split #759</TableRowColumn>
              <TableRowColumn>Sept. 18, 2016, 12:25 p.m.</TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>759/17094</TableRowColumn>
              <TableRowColumn>Decision required</TableRowColumn>
              <TableRowColumn>Decision on Frange1<br/>1 of 3 completed</TableRowColumn>
              <TableRowColumn>Make Decision</TableRowColumn>
              <TableRowColumn>Dynamic split #759</TableRowColumn>
              <TableRowColumn>Sept. 18, 2016, 12:25 p.m.</TableRowColumn>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    )
  }
)
