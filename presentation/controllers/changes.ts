import { ChangeInterface } from "@/models/changes";
import { SessionController } from "@/controllers/session";


export class ChangeController {
    private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

    static async getChanges(): Promise<ChangeInterface[]> {
        try {
            const token = SessionController.getToken();
            if (token) {
                const response = await fetch(`${this.url}/changes`, {
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

}