import { AssignmentInfoResponseSchema, AssignRequestSchema, ReassingRequestSchema, AssignmentStatisticsResponseSchema } from "@/schemas/assignment";

const url = `${process.env.NEXT_PUBLIC_API_URL}`;

/** @class AssignmentService representation of all available API requests for assignment management. */
export class AssignmentService {
   /**
    * Requests the API to create a new assignment.
    *
    * @param {token} string The logged-in user's token.
    * @param {data} AssignRequestSchema The data to create the new assignment.
    * @return {boolean} The status of the completion of the requested operation.
    */
    static async addAssignment(token: string, data: AssignRequestSchema[]): Promise<boolean> {
        return fetch(`${url}/administration/assignments/assign`, {
            method: 'POST',
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

   /**
    * Requests the API to reassign an assignment.
    *
    * @param {token} string The logged-in user's token.
    * @param {data} ReassingRequestSchema The data to reassign the assignment.
    * @return {boolean} The status of the completion of the requested operation.
    */
    static async reassignment(token: string, data: ReassingRequestSchema): Promise<boolean> {
        return fetch(`${url}/administration/assignments/reassign`, {
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

  /**
    * Requests the API to retrieve all pending assignments of the logged-in user.
    *
    * @param {token} string The logged-in user's token.
    * @return {AssignmentInfoResponseSchema[]} An array of assignments.
    */
    static async getPendings(token: string): Promise<AssignmentInfoResponseSchema[]> {
        return fetch(`${url}/operator/info/me/assignments/pending`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentInfoResponseSchema[];
        })
        .catch(error => {
            console.error(error);
            return [];
        });
    }

  /**
    * Requests the API to retrieve all revised assignments of the logged-in user.
    *
    * @param {token} string The logged-in user's token.
    * @return {AssignmentInfoResponseSchema[]} An array of assignments.
    */
    static async getReviseds(token: string): Promise<AssignmentInfoResponseSchema[]> {
        return fetch(`${url}/history/info/me`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentInfoResponseSchema[];
        })
        .catch(error => {
            console.error(error);
            return [];
        });
    }

  /**
    * Requests the API to retrieve all revised assignments of a user.
    *
    * @param {token} string The logged-in user's token.
    * @param {username} string The username of the user.
    * @return {AssignmentInfoResponseSchema[]} An array of assignments.
    */
    static async getRevisedsByUser(token: string, username: string): Promise<AssignmentInfoResponseSchema[]> {
        return fetch(`${url}/history/info?username=${username}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentInfoResponseSchema[];
        })
        .catch(error => {
            console.error(error);
            return [];
        });
    }

  /**
    * Requests the API to retrieve all assignments statistics of the logged-in user.
    *
    * @param {token} string The logged-in user's token.
    * @return {AssignmentStatisticsResponseSchema} The statistics of all assignments.
    */
    static async getTotalPersonal(token: string): Promise<AssignmentStatisticsResponseSchema | null> {
        return fetch(`${url}/statistics/info/me`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentStatisticsResponseSchema;
        })
        .catch(error => {
            console.error(error);
            return null;
        });
    }

  /**
    * Requests the API to retrieve all assignments statistics of a user.
    *
    * @param {token} string The logged-in user's token.
    * @param {username} string The username of the user.
    * @return {AssignmentStatisticsResponseSchema} The statistics of all assignments.
    */
    static async getTotalByUser(token: string, username: string): Promise<AssignmentStatisticsResponseSchema | null> {
        return fetch(`${url}/statistics/info?username=${username}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentStatisticsResponseSchema;
        })
        .catch(error => {
            console.error(error);
            return null;
        });
    }

  /**
    * Requests the API to retrieve all assignments statistics of the system.
    *
    * @param {token} string The logged-in user's token.
    * @return {AssignmentStatisticsResponseSchema} The statistics of all assignments.
    */
    static async getTotal(token: string): Promise<AssignmentStatisticsResponseSchema | null> {
        return fetch(`${url}/statistics/info/all`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentStatisticsResponseSchema;
        })
        .catch(error => {
            console.error(error);
            return null;
        });
    }
}