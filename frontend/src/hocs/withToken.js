import "../services/token"
import "react"
import React
import {getToken}

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