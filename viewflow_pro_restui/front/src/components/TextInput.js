import React from 'react'
import { FormGroup, FormFeedback, Label, Input } from 'reactstrap';


const TextInput = ({id, name, label, error, type, ...rest}) => (
    <FormGroup color={error?"danger":""}>
      { label?<Label htmlFor={id}>{label}</Label>: "" }
      <Input type={type?type:"text"} name={name} id={id} state={error?"danger":""} {...rest} />
      { error? <FormFeedback>{error}</FormFeedback>: "" }
    </FormGroup>
)

export default TextInput;
