// http.ts

export async function getRequest<T>(url: string): Promise<T | undefined> {
    try {
        const response = await fetch(url, {
            method: 'GET',
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

export async function postRequest<T>(url: string, body: any, headers?: any): Promise<T | undefined> {
    try {
        // 检查 body 是否为 FormData，设置默认 headers
        const isFormData = body instanceof FormData;
        const defaultHeaders = isFormData ? {} : { 'Content-Type': 'application/json' };

        // 合并默认 headers 和传入的 headers
        const requestHeaders = headers ? { ...defaultHeaders, ...headers } : defaultHeaders;

        // 配置请求体：FormData 类型不需要 stringify
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


export async function deleteRequest(url: string): Promise<void> {
    try {
        const response = await fetch(url, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error(`DELETE request failed: ${response.statusText}`);
        }

        console.log('Resource deleted successfully');
    } catch (error) {
        console.error('DELETE request error:', error);
    }
}
