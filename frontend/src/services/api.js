import axios from 'axios';
import { getToken } from './token'; // Import getToken from the appropriate location

const getUrl = (url) => {
  const base = 'http://localhost:8001/api/v1';
  if (window.location.port > 80) {
    return base + url.replace('/api', '');
  }
  return url;
};
const Login = (authenticate) => {
    return axios({
            method: 'post',
            url: getUrl('/api/login/access-token'),
            data: authenticate,
            headers: {"Content-Type": "multipart/form-data"}
        }
        , authenticate)
        .then(function (response) {
            return response
        })
        .catch(function (error) {
            return error
        });
}
const GET = (url) => {
    const token = getToken()
    return axios.get(getUrl(url), {
        headers: {'Authorization': 'Bearer ' + token}
    })
    .then(function (response) {
        return response.data
    })
    .catch(function (error) {
        return error
    })
}
const POST = (url, payload) => {
    const token = getToken()
    return axios.post(getUrl(url), payload, {
        headers: {'Authorization': 'Bearer ' + token}
    })
        .then(function (response) {
            return response.data
        })
        .catch(function (error) {
            return error
        })
}

const PUT = (url, payload) => {
    const token = getToken()
    return axios.put(getUrl(url), payload, {
        headers: {'Authorization': 'Bearer ' + token}
    })
        .then(function (response) {
            return response.data
        })
        .catch(function (error) {
            return error
        })
}
const DELETE = (url) => {
    const token = getToken()
    return axios.delete(getUrl(url), {
        headers: {'Authorization': 'Bearer ' + token}
    })
        .then(function (response) {
            return response.data
        })
        .catch(function (error) {
            return error
        })
}
const createAvatar = (file, user_id = null) => {
    const formData = new FormData();
    formData.append("file", file);
    return POST("/api/users/avatar/?user_id=" + user_id , formData);
}
const getUserMe = () => {
    return GET('/api/users/me')
}
const getPagination = (url) => {
    return GET('/api/' + url + '/pagination')
}
// USERS
const createUser = (full_name, email, password, is_active, is_superuser, autotransfer) => {
    return POST('/api/users/', {
        "email": email,
        "is_active": is_active,
        "is_superuser": is_superuser,
        "full_name": full_name,
        "password": password,
        "autotransfer": autotransfer
    })
}
const getUsers = (q="", skip=0, limit=10) => {
    return GET('/api/users/?skip=' + skip + '&limit=' + limit + '&q=' + q)
}
const getUser = (id) => {
    return GET('/api/users/' + id)
}
const updateUser = (id, full_name, email, password, is_active, is_superuser, autotransfer) => {
    return PUT('/api/users/' + id, {
        "email": email,
        "is_active": is_active,
        "is_superuser": is_superuser,
        "full_name": full_name,
        "avatar": "string",
        "description": "string",
        "password": password,
        "autotransfer": autotransfer
    })
}
const deleteUser = (id) => {
    return DELETE('/api/users/' + id)
}



const createDeposit = (wallet, type, sum, currency, status, callback) => {
  return POST('/api/deposits/', {
        "wallet": wallet,
        "type": type,
        "sum": sum,
        "currency": currency,
        "status": status,
        "callback": callback
})
  }
const getDeposits = (q="", skip=0, limit=10) => {
    let url
    if (q == "") {
        url = '/api/deposits/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/deposits/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
  return GET(url)
}
const getDeposit = (id) => {
   return GET('/api/deposits/' + id)
}
const updateDeposit = (id, wallet, type, sum, currency, status, callback) => {
      return PUT('/api/deposits/' + id, {
        "wallet": wallet,
        "type": type,
        "sum": sum,
        "currency": currency,
        "status": status,
        "callback": callback
  })
}
const deleteDeposit = (id) => {
   return DELETE('/api/deposits/' + id)
}

const callbackDeposit = (id) => {
    return GET("/api/deposits/callback/" + id)
}

const createTransaction = (from_wallet, to_wallet, tx, amount, currency, type) => {
  return POST('/api/transactions/', {
        "from_wallet": from_wallet,
        "to_wallet": to_wallet,
        "tx": tx,
        "amount": amount,
        "currency": currency,
        "type": type,
})
  }
const getTransactions = (q="", skip=0, limit=10) => {
    let url = ""
    if (q == "") {
        url = '/api/transactions/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/transactions/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
  return GET(url)
}
const getTransaction = (id) => {
   return GET('/api/transactions/' + id)
}
const updateTransaction = (id, from_wallet, to_wallet, tx, amount, currency, type) => {
      return PUT('/api/transactions/' + id, {
        "from_wallet": from_wallet,
        "to_wallet": to_wallet,
        "tx": tx,
        "amount": amount,
        "currency": currency,
        "type": type,
  })
}
const deleteTransaction = (id) => {
   return DELETE('/api/transactions/' + id)
}

const createWallet = (wallet, type) => {
  return POST('/api/wallets/', {
        "wallet": wallet,
        "type": type,
})
  }
const getWallets = (q="", skip=0, limit=10) => {
    let url = ""
    if (q == "") {
        url = '/api/wallets/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/wallets/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
    return GET(url)
}
const getWallet = (id) => {
   return GET('/api/wallets/' + id)
}
const getWithdraws = (q="", skip=0, limit=10) => {
    let url = ""
    if (q == "") {
        url = '/api/withdraws/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/withdraws/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
    return GET(url)
}
const getWthdraw = (id) => {
   return GET('/api/withdraws/' + id)
}
const getCallbacks = (q="", skip=0, limit=10) => {
    let url = ""
    if (q == "") {
        url = '/api/callbacks/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/callbacks/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
    return GET(url)
}
const getCallback = (id) => {
   return GET('/api/callbacks/' + id)
}
const updateWallet = (id, from_wallet, to_wallet, tx, amount, currency, type) => {
      return PUT('/api/wallets/' + id, {
        "wallet": wallet,
        "type": type,
  })
}
const deleteWallet = (id) => {
   return DELETE('/api/wallets/' + id)
}
//INSERT1
const getSetting = () => {
    return GET("/api/settings/all")
}
const putSetting = (data) => {
    return PUT("/api/settings/all", data)
}

const getOTP = (email) => {
    return GET("/api/users/get_otp/" + email)
}
const verifyOTP = () => {

}
export {
  Login,
  getPagination,
  GET, POST, PUT, DELETE,
  getUserMe, createUser, getUsers, getUser, updateUser, deleteUser, createAvatar,
  createDeposit, getDeposits, getDeposit, updateDeposit, deleteDeposit, callbackDeposit,
  createTransaction, getTransactions, getTransaction, updateTransaction, deleteTransaction,
  createWallet, getWallets, getWallet, updateWallet, deleteWallet,
  getWithdraws, getWthdraw,
  getCallbacks, getCallback,
  getSetting, putSetting,
  getOTP, verifyOTP
  // INSERT2
};
