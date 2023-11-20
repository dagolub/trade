const saveToken = async (token) => {
    if (token) {
        localStorage.setItem('access-token', token)
    }
}
const getToken = () => {
    return localStorage.getItem('access-token')
}
const deleteToken = () => {
    alert("Delete token")
    localStorage.removeItem('access-token')
    window.location.pathname = '/signin'
}
export {saveToken, getToken, deleteToken}