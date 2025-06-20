import { UserModel } from "@/models/users";
import { StatisticsModel } from "@/models/statistics";


export class UserController {
    private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

    static async getUsers(): Promise<UserModel[]> {
        try {
            const response = await fetch(`${this.url}/users`);
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

    static async getAssignmentPending(usernames: string[]): Promise<StatisticsModel[]> {
        try {
            const response = await fetch(`${this.url}/assignment/pending`);
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