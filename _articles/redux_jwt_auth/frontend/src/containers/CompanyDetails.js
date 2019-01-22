import React from 'react'

const CompanyDetails = (props) => {
    const companyId = props.match && props.match.params && props.match.params.id

    return (
        <div>
            <h1>Company {companyId} Details</h1>
        </div>
    )
}

export default CompanyDetails