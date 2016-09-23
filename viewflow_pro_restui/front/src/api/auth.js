function getCookie(name) {
  var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}


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

  fetch (url, options={}) {
    // TODO
  }
}
