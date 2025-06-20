import { NewAssignmentModel, AssignmentModel } from "@/models/assignments";


export class AssignmentController {
    private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

    static async newAssignments(assignments: NewAssignmentModel[]): Promise<boolean> {
        try {
            const response = await fetch(`${this.url}/assignments`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(assignments),
            });
            if (response.ok) return true;
            else {
                console.error(response.status + ': ' + response.statusText);
                return false;
            }
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    static async getAssignments(): Promise<AssignmentModel[]> {
        try {
            const response = await fetch(`${this.url}/assignments`);
            if (response.ok) return await response.json();
            else {
                console.error(response.status + ': ' + response.statusText);
                return [];
            }
        } catch (error) {
            console.error(error);
            return [];
        }
    }
}