import { AssignmentInfoResponseSchema, AssignRequestSchema, ReassingRequestSchema, AssignmentStatisticsResponseSchema, AssignmentUpdateStatusRequestSchema } from "@/schemas/assignment";

const url = `${process.env.NEXT_PUBLIC_API_URL}`;

/** @class AssignmentService representation of all available API requests for assignment management. */
export class AssignmentService {
   /**
    * Requests the API to create a new assignment.
    *
    * @param {string} token The logged-in user's token.
    * @param {AssignRequestSchema[]} data The data to create the new assignment.
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
    * @param {string} token The logged-in user's token.
    * @param {ReassingRequestSchema} data The data to reassign the assignment.
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
    * Requests the API to update the status of assignments.
    *
    * @param {string} token The logged-in user's token.
    * @param {AssignmentUpdateStatusRequestSchema[]} data Assignments to update.
    */
    static async updateStatusAssignments(token: string, data: AssignmentUpdateStatusRequestSchema[]): Promise<boolean> {
        return fetch(`${url}/operator/info/me/assignments/status`, {
            method: 'PATCH',
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
    * @param {string} token The logged-in user's token.
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
    * @param {string} token The logged-in user's token.
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
    * Requests the API to retrieve all revised assignments on a specific month.
    *
    * @param {string} token The logged-in user's token.
    * @param {string} month The username of the user.
    * @return {AssignmentInfoResponseSchema[]} An array of assignments.
    */
    static async getRevisedsByMonth(token: string, month: string): Promise<AssignmentInfoResponseSchema[]> {
        return fetch(`${url}/history/info?month=${month}`, {
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
    * @param {string} token The logged-in user's token.
    * @return {AssignmentStatisticsResponseSchema} The statistics of all assignments.
    */
    static async getStatisticsUser(token: string): Promise<AssignmentStatisticsResponseSchema | null> {
        return fetch(`${url}/statistics/info/me/all`, {
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
    * Requests the API to retrieve all assignments statistics of the logged-in user on the day.
    *
    * @param {string} token The logged-in user's token.
    * @param {string} day The day to retrieve the statistics.
    * @return {AssignmentStatisticsResponseSchema} The statistics of all assignments.
    */
    static async getStatisticsUserByDay(token: string, day: string): Promise<AssignmentStatisticsResponseSchema | null> {
        return fetch(`${url}/statistics/info/me/day?day=${day}`, {
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
    * Requests the API to retrieve all assignments statistics of the logged-in user on the month.
    *
    * @param {string} token The logged-in user's token.
    * @param {string} month The month to retrieve the statistics.
    * @return {AssignmentStatisticsResponseSchema} The statistics of all assignments.
    */
    static async getStatisticsUserByMonth(token: string, month: string): Promise<AssignmentStatisticsResponseSchema | null> {
        return fetch(`${url}/statistics/info/me/month?month=${month}`, {
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
    * @param {string} token The logged-in user's token.
    * @return {AssignmentStatisticsResponseSchema} The statistics of all assignments.
    */
    static async getStatisticsGeneral(token: string): Promise<AssignmentStatisticsResponseSchema | null> {
        return fetch(`${url}/statistics/info/general/all`, {
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