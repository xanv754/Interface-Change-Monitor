import { AssignmentStatusTypes } from "@/constants/types";
import { NewAssignmentModel, AssignmentModel } from "@/models/assignments";
import { SessionController } from "@/controllers/session";


export class AssignmentController {
    private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

    static async newAssignments(assignments: NewAssignmentModel[]): Promise<boolean> {
        try {
            const token = SessionController.getToken();
            if (token) {
                const response = await fetch(`${this.url}/assignments/new`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(assignments),
                });
                if (response.ok) return true;
                else throw new Error(response.status + ': ' + response.statusText);
            } else throw new Error("Token not found");
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    static async getPending(): Promise<AssignmentModel[]> {
        try {
            const token = SessionController.getToken();
            if (token) {
                const response = await fetch(`${this.url}/assignments`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ "status": AssignmentStatusTypes.PENDING }),
                });
                if (response.ok) return await response.json();
                else throw new Error(response.status + ': ' + response.statusText);
            } else throw new Error("Token not found");
        } catch (error) {
            console.error(error);
            return [];
        }
    }
}