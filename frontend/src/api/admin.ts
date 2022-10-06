import api from "src/api/api"
import type { IGetExperimentsResponse, EmptyResponse, IGetExperimentsInput, ILoadCompletenessCurvesInput, ILoadExperimentsOnDbInput, ITrainRegressorInput } from 'src/api/types';

export const loadExperimentsOnDbFn = async (data: ILoadExperimentsOnDbInput) => {
    
    const response = await api.get<EmptyResponse>('load_experiments_on_db', { params: data });
    return response.data;
}
export const loadCompletenessCurvesFn = async (data: ILoadCompletenessCurvesInput) => {
    
    const response = await api.get<EmptyResponse>('load_completeness_curves', { params: data });
    return response.data;
}
export const trainRegressorFn = async (data: ITrainRegressorInput) => {
    
    const response = await api.get<EmptyResponse>('train_regressor', { params: data });
    return response.data;
}


export const getExperimentsFn = async (data: IGetExperimentsInput) => {

    const response = await api.get<IGetExperimentsResponse>('get_experiments', { params: data })
    return response.data

}
