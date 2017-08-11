import React, { Component } from 'react'
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  Container,
  Row,
  Col,
  Jumbotron,
  Button,
  Card,
  CardTitle,
  CardText
} from 'reactstrap';

class App extends Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      isOpen: true
    };
  }
  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }
  render() {
    return (
      <div className="dashboard">
        <div className="dashboar__column">
          <div className="dashboard__title">Start</div>
          <div className="dashboard__content">
             <Card block>
               <CardText>This process demonstrates hello world approval request flow.</CardText>
               <Button>Start</Button>
             </Card>
          </div>
        </div>
        <div className="dashboar__column">
          <div className="dashboard__title">Approve</div>
          <div className="dashboard__content"></div>
        </div>
        <div className="dashboar__column">
          <div className="dashboard__title">Send</div>
          <div className="dashboard__content"></div>
        </div>
        <div className="dashboar__column">
          <div className="dashboard__title">Complete</div>
          <div className="dashboard__content"></div>
        </div>
      </div>
    );
  }
}

export default App;
