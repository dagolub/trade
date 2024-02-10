import axios from 'axios';
import {getToken} from './token'; // Import getToken from the appropriate location

const getUrl = (url) => {
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
const POST = (url, payload, headers = []) => {
    const token = getToken()
    let headers_list = {'Authorization': 'Bearer ' + token}
    for (let h in headers) {
        headers_list[h] = headers[h]
    }
    console.log(headers_list)
    return axios.post(getUrl(url), payload, {
        headers: headers_list
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
const createUser = (full_name, email, password, is_active, is_superuser) => {
    return POST('/api/users/', {
        "email": email,
        "is_active": is_active,
        "is_superuser": is_superuser,
        "full_name": full_name,
        "password": password
    })
}
const getUsers = (q = "", skip = 0, limit = 10) => {
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
        "password": password
    })
}
const deleteUser = (id) => {
    console.log(id)
    return DELETE('/api/users/' + id)
}


const createDocument = (document) => {
    return POST('/api/documents/',
        document
    , {"Content-Type": "multipart/form-data"}
    )
}
const updateDocument = (document) => {
    return POST('/api/documents/',
        document
    , {"Content-Type": "multipart/form-data"}
    )
}
const getDocuments = (q = "", skip = 0, limit = 10) => {
    let url
    if (q === "") {
        url = '/api/documents/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/documents/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
    return GET(url)
}
const getDocument = (id) => {
    return GET('/api/documents/' + id)
}
const deleteDocument = (id) => {
    return DELETE('/api/documents/' + id)
}

const createFolder = (name, folder_id) => {
    return POST('/api/folders/', {
        "name": name,
        "folder_id": folder_id
    })
}
const updateFolder = (name, folder_id) => {
    return POST('/api/folders/', {
        "name": name,
        "folder_id": folder_id
    })
}
const getFolders = (q = "", skip = 0, limit = 10) => {
    let url
    if (q === "") {
        url = '/api/folders/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/folders/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
    return GET(url)
}
const getFolder = (id) => {
    return GET('/api/folders/' + id)
}
const deleteFolder = (id) => {
    return DELETE('/api/folders/' + id)
}
const createPage = (title, description, document) => {
    console.log("Title - " + title)
    console.log("Description - " + description)
    console.log("Document - " + document)
    const formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    formData.append("document", document);
    return POST('/api/pages/', formData,{"Content-Type": "multipart/form-data"})
}
const updatePage = (id, name, description) => {
    return PUT('/api/pages/' + id, {
        "name": name,
        "description": description
    })
}
const getPages = (q = "", skip = 0, limit = 10) => {
    let url
    if (q === "") {
        url = '/api/pages/?skip=' + skip + '&limit=' + limit
    } else {
        url = '/api/pages/?skip=' + skip + '&limit=' + limit + '&q=' + q
    }
    return GET(url)
}
const getPage = (id) => {
    return GET('/api/pages/' + id)
}
const deletePage = (id) => {
    return DELETE('/api/pages/' + id)
}
export {
    Login,
    GET, POST, PUT, DELETE,
    getUserMe, createUser, getUsers, getUser, updateUser, deleteUser,
    createDocument, updateDocument, getDocuments, getDocument, deleteDocument,
    createFolder, updateFolder, getFolders, getFolder, deleteFolder,
    createPage, updatePage, getPages, getPage, deletePage
    // INSERT2
};
