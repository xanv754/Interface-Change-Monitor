import { CurrentSession } from "@/libs/session";
import { ConfigurationService } from "@/services/configuration";
import { ConfigurationResponseSchema } from "@/schemas/configuration";

export class SystemController {
    static async getConfiguration(): Promise<ConfigurationResponseSchema | null> {
        try {
            let token = await CurrentSession.getToken();
            if (token) {
                const configuration = await ConfigurationService.getConfiguration(token);
                if (configuration) return configuration;
                throw new Error("Configuration not found");
            }
            throw new Error("Token not found");
        } catch (error) {
            console.log(error);
            return null;
        }
    }
}