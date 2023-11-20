import {deleteDeposit, GET} from "./services/api";
import React from "react";


const populateSelect = (data, label_field) => {
    let result = []
    for (const i in data) {
        if (typeof data[i] === "object") {
            result.push({value: data[i].id, label: data[i][label_field]})
        } else {
            result.push({value: data[i], label: data[i]})
        }
    }
    return result
}

const convertList = (list, field) => {
    let result = []
    for (const i in list) {
        if (list[i].created) {
            result[list[i].id] = list[i].created
        }
        if (list[i].full_name) {
            result[list[i].id] = list[i].full_name
        }

    }
    return result
}

const deleteRow = (id) => {
    const elements = document.getElementsByClassName("td" + id)
    for (const el in elements) {
        if (elements[el].style) {
            elements[el].style.color = "black"
            elements[el].style.backgroundColor = "red"
        }
    }
}


const showWallet = (wallet) => {
    return wallet.length > 9 ? wallet.substring(0, 5) + " ... " + wallet.substring(wallet.length - 5) : wallet
}

const copyMe = (copy) => {
    alert(copy)
}
const divClass = "font-medium text-slate-800 dark:text-slate-100"
const buttonView = "text-slate-400 hover:text-slate-500 dark:text-slate-500 dark:hover:text-slate-400 rounded-full"
const buttonDelete = "text-rose-500 hover:text-rose-600 rounded-full"

const tdClass = (id) => {
    return "px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap td" + id
}
const getEntities = (getEntities, setList) => {
    let q = document.location.search.split('=')[1];
    let hash = parseInt(window.location.hash.split('#')[1]);
    hash = hash > 0 ? hash : 0;

    getEntities(q, hash * 10).then((data) => {
        if (data.length > 0) {
            setList(data)
        }
    });
}
const setTot = (path, setTotal) => {
    let q = ""
    const query = document.location.search.split('=')
    if (query.length > 0) {
        q = document.location.search.split('=')[1];
    }
    const url = '/api/' + path + '/count' + (q ? "?q=" + q : "")

    GET(url).then((data) => {
        if (data > 0) {
            setTotal(data)
        }
    });
}
const deleteEntity = (deleteEntity, entity_id) => {
    deleteRow(entity_id);
    setTimeout(() => {
        deleteEntity(entity_id).then((response) => {
            if (response.id) {
                document.getElementById("tr" + entity_id).remove();
            }
        });
    }, 200);
}

export {
    populateSelect,
    convertList,
    copyMe,
    deleteRow,
    showWallet,
    divClass,
    buttonView,
    buttonDelete,
    tdClass,
    getEntities,
    setTot,
    deleteEntity
}