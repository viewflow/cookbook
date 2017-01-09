import React, {Component, PropTypes} from 'react';

import TextField from 'material-ui/TextField'
import FlatButton from 'material-ui/FlatButton'


const styles = {
  formField: {
    width: '100%'
  }
}


class Start extends Component {
  constructor(props) {
    super(props)

    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleSubmit() {
  }


  render() {
    const errors = this.state.errors

    return (
        <form>
          <TextField name="text" floatingLabelText="Username" style={styles.formField} errorText={errors.username}/>
          <FlatButton
              label="Submit"
              primary={true}
              onTouchTap={this.handleSubmit}
          />          
        </form>
    )
  }
}

Start.propTypes = {
  task: PropTypes.object.isRequired
}


export default Start;
