import axios from "axios";
import {getToken} from "./token";

const getUrl = (url) => {
    const base = 'http://localhost:8001/api/v1'
    if ( window.location.port > 80 ) {
        return base + url.replace("/api", "");
    }
    return url
}
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
const createUser = (full_name, email, password, is_active, is_superuser) => {
    return POST('/api/users/', {
        "email": email,
        "is_active": is_active,
        "is_superuser": is_superuser,
        "full_name": full_name,
        // "avatar": "string",
        // "description": "string",
        "password": password
    })
}
const getUsers = (q="", skip=0, limit=10) => {
    return GET('/api/users/?skip=' + skip + '&limit=' + limit + '&q=' + q)
}
const getUser = (id) => {
    return GET('/api/users/' + id)
}
const updateUser = (id, full_name, email, password, is_active, is_superuser) => {
    return PUT('/api/users/' + id, {
        "email": email,
        "is_active": is_active,
        "is_superuser": is_superuser,
        "full_name": full_name,
        "avatar": "string",
        "description": "string",
        "password": password
    })
}
const deleteUser = (id) => {
    return DELETE('/api/users/' + id)
}



const createDeposit = (wallet, type, sum, currency) => {
  return POST('/api/deposits/', {
        "wallet": wallet,
        "type": type,
        "sum": sum,
        "currency": currency,
})
  }
const getDeposits = (q="", skip=0, limit=10) => {
  return GET('/api/deposits/?skip=' + skip + '&limit=' + limit + '&q=' + q)
}
const getDeposit = (id) => {
   return GET('/api/deposits/' + id)
}
const updateDeposit = (id, wallet, type, sum, currency) => {
      return PUT('/api/deposits/' + id, {
        "wallet": wallet,
        "type": type,
        "sum": sum,
        "currency": currency,
  })
}
const deleteDeposit = (id) => {
   return DELETE('/api/deposits/' + id)
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
  return GET('/api/transactions/?skip=' + skip + '&limit=' + limit + '&q=' + q)
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
  return GET('/api/wallets/?skip=' + skip + '&limit=' + limit + '&q=' + q)
}
const getWallet = (id) => {
   return GET('/api/wallets/' + id)
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

export {
    Login, getPagination,
    GET, POST, PUT, DELETE,
    getUserMe, createUser, getUsers, getUser, updateUser, deleteUser, createAvatar,

createDeposit, getDeposits, getDeposit, updateDeposit, deleteDeposit,

createTransaction, getTransactions, getTransaction, updateTransaction, deleteTransaction,

createWallet, getWallets, getWallet, updateWallet, deleteWallet
//INSERT2
}