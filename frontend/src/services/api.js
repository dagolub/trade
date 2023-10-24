import axios from 'axios';
import {getToken} from './token'; // Import getToken from the appropriate location

const getUrl = (url) => {
    const base = 'http://localhost:8001/api/v1';
    if (window.location.host === "admin.rpay.io") {
        console.log(base)
        return base + url.replace('admin.rpay.io/api', 'api.rpay.io');
    }
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
const getUserMe = () => {
    return GET('/api/users/me')
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
const getUsers = (q = "", skip = 0, limit = 10) => {
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


const createDeposit = (sum, currency, chain, callback) => {
    return POST('/api/deposits/', {
        "sum": sum,
        "currency": currency,
        "chain": chain,
        "callback": callback
    })
}
const getDeposits = (q = "", skip = 0, limit = 10) => {
    let url
    if (q === "") {
        url = '/api/deposits/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/deposits/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
    return GET(url)
}
const getDeposit = (id) => {
    return GET('/api/deposits/' + id)
}
const deleteDeposit = (id) => {
    return DELETE('/api/deposits/' + id)
}

const callbackDeposit = (id) => {
    return GET("/api/deposits/callback/" + id)
}
const getTransactions = (q = "", skip = 0, limit = 10) => {
    let url
    if (q === "") {
        url = '/api/transactions/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/transactions/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
    return GET(url)
}
const getTransaction = (id) => {
    return GET('/api/transactions/' + id)
}
const getWallets = (q = "", skip = 0, limit = 10) => {
    let url
    if (q === "") {
        url = '/api/wallets/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/wallets/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
    return GET(url)
}
const getWallet = (id) => {
    return GET('/api/wallets/' + id)
}
const createWithdraw = (sum, to, currency, chain, callback) => {
    return POST('/api/withdraws/', {
        "sum": sum,
        "to": to,
        "currency": currency,
        "chain": chain,
        "callback": callback
    })
}
const getWithdraws = (q = "", skip = 0, limit = 10) => {
    let url
    if (q === "") {
        url = '/api/withdraws/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/withdraws/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
    return GET(url)
}
const getWithdraw = (id) => {
    return GET('/api/withdraws/' + id)
}
const deleteWithdraw = (id) => {
    return DELETE('/api/withdraws/' + id)
}

const getCurrencies = () => {
    return GET("/api/deposits/currencies")
}
const getChains = () => {
    return GET("/api/deposits/chains")
}
const getCallbacks = (q = "", skip = 0, limit = 10) => {
    let url
    if (q === "") {
        url = '/api/callbacks/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/callbacks/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
    return GET(url)
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
export {
    Login,
    GET, POST, PUT, DELETE,
    getUserMe, createUser, getUsers, getUser, updateUser, deleteUser,
    createDeposit, getDeposits, getDeposit, deleteDeposit, callbackDeposit, getCurrencies, getChains,
    getTransactions, getTransaction,
    getWallets, getWallet,
    createWithdraw, getWithdraws, getWithdraw, deleteWithdraw,
    getCallbacks,
    getSetting, putSetting,
    getOTP
    // INSERT2
};
