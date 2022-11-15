import api from "src/api/api"
import type { IGetPredictionResponse, IGetUserPredictionData, IGetDatasetInfoResponse, ICleanDatasetData, ICleanDatasetResponse } from 'src/api/types';


export const getPredictionFn = async (data: IGetUserPredictionData) => {

    const response = await api.get<IGetPredictionResponse>('get_prediction', { params: data })
    return response.data

}

export const getDatasetInfoFn = async (file: File) => {
    
    const response = await api.post<IGetDatasetInfoResponse>('get_dataset_info', { file }, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    return response.data

}
export const cleanDatasetFn = async (data: ICleanDatasetData) => {

    const response = await api.post<ICleanDatasetResponse>('clean_dataset', { 
        file: data.file, 
    }, {
        params: {'dataset_percent': data.datasetPercent, 'reducing_method': data.reducingMethod } ,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    return response.data

}