module.exports = {
  getToken() {
    return localstorage.token;
  },

  loggedIn() {
    return !!localStorage.token
  },

  login(formElement, onSuccess, onError) {
    fetch('/login/', {
      method: 'POST',
      accept: 'application/json',
      body: new FormData(formElement)
    }).then(function(response) {
      console.log(response)
    }).catch(onError);
  },

  logout() {
    delete localStorage.token;
  }
}
