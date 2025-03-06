import { AssignmentStatisticsResponseSchema } from "@schemas/assignment";

export class StatisticsHandler {
    static calculatePendingOnTheMonth(data: AssignmentStatisticsResponseSchema){
        console.log(data);
    }
}