export const months = [
                       'Enero', 'Febrero', 'Marzo', 
                       'Abril', 'Mayo', 'Junio', 
                       'Julio', 'Agosto', 'Septiembre', 
                       'Octubre', 'Noviembre', 'Diciembre'
                    ]

export function getCurrentDay(): string {
    let currentDay = new Date().getDate().toString().padStart(2, '0');
    return currentDay;
}

export function getCurrentMonth(): string {
    let month = new Date().getMonth() + 1;
    let currentMonth = month.toString().padStart(2, '0');
    return currentMonth;
}

export function getCurrentYear(): string {
    let year = new Date().getFullYear();
    let currentYear = year.toString();
    return currentYear;
}

export function getCurrentDate(): string {
    let currentDay = new Date().getDate().toString().padStart(2, '0');
    let currentMonth = new Date().getMonth() + 1;
    let currentYear = new Date().getFullYear();
    let date = currentDay + '-' + currentMonth.toString().padStart(2,'0') + '-' + currentYear;
    return date;
}