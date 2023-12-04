import dayjs from "dayjs"
const showDate = (date) => {
    return dayjs(date).format("HH:mm DD MMM YY")
}
export default showDate