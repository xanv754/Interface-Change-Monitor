export class DateHandler {
    static getNow(): string {
        return new Date().toISOString().split('T')[0];
    }

    static getMonth(): string {
        return new Date().toISOString().split('T')[0].split('-')[1];
    }
}