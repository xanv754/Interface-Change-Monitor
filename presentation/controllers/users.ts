import { UserModel } from "@/models/users";
import { AssignmentModel } from "@/models/assignments";
import { SessionController } from "@/controllers/session";


export class UserController {
    private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

    static async getUsers(): Promise<UserModel[]> {
        try {
            const token = SessionController.getToken();
            if (token) {
                const response = await fetch(`${this.url}/user/all`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.ok) return await response.json();
                else throw new Error(response.status + ': ' + response.statusText);
            } else throw new Error("Token not found");
        } catch (error) {
            console.error(error);
            return [];
        }

    }

    static async getHistory(month: number): Promise<AssignmentModel[]> {
        try {
            const token = SessionController.getToken();
            if (token) {
                const response = await fetch(`${this.url}/user/history/?month=${month}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    }
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