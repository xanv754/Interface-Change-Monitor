import { ChangeInterface } from "@/model/changes";


export class OperationData {
    static filterChangeInterfaces(changeInterfaces: ChangeInterface[], filter: string): ChangeInterface[] {
        const lowerFilter = filter.toLowerCase();
        return changeInterfaces.filter(ci => {
            return Object.values(ci).some(
                val => String(val).toLowerCase().includes(lowerFilter)
            );
        });
    }
}