import { ConfigurationResponseSchema } from "@/schemas/configuration";

const url = `${process.env.NEXT_PUBLIC_API_URL}/configuration`;

export class ConfigurationService {
    static async getConfiguration(token: string): Promise<ConfigurationResponseSchema | null> {
        return fetch(`${url}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            }
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as ConfigurationResponseSchema;
        })
        .catch(error => {
            console.error(error);
            return null;
        });
    }

    static async updateConfiguration(token: string, data: ConfigurationResponseSchema): Promise<boolean> {
        return fetch(`${url}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return true;
        })
        .catch(error => {
            console.error(error);
            return false;
        });
    }

}