/** @class convertText representation of all available methods to convert text. */
export class convertText {
   /**
    * Converts a month in text format to a month in numeric format.
    *
    * @param {yearMonth} string The month in text format.
    * @return {string} The month in numeric format.
    */
    static convertMonthToText(yearMonth: string): string {
        const [year, month] = yearMonth.split('-');
        
        const monthNames = [
            'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
            'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
        ];
        
        const monthIndex = parseInt(month, 10) - 1; // Convertir mes a índice (0-11)
        
        if (monthIndex < 0 || monthIndex > 11) {
            throw new Error('Mes inválido');
        }
        
        return `${monthNames[monthIndex]} de ${year}`;
    }
}