import React, { Component, PropTypes } from 'react';
import CircularProgress from 'material-ui/CircularProgress'


const styles = {
  progress: {
    position: "absolute",
    top: "10px",
    right: "10px",
  }
}


class LoadIndicator extends Component {
  render() {
    if(this.props.inProgress) {
      return <CircularProgress style={styles.progress} size={0.5} />
    }
    return null
  }
}

LoadIndicator.propTypes = {
  inProgress: PropTypes.bool.isRequired
}

export default LoadIndicator
