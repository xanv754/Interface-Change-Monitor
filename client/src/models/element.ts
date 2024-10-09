import type { AssignmentModel } from "./assignment";

export interface Element {
    id: string;
    date: string;
    old: {
        ip: string;
        community: string;
        ifIndex: string;
        ifName: string;
        ifDescr: string;
        ifAlias: string;
        ifHighSpeed: string;
        ifOperStatus: string;
        ifAdminStatus: string;
    };
    current: {
        ip: string;
        community: string;
        ifIndex: string;
        ifName: string;
        ifDescr: string;
        ifAlias: string;
        ifHighSpeed: string;
        ifOperStatus: string;
        ifAdminStatus: string;
    };
    assignment: AssignmentModel
}