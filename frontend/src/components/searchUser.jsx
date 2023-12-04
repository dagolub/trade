import React from "react";
import {getUsers} from "../services/api";


const searchUser = (owner_id) => {
    const [users, setUsers] = React.useState([])
    React.useEffect(() => {
        if ( users.length === 0) {
            getUsers().then((data) => {
                    if (data.length > 0) {
                        setUsers(data)
                    }
                }
            )
        }
    }, [])

    if (users.length > 0) {
        for (let user in users) {
            if (users[user]["id"] === owner_id) {

                const login = users[user]["email"].split("@")[0]
                const email = users[user]["email"]
                const q = "/users/list?q=" + email
                return <a href={q} style={{"textDecoration": "underline"}}>{login}</a>
            }
        }
    }
}

export default searchUser