export function setToken(obj) {
    localStorage.setItem('token', obj.token);
    localStorage.setItem('role', obj.role);
    localStorage.setItem('email', obj.email);

}

export function getToken() {
    return localStorage.getItem('token');
}

export function getRole() {
    return localStorage.getItem('role');
}

export function getEmail() {
    return localStorage.getItem('email');
}


export function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('email');
    window.location.href = '/login'
}
