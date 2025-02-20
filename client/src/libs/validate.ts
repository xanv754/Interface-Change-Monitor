export class Validate {
    static validateUsername(username: string) {
        // TODO: Validate not special characters
        if (username && username.length > 0) return true;
        return false;
    }
    
    static validatePassword(password: string) {
        // TODO: Validate not special characters
        if (password && password.length > 0) return true;
        return false;
    }    
}