import React, {Component} from 'react';

import {Card, CardActions, CardTitle, CardMedia} from 'material-ui/Card'
import FlatButton from 'material-ui/FlatButton';

const styles = {
  overlay: {
    position: 'fixed',
    height: '100%',
    width:'100%',

    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',

    background: '#eee',
  },
}


class Logout extends Component {
  constructor (props) {
    super(props)

    this.handleClick = this.handleClick.bind(this)
  }

  componentDidMount() {
    delete window.localStorage.token
  }

  handleClick() {
    this.context.router.replace('/login/')
  }

  render() {
    return (
      <div style={styles.overlay}>
        <Card style={styles.card}>
          <CardMedia overlay={<CardTitle title="Good bye" subtitle="Thanks for spending some quality time with the Web site today."/>}>
            <img src="http://lorempixel.com/business/640/480" alt="Good bye"/>
          </CardMedia>
          <CardActions>
            <FlatButton label="Login again" onClick={this.handleClick} />
          </CardActions>
        </Card>
      </div>
    )
  }
}

Logout.contextTypes = {
  router: React.PropTypes.object.isRequired
}

export default Logout
