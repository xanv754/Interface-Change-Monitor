import { AssignmentSchema, ReassignmentBodySchema, AssignmentsTotalSchema } from "@/schemas/assignment";

const url = `${process.env.NEXT_PUBLIC_API_URL}`;

export class AssignmentService {
    static async addAssignment(token: string, data: AssignmentSchema): Promise<boolean> {
        return fetch(`${url}/administration/assignments/assign`, {
            method: 'POST',
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

    static async reassignment(token: string, data: ReassignmentBodySchema): Promise<boolean> {
        return fetch(`${url}/administration/assignments/reassign`, {
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

    static async getPendings(token: string): Promise<AssignmentSchema[]> {
        return fetch(`${url}/operator/info/me/assignments/pending`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentSchema[];
        })
        .catch(error => {
            console.error(error);
            return [];
        });
    }

    static async getReviseds(token: string): Promise<AssignmentSchema[]> {
        return fetch(`${url}/history/info/me`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentSchema[];
        })
        .catch(error => {
            console.error(error);
            return [];
        });
    }

    static async getRevisedsByUser(token: string, username: string): Promise<AssignmentSchema[]> {
        return fetch(`${url}/history/info?username=${username}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentSchema[];
        })
        .catch(error => {
            console.error(error);
            return [];
        });
    }

    static async getTotalPersonal(token: string): Promise<AssignmentsTotalSchema | null> {
        return fetch(`${url}/statistics/info/me`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentsTotalSchema;
        })
        .catch(error => {
            console.error(error);
            return null;
        });
    }

    static async getTotalByUser(token: string, username: string): Promise<AssignmentsTotalSchema | null> {
        return fetch(`${url}/statistics/info?username=${username}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentsTotalSchema;
        })
        .catch(error => {
            console.error(error);
            return null;
        });
    }

    static async getTotal(token: string): Promise<AssignmentsTotalSchema | null> {
        return fetch(`${url}/statistics/info/all`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as AssignmentsTotalSchema;
        })
        .catch(error => {
            console.error(error);
            return null;
        });
    }
}