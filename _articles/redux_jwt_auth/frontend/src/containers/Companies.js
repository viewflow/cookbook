import React from 'react'
import { Link } from 'react-router-dom'

const Companies = () => (
    <ul>
        <li><Link to="/company/1"> Company 1</Link></li>
        <li><Link to="/company/2"> Company 2</Link></li>
        <li><Link to="/company/3"> Company 3</Link></li>
    </ul>
)

export default Companies