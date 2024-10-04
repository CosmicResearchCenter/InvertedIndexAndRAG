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

export async function postRequest<T>(url: string, body: any): Promise<T | undefined> {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body), // convert body to JSON string
        });

        if (!response.ok) {
            throw new Error(`POST request failed: ${response.statusText}`);
        }

        return await response.json() as T; // assuming the response is JSON
    } catch (error) {
        console.error('POST request error:', error);
        return undefined;
    }
}

export async function putRequest<T>(url: string, body: any): Promise<T | undefined> {
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            throw new Error(`PUT request failed: ${response.statusText}`);
        }

        return await response.json() as T; // assuming the response is JSON
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
