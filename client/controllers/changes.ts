import { ChangeInterface } from "@/models/changes";


export class ChangeController {
    private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

    static async getChanges(): Promise<ChangeInterface[]> {
        try {
            const response = await fetch(`${this.url}/changes`);
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