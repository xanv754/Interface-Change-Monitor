export class Validate {
    static validateUsername(username: string): boolean {
        // TODO: Validate not special characters
        if (username && username.length > 0) return true;
        return false;
    }
    
    static validatePassword(password: string): boolean {
        // TODO: Validate not special characters
        if (password && password.length > 0) return true;
        return false;
    }

    static validateName(name: string): boolean {
        // TODO: Validate not special characters
        if (name && name.length > 0) return true;
        return false;
    }
}