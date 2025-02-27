/** @class Validate representation of all available methods to validate user input. */
export class Validate {
   /**
    * Validates the username.
    * 
    * @param {username} string The username to validate.
    * @return {boolean} The status of the validation.
    */
    static validateUsername(username: string): boolean {
        // TODO: Validate not special characters
        if (username && username.length > 0) return true;
        return false;
    }
    
   /**
    * Validates the password.
    * 
    * @param {password} string The password to validate.
    * @return {boolean} The status of the validation.
    */
    static validatePassword(password: string): boolean {
        // TODO: Validate not special characters
        if (password && password.length > 0) return true;
        return false;
    }

   /**
    * Validates the name.
    * 
    * @param {name} string The name to validate.
    * @return {boolean} The status of the validation.
    */
    static validateName(name: string): boolean {
        // TODO: Validate not special characters
        if (name && name.length > 0) return true;
        return false;
    }
}