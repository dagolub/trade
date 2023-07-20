import React from "react"
import {getToken} from "../services/token";

const withProtectedRoute = (Component) =>{
    return (props) => {
        const token = getToken()

        if (!token) {
            return window.location.href = "/login"
        }
        return <Component {...props} />
    }
}

export default withProtectedRoute;