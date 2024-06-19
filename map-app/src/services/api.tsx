import axios from 'axios';
import { getCurrentUser } from './auth';
import { API_URL } from '../utils/constants';

const api = axios.create({
    baseURL: API_URL,
});

api.interceptors.request.use(
    config => {
        const user = getCurrentUser();
        if (user && user.token) {
            config.headers.Authorization = `Token ${user.token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

export const fetchPoints = async () => {
    const response = await api.get('/points/');
    return response.data;
};

export const addPoint = async (point: any) => {
    const response = await api.post('/points/', point);
    return response.data;
};

export const deletePoint = async (id: number) => {
    const response = await api.delete(`/points/${id}/`);
    return response.data;
};

export const fetchUser = async () => {
    const response = await api.get('/auth/user/');
    return response.data;
};

export default api;
