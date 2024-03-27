import axios from "axios";


axios.defaults.baseURL = "http://localhost:5000/api";


const token = localStorage.getItem('token');
if (token) {
    axios.defaults.headers.common['Authentication-Token'] = token;
}