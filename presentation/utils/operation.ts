import { InterfaceChangeSchema } from "@/schemas/interface";


export class OperationData {
    static filterChangeInterfaces(changeInterfaces: InterfaceChangeSchema[], filter: string): InterfaceChangeSchema[] {
        const lowerFilter = filter.toLowerCase();
        return changeInterfaces.filter(ci => {
            return Object.values(ci).some(
                val => String(val).toLowerCase().includes(lowerFilter)
            );
        });
    }
}