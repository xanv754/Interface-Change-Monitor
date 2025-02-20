import { TokenSchema } from '@schemas/token';

class LoginController {
    private url_base: string = process.env.NEXT_PUBLIC_API_URL_BASE;
    private url: string = process.env.NEXT_PUBLIC_API_URL;


    async getToken(username: string, password: string): Promise<TokenSchema | null> {
        const response = await fetch(`${this.url_base}/token`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
              username,
              password,
            }).toString(),
        });
        if (response.ok) {
            let res = await response.json();
            return res;
        }
        return null;
    }
}

export const Login = new LoginController();