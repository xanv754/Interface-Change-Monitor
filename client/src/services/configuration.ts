import { ConfigurationResponseSchema } from "@/schemas/configuration";

const url = `${process.env.NEXT_PUBLIC_API_URL}/configuration`;

/** @class ConfigurationService representation of all available API requests to manage the system. */
export class ConfigurationService {
   /**
    * Requests the API to retrieve all the system configuration.
    *
    * @param {token} string The logged-in user's token.
    * @return {ConfigurationResponseSchema} The system configuration.
    */
    static async getConfiguration(token: string): Promise<ConfigurationResponseSchema | null> {
        return fetch(`${url}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
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

   /**
    * Requests the API to update the system configuration.
    *
    * @param {token} string The logged-in user's token.
    * @param {data} ConfigurationResponseSchema The data to update the system configuration.
    * @return {boolean} The status of the completion of the requested operation.
    */
    static async updateConfiguration(token: string, data: ConfigurationResponseSchema): Promise<boolean> {
        return fetch(`${url}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
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