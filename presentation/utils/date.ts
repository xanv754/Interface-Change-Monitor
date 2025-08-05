export class DateHandler {
    static getNow(): string {
        return new Date().toISOString().split('T')[0];
    }

    static getMonth(): string {
        return new Date().toISOString().split('T')[0].split('-')[1];
    }

    static getYear(): string {
        return new Date().toISOString().split('T')[0].split('-')[0];
    }

    static getYearMonth(): string {
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        return `${year}-${month}`;
    }
}