export function login (formData) {
  return window.fetch('/login/', {
    method: 'POST',
    body: formData
  }).then(response => {
    if (response.status === 500) {
      return response.text().then(
        text => {
          throw Error(text)
        }
      )
    } else {
      return response.json().then(
        json => ({ json, response })
      )
    }
  }).catch(response => {
    return Promise.reject({'non_field_errors': response.message})
  }).then(({ json, response }) => {
    if (!response.ok) {
      return Promise.reject(json)
    }
    return Promise.resolve(json)
  })
}
