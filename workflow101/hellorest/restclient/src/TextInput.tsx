export const TextInput = (props: any) => {
  return (
  <div class="form-floating mb-3">
    <input
      type={props.type}
      classList={{
        "form-control":  true,
        "is-invalid": !!props.error
      }}
      id={"id_"+props.name}
      placeholder={props.placeholder}/ >
    <label for={"id_"+props.name}>{props.label}</label>
    <div class="invalid-feedback">{props.error}</div>
  </div>
  )
}
