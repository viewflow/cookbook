module.exports = {
  /**
   * Token authentification
   *  
   * @param {Object} formData a FormData object with auth credentials
   */
  login (formData) {
    return fetch('/login/', {
      method: 'POST',
      accept: 'application/json',
      body: formData
    }).then(response => {
      return response.json().then(
        json => ({ json, response })
      )
    }).catch(response => {
      return Promise.reject({'non_field_errors': response.message})
    }).then(({ json, response }) => {
      if (!response.ok) {
        return Promise.reject(json)
      }

      return Promise.resolve(json)
    })
  }
}
