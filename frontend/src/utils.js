

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

const copyMe = (copy) => {
    alert(copy)
}
export {populateSelect, convertList, copyMe, deleteRow}