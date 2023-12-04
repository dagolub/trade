import Banner from "./Banner";

function showError(data) {
    let error = ""
    if (data.hasOwnProperty("response")) {
        if (data.response.hasOwnProperty("data")
            && data.response.hasOwnProperty("status")
            && data.response.status === 500) {
            error = data.response.data
        }
        if (data.response.hasOwnProperty("data")
            && data.response.data.hasOwnProperty("detail")) {
            error = data.response.data.detail
        }
        return <Banner type="error">{error}</Banner>
    }
}

export default showError;