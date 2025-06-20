import { TokenModel } from "@/models/session";


export class LoginController {
    private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

    static async login(username: string, password: string): Promise<string | null> {
        try {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);
            const response = await fetch(`${this.url}/token`, {
                method: 'POST',
                body: formData,
            });
            if (response.ok) {
                const token = await response.json();
                console.log(token);
                return "";
            }
            else throw new Error(response.status + ': ' + response.statusText);
        } catch (error) {
            console.error(error);
            return null;
        }
    }
}