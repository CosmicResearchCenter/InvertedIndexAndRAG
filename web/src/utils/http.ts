// http.ts

// 添加token相关的工具函数
export const saveToken = (token: string) => {
    localStorage.setItem('token', token);
};

export const getToken = () => {
    return localStorage.getItem('token');
};

export const removeToken = () => {
    localStorage.removeItem('token');
};

export async function getRequest<T>(url: string): Promise<T | undefined> {
    try {
        const token = getToken();
        const headers: HeadersInit = {
            'Authorization': token ? `Bearer ${token}` : ''
        };

        const response = await fetch(url, {
            method: 'GET',
            headers
        });

        if (!response.ok) {
            throw new Error(`GET request failed: ${response.statusText}`);
        }

        return await response.json() as T; // assuming the response is JSON
    } catch (error) {
        console.error('GET request error:', error);
        return undefined;
    }
}

export async function postRequest<T>(url: string, body: any, customHeaders?: any): Promise<T | undefined> {
    try {
        const token = getToken();
        const isFormData = body instanceof FormData;
        const defaultHeaders = {
            ...(!isFormData && { 'Content-Type': 'application/json' }),
            'Authorization': token ? `Bearer ${token}` : ''
        };

        // 合并默认headers和自定义headers
        const requestHeaders = customHeaders ? { ...defaultHeaders, ...customHeaders } : defaultHeaders;
        const requestBody = isFormData ? body : JSON.stringify(body);

        const response = await fetch(url, {
            method: 'POST',
            headers: requestHeaders,
            body: requestBody,
        });

        if (!response.ok) {
            throw new Error(`POST request failed: ${response.statusText}`);
        }

        return await response.json() as T;
    } catch (error) {
        console.error('POST request error:', error);
        return undefined;
    }
}

export async function putRequest<T>(url: string, body: any, headers?: any): Promise<T | undefined> {
    try {
        const isFormData = body instanceof FormData;

        // 默认请求头（如果是 FormData，则不设置 Content-Type）
        const defaultHeaders = isFormData ? {} : { 'Content-Type': 'application/json' };

        // 合并默认 headers 和传入的 headers
        const requestHeaders = headers ? { ...defaultHeaders, ...headers } : defaultHeaders;

        // 如果 body 是 FormData，则直接传递；否则进行 JSON 序列化
        const requestBody = isFormData ? body : JSON.stringify(body);

        const response = await fetch(url, {
            method: 'PUT',
            headers: requestHeaders,
            body: requestBody,
        });

        if (!response.ok) {
            const errorText = `PUT request failed with status ${response.status}: ${response.statusText}`;
            console.error(errorText);
            throw new Error(errorText);
        }

        // 确保响应体为 JSON 格式再解析
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            return await response.json() as T;
        }

        // 如果不是 JSON 格式，返回空
        return undefined;
    } catch (error) {
        console.error('PUT request error:', error);
        return undefined;
    }
}


export async function deleteRequest<T>(url: string): Promise<T | undefined> {
    try {
        const response = await fetch(url, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error(`DELETE request failed: ${response.statusText}`);
        }

        console.log('Resource deleted successfully');
        return await response.json() as T;
    } catch (error) {
        console.error('DELETE request error:', error);
    }
}

// 添加登录方法
export async function login(username: string, password: string) {
    try {
        const baseURL = import.meta.env.VITE_APP_BASE_URL || 'http://127.0.0.1:9988';
        const response = await fetch(`${baseURL}/v1/api/mark/account/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error('登录失败');
        }

        const result = await response.json();
        if (result.code === 200 && result.data.access_token) {
            saveToken(result.data.access_token);
            return result;
        }
        
        throw new Error(result.message || '登录失败');
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}
