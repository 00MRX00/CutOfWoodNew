import {
    USER_LOADED,
    USER_LOADING,
    AUTH_ERROR,
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT_SUCCESS,
    REGISTER_SUCCESS,
    REGISTER_FAIL,
} from "../actions/actionTypes";

const initialState = {
    token: localStorage.getItem('token'),       // Токен для доступа к закрытым страницам
    isAuthenticated: null,      // true, если пользователь авторизован, иначе false
    isLoading: false,       // true, если информация о пользователе загружается, иначе false
    user: null,     // Информация о пользователе
}

// Редюсер для авторизации, регистрации пользователя, а также выхода пользователя из аккаунта
export default function authReducer(state = initialState, action) {
    switch (action.type) {
        case USER_LOADING:
            return {
                ...state,
                isLoading: true,
            };
        case USER_LOADED:
            return {
                ...state,
                isAuthenticated: true,
                isLoading: false,
                user: action.payload,
            };
        case LOGIN_SUCCESS:
        case REGISTER_SUCCESS:
            localStorage.setItem('token', action.payload.token);
            return {
                ...state,
                ...action.payload,
                isAuthenticated: true,
                isLoading: false,
            };
        case AUTH_ERROR:
        case LOGIN_FAIL:
        case LOGOUT_SUCCESS:
        case REGISTER_FAIL:
            localStorage.removeItem('token');
            return {
                ...initialState,
                token: null
            };
        default:
            return state;
    }
}