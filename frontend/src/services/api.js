import axios from "axios";
import {getToken} from "./token";
import {id2key} from "../utils";

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
const createUser = (full_name, email, password, is_superuser, is_active) => {
    return POST('/api/users/', {
        "email": email,
        "is_active": is_active,
        "is_superuser": is_superuser,
        "full_name": full_name,
        "avatar": "string",
        "description": "string",
        "password": password
    })
}
const getUsers = (skip=0, limit=10) => {
    return GET('/api/users/?skip=' + skip + '&limit=' + limit)
}
const getUser = (id) => {
    return GET('/api/users/' + id)
}
const updateUser = (id, full_name, email, password, is_superuser, is_active) => {
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

export {
    Login, getPagination,
    getUserMe, createUser, getUsers, getUser, updateUser, deleteUser, createAvatar,
}
