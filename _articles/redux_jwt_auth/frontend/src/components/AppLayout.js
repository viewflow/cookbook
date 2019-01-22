import React from 'react'
import Navbar from './Navbar'
import PrivateRoute from '../containers/PrivateRoute'

const AppLayout = ({component: Component, ...rest}) => {
    return (
        <PrivateRoute {...rest} component={props => (
            <div className="wrapper">
                <Navbar/>
                <Component {...props} />
            </div>
        )}/>
    )
}

export default AppLayout