import axios from 'axios';
import type{ AxiosResponse, AxiosRequestConfig } from 'axios';

import { camelizeKeys, decamelizeKeys } from 'humps';


const BASE_URL = 'http://localhost:5000/api/'

const api = axios.create({
  baseURL: BASE_URL,
});

api.defaults.headers.common['Content-Type'] = 'application/json';


// Axios middleware to convert all api responses to camelCase
api.interceptors.response.use((response: AxiosResponse) => {
  if (
    response.data &&
    response.headers['content-type'] === 'application/json'
  ) {
    response.data = camelizeKeys(response.data);
  }

  return response;
});

// Axios middleware to convert all api requests to snake_case
api.interceptors.request.use((config: AxiosRequestConfig) => {
  const newConfig = { ...config };

  if (newConfig.headers && newConfig.headers['Content-Type'] === 'multipart/form-data')
    return newConfig;

  if (config.params) {
    newConfig.params = decamelizeKeys(config.params);
  }

  if (config.data) {
    newConfig.data = decamelizeKeys(config.data);
  }

  return newConfig;
});


export default api