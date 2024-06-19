import axios from 'axios';
import { AUTH_URL } from '../utils/constants';

export const login = async (username: string, password: string) => {
    const response = await axios.post(AUTH_URL, { username, password });
    if (response.data.token) {
        localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
};

export const logout = () => {
    localStorage.removeItem('user');
};

export const getCurrentUser = () => {
    return JSON.parse(localStorage.getItem('user') || '{}');
};
