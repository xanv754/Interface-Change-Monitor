export class DateHandler {
    static getNow(): string {
        return new Date().toISOString().split('T')[0];
    }
}