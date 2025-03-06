export class DateHandler {
    static getCurrentDate(): string {
        const date = new Date();
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); 
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    static getCurrentMonth(): string {
        const date = new Date();
        const month = String(date.getMonth() + 1).padStart(2, '0'); 
        return month;
    }
}